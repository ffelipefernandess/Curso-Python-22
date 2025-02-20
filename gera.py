import pandas as pd
import random
from datetime import datetime, timedelta

# Função para gerar dados de vendas fictícios
def gerar_dados_vendas(num_linhas):
    produtos = ['Produto A', 'Produto B', 'Produto C', 'Produto D']
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste']
    dados = []

    for _ in range(num_linhas):
        produto = random.choice(produtos)
        regiao = random.choice(regioes)
        valor = round(random.uniform(50, 500), 2)
        data = datetime.today() - timedelta(days=random.randint(0, 365))
        dados.append([produto, regiao, valor, data])

    return dados

# Gerar 100 linhas de dados fictícios
dados_vendas = gerar_dados_vendas(100)

# Criando o dataframe
df_vendas = pd.DataFrame(dados_vendas, columns=['produto', 'regiao', 'valor', 'data'])

# Salvando o arquivo CSV
df_vendas.to_csv('vendas.csv', index=False)

print("Arquivo vendas.csv gerado com sucesso!")
