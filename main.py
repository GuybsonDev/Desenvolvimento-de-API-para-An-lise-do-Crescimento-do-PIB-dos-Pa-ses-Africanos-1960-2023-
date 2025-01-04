# Importações
import pandas as pd
from flask import Flask, jsonify, request

# Comando para iniciação do Flask
app = Flask(__name__)


# Objeto para iniciar a Página inicial
@app.route('/')
def paginainicial():
  return 'A API está no ar'


# Endpoint de todos os dados
@app.route('/dadoscompletos')
def pegar_dados():
  # Carrega os dados a partir do arquivo CSV
  dados = pd.read_csv('Africa_GDP.csv')

  # Define a coluna "Year" como índice para facilitar a consulta dos dados
  dados.set_index("Year", inplace=True)

  # Converte os dados para um dicionário, onde cada ano será uma chave (index) e os        dados do ano serão o valor
  resposta_api_dict = dados.to_dict(orient="index")

  # Cria a resposta da API encapsulando os dados em um dicionário com a chave 'Dados       completos'
  resposta_api = {'Dados completos': resposta_api_dict}

  # Exibe os dados no console (opcional, para fins de debug)
  print(jsonify(resposta_api))

  # Retorna os dados como um JSON para a resposta da API
  return jsonify(resposta_api)


# Endpoint para filtrar por período
@app.route('/dadosperiodo')
def pegar_dados_por_periodo():
  # Verifica se os parâmetros de consulta foram fornecidos
  inicio = request.args.get('inicio', type=int)
  fim = request.args.get('fim', type=int)

  # Caso os parâmetros não sejam informados
  if inicio is None or fim is None:
    return jsonify({
        "Mensagem":
        "Periodo não informado. Por favor, forneca os parametros 'inicio' e 'fim'.",
        "Exemplo": "/dadosperiodo?inicio=2000&fim=2010"
    }), 400  # Código HTTP 400: Bad Request

  # Carrega os dados
  dados = pd.read_csv('Africa_GDP.csv')

  # Filtra pelo período
  dados_filtrados = dados[(dados['Year'] >= inicio) & (dados['Year'] <= fim)]
  dados_filtrados.set_index("Year", inplace=True)

  # Converte para dicionário
  resposta_api_dict = dados_filtrados.to_dict(orient="index")
  resposta_api = {
      "Periodo": f"{inicio}-{fim}",
      "Dados filtrados": resposta_api_dict
  }

  return jsonify(resposta_api)


# Inicializando o aplicativo
app.run(host='0.0.0.0')
