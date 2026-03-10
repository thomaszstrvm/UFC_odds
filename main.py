import requests
import pandas as pd
from datetime import datetime
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SPORT   = 'mma_mixed_martial_arts'
REGIONS = 'us,eu'
MARKETS = 'h2h'
DB_PATH = 'historico_odds_ufc.db'


def classificar_aposta(nome: str) -> str:
    return 'Empate' if nome.lower() in ('draw', 'empate') else f'Vitória: {nome}'


def analisar_proximo_evento_ufc():
    response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
        params={'apiKey': API_KEY, 'regions': REGIONS, 'markets': MARKETS, 'oddsFormat': 'decimal'}
    )

    if response.status_code != 200:
        print(f" Erro {response.status_code}: {response.text}")
        return

    dados = response.json()
    if not dados:
        print("Nenhum evento futuro encontrado.")
        return

    proxima_data = min(e['commence_time'][:10] for e in dados)
    print(f"📅 Próximo evento: {proxima_data}\n")

    lista_lutas = [
        {
            'Luta':   f"{evento['home_team']} vs {evento['away_team']}",
            'Aposta': classificar_aposta(outcome['name']),
            'Casa':   bookmaker['title'],
            'Odd':    outcome['price'],
        }
        for evento in dados
        if evento['commence_time'][:10] == proxima_data
        for bookmaker in evento['bookmakers']
        for market in bookmaker['markets']
        if market['key'] == 'h2h'
        for outcome in market['outcomes']
    ]

    if not lista_lutas:
        print(f"Nenhuma odd encontrada para {proxima_data}.")
        return

    df = pd.DataFrame(lista_lutas)

    df_melhores = (
        df.loc[df.groupby(['Luta', 'Aposta'])['Odd'].idxmax()]
        .sort_values('Luta')
        .assign(Data_Coleta=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        .reset_index(drop=True)
    )

    with sqlite3.connect(DB_PATH) as con:
        df_melhores.to_sql('tabela_odds', con, if_exists='append', index=False)

    print("✅ Dados salvos no banco de dados!")
    print(f"\n MELHORES ODDS — {proxima_data}:")
    print(df_melhores[['Luta', 'Aposta', 'Odd', 'Casa']].to_string(index=False))


if __name__ == "__main__":
    analisar_proximo_evento_ufc()