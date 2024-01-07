#Imports
import streamlit as st
from streamlit.proto.Checkbox_pb2 import Checkbox
from unidecode import unidecode
import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from sklearn.metrics import precision_score, recall_score, f1_score

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

############################################################################################
#Streamlit Config
st.set_page_config(
	page_title = 'Brasileirões | Olhar estatístico',
	page_icon = 'images/logo_brasileirao.jpg',
	layout = 'wide',
	initial_sidebar_state='expanded')
############################################################################################
def main():
############################################################################################
    
    #loading data
    df_completo = pd.read_parquet('../dados/df_completo.parquet')

    with st.sidebar:
        st.image('./images/logo_brasileirao.jpg', width = 175)                
        st.markdown(f"<h1 style='text-align: left;'>Campeonatos Brasileiros</h1>", unsafe_allow_html=True)

        #Tipo de análise
        tipo_analise = st.radio('Tipo de Análise', ['Lista de Campeões',
                                                    'Estatísticas por ano',
                                                    'Evolução por rodada por times', 
                                                    'Evolução por rodada por ano',
                                                    'Comparativo entre 2 anos',
                                                    'Análise de distribuições'
                                                    ])
        
    if tipo_analise == 'Lista de Campeões':
        df_plot = df_completo.loc[(df_completo.classificacao == 1) & (df_completo.rodada == 38)][['ano_campeonato','time']].sort_values('ano_campeonato', ascending = False).reset_index(drop=True)
        lista_anos = np.sort(df_plot.ano_campeonato.unique().tolist())[::-1]
        
        st.subheader('Lista de Campeões')
        for ano in lista_anos:
            c1, c2 = st.columns([.3,.7])
            df_plot = df_completo.loc[df_completo.ano_campeonato == ano]
            campeao = df_plot.loc[df_plot.classificacao == 1]['time'].mode()[0]
            
            c1.metric(str(ano), campeao)
            c2.image(f'./images/escudos/{campeao}.png', width = 50)
            st.divider()

    elif tipo_analise == 'Estatísticas por ano':
        choose_year = st.sidebar.number_input('Escolher ano', min_value = int(df_completo.ano_campeonato.min()), max_value = int(df_completo.ano_campeonato.max()), value = df_completo.ano_campeonato.max())
        df_plot = df_completo.loc[df_completo.ano_campeonato == choose_year]
        classificacao = df_plot.groupby('classificacao').agg({'time': 'first'}).reset_index(drop = False)
        st.title(f'Brasileirão {choose_year}')

        c0, c1, c2, c3, c4, c5 = st.columns([.15,.45,.1,.1,.1,.1])
        campeao = df_plot.loc[df_plot.classificacao == 1]['time'].mode()[0]

        c0.image(f'./images/escudos/{campeao}.png', width = 50)

        c1.metric('Campeão', campeao)

        pontos_campeao = df_plot.loc[(df_plot.classificacao == 1) & (df_plot.rodada == 38)]['pontos_acum']
        c2.metric('Pontos', pontos_campeao)

        vitorias_campeao = df_plot.loc[(df_plot.classificacao == 1) & (df_plot.rodada == 38)]['vitorias_acum']
        c3.metric('Vitórias', vitorias_campeao)

        saldo_gols_campeao = int(df_plot.loc[(df_plot.classificacao == 1) & (df_plot.rodada == 38)]['saldo_gols_acum'])
        c4.metric('Saldo de gols', saldo_gols_campeao)

        gols_pro_campeao = int(df_plot.loc[(df_plot.classificacao == 1) & (df_plot.rodada == 38)]['gols_pro_acum'])
        c5.metric('Gols pro', gols_pro_campeao)

        #classificacao
        st.subheader(f'Classificacao {choose_year}')
        st.write(classificacao)

        #tabela de jogos
        st.subheader('Tabela de Jogos')
        choose_times = st.radio('Escolher times', ['Todos', 'Campeão','G4', 'G6', 'Rebaixados', 'Selecionar'])
        if choose_times == 'Campeão':
            df_plot = df_plot.loc[df_completo.classificacao == 1]
        elif choose_times == 'G4':
            df_plot = df_plot.loc[df_completo.classificacao <= 4]
        elif choose_times == 'G6':
            df_plot = df_plot.loc[df_completo.classificacao <= 6]
        elif choose_times == 'Rebaixados':
            df_plot = df_plot.loc[df_completo.classificacao >= 17]
        elif choose_times == 'Selecionar':
            list_times = st.sidebar.multiselect('Selecionar times', df_completo.time.unique(), default = df_completo.time.unique()[0])
            df_plot = df_plot.loc[df_completo.time.isin(list_times)]
        else:
            df_plot = df_plot.copy()

        st.table(df_plot.sort_values(['rodada', 'classificacao']).reset_index(drop = True))

    elif tipo_analise == 'Evolução por rodada por times':
        choose_year = st.sidebar.number_input('Escolher ano', min_value = int(df_completo.ano_campeonato.min()), max_value = int(df_completo.ano_campeonato.max()), value = df_completo.ano_campeonato.max())
        choose_metric = st.sidebar.selectbox('Escolher a métrica', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])
        choose_times = st.sidebar.radio('Escolher times', ['Todos', 'Campeão','G4', 'G6', 'Rebaixados', 'Selecionar'])
        
        df_plot = df_completo.loc[df_completo.ano_campeonato == choose_year]

        if choose_times == 'Campeão':
            df_plot = df_plot.loc[df_completo.classificacao == 1]
        elif choose_times == 'G4':
            df_plot = df_plot.loc[df_completo.classificacao <= 4]
        elif choose_times == 'G6':
            df_plot = df_plot.loc[df_completo.classificacao <= 6]
        elif choose_times == 'Rebaixados':
            df_plot = df_plot.loc[df_completo.classificacao >= 17]
        elif choose_times == 'Selecionar':
            list_times = st.sidebar.multiselect('Selecionar times', df_completo.time.unique(), default = df_completo.time.unique()[0])
            df_plot = df_plot.loc[df_completo.time.isin(list_times)]
        else:
            df_plot = df_plot.copy()

        #plot
        plt.figure(figsize = (20,7))
        fig = px.line(df_plot, x ='rodada', y = choose_metric, color = 'time', title = f'Brasileirão {choose_year} | {choose_times}', hover_data=['adversário','classificacao'])
        fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
        st.plotly_chart(fig)

        if st.toggle('Mostrar tabela'):
            st.markdown(df_plot.shape)
            st.table(df_plot.reset_index(drop = True))


    elif tipo_analise == 'Evolução por rodada por ano':
        with st.sidebar:
            c1, c2 = st.columns(2)
            filter_year_start = c1.number_input('De ano:', min_value = df_completo.ano_campeonato.min(),
                                        max_value = df_completo.ano_campeonato.max(), step = 1)
            
            filter_year_end = c2.number_input('Até ano:', min_value = df_completo.ano_campeonato.min(),
                                    max_value = df_completo.ano_campeonato.max(), step = 1, value = df_completo.ano_campeonato.max())
            
            choose_metric = st.selectbox('Escolher a métrica', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])
            choose_times = st.radio('Escolher times', ['Campeões', 'Selecionar'])
        
            df_plot = df_completo.loc[df_completo.ano_campeonato.between(filter_year_start, filter_year_end)]

            if choose_times == 'Campeões':
                df_plot = df_plot.loc[df_completo.classificacao == 1]
            
            else: #'Selecionar':
                chosen_time = st.sidebar.selectbox('Selecionar time', df_completo.time.unique())
                df_plot = df_plot.loc[df_completo.time == chosen_time]

        #plot
        plt.figure(figsize = (20,7))
        fig = px.line(df_plot, x ='rodada', y = choose_metric, color = 'ano_campeonato', title = f'Brasileirão {filter_year_start} a {filter_year_end} | {choose_times if choose_times != "Selecionar" else chosen_time}', hover_name = 'time', hover_data=['adversário','classificacao'])
        fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
        st.plotly_chart(fig)
        if st.toggle('Mostrar tabela'):
            st.markdown(df_plot.shape)
            st.table(df_plot.reset_index(drop = True))

    elif tipo_analise == 'Comparativo entre 2 anos':
        #Comparativo entre todos os times por temporada
        with st.sidebar:
            c1, c2 = st.columns(2)
            filtro_ano1 = c1.number_input('Ano 1', value = df_completo.ano_campeonato.unique()[-2], 
                                                    min_value = df_completo.ano_campeonato.min(),
                                                    max_value = df_completo.ano_campeonato.max())
            filtro_ano2 = c2.number_input('Ano 2', value = df_completo.ano_campeonato.unique()[-1], 
                                            min_value = df_completo.ano_campeonato.min(),
                                            max_value = df_completo.ano_campeonato.max())
            choose_metric = st.selectbox('Escolher a métrica', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])
            choose_times = st.radio('Escolher times', ['Todos','Campeões','G4', 'Rebaixados', 'Selecionar'])

            df_plot = df_completo.loc[(df_completo.ano_campeonato == filtro_ano1) | (df_completo.ano_campeonato == filtro_ano2) ]

            if choose_times == 'Todos':
                None
            elif choose_times == 'Campeões':
                df_plot = df_plot.loc[df_completo.classificacao == 1]
            elif choose_times == 'G4':
                df_plot = df_plot.loc[df_completo.classificacao <= 4]
            elif choose_times == 'Rebaixados':
                df_plot = df_plot.loc[df_completo.classificacao >= 17]
            else: #'Selecionar':
                chosen_time = st.selectbox('Selecionar time', df_completo.time.unique())
                df_plot = df_plot.loc[df_completo.time == chosen_time]

        plt.figure(figsize = (30,7))
        fig = px.line(df_plot, x ='rodada', 
                      y = choose_metric, 
                      color = 'time', 
                      facet_col= 'ano_campeonato', 
                      facet_col_spacing = .05,
                      title = f'Brasileirão | Comparativo')
        fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
        fig.update_layout(showlegend=True, width=900, height=400)
        st.plotly_chart(fig)

        if st.toggle('Mostrar tabela'):
            st.markdown(df_plot.shape)
            st.table(df_plot.reset_index(drop = True))

    elif tipo_analise == 'Análise de distribuições':
        with st.sidebar:
            c1, c2 = st.columns(2)
            filter_year_start = c1.number_input('De ano:', min_value = df_completo.ano_campeonato.min(),
                                        max_value = df_completo.ano_campeonato.max(), step = 1)
            
            filter_year_end = c2.number_input('Até ano:', min_value = df_completo.ano_campeonato.min(),
                                    max_value = df_completo.ano_campeonato.max(), step = 1, value = df_completo.ano_campeonato.max())
            
            choose_metric = st.selectbox('Escolher a métrica', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])
            choose_times = st.sidebar.radio('Escolher times', ['Todos', 'G4', 'G6', 'Rebaixados'])
        
            df_plot = df_completo.loc[(df_completo.ano_campeonato.between(filter_year_start, filter_year_end)) & (df_completo.rodada == 38)]

        if choose_times == 'G4':
            df_plot = df_plot.loc[df_plot.classificacao <= 4]
        elif choose_times == 'G6':
            df_plot = df_plot.loc[df_plot.classificacao <= 6]
        elif choose_times == 'Rebaixados':
            df_plot = df_plot.loc[df_plot.classificacao >= 17]
        else: #Todos':
            None
        
        #boxplot
        plt.figure(figsize = (30,7))
        fig = px.box(df_plot, x ='ano_campeonato', y = choose_metric, hover_data=['time','adversário'] ,title = f'Distribuição: {choose_metric} | Times: {choose_times}')
        fig.update_layout(showlegend=True, width=900, height=400)
        fig.update_xaxes(type = 'category')
        
        st.plotly_chart(fig)

        #kdeplot
        group_labels = []
        hist_data = []

        for ano in df_plot.ano_campeonato.unique():
            group_labels.append(str(ano))
            df_ano = df_plot.loc[df_plot.ano_campeonato == ano][choose_metric].tolist()
            hist_data.append(df_ano)

        fig = ff.create_distplot(hist_data,group_labels, curve_type = 'kde', show_hist=False, show_rug = False)

        # Add title
        fig.update_layout(title_text= f'Curva Densidade Probabilidade: {choose_metric} | Times: {choose_times}')
        fig.show()
        st.plotly_chart(fig)


        if st.toggle('Mostrar tabela'):
            st.markdown(df_plot.shape)
            st.table(df_plot.reset_index(drop = True))

if __name__ == '__main__':
        main()