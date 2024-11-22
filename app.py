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
import os
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import root_mean_squared_error as rmse


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
    try:
        os.chdir(r'C:\Users\m4005001\Documents\_SG\Pessoal\Estatisticas_Brasileirao\estatisticas-brasileirao-masc')
        # st.write(os.getcwd())#
    except:
        pass
    
    #loading data
    df_completo = pd.read_csv(r'./dados/df_completo.csv', sep = ";")
    #provisoriamente foi excluido 2006 até que se corrija a base
    df_completo = df_completo.loc[df_completo.ano_campeonato >= 2006]
    df_completo.dropna(inplace = True)
    # df_completo
    df_completo[['gols_pro', 'gols_contra','gols_pro_acum','gols_contra_acum','saldo_gols_acum']] = df_completo[['gols_pro', 'gols_contra','gols_pro_acum','gols_contra_acum','saldo_gols_acum']].astype('int64')

    with st.sidebar:
        st.image('./images/DataIndus_green.png', width = 150)
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
                    
Medium: https://medium.com/@mariodedeus.engenharia/brasileir%C3%A3o-sob-um-olhar-estat%C3%ADstico-a263b97e1c6a
''', unsafe_allow_html=True)

    ############################################################################################
    c1, c2, c3 = st.columns([.15,.75,.1])

    c1.image('./images/logo_brasileirao_shadow.png', width = 120)
    c2.markdown(f"<h1 style='text-align: left;'>Brasileirões</h1> <h5 style='text-align: left;'>Sob um olhar estatístico</h5>", unsafe_allow_html=True)
    c3.image('./images/DataIndus_green.png', width = 90)

    tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                                        'Home',
                                        'Lista de campeões', 
                                        'Estatísticas por ano', 
                                        'Evolução por rodada', 
                                        'Comparativos', 
                                        'Distribuições estatísticas',
                                        'Turno 1 vs Campeões',
                                        'Projeções'])
    
    ########################################################
    ########################################################
    with tab0:

        st.markdown('''
                    O desenvolvimento deste aplicativo web foi motivado pelos resultados do Campeonato Brasileiro de Futebol Masculino 2023, que demonstrou surpresas como: 

                    😴 o Botafogo ter feito um primeiro turno histórico e depois ter perdido o título; 

                    🏆 o time campeão, no caso o Palmeiras, ter tido uma pontuação baixa em comparação à média dos campeões dos demais anos; 

                    😪 a pontuação do rebaixamento ter sido maior que a média dos demais anos;
                    
                    Agora o app está atualizado com os resultados de 2024.''')
        
        st.info('Que tal avaliar a performance dos times, rodada a rodada, e compará-los com os campeões ou z4 dos anos anteriores... Arrisca um palpite sobre quem será o campeão?')
        st.subheader('Explore todos os menus e tire as suas próprias conclusões !')
        st.divider()

        st.markdown('''<i> Notas: 

1. Os dados utilizados referem-se aos campeonatos brasileiros de futebol masculino desde o ano 2006. Apesar da era dos pontos corridos ter iniciado em 2003, foi a partir de 2006 que o campeonato passou a contar com 20 times, 
configuração que se mantém até o ano de 2023.
2. Fontes utilizadas para o download dos dados brutos:
    * 2006 a 2024 (até rodada 25): https://basedosdados.org/dataset/c861330e-bca2-474d-9073-bc70744a1b23?table=18835b0d-233e-4857-b454-1fa34a81b4fa
    * 2024 (rodada 26 a 38): https://ge.globo.com/futebol/brasileirao-serie-a/''', unsafe_allow_html=True)

    ########################################################
    ########################################################
    with tab1:
        st.subheader('Lista de Campeões')
        st.write('Lista de campeões desde 2006, incluindo as principais métricas de cada time.')
        st.divider()

        df_plot = df_completo.loc[(df_completo.classificacao_final == 1) & (df_completo.rodada == 38)][['ano_campeonato','time']].sort_values('ano_campeonato', ascending = False).reset_index(drop=True)
        lista_anos = np.sort(df_plot.ano_campeonato.unique().tolist())[::-1]

        for i,ano in enumerate(lista_anos):
            df_plot = df_completo.loc[df_completo.ano_campeonato == ano]
            campeao = df_plot.loc[df_plot.classificacao_final == 1]['time'].mode()[0]
            pontos_campeao = df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['pontos_acum']
            vitorias_campeao = df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['vitorias_acum']
            saldo_gols_campeao = int(df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['saldo_gols_acum'])
            gols_pro_campeao = int(df_plot.loc[(df_plot.classificacao_final == 1) & (df_plot.rodada == 38)]['gols_pro_acum'])

            c0, c1, c2, c3, c4, c5 = st.columns([.15,.33,.13,.13,.13,.13])
            c0.image(f'./images/escudos/{campeao}.png', width = 50)
            c1.metric(str(ano), campeao)
            c2.metric('Pontos', pontos_campeao)
            c3.metric('Vitórias', vitorias_campeao)
            c4.metric('Saldo de gols', saldo_gols_campeao)
            c5.metric('Gols pro', gols_pro_campeao)
            st.divider()

    ########################################################
    ########################################################
    with tab2:
        st.subheader('Estatísticas por ano')
        st.markdown('''Selecione um ano entre 2006 e 2023 e visualize a classificação final dos 20 times daquela temporada, 
                    assim como a tabela de jogos e resultados com filtros bem intuitivos.''')
        st.divider()

        c1, c2, c3 = st.columns([.15,.15,.7])
        choose_year = c1.number_input('Escolher ano', min_value = int(df_completo.ano_campeonato.min()), max_value = int(df_completo.ano_campeonato.max()), value = df_completo.ano_campeonato.max())
        df_plot = df_completo.loc[(df_completo.ano_campeonato == choose_year)]
        rodada_max = df_plot.rodada.max() if (df_plot.gols_pro.count() / df_plot.rodada.max() == 20) else (df_plot.rodada.max() - 1)
        df_plot = df_plot.loc[(df_plot.rodada == rodada_max)].sort_values('pontos_acum', ascending = False).reset_index(drop = True)
        if rodada_max < 38:
            c2.metric('Até a rodada:', rodada_max)
        c3.title(f'Brasileirão {str(choose_year)}')


        #classificacao_final
        with st.expander('Classificação Final Geral', expanded = False):
            c0, c1, c2, c3, c4, c5, c6, _ = st.columns([.15,.15,.25,.13,.13,.13, .13, .6])


            c0.markdown('Classificação')
            c1.markdown('Escudo')
            c2.markdown('Time')
            c3.markdown('Pontos')
            c4.markdown('Vitórias')
            c5.markdown('Saldo de gols')
            c6.markdown('Gols pró')
            st.divider()

            for i in range(20):
                c0, c1, c2, c3, c4, c5, c6, _ = st.columns([.1,.15,.25,.13,.13,.13, .13, .6])
                c0.subheader(df_plot.classificacao_final[i])
                try:
                    c1.image(f'./images/escudos/{df_plot.time[i]}.png', width = 50)
                except:
                    c1.info(df_plot.time[i])
                
                c2.subheader(df_plot.time[i])
                c3.markdown(df_plot.pontos_acum[i])
                c4.markdown(df_plot.vitorias_acum[i])
                c5.markdown(df_plot.saldo_gols_acum[i])
                c6.markdown(df_plot.gols_pro_acum[i])

        #tabela de jogos
        with st.expander('Tabela de jogos', expanded = False):
            df_plot = df_completo.loc[df_completo.ano_campeonato == choose_year].sort_values(['rodada','classificacao_final']).reset_index(drop = True)
            df_tabela_jogos = df_plot[['rodada', 'time', 'adversário', 'pontos_acum','gols_pro', 'gols_contra', 'classificacao_1o_turno','classificacao_final']].copy()

            if rodada_max == 38:
                choose_times = st.radio('Escolher times', ['Todos', 'Campeão', 'Campeão 1o_turno', 'G4', 'Z4', 'Selecionar'], horizontal = True)
            else:
                choose_times = st.radio('Escolher times', ['Todos', '1o colocado', 'Campeão 1o_turno', 'G4', 'Z4', 'Selecionar'], horizontal = True)

            if choose_times == 'Campeão' or choose_times == '1o colocado':
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.classificacao_final == 1]
            elif choose_times == 'Campeão 1o_turno':
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.classificacao_1o_turno == 1]
            elif choose_times == 'G4':
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.classificacao_final <= 4]
            elif choose_times == 'Z4':
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.classificacao_final >= 17]
            elif choose_times == 'Selecionar':
                list_times = st.multiselect('Selecionar times', df_tabela_jogos.time.unique(), default = df_tabela_jogos.time.unique()[0])
                df_tabela_jogos = df_tabela_jogos.loc[df_tabela_jogos.time.isin(list_times)]

            st.dataframe(df_tabela_jogos)

    ########################################################
    ########################################################
    with tab3:
        st.subheader('Evolução por rodada')
        st.markdown('''Visualize a evolução dos times rodada a rodada, 
                    comparando pontos, vitórias, saldo de gols e outras métricas 
                    entre os times e/ou entre os anos. 
                    Não deixe de passar o mouse pelas linhas do gráfico e clicar na legenda, 
                    pois ele é interativo!''')
        st.divider()

        with st.expander('Por times', expanded = False):
            c1, c2, c3 = st.columns([.35,.3,.35])
            choose_year = c1.number_input('Escolher ano ', min_value = int(df_completo.ano_campeonato.min()), max_value = int(df_completo.ano_campeonato.max()), value = df_completo.ano_campeonato.max())
            df_plot = df_completo.loc[df_completo.ano_campeonato == choose_year]

            rodada_max = df_plot.rodada.max() if (df_plot.gols_pro.count() / df_plot.rodada.max() == 20) else (df_plot.rodada.max() - 1)

            if rodada_max == 38:
                choose_times_evolucao = st.radio('Escolher times', ['Todos', 'Campeão', 'Campeão 1o_turno', 'G4', 'Z4', 'Selecionar'], horizontal = True, key = 'choose_times_evolucao')
            else:
                choose_times_evolucao = st.radio('Escolher times', ['Todos', '1o colocado', 'Campeão 1o_turno', 'G4', 'Z4', 'Selecionar'], horizontal = True, key = 'choose_times_evolucao')
            
            choose_metric = c1.selectbox('Escolher a métrica', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])

            if choose_times_evolucao == 'Campeão' or choose_times_evolucao == '1o colocado':
                df_plot = df_plot.loc[df_completo.classificacao_final == 1]
            elif choose_times_evolucao == 'Campeão 1o_turno':
                df_plot = df_plot.loc[df_completo.classificacao_1o_turno == 1]
            elif choose_times_evolucao == 'G4':
                df_plot = df_plot.loc[df_completo.classificacao_final <= 4]
            elif choose_times_evolucao == 'Z4':
                df_plot = df_plot.loc[df_completo.classificacao_final >= 17]
            elif choose_times_evolucao == 'Selecionar':
                list_times = c3.multiselect('Selecionar times', df_completo.time.unique(), default = df_completo.time.unique()[0])
                df_plot = df_plot.loc[df_completo.time.isin(list_times)]
            else:
                df_plot = df_plot.copy()

            #plot
            plt.figure(figsize = (20,7))
            fig = px.line(df_plot, x ='rodada', y = choose_metric, color = 'time', title = f'Brasileirão {choose_year} | Time(s): {choose_times_evolucao if choose_times_evolucao != "Selecionar" else list_times} | Métrica: {choose_metric}', hover_data=['adversário','classificacao_1o_turno','classificacao_final'])
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
            fig = px.line(df_plot, x ='rodada', y = choose_metric, color = 'ano_campeonato', title = f'Brasileirão {filter_year_start} a {filter_year_end} | Time(s): {choose_times if choose_times != "Selecionar" else chosen_time} | Métrica: {choose_metric}', hover_name = 'time', hover_data=['adversário','classificacao_1o_turno','classificacao_final'])
            fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
            st.plotly_chart(fig)
            if st.toggle('Mostrar tabela '):
                st.markdown(df_plot.shape)
                st.table(df_plot.reset_index(drop = True))

        with st.expander('Comparar um time com o histórico de campeões ou z4', expanded = False):
            c1, c2, c3, c4 = st.columns(4)

            #filter campeos
            choose_campeoes_z4 = c1.selectbox('Comparar com:',('Campeões', 'z4'), key = 'choose_campeoes_z4')

            filter_year_start_comparar_campeoes = c2.number_input('De ano:', min_value = df_completo.ano_campeonato.min(),
                                        max_value = df_completo.ano_campeonato.max(), step = 1, key = 'filter_year_start_comparar_campeoes')
            
            filter_year_end_comparar_campeoes = c3.number_input('Até ano:', min_value = df_completo.ano_campeonato.min(),
                                    max_value = df_completo.ano_campeonato.max(), step = 1, value = df_completo.ano_campeonato.max(), key = 'filter_year_end_comparar_campeoes')

            df_plot_campeoes = df_completo.loc[df_completo.ano_campeonato.between(filter_year_start_comparar_campeoes, filter_year_end_comparar_campeoes)]

            if choose_campeoes_z4 == 'Campeões':
                df_plot_campeoes = df_plot_campeoes.loc[df_plot_campeoes.classificacao_final == 1]
            
            else:# choose_campeoes_z4 == 'z4'
                df_plot_campeoes = df_plot_campeoes.loc[df_plot_campeoes.classificacao_final == 17]

            #choose metrica
            choose_metric_comparar_campeoes = c3.selectbox('Escolher a métrica ', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'], key = 'choose_metric_comparar_campeoes')
            
            #choose time para comparar
            filter_year_time = c2.number_input('Ano:', min_value = df_completo.ano_campeonato.min(),
                                    max_value = df_completo.ano_campeonato.max(), step = 1, value = df_completo.ano_campeonato.max())

            df_plot_time = df_completo.loc[df_completo.ano_campeonato == filter_year_time]
            filter_time_comparacao = c1.selectbox('Escolher time para comparação', np.sort(df_plot_time.time.unique()))
            df_plot_time = df_plot_time.loc[df_plot_time.time == filter_time_comparacao]

            #plot
            plt.figure(figsize = (20,7))
            fig = px.line(df_plot_campeoes, x='rodada', 
                          y=choose_metric_comparar_campeoes, 
                          color_discrete_sequence=['grey'], 
                          line_shape='linear',
                          color = 'ano_campeonato', 
                          title = f'Brasileirão {filter_year_start_comparar_campeoes} a {filter_year_end_comparar_campeoes} | Time(s): {choose_campeoes_z4} | Métrica: {choose_metric_comparar_campeoes}', 
                          hover_name = 'time', 
                          hover_data=['ano_campeonato','time'])
            

            fig.add_scatter(x=df_plot_time['rodada'], y=df_plot_time[choose_metric_comparar_campeoes], mode='lines', line=dict(color='orange', width=2))
            fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
            fig.update_traces(opacity=0.5, selector=dict(name='grey'))
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

            # if st.toggle('Mostrar tabela '):
            #     st.markdown(, df_plot.shape)
            #     st.table(pd.concat([df_plot_campeoes, df_plot_time]).reset_index(drop = True))


    ########################################################
    ########################################################
    with tab4:
        st.subheader('Comparativos por ano e time')
        st.markdown('''Compare dois anos distintos, rodada a rodada, sob a ótica da métrica que desejar: 
                    pontos, vitórias, saldo de gols entre outras.
                    Também é possível filtrar apenas os campeões, G4, Z4 ou escolher os times um a um.''')
        st.divider() 

        #Comparativo entre todos os times por temporada        
        c1, c2 = st.columns([.3,.7])
        choose_metric = c1.selectbox('Escolher a métrica  ', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])
        choose_times = c2.radio(' Escolher times', ['Todos','Campeões','Campeões 1o_turno','G4', 'Z4', 'Selecionar'], horizontal = True)

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
        elif choose_times == 'Z4':
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
                        category_orders={"ano_campeonato": [filtro_ano1, filtro_ano2]},
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
        st.markdown('''
                    Visualize a dispersão dos pontos na classificação final (após a rodada 38)
                    entre os 20 times de cada ano através de dois tipos de gráficos muito utilizados entre os profissionais de dados:
                    \n1. Boxplots \n2. Curvas de Distribuição
                    \nDe forma bem superficial, quanto mais “alongado” for o boxplot ou mais “aberta” for a curva, maior terá sido a 
                    variação de pontos entre os times daquele ano.
                    \nExiste ainda a opção de ordenar os gráficos por ordem crescente do "Desvio Padrão". 
                    O desvio padrão é uma medida de dispersão utilizada na estatística que indica 
                    o grau de variação de um conjunto de elementos, neste caso, o número de pontos na 
                    classificação final de cada ano. Quanto maior o desvio padrão, 
                    maior a variação de pontos entre os times daquele ano.''')
        st.divider()    

        c1, c2, c3, _ = st.columns([.15,.25,.15,.45])
        df_plot = df_completo.loc[df_completo.rodada == 38]
        
        order_year_by = c1.radio('Ordernar por', ('Ano', 'Desvio Padrão'))
        choose_metric = c2.selectbox('Escolher a métrica   ', ['pontos_acum','vitorias_acum','empates_acum','derrotas_acum','gols_pro_acum','gols_contra_acum','saldo_gols_acum'])
        choose_times = c3.radio(' Escolher times ', ['Todos', 'G4', 'G6', 'Z4'])

        if choose_times == 'G4':
            df_plot = df_plot.loc[df_plot.classificacao_final <= 4]
        elif choose_times == 'G6':
            df_plot = df_plot.loc[df_plot.classificacao_final <= 6]
        elif choose_times == 'Z4':
            df_plot = df_plot.loc[df_plot.classificacao_final >= 17]

        #desvio padrao
        df_std = df_plot.copy()
        df_std = df_std.groupby('ano_campeonato')[choose_metric].std().reset_index().sort_values(choose_metric).reset_index(drop = True)
        df_std.rename(columns=({choose_metric:choose_metric+'_std'}), inplace = True)
        #ordenar por
        df_plot = df_plot.merge(df_std, on ='ano_campeonato')
        df_plot = df_plot.sort_values('ano_campeonato' if order_year_by == 'Ano' else choose_metric+'_std')

        with st.expander('Gráfico Boxplot', expanded = False):
            #boxplot
            plt.figure(figsize = (30,7))
            fig = px.box(df_plot, x ='ano_campeonato', y = choose_metric, hover_data=['time','adversário'] ,
                         title = f'Distribuição | Time(s): {choose_times} | Métrica: {choose_metric}')
            fig.update_layout(showlegend=True, width=900, height=400)
            fig.update_xaxes(type = 'category')
            
            st.plotly_chart(fig)

        with st.expander('Curva de distribuição', expanded = False):
            #kdeplot
            group_labels = []
            hist_data = []
            for ano in df_plot.ano_campeonato.unique():
                group_labels.append(str(ano))
                df_ano = df_plot.loc[df_plot.ano_campeonato == ano][choose_metric].tolist()
                hist_data.append(df_ano)

            fig = ff.create_distplot(hist_data,group_labels, curve_type = 'normal', show_hist=False, show_rug = False)

            # Add title
            fig.update_layout(title_text= f'Distribuição dos pontos na classificação final: {choose_metric} | Times: {choose_times}')
            fig.show()
            st.plotly_chart(fig)

        if st.toggle(' Mostrar tabela '):
            st.markdown(df_plot.shape)
            st.table(df_plot.reset_index(drop = True))

    ########################################################
    ########################################################
    with tab6:
        st.subheader('Comparativo entre os campeões do 1º e 2º turnos')
        st.markdown('''
                    O gráfico da esquerda demonstra a classificação final dos times que finalizaram o 1o. turno 
                    na primeira colocação dos respectivos anos. 
                    Já o gráfico da direita demonstra qual foi a classificação no 1o. turno daqueles times que 
                    sagraram-se campeões dos respectivos anos. 
                    \nEm resumo, é possível responder a perguntas como: Os times que terminaram o 1o. turno na liderança 
                    geralmente sagram-se campeões? 
                    Percebemos que em 12 campeonatos de 18 anos sim, ou seja, em 66% das vezes.
                    \nPasse o mouse sobre os gráficos e visualize a quantidade de times contidos em cada fluxo.
                    ''')
        st.divider()
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

        c1.info('Qual foi a classificação final dos times que completaram o 1o turno na 1a. colocação?')
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

        c2.info('Em qual posição, os times campeões, haviam completado o 1o turno?')
        fig = go.Figure(data)
        fig.update_layout(
            hovermode = 'x',
            title = 'Classificação no 1o Turno dos Times Campeões',
            font = dict(size = 15, color = 'white'),
            width = 500,
            )
        c2.plotly_chart(fig)

    ########################################################
    ########################################################
    with tab7:

        with st.expander('Curva da posição 1 de cada ano_campeonato', expanded= False):
            df_pos1 = df_completo.groupby(['ano_campeonato','rodada'])['pontos_acum'].max().reset_index()
            df_pos1 = df_pos1.pivot(index='rodada', columns='ano_campeonato', values='pontos_acum').reset_index()
            df_pos1.index.name = None

            plt.figure(figsize = (20,7))
            fig = px.line(df_pos1, x ='rodada', y = df_pos1.iloc[:,1:].columns, title = f'Brasileirão 2006 - 2024 | Pontos do 1o. colocado a cada rodada')
            fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
            st.plotly_chart(fig)

        with st.expander('Similaridades entre curvas da posição 1', expanded = False):

            c1, c2, _ = st.columns([.25,.25, .50])
            ano_analisado = 2024
            c1.metric('Ano a ser analisado', ano_analisado)
            df_plot = df_completo.loc[(df_completo.ano_campeonato == ano_analisado)]

            rodada_max = df_plot.rodada.max() if (df_plot.gols_pro.count() / df_plot.rodada.max() == 20) else (df_plot.rodada.max() - 1)
            rodada_max = c2.number_input('Até a rodada', value = rodada_max, max_value=rodada_max, min_value=19)

            #####################
            def identificar_curva_pos1_menor_rmse(ano_analisado: int, rodada_max: int):
                '''
                Função para identificar o ano cuja curva da posição #1 de cada rodada apresenta maior similaridade com a curva do ano + rodada escolhidos

                ARGS
                ano_analisado: ano em estudo para realizar a projeção
                rodada_max: ou a última rodada realizada ou rodada anteriores para avaliar o algoritmo
                '''

                df_pos1_rodada_max_atual = df_pos1.loc[df_pos1.rodada <= rodada_max]
                df_pos1_rodada_max_atual.index.name = None
                df_pos1_rodada_max_atual.columns.name = None
                list_cols = df_pos1_rodada_max_atual.columns.tolist()

                if rodada_max <= 19:
                    list_rmse = []
                    for col in list_cols:
                        rmse_col = rmse(df_pos1_rodada_max_atual[ano_analisado], df_pos1_rodada_max_atual[col])
                        list_rmse.append(rmse_col)

                else: #rodada > 19
                    df_turno1 = df_pos1_rodada_max_atual.loc[df_pos1_rodada_max_atual.rodada <= 19]
                    df_turno2 = df_pos1_rodada_max_atual.loc[df_pos1_rodada_max_atual.rodada > 19]

                    list_rmse = []
                    for col in list_cols:
                        rmse_col_t1 = rmse(df_turno1[ano_analisado], df_turno1[col])
                        rmse_col_t2 = rmse(df_turno2[ano_analisado], df_turno2[col])
                        rmse_col = (rmse_col_t1 + (3*rmse_col_t2))/4
                        list_rmse.append(rmse_col)

                df_rmse_sim = pd.DataFrame({'ano_campeonato':list_cols, f'rmse_{ano_analisado}':list_rmse})
                df_rmse_sim = df_rmse_sim.sort_values(df_rmse_sim.columns[-1]).reset_index(drop = True)

                #ano com maior similaridade por RMSE com o ano analisado
                ano_min_rmse_sim = df_rmse_sim.ano_campeonato.iloc[1]
                min_rmse = df_rmse_sim.iloc[1,1]
                print(f'{"#"*50}\nANO: {ano_analisado} | RODADA: {rodada_max} | Maior Similaridade com pos#1 de {ano_min_rmse_sim}\n{"#"*50}')
                #######################################

                plt.figure(figsize = (20,7))
                fig = px.line(df_pos1_rodada_max_atual, x ='rodada', y = [int(ano_min_rmse_sim), int(ano_analisado)], title = f'Brasileirão | Ano analisado: {ano_analisado} | Até a rodada: {rodada_max} | Turno 2: Peso 3 <br>Curva pos.1 com maior similaridade por RMSE: Ano {ano_min_rmse_sim} | RMSE {np.round(min_rmse, 4)}</br>')
                fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")

                return fig, df_rmse_sim, ano_min_rmse_sim, min_rmse
            
            c1, c2 = st.columns([.75, .25])
            fig, df_rmse_sim, ano_min_rmse_sim, min_rmse = identificar_curva_pos1_menor_rmse(ano_analisado = ano_analisado, rodada_max = rodada_max)
            c1.plotly_chart(fig)
            c2.dataframe(df_rmse_sim.round(3))

        with st.expander('Times mais similares à curva da posição 1', expanded  = False):
            
            #####################
            def identificar_g4_menor_rmse(ano_analisado: int, rodada_max: int, ano_min_rmse_sim: int):
                    
                '''
                Função para identificar os times g4 com menor RMSE em relação a curva pos.1 do ano mais similar ao ano escolhido

                ARGS
                ano_analisado: ano em estudo para realizar a projeção
                rodada_max: ou a última rodada realizada ou rodada anteriores para avaliar o algoritmo
                ano_min_rmse_sim: ano cuja curva pos.1 apresenta maior similaridade com o ano escolhido (esta variável é a saída da função "identificar_curva_pos1_menor_rmse")
                '''

                # Análise dos times do ano selecionado em comparação ao ano com maior similaridade
                df_times_ano_analisado = df_completo.loc[(df_completo.ano_campeonato == ano_analisado) & (df_completo.rodada <= rodada_max)][['time', 'rodada','pontos_acum']]
                df_times_ano_analisado = df_times_ano_analisado.pivot(index = 'rodada', columns = 'time', values = 'pontos_acum').reset_index()

                #adicionando a coluna do ano com maior similaridade
                df_pos1_rodada_max_atual = df_pos1.loc[df_pos1.rodada <= rodada_max]
                df_pos1_rodada_max_atual.index.name = None
                df_pos1_rodada_max_atual.columns.name = None
                # list_cols = df_pos1_rodada_max_atual.columns.tolist()

                #filtrando o dataframe até a rodada selecionada
                df_times_ano_analisado[ano_min_rmse_sim] = df_pos1_rodada_max_atual[ano_min_rmse_sim]
                df_times_ano_analisado.dropna(inplace = True)

                ###########################################################################################################################################

                #calculando o RMSE de cada time do ano escolhido com a curva pos.1 do ano com maior similaridade com o ano escolhido

                # Calculando o RMSE
                list_times = df_times_ano_analisado.columns.tolist()
                list_rmse = []

                if rodada_max <= 19:
                    for time in list_times:
                        rmse_col = rmse(df_times_ano_analisado[time], df_times_ano_analisado[ano_min_rmse_sim])
                        list_rmse.append(rmse_col)

                else:
                    df_times_ano_analisado = df_times_ano_analisado.reset_index()
                    df_turno1 = df_times_ano_analisado.loc[df_times_ano_analisado.rodada <= 19]
                    df_turno2 = df_times_ano_analisado.loc[(df_times_ano_analisado.rodada > 19) & (df_times_ano_analisado.rodada <= rodada_max)]
                    for time in list_times:
                        rmse_col_t1 = rmse(df_turno1[time], df_turno1[ano_min_rmse_sim])
                        rmse_col_t2 = rmse(df_turno2[time], df_turno2[ano_min_rmse_sim])
                        rmse_col = (rmse_col_t1 + (3*rmse_col_t2))/4
                        list_rmse.append(rmse_col)
                        # print(time, rmse_col_t1, rmse_col_t2, rmse_col)

                df_times_rmse_sim = pd.DataFrame({'time':list_times, f'rmse_{int(ano_analisado)}_{int(ano_min_rmse_sim)}':list_rmse})
                df_times_rmse_sim = df_times_rmse_sim.sort_values(df_times_rmse_sim.columns[-1]).reset_index(drop = True)

                # # #######################################
                #Plot top 4 mais similares com a curva pos#1 do ano referencia
                list_top_4_similaridade = df_times_rmse_sim['time'][:5].tolist()

                plt.figure(figsize = (20,7))
                fig = px.line(df_times_ano_analisado[list_top_4_similaridade], 
                            # title = f'Top 4 times de {ano_analisado} com maior similaridade por RMSE com a curva pos.1 de {ano_min_rmse_sim}</sup>')
                            title =f'Brasileirão | Ano analisado: {ano_analisado} | Até a rodada: {rodada_max} | Turno 2: Peso 3 | <br><sup>Top 4 times de {ano_analisado} com maior similaridade por menor RMSE com a curva pos.1 de {ano_min_rmse_sim}</sup></br>')
                fig.add_vline(x=19, line_width=3, line_dash="dash", line_color="green")
                fig.update_xaxes(ticktext=np.arange(1,33))
                
                return df_times_rmse_sim, fig
            c1, _ = st.columns([.25,.75])
            pontuacao_campeao = df_completo.loc[df_completo.ano_campeonato == ano_min_rmse_sim]['pontos_acum'].max()

            c1, c2, c3 = st.columns([.65,.2,.15], gap='medium')
            df_times_rmse_sim, fig = identificar_g4_menor_rmse(ano_analisado = ano_analisado, rodada_max = rodada_max, ano_min_rmse_sim = ano_min_rmse_sim)
            c1.plotly_chart(fig)
            c2.title(' ')
            c2.metric('Provável Pontuação do Campeão', int(pontuacao_campeao))
            c3.title(' ')
            c3.info('Prováveis G4:')
            c3.dataframe(df_times_rmse_sim.iloc[1:5, :]['time'])

if __name__ == '__main__':
        main()