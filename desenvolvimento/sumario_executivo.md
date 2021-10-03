# Sumário Executivo

Suggeri é um sistema de recomendação como serviço usando inteligência artificial.

Este sumário apresenta as informações essenciais do projeto Suggeri, para mais detalhamento acesse as outras áreas disponíveis no repositório.


## Ferramentas

O sistema de recomendação como serviço tem como base:
- [Site do Suggeri](http://www.suggeri.com.br/), explicando o funcionamento e preços
- [Documentação da API](http://www.suggeri.com.br/api.html), com todos os detalhes de como acessar o serviço
- [Site Administrativo](https://suggeri.anvil.app/) para receber as empresas e suas bases de dados
- API para receber as chamadas dos sites dos clientes
- Servidor na nuvem escalável para treino automático de modelos a partir das bases

Para o seu funcionamento são utilizados:
- [Surprise](http://surpriselib.com/), scikit Python para construir e analisar sistemas de recomendação
- [Pandas](https://pandas.pydata.org/), biblioteca de software escrita para a linguagem de programação Python para manipulação e análise de dados
- [REST API](https://restfulapi.net/), estilo de arquitetura para sistemas distribuídos
- [Docker](https://www.docker.com/), sistema de virtulização para entregar sofwares como containers escaláveis
- [Anvil Works](https://anvil.works/), plataforma para contrução e hospedagem de aplicativos web full-stack escritos em Python
- [Google Cloud](https://cloud.google.com/), serviço de cloud fornecido pela Google


## Dataset

O dataset analisado para definir o conceito do produto Suggeri foi a listagem de avaliações de produtos de beleza da Amazon, disponível publicamente no link https://www.kaggle.com/skillsmuggler/amazon-ratings.

Uma versão reduzida do dataset pode ser encontrado neste repositório no arquivo (dataset_test.csv)[../data/dataset_test.csv].


## Gerenciamento do Projetos

Durante a execução, os seguintes artefatos foram utilizados:
- [plano_trabalho.md](plano_trabalho.md) - Plano de Trabalho
- [plano_custos.md](plano_custos.md) - Plano de Custo do Projeto
- [cronograma_implementacao.md](cronograma_implementacao.md) - Cronograma de Implementação
- [analise_riscos.md](analise_riscos.md) - Análise de Risco
- [licoes_aprendidas.md](licoes_aprendidas.md) - Lições Aprendidas