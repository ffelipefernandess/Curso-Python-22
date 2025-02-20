import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import base64

# Inicializando o app Dash
app = dash.Dash(__name__)

# Carregando o dataset de vendas
df = pd.read_csv('vendas.csv')

# Classe para estrutura de análise de dados
class AnalisadorDeVendas:
    def __init__(self, dados):
        """Inicializa a classe com o dataframe de vendas."""
        self.dados = dados
        self.limpar_dados()

    def limpar_dados(self):
        """Limpeza e preparação dos dados para análise."""
        self.dados['data'] = pd.to_datetime(self.dados['data'], errors='coerce')  # Converte para datetime
        self.dados['valor'] = self.dados['valor'].replace({',': '.'}, regex=True).astype(float)  # Corrige valores monetários
        self.dados.dropna(subset=['produto', 'valor'], inplace=True)  # Remove dados ausentes em colunas importantes
        self.dados['mes'] = self.dados['data'].dt.month  # Adiciona coluna para o mês
        self.dados['ano'] = self.dados['data'].dt.year  # Adiciona coluna para o ano
        self.dados['dia'] = self.dados['data'].dt.day  # Adiciona coluna para o dia
        self.dados['dia_da_semana'] = self.dados['data'].dt.weekday  # Adiciona coluna para o dia da semana (0=segunda, 6=domingo)

    def analise_vendas_por_produto(self, produtos_filtrados):
        """Retorna gráfico de vendas totais por produto."""
        df_produto = self.dados[self.dados['produto'].isin(produtos_filtrados)]
        df_produto = df_produto.groupby('produto')['valor'].sum().reset_index().sort_values(by='valor', ascending=False)
        fig = px.bar(df_produto, x='produto', y='valor', title='Vendas por Produto', color='valor')
        return fig

    def analise_vendas_por_regiao(self, regioes_filtradas):
        """Retorna gráfico de vendas totais por região."""
        df_regiao = self.dados[self.dados['regiao'].isin(regioes_filtradas)]
        df_regiao = df_regiao.groupby('regiao')['valor'].sum().reset_index().sort_values(by='valor', ascending=False)
        fig = px.pie(df_regiao, names='regiao', values='valor', title='Vendas por Região', color='valor')
        return fig

    def analise_vendas_mensais(self, ano_filtrado):
        """Retorna gráfico de vendas por mês (com linha de tendência)."""
        df_mes = self.dados[self.dados['ano'] == ano_filtrado]
        df_mes = df_mes.groupby(['ano', 'mes'])['valor'].sum().reset_index()
        fig = px.line(df_mes, x='mes', y='valor', color='ano', title=f'Vendas Mensais - {ano_filtrado}', markers=True, line_shape='spline')
        return fig

    def analise_vendas_diarias(self, data_inicio, data_fim):
        """Retorna gráfico de vendas diárias ao longo do tempo.""" 
        df_dia = self.dados[(self.dados['data'] >= data_inicio) & (self.dados['data'] <= data_fim)]
        df_dia = df_dia.groupby('data')['valor'].sum().reset_index()
        fig = px.line(df_dia, x='data', y='valor', title='Vendas Diárias', markers=True)
        return fig

    def analise_vendas_por_dia_da_semana(self):
        """Retorna gráfico de vendas por dia da semana (analisa o impacto do dia)."""
        df_dia_semana = self.dados.groupby('dia_da_semana')['valor'].sum().reset_index()
        df_dia_semana['dia_da_semana'] = df_dia_semana['dia_da_semana'].map({
            0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta', 4: 'Sexta', 5: 'Sábado', 6: 'Domingo'
        })
        fig = px.bar(df_dia_semana, x='dia_da_semana', y='valor', title='Vendas por Dia da Semana', color='valor')
        return fig

    def analise_outliers(self):
        """Identifica outliers com base em um intervalo interquartil."""        
        q1 = self.dados['valor'].quantile(0.25)
        q3 = self.dados['valor'].quantile(0.75)
        iqr = q3 - q1
        lim_inferior = q1 - 1.5 * iqr
        lim_superior = q3 + 1.5 * iqr
        outliers = self.dados[(self.dados['valor'] < lim_inferior) | (self.dados['valor'] > lim_superior)]
        fig = px.scatter(outliers, x='data', y='valor', title='Outliers de Vendas')
        return fig

    def distribucao_vendas(self):
        """Retorna gráfico de distribuição de vendas utilizando o Plotly"""
        fig = px.histogram(self.dados, x='valor', nbins=30, title="Distribuição de Vendas", color='valor')
        return fig

    def analise_media_desvio(self):
        """Cálculos de média e desvio padrão das vendas.""" 
        media = self.dados['valor'].mean()
        desvio = self.dados['valor'].std()
        return media, desvio

    def vendas_acumuladas(self):
        """Calcula vendas acumuladas ao longo do tempo, com insights estatísticos.""" 
        df_acumulado = self.dados.groupby('data')['valor'].sum().cumsum().reset_index()
        
        # Cálculos adicionais para enriquecer a análise
        df_acumulado['media_movel_7'] = df_acumulado['valor'].rolling(window=7).mean()  # Média móvel de 7 dias
        df_acumulado['desvio_padrao_7'] = df_acumulado['valor'].rolling(window=7).std()  # Desvio padrão de 7 dias
        df_acumulado['crescimento_percentual'] = df_acumulado['valor'].pct_change() * 100  # Crescimento percentual
        df_acumulado['max_valor'] = df_acumulado['valor'].expanding().max()  # Valor máximo acumulado até o momento
        df_acumulado['min_valor'] = df_acumulado['valor'].expanding().min()  # Valor mínimo acumulado até o momento

        # Criação do gráfico
        fig = px.line(
            df_acumulado, 
            x='data', 
            y=['valor', 'media_movel_7', 'max_valor', 'min_valor'], 
            title='Vendas Acumuladas ao Longo do Tempo com Insights Estatísticos',
            labels={'valor': 'Vendas Acumuladas', 'media_movel_7': 'Média Móvel (7 dias)', 'max_valor': 'Máximo Acumulado', 'min_valor': 'Mínimo Acumulado'},
            markers=True
        )

        # Adicionando o crescimento percentual ao gráfico como uma linha de anotações
        fig.add_trace(
            go.Scatter(
                x=df_acumulado['data'],
                y=df_acumulado['crescimento_percentual'],
                mode='lines+markers',
                name='Crescimento Percentual',
                line=dict(color='orange', width=2, dash='dot'),
                yaxis='y2'
            )
        )
        
        # Estilização do gráfico
        fig.update_layout(
            title_font=dict(size=20, family='Poppins', color='#2980B9'),
            plot_bgcolor="#34495E",  # Fundo escuro para o gráfico
            paper_bgcolor="#2C3E50",  # Fundo do papel
            font=dict(color='#ECF0F1', family='Roboto'),
            xaxis=dict(
                title='Data',
                tickformat='%Y-%m-%d',
                showgrid=True,
                gridcolor='#7f8c8d',
                tickangle=45
            ),
            yaxis=dict(
                title='Vendas Acumuladas',
                showgrid=True,
                gridcolor='#7f8c8d',
            ),
            yaxis2=dict(
                title='Crescimento Percentual (%)',
                overlaying='y',
                side='right',
                showgrid=False,
                tickformat='.1f'
            ),
            legend=dict(
                title="Métricas",
                orientation="h",
                yanchor="bottom",
                y=1.1,
                xanchor="center",
                x=0.5
            ),
            hovermode="x unified",
            autosize=True,
            margin=dict(t=50, b=50, l=40, r=40),
            shapes=[
                dict(
                    type="line",
                    x0=df_acumulado['data'].min(),
                    x1=df_acumulado['data'].max(),
                    y0=df_acumulado['max_valor'].max(),
                    y1=df_acumulado['max_valor'].max(),
                    line=dict(color="red", width=2, dash='dash'),
                    name="Máximo Histórico"
                ),
                dict(
                    type="line",
                    x0=df_acumulado['data'].min(),
                    x1=df_acumulado['data'].max(),
                    y0=df_acumulado['min_valor'].min(),
                    y1=df_acumulado['min_valor'].min(),
                    line=dict(color="green", width=2, dash='dash'),
                    name="Mínimo Histórico"
                )
            ]
        )

        return fig

# Instanciando o objeto de análise de vendas
analise = AnalisadorDeVendas(df)

# Layout do app Dash
app.layout = html.Div([
    html.H1("Dashboard de Análise de Vendas", style={'textAlign': 'center'}),

    # Filtros de Seleção
    html.Div([
        html.Label('Selecione os Produtos:'),
        dcc.Dropdown(
            id='produto-dropdown',
            options=[{'label': produto, 'value': produto} for produto in df['produto'].unique()],
            multi=True,
            value=df['produto'].unique().tolist(),
            style={'width': '48%'}
        ),
        html.Label('Selecione as Regiões:'),
        dcc.Dropdown(
            id='regiao-dropdown',
            options=[{'label': regiao, 'value': regiao} for regiao in df['regiao'].unique()],
            multi=True,
            value=df['regiao'].unique().tolist(),
            style={'width': '48%'}
        ),
        html.Label('Selecione o Ano:'),
        dcc.Dropdown(
            id='ano-dropdown',
            options=[{'label': str(ano), 'value': ano} for ano in df['ano'].unique()],
            value=df['ano'].min(),
            style={'width': '48%'}
        ),
        html.Label('Selecione o Período:'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['data'].min().date(),
            end_date=df['data'].max().date(),
            display_format='YYYY-MM-DD',
            style={'width': '48%'}
        ),
    ], style={'padding': '20px'}),

    # Gráficos
    html.Div([
        dcc.Graph(id='grafico-produto'),
        dcc.Graph(id='grafico-regiao'),
        dcc.Graph(id='grafico-mensal'),
        dcc.Graph(id='grafico-diario'),
        dcc.Graph(id='grafico-dia-da-semana'),
        dcc.Graph(id='grafico-outliers'),
        dcc.Graph(id='grafico-distribuicao'),
        dcc.Graph(id='grafico-media-desvio'),
        dcc.Graph(id='grafico-acumulado'),
    ])
])

# Callbacks para atualizar os gráficos conforme filtros
@app.callback(
    Output('grafico-produto', 'figure'),
    Output('grafico-regiao', 'figure'),
    Output('grafico-mensal', 'figure'),
    Output('grafico-diario', 'figure'),
    Output('grafico-dia-da-semana', 'figure'),
    Output('grafico-outliers', 'figure'),
    Output('grafico-distribuicao', 'figure'),
    Output('grafico-media-desvio', 'figure'),
    Output('grafico-acumulado', 'figure'),
    Input('produto-dropdown', 'value'),
    Input('regiao-dropdown', 'value'),
    Input('ano-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_graphs(produtos, regioes, ano, start_date, end_date):
    try:
        # Convertendo as datas para o formato correto
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Atualizando os gráficos com base nos filtros selecionados
        fig_produto = analise.analise_vendas_por_produto(produtos)
        fig_regiao = analise.analise_vendas_por_regiao(regioes)
        fig_mensal = analise.analise_vendas_mensais(ano)
        fig_diario = analise.analise_vendas_diarias(start_date, end_date)
        fig_dia_semana = analise.analise_vendas_por_dia_da_semana()
        fig_outliers = analise.analise_outliers()
        fig_distribuicao = analise.distribucao_vendas()
        media, desvio = analise.analise_media_desvio()
        fig_media_desvio = go.Figure(data=[
            go.Bar(x=['Média', 'Desvio Padrão'], y=[media, desvio], marker_color=['blue', 'red'])
        ], layout=go.Layout(title=f'Média e Desvio Padrão: Média={media:.2f}, Desvio={desvio:.2f}'))
        fig_acumulado = analise.vendas_acumuladas()

        return fig_produto, fig_regiao, fig_mensal, fig_diario, fig_dia_semana, fig_outliers, fig_distribuicao, fig_media_desvio, fig_acumulado
    
    except Exception as e:
        # Caso ocorra algum erro, logar a mensagem de erro e retornar gráficos vazios
        print(f"Erro ao atualizar os gráficos: {str(e)}")
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()

# Rodando o app
if __name__ == '__main__':
    app.run_server(debug=True)
