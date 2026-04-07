```markdown
# Sistema de Medição de Estação Meteorológica IoT

Este projeto é um sistema completo de ponta a ponta para monitoramento meteorológico. Um dispositivo físico (Arduino) lê dados de sensores e os envia via comunicação serial para um servidor backend em Python (Flask). Os dados são persistidos em um banco de dados SQLite e exibidos em uma interface web responsiva com gráficos em tempo real.

## Funcionalidades
- Comunicação Serial: Leitura de dados do Arduino (Temperatura, Umidade e Pressão).
- API REST: Rotas para criar, ler, atualizar e excluir (CRUD) as leituras.
- Banco de Dados: Armazenamento persistente usando SQLite (`dados.db`).
- Dashboard Web: Visualização em tempo real das últimas leituras com gráficos interativos usando Chart.js.
- Histórico e Gestão: Página dedicada para visualização do histórico completo, com formulário para edição e opção de exclusão de registros.

## Estrutura do Projeto
```

/
|-- main.py              # Servidor Flask e rotas da interface web e API
|-- serial_reader.py     # Script responsável por ler a porta serial e enviar para a API
|-- database.py          # Configurações e funções de manipulação do banco de dados (SQLite)
|-- dados.db             # Arquivo do banco de dados (contém as leituras de exemplo)
|-- templates/           # Arquivos HTML da interface
|   |-- index.html       # Dashboard principal
|   |-- historico.html   # Tabela de histórico
|   |-- editar.html      # Formulário de edição
|-- static/
|-- css/
|   |-- style.css    # Folha de estilos da página
|-- js/
|-- main.js      # Lógica do frontend (gráficos, tabelas e integração com a API)

````

## Tecnologias Utilizadas
- Hardware: Arduino Uno, Sensores DHT11 e BMP180.
- Backend: Python 3, Flask, PySerial, Requests.
- Frontend: HTML5, CSS3, JavaScript (Vanilla), Chart.js.
- Banco de Dados: SQLite.

## Instruções de Instalação e Execução

### Pré-requisitos
1. Ter o Python 3.x instalado em sua máquina.
2. Ter o Arduino conectado na porta USB rodando o código fonte `.ino` do projeto.

### Instalação
1. Clone o repositório para o seu computador:
   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
````

2. Instale as bibliotecas Python necessárias:

   ```bash
   pip install flask pyserial requests
   ```

### Como Executar

1. Ligue o Servidor Web: No terminal, na raiz do projeto, execute o arquivo principal do Flask:

   ```bash
   python main.py
   ```

   O servidor estará rodando no endereço local: [http://127.0.0.1:5000](http://127.0.0.1:5000)

2. Inicie a Leitura Serial: Abra um NOVO terminal, verifique se a porta configurada no arquivo `serial_reader.py` (ex: COM5) está correta para o seu Arduino, e execute:

   ```bash
   python serial_reader.py
   ```

3. Visualização: Acesse [http://127.0.0.1:5000](http://127.0.0.1:5000) no seu navegador para ver o painel em funcionamento.

## Rotas da API REST

| Método | Rota           | Descrição                                               |
| ------ | -------------- | ------------------------------------------------------- |
| GET    | /leituras      | Retorna todas as leituras armazenadas em formato JSON.  |
| POST   | /leituras      | Recebe um JSON do `serial_reader.py` e insere no banco. |
| PUT    | /editar/<id>   | Atualiza os dados de uma leitura específica.            |
| DELETE | /leituras/<id> | Exclui uma leitura específica do banco de dados.        |


# Fotos do prototipo:

![Imagem 1](/POND1.jpeg)

![Imagem 2](/POND2.jpeg)

![Imagem 3](/POND3.jpeg)


