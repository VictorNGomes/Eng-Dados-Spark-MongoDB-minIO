# Projeto de Automação de Atualização de Notícias Tecnológicas - Readme

Este é o readme.md do Projeto de Automação de Atualização de Notícias Tecnológicas. Aqui você encontrará informações sobre a descrição do projeto, detalhes da implementação da infraestrutura, conjunto de dados escolhido, resultados obtidos, dificuldades encontradas e ferramentas utilizadas.

## Descrição do Projeto

O Projeto de Automação de Atualização de Notícias Tecnológicas consiste em utilizar o Apache Airflow para automatizar e agendar tarefas em um fluxo de pipeline. O objetivo principal é coletar notícias sobre tecnologia da API do New York Times, armazenar os dados brutos em uma Object Store (MinIO) em uma pasta chamada "raw" e, ao mesmo tempo, filtrar as notícias usando o Apache Spark para obter apenas as notícias relevantes, que serão enviadas para um banco de dados MongoDB. O Airflow será responsável por executar diariamente o fluxo de pipeline, atualizando o banco de dados com as novas notícias.

## Detalhes da Implementação da Infraestrutura

A implementação da infraestrutura do Projeto de Automação de Atualização de Notícias Tecnológicas envolve os seguintes componentes:

1. **Apache Airflow**: O Airflow é utilizado para definir, agendar e executar as tarefas do fluxo de pipeline. Ele permite criar tarefas independentes e orquestrá-las em uma sequência lógica definida. O Airflow também fornece um painel de controle para monitorar o status das tarefas e acompanhar o fluxo de trabalho.

2. **API do New York Times**: Utilizamos a API do New York Times para coletar as notícias sobre tecnologia. Por meio do módulo `requests` do Python, fazemos requisições HTTP para a API e obtemos os dados necessários.

3. **Object Store (MinIO)**: Uma Object Store, no caso utilizamos o MinIO, é usada para armazenar os dados brutos das notícias coletadas da API. Os arquivos são armazenados em uma pasta chamada "raw", onde permanecem disponíveis para consultas futuras ou análises adicionais.

4. **Apache Spark**: O Apache Spark é utilizado para processar e filtrar os dados brutos das notícias. Usamos o Spark para realizar as transformações necessárias e filtrar apenas as notícias relacionadas à tecnologia. O resultado é um conjunto de dados filtrado que será armazenado no banco de dados MongoDB.

5. **Banco de Dados MongoDB**: O MongoDB é o banco de dados escolhido para armazenar as notícias filtradas. Cada notícia é armazenada como um documento JSON em uma coleção específica, representando um mês específico. O Airflow é responsável por atualizar o banco de dados diariamente com as novas notícias coletadas.

6. **Docker e Docker Compose**: Utilizamos o Docker para criar contêineres independentes para cada componente do projeto, como o servidor de aplicação Flask, o Spark, o MongoDB e o MinIO. O Docker Compose foi utilizado para definir e configurar os serviços em um único arquivo, simplificando o processo de implantação e garantindo uma infraestrutura consistente.

## Conjunto de Dados Escolhido

O conjunto de dados escolhido para o Projeto de Automação de Atualização de Notícias Tecnológicas são as notícias sobre tecnologia obtidas da API do New York Times. As notícias são fornecidas em formato JSON e contêm informações como título, autor, data de publicação, conteúdo e outras metainformações relevantes. Esses dados brutos são armazenados na Object Store (MinIO) na pasta "raw" e, em seguida, filtrados e processados usando o Apache Spark.

## Resultados Obtidos

Após a implementação do fluxo de pipeline automatizado utilizando o Apache Airflow, realizamos testes e avaliações do projeto. Os resultados obtidos mostraram que o sistema foi capaz de coletar as notícias sobre tecnologia da API do New York Times, armazenar os dados brutos na Object Store e filtrar as notícias relevantes usando o Apache Spark. As notícias filtradas foram armazenadas no banco de dados MongoDB em coleções específicas para cada mês. O Airflow foi responsável por executar o pipeline diariamente e atualizar o banco de dados com as novas notícias.

## Dificuldades Encontradas

Durante o desenvolvimento do Projeto de Automação de Atualização de Notícias Tecnológicas, encontramos algumas dificuldades. Uma das principais dificuldades foi lidar com a implementação e configuração da infraestrutura, em destaque a integração do Apache Spark com o MongoDB e o MinIO.

Foi necessário configurar os conectores adequados no Spark para permitir a leitura e gravação de dados entre o Spark e o MongoDB, bem como para o MinIO por meio do protocolo S3. Isso envolveu a instalação e configuração dos drivers e bibliotecas necessários, além de ajustar as configurações do Spark para garantir um desempenho adequado durante as operações de leitura e gravação.

Superar essas dificuldades exigiu pesquisa, experimentação e ajustes iterativos para garantir que todas as peças do sistema estivessem corretamente configuradas e se comunicassem adequadamente.

## Ferramentas Utilizadas

As principais ferramentas utilizadas no Projeto de Automação de Atualização de Notícias Tecnológicas incluem:

- Apache Airflow: Utilizado para agendar e executar as tarefas do fluxo de pipeline.
- API do New York Times: Utilizada para coletar as notícias sobre tecnologia.
- MinIO: Object Store utilizada para armazenar os dados brutos das notícias.
- Apache Spark: Framework utilizado para processar e filtrar os dados brutos das notícias.
- MongoDB: Banco de dados escolhido para armazenar as notícias filtradas em coleções mensais.
- Docker: Utilizado para criar contêineres independentes para cada componente do projeto.
- Docker Compose: Utilizado para definir e configurar os serviços do projeto em um único arquivo.

## Conclusão

O Projeto de Automação de Atualização de Notícias Tecnológicas foi desenvolvido com sucesso, permitindo coletar notícias sobre tecnologia da API do New York Times, armazenar os dados brutos em uma Object Store (MinIO), filtrar as notícias usando o Apache Spark e armazenar as notícias filtradas no MongoDB. O uso do Apache Airflow possibilitou automatizar e agendar a execução do fluxo de pipeline, garantindo que o banco de dados MongoDB fosse atualizado diariamente com as novas notícias. Durante o processo, superamos desafios relacionados à implementação e configuração da infraestrutura, em destaque a integração do Spark com o MongoDB e o MinIO. Com a infraestrutura implementada e as ferramentas utilizadas, obtivemos um sistema funcional e escalável para automação da atualização de notícias tecnológicas.
