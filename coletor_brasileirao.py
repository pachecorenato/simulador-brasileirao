import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from banco_de_dados import motor, TimeHistorico

# ==========================================
# CLASSE DO COLETOR (Orientação a Objetos)
# ==========================================
class ColetorBrasileirao:
    """Coleta a tabela de classificação do Campeonato Brasileiro (Série A) na Wikipédia.

    Para um ano específico, monta a URL da página correspondente na
    Wikipédia em português, faz o download do HTML, localiza a tabela
    de classificação (identificada pelas colunas 'Pts' e 'V') e extrai
    os dados de cada time em formato estruturado.

    Attributes:
        ano (int): Ano da temporada do Brasileirão a ser coletado.
        url (str): URL da página da Wikipédia referente ao ano informado.
        headers (dict): Cabeçalhos HTTP (User-Agent) usados na requisição,
            para simular um navegador comum e evitar bloqueios.
    """
    
    def __init__(self, ano):
        """Inicializa o coletor para um ano específico do Brasileirão.

        Args:
            ano (int): Ano da temporada a ser coletada (ex.: 2024).
        """
        self.ano = ano
        self.url = f"https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{ano}_-_S%C3%A9rie_A"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
    def extrair_dados(self):
        """Extrai a tabela de classificação da Série A para o ano configurado.

        Faz uma requisição HTTP à página da Wikipédia referente ao ano
        (`self.ano`), localiza a tabela de classificação (a primeira
        tabela com classe 'wikitable' que contenha as colunas 'Pts' e
        'V') e percorre suas linhas extraindo nome do time, pontos,
        vitórias, empates e derrotas.

        Args:
            Nenhum parâmetro adicional é recebido; a função utiliza os
            atributos `self.url` e `self.headers` definidos no
            construtor da classe.

        Returns:
            list[dict]: Lista de dicionários, um por time, cada um
                contendo as chaves:
                    - 'time' (str): nome do time, já limpo de notas
                      e referências entre parênteses/colchetes.
                    - 'pontos' (int): total de pontos na temporada.
                    - 'vitorias' (int): total de vitórias na temporada.
                    - 'empates' (int): total de empates na temporada.
                    - 'derrotas' (int): total de derrotas na temporada.
                Retorna uma lista vazia caso a requisição falhe
                (status diferente de 200) ou a tabela de classificação
                não seja encontrada na página.
        """
        print(f"Buscando dados do Brasileirão {self.ano}...")
        resposta = requests.get(self.url, headers=self.headers)
        
        if resposta.status_code != 200:
            print(f"Erro de conexão no ano {self.ano}!")
            return []
            
        sopa = BeautifulSoup(resposta.text, 'html.parser')
        tabelas = sopa.find_all('table', class_='wikitable')
        tabela_classificacao = None
        
        for tabela in tabelas:
            cabecalhos = [c.text.strip() for c in tabela.find_all('th')]
            if 'Pts' in cabecalhos and 'V' in cabecalhos:
                tabela_classificacao = tabela
                break
                
        if not tabela_classificacao:
            print(f"Tabela não encontrada para o ano {self.ano}.")
            return []
            
        resultados = []
        linhas = tabela_classificacao.find_all('tr')
        
        for linha in linhas[1:]:
            colunas = linha.find_all('td')
            if len(colunas) >= 8:
                # Pega o texto bruto
                nome_time_sujo = colunas[0].text.strip()
                
                # A TESOURA: Corta no '(' e no '[', pegando só a primeira parte (o nome limpo)
                nome_time = nome_time_sujo.split('(')[0].split('[')[0].strip()
                
                pontos = colunas[1].text.strip()
                vitorias = colunas[3].text.strip()
                empates = colunas[4].text.strip()
                derrotas = colunas[5].text.strip()
                
                # Guardando como números inteiros (int) para permitir os cálculos
                dados_time = {
                    "time": nome_time,
                    "pontos": int(pontos),
                    "vitorias": int(vitorias),
                    "empates": int(empates),
                    "derrotas": int(derrotas)
                }
                
                resultados.append(dados_time)
                
        return resultados

# ==========================================
# O MOTOR DE AGREGAÇÃO (2020 a 2025)
# ==========================================
anos_para_buscar = [2020, 2021, 2022, 2023, 2024, 2025]
historico_times = {}

print("\nIniciando extração do histórico...\n")

for ano in anos_para_buscar:
    coletor = ColetorBrasileirao(ano)
    tabela_ano = coletor.extrair_dados()
    
    for linha in tabela_ano:
        nome = linha['time']
        
        if nome not in historico_times:
            historico_times[nome] = {
                "pontos": 0,
                "vitorias": 0,
                "empates": 0,
                "derrotas": 0,
                "participacoes": 0
            }
            
        historico_times[nome]["pontos"] += linha["pontos"]
        historico_times[nome]["vitorias"] += linha["vitorias"]
        historico_times[nome]["empates"] += linha["empates"]
        historico_times[nome]["derrotas"] += linha["derrotas"]
        historico_times[nome]["participacoes"] += 1

# Ordenamos o resultado do maior pontuador para o menor
tabela_consolidada = sorted(
    historico_times.items(), 
    key=lambda x: x[1]["pontos"], 
    reverse=True
)

# Imprimimos o resultado final formatado
print("\n" + "=" * 80)
print("🏆 RANKING CONSOLIDADO DO BRASILEIRÃO (2020 - 2025) 🏆".center(80))
print("=" * 80)
print(f"{'Time': <20} | {'Anos': <4} | {'Pts': <4} | {'V': <4} | {'E': <4} | {'D': <4}")
print("-" * 80)

for time, stats in tabela_consolidada:
    print(f"{time: <20} | {stats['participacoes']: <4} | {stats['pontos']: <4} | {stats['vitorias']: <4} | {stats['empates']: <4} | {stats['derrotas']: <4}")

print("=" * 80)

# ==========================================
# SALVANDO NO BANCO DE DADOS
# ==========================================

print("\nAbrindo conexão com o Banco de Dados...")

# 1. Criamos a Sessão ligada ao nosso motor
Session = sessionmaker(bind=motor)
sessao = Session()

# 2. Varremos a nossa tabela consolidada
for time, stats in tabela_consolidada:
    
    # REGRA DE NEGÓCIO: Verificamos se o time já existe no banco
    # Isso evita que o código quebre tentando salvar o Flamengo duas vezes
    time_existente = sessao.query(TimeHistorico).filter_by(nome=time).first()
    
    if time_existente:
        # Se o time já está no banco, nós apenas ATUALIZAMOS os dados dele
        time_existente.participacoes = stats['participacoes']
        time_existente.pontos = stats['pontos']
        time_existente.vitorias = stats['vitorias']
        time_existente.empates = stats['empates']
        time_existente.derrotas = stats['derrotas']
    else:
        # Se não existe, CRIAMOS um registro novo (Instanciamos a classe TimeHistorico)
        novo_time = TimeHistorico(
            nome=time,
            participacoes=stats['participacoes'],
            pontos=stats['pontos'],
            vitorias=stats['vitorias'],
            empates=stats['empates'],
            derrotas=stats['derrotas']
        )
        # Colocamos o time novo no "carrinho de compras"
        sessao.add(novo_time)

# 3. Mandamos o banco de dados salvar tudo de uma vez
sessao.commit()
print("Dados salvos no SQLite com sucesso!")

# 4. Fechamos a conexão por segurança
sessao.close()
