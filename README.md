# UFC Odds Tracker

Um pipeline de dados desenvolvido em Python para extrair, processar e armazenar o histórico de odds (cotações de apostas) para eventos do UFC. O projeto registra a movimentação das linhas de aposta ao longo do tempo para facilitar a análise de tendências no mercado de MMA.

## Estrutura do Projeto

O sistema é dividido em dois módulos principais:
1. **Coleta e Processamento:** Consome dados da The Odds API, limpa o JSON via Pandas, filtra as melhores cotações disponíveis para cada lutador no mercado "Head to Head" (Vitória/Empate) e salva no banco de dados.
2. **Consulta e Análise:** Interface de busca via terminal que realiza consultas SQL para retornar o histórico de um lutador, incluindo estatísticas de variação das odds.

## Tecnologias

* Python 3
* Pandas
* SQLite3
* Requests
* Python-dotenv

## Instalação e Configuração

**1. Clonar o repositório**

```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
cd NOME_DO_REPOSITORIO
```
2. Instalar dependências
```bash
pip install requests pandas python-dotenv
```
3. Configurar credenciais

Crie um arquivo .env na pasta raiz do projeto e insira a sua chave da The Odds API:
````bash
API_KEY=sua_chave_de_api_aqui
````
# Como Usar?

Coletar e armazenar dados:
Busca o evento de MMA mais próximo e grava as odds atuais no banco historico_odds_ufc.db.
```bash
main.py
```
Consultar dados:
```bash
consultar_banco.py
