# Guia básico de configuração do Anvil

1)	Faça um clone do nosso código fonte para a sua conta, clicando no link abaixo:
2)	Você deve habilitar o Anvil Uplink. Na barra lateral esquerda, na tela de edição do código, clique no ícone de engrenagem, vá até Uplink e confirue a opção para conectar como Server Code, como no exemplo abaixo:

 
Esta será a tua chave que você vai utilizar no python, para criar uma conexão entre o Anvil e toda a estrutura de APIs que criamos no python – que farão o treinamento e as predições.

3)	Na barra de navegação lateral, clique em “ServerModule1”:

 

4)	No rodapé da janela de código, o Anvil irá lhe mostrar qual o caminho para você testar suas APIs, conforme exemplo abaixo:

 
 
5)	Se você desejar um caminho mais amigável, é necessário tornar o teu “clone” da nossa aplicação algo público, onde você poderá criar um endereço único para acessar o site da aplicação. Faça isto, vai facilitar sua vida.

# Guia básico de instalação no Google Cloud

1)	Um guia básico e direto pode ser visualizado neste link: https://www.youtube.com/watch?v=5OL7fu2R4M8&list=PLm282P3sC0ge0NNrClpv9i_-BKkKU5zVv&index=1&t=368s

2)	Acessar o site cloud.google.com e criar um cadastro com uma conta do google
a.	Clicar em “Console”
b.	Ativar as funções de faturamento (inserir dados de cartão de crédito)
c.	Abrir o link “Compute Engine” e depois em “Instâncias de VM”
d.	Abrir “Criar Instância” e escolher as configurações mais adequadas (sugestão é utilizar uma máquina com pelo menos 8GbRAM, uma vez que o treinamento exige uma quantidade razoável de RAM. O ideal seriam 16 GB, mas isso tornaria os custos muito altos, porém a ideia é apenas fazer uma prova de conceito. É interessante que de instalação da VM seja região seja São Paulo. Utilizar o disco  de inicialização padrão, e configurar o firewall para permitir tráfego HTTP e HTTPS. 
e.	Após a criação da VM, conectar usando o ícone de SSH.
f.	Pronto, a VM já está funcional, os próximos passos são instalar as nossas APIs.

3)	Configurando a API
a.	Crie um diretório para a aplicação usando o comando:
i.	“mkdir <nome>”, substituindo <nome> pelo nome que você achar mais interessante.
b.	Navegue até o diretório com o comando “cd <nome>”
c.	A tela do SSH possui um ícone no canto superior direito parecido com uma engrenagem. Clique nele e escolha as opções de fazer upload de arquivo, onde devem ser enviados os 2 arquivos de intalação (requiriments.txt e api_suggeri_cloud.py).
d.	Para instalar, execute:
i.	“pip install -r requirements.txt”
e.	Caso a instalação termine com sucesso, agora vamos instalar o tmux, que é um terminal que irá rodar em background mesmo que você fecha a sua conexão SSH:
i.	Execute “sudo apt install tmux”
f.	A instalação está pronta.

4)	Executando a API
a.	Abra o tmux:
i.	Basta executar o comando “tmux” no terminal do linux
b.	Execute a nossa aplicação:
i.	No terminal do linux, execute “python api_suggeri_cloud.py”
c.	Pronto! Neste momento, vc irá visualizar que a conexão foi realizada com sucesso ao servidor Anvil.



# Como configurar a API para conectar ao Anvil

Se você for executar a aplicação conectada à sua própria instância do Anvil (o que é uma boa ideia), é necessário configurar o arquivo python api_suggeri_cloud.py para a conexão correta.
Edite este arquivo em um editor de textos puro ou preferencialmente no seu editor python favorito.
Na linha 59, você deve informar ao Anvil qual a chave de conexão com a sua instância:

anvil.server.connect("GOV2WLOJBBXX5MY4ZP5PTBXD-QEV7AO4O3G54JYOU")

Nas linhas 319:
site = "https://suggeri.anvil.app/_/api/api_treinamento_iniciado/" + modelo_id

E 328:
site = "https://suggeri.anvil.app/_/api/api_treinamento_finalizado/" + modelo_id

Você deve substituir o endereço https pelo endereço da API que você configurou no seu servidor Anvil, conforme sugerido no item 5 do nosso “Guia básico de configuração do Anvil”, no início deste documento.



