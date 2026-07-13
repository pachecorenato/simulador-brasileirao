from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

# Importamos o motor do nosso banco de dados
from banco_de_dados import motor

# 1. Ligando o servidor Flask
app = Flask(__name__)
CORS(app) # Isso libera o Front-end para fazer pedidos na API

# 2. O Cérebro: Carregamos os dados com Pandas assim que a API liga
print("Carregando o Cérebro Analítico...")
query = "SELECT * FROM historico_serie_a"
df = pd.read_sql(query, motor)
df['total_jogos'] = df['vitorias'] + df['empates'] + df['derrotas']
df['chance_vitoria_%'] = ((df['vitorias'] / df['total_jogos']) * 100).round(2)

# ==========================================
# ROTA 1: Entregar o Top 10
# ==========================================
@app.route('/api/top10', methods=['GET'])
def top_10():
    """Retorna os 10 times com maior probabilidade histórica de vitória.

    Endpoint: GET /api/top10

    Ordena o DataFrame global `df` pela coluna 'chance_vitoria_%' em
    ordem decrescente e seleciona os 10 primeiros registros.

    Args:
        Nenhum parâmetro de rota, querystring ou corpo é esperado.

    Returns:
        flask.Response: Resposta JSON contendo uma lista de até 10
            objetos, cada um com as chaves 'nome', 'participacoes',
            'total_jogos' e 'chance_vitoria_%', representando o
            ranking dos times mais "letais" historicamente.
    """
    # Ordenamos igual fizemos no terminal
    df_ordenado = df.sort_values(by='chance_vitoria_%', ascending=False).head(10)
    
    # O jsonify transforma a tabela do Pandas no formato JSON (que o front-end entende)
    resultado = df_ordenado[['nome', 'participacoes', 'total_jogos', 'chance_vitoria_%']].to_dict(orient='records')
    
    return jsonify(resultado)

# ==========================================
# ROTA 2: O Simulador de Confrontos
# ==========================================
@app.route('/api/simular', methods=['GET'])
def simular():
    """Simula um confronto entre dois times e retorna as probabilidades de vitória.

    Endpoint: GET /api/simular?time_a=<nome>&time_b=<nome>

    Lê os nomes dos dois times a partir da querystring da requisição,
    busca a taxa histórica de vitória ('chance_vitoria_%') de cada um
    no DataFrame global `df` e calcula a probabilidade relativa de
    vitória de cada time no confronto direto (regra de três simples
    sobre a soma das forças históricas).

    Args:
        time_a (str, via querystring 'time_a'): Nome do time mandante.
            Deve corresponder exatamente a um valor da coluna 'nome'
            no DataFrame.
        time_b (str, via querystring 'time_b'): Nome do time visitante.
            Deve corresponder exatamente a um valor da coluna 'nome'
            no DataFrame.

    Returns:
        flask.Response: Uma tupla (JSON, status_code) em três cenários possíveis:
            - 400 Bad Request: se 'time_a' ou 'time_b' não forem enviados,
              retorna {"erro": "Você precisa enviar o time_a e o time_b!"}.
            - 404 Not Found: se algum dos times não existir no DataFrame,
              retorna {"erro": "Um dos times não foi encontrado no banco."}.
            - 200 OK (implícito): em caso de sucesso, retorna um objeto
              com as chaves 'confronto' (string "time_a x time_b"),
              'time_a' (dict com 'nome' e 'probabilidade_vitoria') e
              'time_b' (dict com 'nome' e 'probabilidade_vitoria').
    """
    # Pegamos os nomes dos times que o Front-end vai mandar pela URL
    time_a = request.args.get('time_a')
    time_b = request.args.get('time_b')

    # Filtro de segurança: Se o usuário esquecer de mandar os times
    if not time_a or not time_b:
        return jsonify({"erro": "Você precisa enviar o time_a e o time_b!"}), 400

    try:
        # Puxamos a força de cada time no DataFrame
        forca_a = df.loc[df['nome'] == time_a, 'chance_vitoria_%'].values[0]
        forca_b = df.loc[df['nome'] == time_b, 'chance_vitoria_%'].values[0]
    except IndexError:
        return jsonify({"erro": "Um dos times não foi encontrado no banco."}), 404

    # A nossa matemática da probabilidade
    forca_total = forca_a + forca_b
    prob_a = round((forca_a / forca_total) * 100, 1)
    prob_b = round((forca_b / forca_total) * 100, 1)

    # Entregamos o "prato pronto" em formato JSON
    resposta = {
        "confronto": f"{time_a} x {time_b}",
        "time_a": {
            "nome": time_a, 
            "probabilidade_vitoria": prob_a
        },
        "time_b": {
            "nome": time_b, 
            "probabilidade_vitoria": prob_b
        }
    }
    
    return jsonify(resposta)

# ==========================================
# ROTA 3: Listar todos os times (Para o Menu)
# ==========================================
@app.route('/api/times', methods=['GET'])
def listar_times():
    """Lista todos os nomes de times disponíveis no banco de dados.

    Endpoint: GET /api/times

    Extrai a coluna 'nome' do DataFrame global `df`, remove valores
    duplicados e ordena os nomes em ordem alfabética. Usado para
    popular os menus de seleção (dropdowns) do front-end.

    Args:
        Nenhum parâmetro de rota, querystring ou corpo é esperado.

    Returns:
        flask.Response: Resposta JSON contendo uma lista de strings
            com os nomes de todos os times cadastrados, em ordem
            alfabética.
    """
    # O Pandas pega a coluna 'nome', remove duplicatas (se houver) e converte para lista
    times = sorted(df['nome'].unique().tolist())
    return jsonify(times)

# 3. Colocando o servidor no ar
if __name__ == '__main__':
    print("🚀 API do Brasileirão rodando! O Garçom está pronto para anotar os pedidos.")
    app.run(debug=True, port=5000)
