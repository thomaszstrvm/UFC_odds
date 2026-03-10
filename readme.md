# UFC Odds Tracker

Um pipeline de dados desenvolvido em Python para extrair, processar e armazenar o histórico de odds (cotações de apostas) para eventos do UFC. O objetivo do projeto é registrar a movimentação das linhas de aposta ao longo do tempo, facilitando a análise de tendências e a identificação de valor no mercado de MMA.

## Estrutura do Projeto

O sistema é dividido em dois módulos principais:
1. **Coleta e Processamento:** Um script que consome dados da *The Odds API*, limpa o JSON utilizando Pandas, filtra as melhores cotações disponíveis para cada lutador no mercado "Head to Head" (Vitória/Empate) e salva o snapshot no banco de dados.
2. **Consulta e Análise:** Uma interface de busca via linha de comando que realiza consultas SQL no banco de dados para retornar o histórico de um lutador específico, incluindo estatísticas básicas de variação da odd.

## Tecnologias

* Python 3
* Pandas (Manipulação e limpeza de dados)
* SQLite3 (Armazenamento relacional local)
* Requests (Integração com API REST)
* Python-dotenv (Gerenciamento de variáveis de ambiente)

## Como executar o projeto localmente

### 1. Clonar o repositório
```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
cd NOME_DO_REPOSITORIO
2. Instalar dependências
É recomendado o uso de um ambiente virtual (venv). Após ativá-lo, instale as bibliotecas necessárias:

Bash
pip install requests pandas python-dotenv
3. Configuração de credenciais
O projeto exige uma chave de API gratuita da The Odds API.
Crie um arquivo chamado .env na pasta raiz do projeto e insira a sua chave no seguinte formato:

Plaintext
API_KEY=sua_chave_de_api_aqui
4. Utilização
Para coletar e armazenar dados:
Execute o script principal. Ele buscará o evento de MMA mais próximo e gravará as odds atuais no banco de dados historico_odds_ufc.db.

Bash
python main.py
Para consultar o histórico de um lutador:
Execute o script de consulta. Ele pedirá o nome do lutador e retornará a variação temporal das odds e a média registrada.

Bash
python consultar_banco.py
Próximos Passos
Implementação de visualização de dados com Matplotlib para geração de gráficos de linha da variação temporal.

Mapeamento automatizado de oportunidades de arbitragem (Surebets) entre diferentes casas de apostas.