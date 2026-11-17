import math
import os
import sqlite3
from datetime import datetime

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SPORT = 'mma_mixed_martial_arts'
REGIONS = 'us,eu,uk,au'
MARKETS = 'h2h'


def _odd_valida(valor):
    """Odds decimais são números finitos maiores que 1."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool) and math.isfinite(valor) and valor > 1


def _evento_valido(evento):
    """Confere apenas a estrutura usada abaixo; não valida o conteúdo esportivo."""
    try:
        if not (isinstance(evento['commence_time'], str) and isinstance(evento['home_team'], str)
                and isinstance(evento['away_team'], str) and isinstance(evento['bookmakers'], list)):
            return False
        for bookmaker in evento['bookmakers']:
            if not isinstance(bookmaker['title'], str):
                return False
            for market in bookmaker['markets']:
                if not isinstance(market['key'], str):
                    return False
                for outcome in market['outcomes']:
                    if not isinstance(outcome['name'], str) or 'price' not in outcome:
                        return False
        return True
    except (KeyError, TypeError):
        return False


def analisar_proximo_evento_ufc():
    url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'

    params = {
        'apiKey': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': 'decimal',
    }

    if not API_KEY:
        print("Erro: API_KEY ausente. Configure o arquivo .env.")
        return

    print("Buscando eventos futuros de UFC/MMA na API...")
    try:
        response = requests.get(url, params=params, timeout=(5, 20))
    except requests.RequestException as erro:
        # A mensagem da exceção contém a URL com a chave; exibir apenas o tipo.
        print(f"Erro de rede ao consultar a API: {type(erro).__name__}")
        return

    if response.status_code != 200:
        print(f"Erro: {response.status_code}")
        return

    try:
        dados = response.json()
    except ValueError:
        print("Erro: a API não retornou JSON válido.")
        return

    if not dados:
        print("Nenhum evento futuro encontrado na API no momento.")
        return

    if not isinstance(dados, list) or not all(_evento_valido(evento) for evento in dados):
        print("Erro: resposta da API em formato inesperado; nada foi gravado.")
        return

    proxima_data = min([evento['commence_time'][:10] for evento in dados])
    print(f"Proximo evento detectado para o dia: {proxima_data}\n")

    lista_lutas = []

    for evento in dados:
        if evento['commence_time'][:10] == proxima_data:
            lutador_a = evento['home_team']
            lutador_b = evento['away_team']

            for bookmaker in evento['bookmakers']:
                casa = bookmaker['title']

                for market in bookmaker['markets']:
                    if market['key'] == 'h2h':
                        for outcome in market['outcomes']:
                            nome_selecao = outcome['name']
                            odd = outcome['price']
                            if not _odd_valida(odd):
                                continue

                            tipo_aposta = 'Empate' if nome_selecao.lower() in ('draw',
                                                                               'empate') else f'Vitória: {nome_selecao}'

                            lista_lutas.append({
                                'Data_Evento': proxima_data,
                                'Luta': f"{lutador_a} vs {lutador_b}",
                                'Aposta': tipo_aposta,
                                'Casa': casa,
                                'Odd': odd
                            })

    df = pd.DataFrame(lista_lutas)

    if not df.empty:
        df['Probabilidade Real (%)'] = (1 / df['Odd'] * 100).round(2)

        df_para_banco = df.copy()
        df_para_banco['Data_Coleta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect('historico_odds_ufc.db') as conexao:
            df_para_banco.to_sql('tabela_odds', conexao, if_exists='append', index=False)

        print("Dados salvos com sucesso no banco de dados.")
        df_ordenado = df.sort_values(by=['Luta', 'Aposta', 'Odd'], ascending=[True, True, False])
        df_unico = df_ordenado.drop_duplicates(subset=['Luta', 'Aposta', 'Casa'])
        df_top_3_casas = df_unico.groupby(['Luta', 'Aposta']).head(3)

        print(f"\nTOP ODDS PARA O EVENTO! ({proxima_data}):")
        print(df_top_3_casas[['Luta', 'Aposta', 'Odd', 'Probabilidade Real (%)', 'Casa']].to_string(index=False))

    else:
        print(f"Nenhuma odd encontrada especificamente para o evento do dia {proxima_data}.")

if __name__ == "__main__":
    analisar_proximo_evento_ufc()