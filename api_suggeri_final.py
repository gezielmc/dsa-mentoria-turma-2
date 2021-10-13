# -*- coding: utf-8 -*-
"""ApiSuggeri.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O-AY9zXJCU4P7Y2lqyZ6rT2WIS4UdXVw

#Installs
"""





"""usar um arquivo requeriments.txt -- coloca os modulos e versoes -- pip install -r requiriments.txt


"""
#!pip install anvil-uplink
#!pip install surprise
#!pip install requests

"""#Imports"""

# Anvil
import anvil.media
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# thread para a API
from threading import Thread
# para acionar a API no servidor do Anvil
import requests


# para gerar o id dos modelos
from uuid import uuid4

# surprise e toda a estrutura para IA
import sys
import os
import pickle
import time
from collections import defaultdict
from surprise.prediction_algorithms import knns
from surprise import SVD
from surprise import Dataset,  Trainset, Reader
import pandas as pd

# arquivo de configurações da conexão com o Anvil
from config import *

"""# Esqueleto API/Colab/Frontend"""

## para conectar com a versão do front-end
anvil.server.connect(anvil_server_key)


## Cache Memoize para funções
"""Cache para funções com limite em Python.

Cópia e adaptação desse link: https://code.activestate.com/recipes/496879/ 
"""
##
def memoize(function, limit=None):
  if isinstance(function, int):
    def memoize_wrapper(f):
      return memoize(f, function)

    return memoize_wrapper

  m_dict = {}
  m_list = []

  def memoize_wrapper(*args, **kwargs):
    print('-' * 80)
    key = args[0]
    try:
      print('cache={}'.format(m_dict.keys()))
      print('o cache agora tem {} itens'.format(len(m_dict)))
      print('tentando obter o item {} do cache'.format(key))
      m_list.append(m_list.pop(m_list.index(key)))
      print('sucesso ao obter o item {} do cache'.format(key))
    except ValueError:
      print('o item {} nao esta no cache'.format(key))
      print('chamando a execucao da funcao')
      m_dict[key] = function(*args, **kwargs)
      print('adicionando no cache')
      m_list.append(key)
      if limit is not None and len(m_list) > limit:
        print('cache ultrapassou limite, atualmente ja tem {} itens'.format(len(m_dict)))
        print('removendo o item mais velho={}'.format(list(m_dict.keys())[0]))
        del m_dict[m_list.pop(0)]
    print('o cache agora tem {} itens'.format(len(m_dict)))

    return m_dict[key]

  memoize_wrapper._memoize_m_dict = m_dict
  memoize_wrapper._memoize_m_list = m_list
  memoize_wrapper._memoize_limit = limit
  memoize_wrapper._memoize_origfunc = function
  return memoize_wrapper


"""#API - Chamadas do Anvil para o COLAB"""

## COLAB ##

def colab_servercall_treinar_modelo(csv_filename):
  # gera o nome do modelo (apenas 8 caracteres para ficar melhor)
  #model_name = str(uuid4())[:8]
  model_name = csv_filename[:8]
  # cria a thread para inciar treinamento
  t = Thread(target=colab_thread_treinar, args=(csv_filename, model_name, ))
  t.start()
  # retorna o nome modelo
  return model_name

def colab_predict_item(model_name, user_id, n=5):
  ## carrega modelo
  # model_filename = f'{model_name}.model'
  model_filename = model_name + '.model'
  print('modelo {} carregado'.format(model_filename))
  model = load_model(model_filename)  
  # model = carregar()
  # items = predict(model, user_id, n=5)
  itens = []
  itens = predict_user(model, user_id, n)
  return itens

def colab_predict_user_item(model_name, user_id, item_id):
  ## carrega modelo
  # model_filename = f'{model_name}.model'
  model_filename = model_name + '.model'
  print('modelo {} carregado'.format(model_filename))
  model = load_model(model_filename)
  # model = carregar()
  rating = predict_user_item(model, user_id=user_id, item_id=item_id)
  return rating 

def colab_predict_users(model_name, item_id, n=5):
  ## carrega modelo
  # model_filename = f'{model_name}.model'
  model_filename = model_name + '.model'
  print('modelo {} carregado'.format(model_filename))
  model = load_model(model_filename)  
    # items = predict(model, user_id, n=5)
  itens = []
  itens = predict_item(model, item_id, n)
  return itens

@anvil.server.callable
def thread_treinar(csv_filename, model_name):
  return colab_thread_treinar(csv_filename, model_name)

@anvil.server.callable
def treinar_modelo(csv_filename):
  return  colab_servercall_treinar_modelo(csv_filename)

@anvil.server.callable
def predict_item(model_name, user_id, n=5):
  return colab_predict_item(model_name, user_id, n)

@anvil.server.callable
def predict_users(model_name, item_id, n=5):  
  return colab_predict_users(model_name, item_id, n=5)  

@anvil.server.callable
def predict_user_item(model_name, user_id, item_id):
  return colab_predict_user_item(model_name, user_id, item_id)

@anvil.server.callable
def get_uuid():
    return str(uuid4())[:8]

@anvil.server.callable
def colab_online():
  return True

"""# VERSÃO FINAL COM SURPRISE (Toda a parte de IA está aqui)"""

def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        if n:
          top_n[uid] = user_ratings[:n]
        else:
          top_n[uid] = user_ratings

    return top_n

def train_model(csv_filename, n=None):
  start = time.time()
  # TODO: alterar para ler .csv
  print('carregando dados do dataset {}'.format(csv_filename))
  df = pd.read_csv(csv_filename)
  data = Dataset.load_from_df(df[['UserId', 'ProductId', 'Rating']], Reader(rating_scale=(1,5)))
  #data = Dataset.load_builtin('ml-100k') # Se você desejar fazer um teste com base do Surprise, descomente aqui.
  trainset = data.build_full_trainset()
  algo = SVD(random_state=1)
  algo.fit(trainset)

  # Than predict ratings for all pairs (u, i) that are NOT in the training set.
  testset = trainset.build_anti_testset()
  predictions = algo.test(testset)

  model = get_top_n(predictions, n=n)
  elapsed_seconds = time.time() - start
  print('model trained in {:.1f} seconds'.format(elapsed_seconds))
  return model

def save_model(model, filename=''):
  tamanho_modelo = sys.getsizeof(model)
  # print(f'tamanho do modelo: {tamanho_modelo} bytes')
  if filename == '':
    file_name2 = str(uuid.uuid4())[:8] + '.model'
  else:
    file_name2 = filename + '.model'
  pickle.dump(model, open(file_name2, 'wb'))
  tamanho_arquivo = os.stat(file_name2).st_size
  print('tamanho do arquivo: {} bytes'.format(tamanho_arquivo))
  return file_name2

@memoize(10)
def load_model(file_name):
  print('Carregando o modelo {}'.format(file_name))
  loaded_model = pickle.load(open(file_name, 'rb'))
  print ("Modelo carregado")
  return loaded_model

def predict_user(model, user_id, n=5):
  print('Predict Itens for User {}'.format(user_id))
  result = []
  # Print the recommended items for each user
  for uid, user_ratings in model.items():
    if str(uid) == str(user_id):
      result = [iid for (iid, _) in user_ratings][:n]
  return result

def predict_item(model, item_id, n=5):
  print('Predict Users for Item {}'.format(item_id))
  result = []
  # Print the recommended items for each user
  top_n_iid = defaultdict(list)
  for uid, user_ratings in model.items():
    for (iid, rating) in user_ratings:
      if str(iid) == str(item_id):
        top_n_iid[iid].append((uid, rating))        

  # Then sort the predictions for each user and retrieve the k highest ones.
  for iid, user_ratings in top_n_iid.items():
    user_ratings.sort(key=lambda x: x[1], reverse=True)
  result = [uid for (uid, _) in user_ratings][:n]
  return result  

def predict_user_item(model, user_id, item_id):
  print('Predict Rating for a Item by User {}'.format(user_id))
  result = []
  # Print the recommended items for each user
  for uid, user_ratings in model.items():
    if str(uid) == str(user_id):
      for (iid, rating) in user_ratings:
        if str(iid) == str(item_id):
          result.append(rating)
  return result

# esta função é acionada pelo anvil para que o colab/python receba o arquivo
# com os dados (csv), e inicia automaticamente o treinamento.


@anvil.server.callable
def get_data(file, modelo_id):
    print(modelo_id)
    try:
        with anvil.media.TempFile(file) as file_name:
            nome = modelo_id + '.csv'
            # file = open(nome,'w+')
            df = pd.read_csv(file_name)
            df.to_csv(nome)
            if(df.empty):
                return 'Não recebemos o arquivo, gentileza enviar novamente!'
            else:
                # training_model()
                colab_treinar_modelo(nome)
                ## print(df)
                return 'Arquivo Em Treinamento!'
    except:
        return 'Não foi possível obter o arquivo devido ao tamanho do mesmo'

@anvil.server.callable
def send_file(file):
    # print(modelo_id)
    with anvil.media.TempFile(file) as file_name:
        df = pd.read_csv(file_name)
        if(df.empty):
            return 'Não recebemos o arquivo, gentileza enviar novamente!'
        else:
            return colab_servercall_treinar_modelo(csv_filename) #retorna id modelo e treina numa thread

# exemplo
# /notify/start/:model_id e /notify/finish/:model_id

def notify_start(modelo_id):
  # executa o request para a api de acordo com os parametros
  site = api_treinamento_iniciado + modelo_id
  #response = requests.get(f'https://cd7jwv2auk4wzkrn.anvil.app/_/private_api/NAUJWAV2RPBGYXSGAHBTFQXI/api_treinamento_iniciado/{modelo_id}')
  response = requests.get(site)
  # obtem o json de resposta
  data = response.json()
  return data

def notify_finish(modelo_id):
  # executa o request para a api de acordo com os parametros
  site = api_treinamento_finalizado + modelo_id
  response = requests.get(site)
  # response = requests.get(f'https://cd7jwv2auk4wzkrn.anvil.app/_/private_api/NAUJWAV2RPBGYXSGAHBTFQXI/api_treinamento_finalizado/{modelo_id}')
  # obtem o json de resposta
  data = response.json()
  return data

# esta é a função que efetivamente aciona o treinamento do modelo.
def colab_treinar_frontend(csv_filename):

  # try:
  model_name = csv_filename[:8]
  print('Training model {}'.format(model_name))
  # aciona o servidor anvil para informar que o modelo está treinado
  print("Aciona servidor Anvil para informar treinamento inicializado")
  print(notify_start(model_name))
  # site = "https://CD7JWV2AUK4WZKRN.anvil.app/_/private_api/NAUJWAV2RPBGYXSGAHBTFQXI/api_treinamento_iniciado/" + model_name
  # r = requests.get(site)
  # print(r.status_code)
  # print(r.headers)
  # print(r.content)
  try:
    model = train_model(csv_filename)
    print("Saving model...")
    model_filename = save_model(model, model_name)
    print("Modelo salvo!")
  except:
      print('Um erro ocorreu ao executar o treinamento de {}'.format(model_name))

  # print(f'model saved to {model_filename}')

  # aciona o servidor anvil para informar que o modelo está treinado
  print("Aciona servidor Anvil para informar treinamento finalizado")
  print(notify_finish(model_name))
  # site = "https://CD7JWV2AUK4WZKRN.anvil.app/_/private_api/NAUJWAV2RPBGYXSGAHBTFQXI/api_treinamento_finalizado/" + model_name
  # r = requests.get(site)
  # print(r.status_code)
  # print(r.headers)
  # print(r.content)
  # except:


# esta funcao inicia o treinamento de um arquivo salvo no diretorio
def colab_treinar_modelo(csv_filename):
  model_name = csv_filename[:8]
  # cria a thread para inciar treinamento
  t = Thread(target=colab_treinar_frontend, args=(csv_filename, ))
  t.start()
  # retorna o nome modelo
  return model_name

"""# Inicia o servidor anvil para rodar até o fim dos tempos..."""

################### aqui roda o serviço e faz todos os prints das APIs acionadas ####### essa é a melhor opção para rodar
anvil.server.wait_forever()