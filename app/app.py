#Imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)

############################################################################################
#Streamlit Config
st.set_page_config(
	page_title = 'Brasileirões | Olhar estatístico',
	page_icon = 'images/logo_brasileirao.png',
	layout = 'wide',
	initial_sidebar_state='collapsed')
############################################################################################
def main():
############################################################################################
    
    #loading data
    df_completo = pd.read_parquet('../dados/df_completo.parquet')

    with st.sidebar:
        st.image('./images/DataIndus_blue.png', width = 150)
        st.markdown('''<b>DataIndus</b> é uma iniciativa criada pelo cientista de dados e engenheiro mecânico Mario de Deus, de São Paulo/SP - Brasil,
com o objetivo de compartilhamento de conteúdos relacionados a aplicação de análise e ciência de dados, em diferentes tipos de aplicação, 
porém com ênfase em contextos industriais. 
                    
Neste sentido, busca a integração entre temas de tecnologia como:
* programação em Python, 
* Estatística, 
* Machine Learning, 
* MLOps, 
* Banco de Dados, 
* Engenharia de Dados, 
* Arquitetura Cloud 

com temas industriais como:
* Automação, 
* Redes Industriais, 
* IIOT, 
* PLC, 
* Edge Computing, 
* Scada, 
* MES 
* e outros

Youtube: https://www.youtube.com/@dataindus/
                    
Linkedin: https://www.linkedin.com/in/mario-andre-de-deus/
''', unsafe_allow_html=True)

    ############################################################################################
    c1, c2, c3 = st.columns([.15,.75,.1])

    c1.image('./images/logo_brasileirao.png', width = 120)
    c2.markdown(f"<h1 style='text-align: left;'>Brasileirões</h1> <h5 style='text-align: left;'>Sob um olhar estatístico</h5>", unsafe_allow_html=True)
    c3.image('./images/DataIndus_blue.png', width = 90)

    tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                                        'Home',
                                        'Lista de campeões', 
                                        'Estatísticas por ano', 
                                        'Evolução por rodada', 
                                        'Comparativos', 
                                        'Distribuições estatísticas',
                                        'Turno 1 vs Campeões'])
    
    ########################################################
    ########################################################
    with tab0:

        st.markdown('''
                    O desenvolvimento deste aplicativo web foi motivado pelos resultados do Campeonato Brasileiro de Futebol Masculino 2023, que demonstrou surpresas como: 

                    😴 o Botafogo ter feito um primeiro turno histórico e depois ter perdido o título; 

                    🏆 o time campeão, no caso o Palmeiras, ter tido uma pontuação baixa em comparação à média dos campeões dos demais anos; 

                    😪 a pontuação do rebaixamento ter sido maior que a média dos demais anos;
                    
                    Tais fatos levaram a resenhas entre os amantes do futebol por todo o país.''')
        
        st.info('Mas será que 2023 foi de fato o campeonato mais concorrido da era dos pontos corridos?')
        st.subheader('Explore todos os menus e tire as suas próprias conclusões !')
        st.divider()

        st.markdown('''<i> Notas: 

1. Os dados utilizados referem-se aos campeonatos brasileiros de futebol masculino desde o ano 2006. Apesar da era dos pontos corridos ter iniciado em 2003, foi a partir de 2006 que o campeonato passou a contar com 20 times, 
configuração que se mantém até o ano de 2023.
2. Fontes utilizadas para o download dos dados brutos:
    * 2006 a 2023 (até rodada 25): https://basedosdados.org/dataset/c861330e-bca2-474d-9073-bc70744a1b23?table=18835b0d-233e-4857-b454-1fa34a81b4fa
    * 2023 (rodada 26 a 38): https://footystats.org/pt/brazil/serie-a/fixtures''', unsafe_allow_html=True)

    ########################################################
    ########################################################
    with tab1:
        st.subheader('Lista de Campeões')
        st.divider()

        df_plot = df_completo.loc[(df_completo.classificacao_final == 1) & (df_completo.rodada == 38)][['ano_campeonato','time']].sort_values('ano_campeonato', ascending = False).reset_index(drop=True)
        lista_anos = np.sort(df_plot.ano_campeonato.unique().tolist())[::-1]
        
        for ano in lista_anos:
            c0, c1, c2, c3, c4, c5 = st.columns([.15,.33,.13,.13,.13,.13])
            df_plot = df_completo.loc[df_completo.ano_campeonato == ano]
            campeao = df_plot.loc[df_plot.classificacao_final == 1]['time'].mode()[0]
            
            c0.image(f'./images/escudos/{campeao}.png', width = 50)
            c1.metric(str(ano), campeao)

            pontos_campeao = df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['pontos_acum']
            c2.metric('Pontos', pontos_campeao)

            vitorias_campeao = df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['vitorias_acum']
            c3.metric('Vitórias', vitorias_campeao)

            saldo_gols_campeao = int(df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['saldo_gols_acum'])
            c4.metric('Saldo de gols', saldo_gols_campeao)

            gols_pro_campeao = int(df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['gols_pro_acum'])
            c5.metric('Gols pro', gols_pro_campeao)

            st.divider()

    ########################################################
    ########################################################
    with tab2:
        st.subheader('Estatísticas por ano')
        st.divider()

        c1, _ = st.columns([.3,.7])
        choose_year = c1.number_input('Escolher ano', min_value = int(df_completo.ano_campeonato.min()), max_value = int(df_completo.ano_campeonato.max()), value = df_completo.ano_campeonato.max())
        df_plot = df_completo.loc[df_completo.ano_campeonato == choose_year]
        classificacao_final = df_plot.groupby('classificacao_final').agg({'time': 'first'}).reset_index(drop = False)
        st.title(f'Brasileirão {choose_year}')

        c0, c1, c2, c3, c4, c5 = st.columns([.15,.33,.13,.13,.13,.13])
        campeao = df_plot.loc[df_plot.classificacao_final == 1]['time'].mode()[0]

        c0.image(f'./images/escudos/{campeao}.png', width = 50)

        c1.metric('Campeão', campeao)

        pontos_campeao = df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['pontos_acum']
        c2.metric('Pontos', pontos_campeao)

        vitorias_campeao = df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['vitorias_acum']
        c3.metric('Vitórias', vitorias_campeao)

        saldo_gols_campeao = int(df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['saldo_gols_acum'])
        c4.metric('Saldo de gols', saldo_gols_campeao)

        gols_pro_campeao = int(df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['gols_pro_acum'])
        c5.metric('Gols pro', gols_pro_campeao)

        #classificacao_final
        with st.expander('classificacao_final geral', expanded = False):
            st.write(classificacao_final)

        #tabela de jogos
        with st.expander('Tabela de jogos', expanded = False):

            df_tabela_jogos = df_plot[['ano_campeonato', 'rodada', 'time', 'adversário', 'gols_pro', 'gols_contra', 'classificacao_1o_turno','classificacao_final']].copy()

            choose_times = st.radio('Escolher times', ['Todos', 'Campeão', 'Campeão 1o_turno', 'G4', 'Rebaixados', 'Selecionar'], horizontal = True)
            if choose_times == 'Campeão':
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.classificacao_final == 1]
            elif choose_times == 'Campeão 1o_turno':
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.classificacao_1o_turno == 1]
            elif choose_times == 'G4':
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.classificacao_final <= 4]
            elif choose_times == 'Rebaixados':
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.classificacao_final >= 17]
            elif choose_times == 'Selecionar':
                list_times = st.multiselect('Selecionar times', df_tabela_jogos.time.unique(), default = df_tabela_jogos.time.unique()[0])
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.time.isin(list_times)]

            st.table(df_tabela_jogos.sort_values(['rodada', 'classificacao_final']).reset_index(drop = True))

    ########################################################
    ########################################################
    with tab3:
        st.subheader('Evolução por rodada')
        st.divider()

        with st.expander('Por times', expanded = False):
            c1, c2, c3 = st.columns([.35,.3,.35])
            choose_year = c1.number_input('Escolher ano ', min_value = int(df_completo.ano_campeonato.min()), max_value = int(df_completo.ano_campeonato.max()), value = df_completo.ano_campeonato.max())
            choose_metric = c1.selectbox('Escolher a métrica', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])
            choose_times = c2.radio('Escolher times ', ['Todos', 'Campeão','Campeão 1o_turno','G4', 'Rebaixados', 'Selecionar'], horizontal=False)
            
            df_plot = df_completo.loc[df_completo.ano_campeonato == choose_year]

            if choose_times == 'Campeão':
                df_plot = df_plot.loc[df_completo.classificacao_final == 1]
            elif choose_times == 'Campeão 1o_turno':
                df_plot = df_plot.loc[df_completo.classificacao_1o_turno == 1]
            elif choose_times == 'G4':
                df_plot = df_plot.loc[df_completo.classificacao_final <= 4]
            elif choose_times == 'Rebaixados':
                df_plot = df_plot.loc[df_completo.classificacao_final >= 17]
            elif choose_times == 'Selecionar':
                list_times = c3.multiselect('Selecionar times', df_completo.time.unique(), default = df_completo.time.unique()[0])
                df_plot = df_plot.loc[df_completo.time.isin(list_times)]
            else:
                df_plot = df_plot.copy()

            #plot
            plt.figure(figsize = (20,7))
            fig = px.line(df_plot, x ='rodada', y = choose_metric, color = 'time', title = f'Brasileirão {choose_year} | Time(s): {choose_times if choose_times != "Selecionar" else list_times} | Métrica: {choose_metric}', hover_data=['adversário','classificacao_final'])
            fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
            st.plotly_chart(fig)

            if st.toggle('Mostrar tabela'):
                st.markdown(df_plot.shape)
                st.table(df_plot.reset_index(drop = True))


        with st.expander('Por anos', expanded = False):
            c1, c2, c3, c4 = st.columns(4)
            filter_year_start = c1.number_input('De ano:', min_value = df_completo.ano_campeonato.min(),
                                        max_value = df_completo.ano_campeonato.max(), step = 1)
            
            filter_year_end = c2.number_input('Até ano:', min_value = df_completo.ano_campeonato.min(),
                                    max_value = df_completo.ano_campeonato.max(), step = 1, value = df_completo.ano_campeonato.max())

            choose_metric = c3.selectbox('Escolher a métrica ', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])

            choose_times = c4.radio('Escolher times  ', ['Campeões', 'Campeões 1o_turno','Selecionar'])
        
            df_plot = df_completo.loc[df_completo.ano_campeonato.between(filter_year_start, filter_year_end)]

            if choose_times == 'Campeões':
                df_plot = df_plot.loc[df_completo.classificacao_final == 1]
            
            elif choose_times == 'Campeões 1o_turno':
                df_plot = df_plot.loc[df_completo.classificacao_1o_turno == 1]
            
            else: #'Selecionar':
                # c1,_,_,_ = st.columns(4)
                chosen_time = c4.selectbox('', df_completo.time.unique())
                df_plot = df_plot.loc[df_completo.time == chosen_time]

            #plot
            plt.figure(figsize = (20,7))
            fig = px.line(df_plot, x ='rodada', y = choose_metric, color = 'ano_campeonato', title = f'Brasileirão {filter_year_start} a {filter_year_end} | Time(s): {choose_times if choose_times != "Selecionar" else chosen_time} | Métrica: {choose_metric}', hover_name = 'time', hover_data=['adversário','classificacao_final'])
            fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
            st.plotly_chart(fig)
            if st.toggle('Mostrar tabela '):
                st.markdown(df_plot.shape)
                st.table(df_plot.reset_index(drop = True))


    ########################################################
    ########################################################
    with tab4:
        st.subheader('Comparativos por ano e time')
        st.divider() 

        #Comparativo entre todos os times por temporada        
        c1, c2 = st.columns([.3,.7])
        choose_metric = c1.selectbox('Escolher a métrica  ', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])
        choose_times = c2.radio(' Escolher times', ['Todos','Campeões','Campeões 1o_turno','G4', 'Rebaixados', 'Selecionar'], horizontal = True)

        c1, c2, c3 = st.columns([.4,.4,.2])
        filtro_ano1 = c1.number_input('Ano 1', value = df_completo.ano_campeonato.unique()[-2], 
                                                min_value = df_completo.ano_campeonato.min(),
                                                max_value = df_completo.ano_campeonato.max())
        filtro_ano2 = c2.number_input('Ano 2', value = df_completo.ano_campeonato.unique()[-1], 
                                        min_value = df_completo.ano_campeonato.min(),
                                        max_value = df_completo.ano_campeonato.max())
        df_plot = df_completo.loc[(df_completo.ano_campeonato == filtro_ano1) | (df_completo.ano_campeonato == filtro_ano2) ]

        if choose_times == 'Campeões':
            df_plot = df_plot.loc[df_plot.classificacao_final == 1]
        elif choose_times == 'Campeões 1o_turno':
            df_plot = df_plot.loc[df_plot.classificacao_1o_turno == 1]
        elif choose_times == 'G4':
            df_plot = df_plot.loc[df_plot.classificacao_final <= 4]
        elif choose_times == 'Rebaixados':
            df_plot = df_plot.loc[df_plot.classificacao_final >= 17]
        elif choose_times == 'Selecionar':
            chosen_time = c3.selectbox('Selecionar time', df_plot.time.unique())
            df_plot = df_plot.loc[df_plot.time == chosen_time]

        plt.figure(figsize = (30,7))
        fig = px.line(  df_plot, x ='rodada', 
                        y = choose_metric, 
                        color = 'time', 
                        facet_col= 'ano_campeonato', 
                        facet_col_spacing = .05,
                        title = f'Brasileirão | {filtro_ano1} vs {filtro_ano2} | Time(s): {choose_times if choose_times != "Selecionar" else chosen_time} | Métrica: {choose_metric}',
                        hover_data=['classificacao_final'])
        fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
        fig.update_layout(showlegend=True, width=900, height=400)
        st.plotly_chart(fig)

        if st.toggle('Mostrar tabela  '):
            st.markdown(df_plot.shape)
            st.table(df_plot.reset_index(drop = True))

    ########################################################
    ########################################################
    with tab5:
        st.subheader('Distribuições estatísticas')
        st.divider()    


        c1, c2, c3, c4 = st.columns([.2,.2,.3,.3])
        filter_year_start = c1.number_input('De ano :', min_value = df_completo.ano_campeonato.min(),
                                    max_value = df_completo.ano_campeonato.max(), step = 1)
        
        filter_year_end = c2.number_input('Até ano :', min_value = df_completo.ano_campeonato.min(),
                                max_value = df_completo.ano_campeonato.max(), step = 1, value = df_completo.ano_campeonato.max())
        
        choose_metric = c3.selectbox(' Escolher a métrica ', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])
        choose_times = c4.radio(' Escolher times ', ['Todos', 'G4', 'G6', 'Rebaixados'])
    
        df_plot = df_completo.loc[(df_completo.ano_campeonato.between(filter_year_start, filter_year_end)) & (df_completo.rodada == 38)]

        if choose_times == 'G4':
            df_plot = df_plot.loc[df_plot.classificacao_final <= 4]
        elif choose_times == 'G6':
            df_plot = df_plot.loc[df_plot.classificacao_final <= 6]
        elif choose_times == 'Rebaixados':
            df_plot = df_plot.loc[df_plot.classificacao_final >= 17]
        
        with st.expander('Gráfico boxplot', expanded = False):
            #boxplot
            plt.figure(figsize = (30,7))
            fig = px.box(df_plot, x ='ano_campeonato', y = choose_metric, hover_data=['time','adversário'] ,title = f'Distribuição | Time(s): {choose_times} | Métrica: {choose_metric}')
            fig.update_layout(showlegend=True, width=900, height=400)
            fig.update_xaxes(type = 'category')
            
            st.plotly_chart(fig)

        with st.expander('Gráfico de Curva Densidade Probabilidade', expanded = False):
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


        if st.toggle(' Mostrar tabela '):
            st.markdown(df_plot.shape)
            st.table(df_plot.reset_index(drop = True))

    ########################################################
    ########################################################
    with tab6:

        with st.expander('Gráfico Sankey', expanded = True):

            c1, c2 = st.columns(2)
            #####################################################
            #classificação turno1 para classificação final
            #####################################################
            df_plot = df_completo.groupby(['ano_campeonato','time'])[['classificacao_1o_turno','classificacao_final']].max().reset_index()
            df_plot = df_plot.groupby(['classificacao_1o_turno','classificacao_final'])['time'].count().reset_index()
            df_plot = df_plot.loc[df_plot.classificacao_1o_turno == 1]

            #data
            label = ['Turno1_1o',   #0

                    'Final_1o.',    #1
                    'Final_2o.',    #2
                    'Final_3o.',    #3
                    'Final_4o.',    #4
                    'Final_5o.']    #5

            source = [0,0,0,0]
            target = [1,2,4,5]
            value = df_plot.time.tolist()

            #data to dict, dict to sankey
            link = dict(source = source, target = target, value = value)
            node = dict(label = label, pad = 35, thickness = 10)
            data = go.Sankey(link = link, node = node, orientation = 'h')

            fig = go.Figure(data)
            fig.update_layout(
                hovermode = 'x',
                title = 'Classificação Final dos Times "Campeões" do 1o Turno',
                font = dict(size = 15, color = 'white'),
                width = 500,
            )
            c1.plotly_chart(fig)

            ###################################################
            #classificação turno1 para campeões
            df_plot = df_completo.groupby(['ano_campeonato','time'])[['classificacao_1o_turno','classificacao_final']].max().reset_index()
            df_plot = df_plot.groupby(['classificacao_final','classificacao_1o_turno'])['time'].count().reset_index()
            df_plot = df_plot.loc[df_plot.classificacao_final == 1]

            #data
            label = ['Campeões',   #0

                    'Turno1_1o.',    #1
                    'Turno1_2o.',    #2
                    'Turno1_3o.',    #3
                    'Turno1_4o.',    #4
                    'Turno1_5o.',    #5
                    'Turno1_6o.',    #6
                    'Turno1_7o.',    #7
                    'Turno1_8o.',    #8
                    'Turno1_9o.',    #9
                    'Turno1_10o.']   #10

            target = [0,0,0,0,0,0]
            source = [1,2,3,4,6,10]
            value = df_plot.time.tolist()

            #data to dict, dict to sankey
            link = dict(source = source, target = target, value = value)
            node = dict(label = label, pad = 35, thickness = 10)
            data = go.Sankey(link = link, node = node, orientation = 'h')

            fig = go.Figure(data)
            fig.update_layout(
                hovermode = 'x',
                title = 'Classificação no 1o Turno dos Times Campeões',
                font = dict(size = 15, color = 'white'),
                width = 500,
                )
            c2.plotly_chart(fig)

###########################################################################
        with st.expander('Gráfico de colunas', expanded = False):
            c1, c2 = st.columns(2)

            #Classificação final dos times campeões do 1o.turno
            df_campeoes_turno1_qual_final = df_completo.loc[(df_completo.classificacao_1o_turno == 1) & (df_completo.rodada==38)][['ano_campeonato',
                                                                                                                        'rodada',
                                                                                                                        'time',
                                                                                                                        'classificacao_1o_turno',
                                                                                                                        'classificacao_final']]

            df_plot = df_campeoes_turno1_qual_final.classificacao_final.value_counts()
            
            fig1 = px.bar(df_plot, 
                            x = df_plot.index,
                            y = 'classificacao_final', 
                            labels = {'classificacao_final':'qtd de times',
                                    'index':'classificação final'},
                            title = 'Classificação Final dos Times "Campeões" do 1o Turno',
                            width = 500)
            c1.plotly_chart(fig1)


            #Classificação no 1o.turno dos times campeões
            df_campeoes_final_qual_turno1 = df_completo.loc[(df_completo.classificacao_final == 1) & (df_completo.rodada==38)][['ano_campeonato',
                                                                                                                        'rodada',
                                                                                                                        'time',
                                                                                                                        'classificacao_1o_turno',
                                                                                                                        'classificacao_final']]

            df_plot = df_campeoes_final_qual_turno1.classificacao_1o_turno.value_counts()

            fig2 = px.bar(df_plot, 
                            x = df_plot.index,
                            y = 'classificacao_1o_turno', 
                            labels = {'classificacao_1o_turno':'qtd de times',
                                    'index':'classificação no 1o. turno'},
                            title = 'Classificação no 1o Turno dos Times Campeões',
                            width = 500)
            c2.plotly_chart(fig2)



if __name__ == '__main__':
        main()