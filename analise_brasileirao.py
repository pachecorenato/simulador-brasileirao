import pandas as pd

# Importe o motor do seu arquivo de banco de dados

from banco_de_dados import motor 

print("Conectando ao banco de dados e puxando o histórico...\n")

# 1. Lendo os dados: O Pandas executa a query SQL e transforma direto numa super planilha (DataFrame)
query = "SELECT * FROM historico_serie_a"
df = pd.read_sql(query, motor)

# 2. Criando o motor de probabilidade
# Primeiro, descobrimos o total de jogos somando as colunas
df['total_jogos'] = df['vitorias'] + df['empates'] + df['derrotas']

# Depois, calculamos a chance matemática de vitória de cada time (Vitórias / Total de Jogos)
df['chance_vitoria_%'] = (df['vitorias'] / df['total_jogos']) * 100

# 3. Tratamento visual: Arredondamos para 2 casas decimais para não ficar feio
df['chance_vitoria_%'] = df['chance_vitoria_%'].round(2)

# 4. Ordenamos do mais letal (maior chance de vitória) para o menor
df_ordenado = df.sort_values(by='chance_vitoria_%', ascending=False)

# 5. Imprimimos o Top 10 dos times mais letais do Brasil (2020-2025)
print("🎯 TOP 10: PROBABILIDADE HISTÓRICA DE VITÓRIA (2020-2025) 🎯")
print("-" * 65)
# Imprimimos apenas as colunas que importam para essa análise
print(df_ordenado[['nome', 'participacoes', 'total_jogos', 'chance_vitoria_%']].head(10).to_string(index=False))
print("-" * 65)


# ==========================================
# SIMULADOR DE CONFRONTOS
# ==========================================

def simular_confronto(time_a, time_b, dataframe):
    """Simula a probabilidade de vitória entre dois times com base no histórico.

    Calcula a força histórica de cada time (percentual de vitórias já
    calculado na coluna 'chance_vitoria_%') e distribui essa força
    proporcionalmente entre os dois times (regra de três simples) para
    estimar a probabilidade de cada um vencer o confronto direto.
    Imprime o resultado formatado no console.

    Args:
        time_a (str): Nome do primeiro time (ex.: "Flamengo"), deve
            corresponder exatamente ao valor da coluna 'nome' no DataFrame.
        time_b (str): Nome do segundo time (ex.: "Fluminense"), deve
            corresponder exatamente ao valor da coluna 'nome' no DataFrame.
        dataframe (pandas.DataFrame): DataFrame contendo, no mínimo, as
            colunas 'nome' e 'chance_vitoria_%' com o histórico dos times.

    Returns:
        str: Mensagem de erro ("Erro: Um dos times não foi encontrado no
            banco de dados.") caso `time_a` ou `time_b` não existam no
            DataFrame. Quando a simulação é bem-sucedida, a função não
            retorna valor (retorna None implicitamente); o resultado é
            apenas impresso no console.
    """
    # 1. Buscamos a taxa de vitória de cada time na nossa tabela
    # O comando .loc acha a linha do time e puxa o valor da coluna 'chance_vitoria_%'
    try:
        forca_a = dataframe.loc[dataframe['nome'] == time_a, 'chance_vitoria_%'].values[0]
        forca_b = dataframe.loc[dataframe['nome'] == time_b, 'chance_vitoria_%'].values[0]
    except IndexError:
        return "Erro: Um dos times não foi encontrado no banco de dados."

    # 2. Somamos a força total do confronto
    forca_total = forca_a + forca_b

    # 3. Calculamos a fatia de cada um nesse duelo (Regra de 3 simples)
    prob_a = (forca_a / forca_total) * 100
    prob_b = (forca_b / forca_total) * 100

    # 4. Retornamos o resultado formatado
    print(f"\n⚽ SIMULAÇÃO DE CONFRONTO: {time_a} x {time_b} ⚽")
    print(f"Força histórica ({time_a}): {forca_a}% de vitórias gerais")
    print(f"Força histórica ({time_b}): {forca_b}% de vitórias gerais")
    print("-" * 45)
    print(f"Probabilidade de vitória do {time_a}: {prob_a:.2f}%")
    print(f"Probabilidade de vitória do {time_b}: {prob_b:.2f}%")
    print("-" * 45)

# Testando a nossa função:
# Você pode trocar os nomes aqui para testar com os times que quiser!
simular_confronto("Flamengo", "Fluminense", df)
simular_confronto("Palmeiras", "Corinthians", df)
