# Detalhes do Desenvolvimento

O projeto foi dividido em várias etapas e documentado da seguinte forma:
- [Plano de Trabalho e Sessões](./plano_trabalho.md)
- [Plano de Custos](./plano_custos.md)

Como estamos estruturados:
- [Site do Suggeri](http://www.suggeri.com.br/), explicando o funcionamento e preços
- [Documentação da API](http://www.suggeri.com.br/api.html), com todos os detalhes de como acessar o serviço
- [Site Administrativo](https://suggeri.anvil.app/) para receber as empresas e suas bases de dados
- API para receber as chamadas dos sites dos clientes
- Servidor na nuvem escalável para treino automático de modelos a partir das bases

Sub projetos:
- [Notebooks](./notebooks) utilizados durante a análise e implementação
- [Site](./site) com o nosso cartão de visitas online da Suggeri
- [Site Administrativo](./site_adm) para o treinamento dos modelos
- [Servidor de Predição](./servidor_predicao) para processar as requisição da API de Treinamento e Predição

