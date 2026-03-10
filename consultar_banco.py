import sqlite3
import pandas as pd

DB_PATH = 'historico_odds_ufc.db'

QUERY = """
    SELECT Data_Coleta, Luta, Aposta, Odd, Casa
    FROM tabela_odds
    WHERE Aposta LIKE ? OR Luta LIKE ?
    ORDER BY Data_Coleta DESC
"""

def buscar_historico_lutador(nome: str):
    termo = f"%{nome}%"

    try:
        with sqlite3.connect(DB_PATH) as con:
            df = pd.read_sql_query(QUERY, con, params=(termo, termo))
    except sqlite3.OperationalError:
        print("\n❌ Banco de dados não encontrado. Rode o script de coleta primeiro.")
        return

    if df.empty:
        print(f"\nNenhum registro encontrado para '{nome}'.")
        return

    print(f"\n=== RESULTADOS PARA '{nome.upper()}' ===")
    print(df.to_string(index=False))

    print("\n📊 RESUMO ESTATÍSTICO:")

    idx_max = df['Odd'].idxmax()
    idx_min = df['Odd'].idxmin()

    print(f"  Maior Odd : {df.loc[idx_max, 'Odd']} ({df.loc[idx_max, 'Aposta']})")
    print(f"  Menor Odd : {df.loc[idx_min, 'Odd']} ({df.loc[idx_min, 'Aposta']})")
    print(f"  Odd Média : {df['Odd'].mean():.2f}")

if __name__ == "__main__":
    nome = input("Digite o nome do lutador (ex: Makhachev, Oliveira, Volkanovski): ").strip()
    buscar_historico_lutador(nome)