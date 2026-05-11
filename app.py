"""
Brasileirão sob um olhar estatístico
Versão didática e lúdica para estudantes de Estatística, Ciência de Dados e fãs de futebol.

Principais melhorias desta versão:
- Menus mais amigáveis e orientados por perguntas.
- Modo aprendiz com explicações conceituais.
- Glossário lateral.
- Rótulos amigáveis para métricas.
- Cards didáticos: Pergunta / Conceito / Explore.
- Caminhos relativos com pathlib.
- Cache de dados.
- Gráficos responsivos com use_container_width=True.
- Textos revisados para evitar interpretação de projeção como aposta.
"""

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
from sklearn.metrics import root_mean_squared_error as rmse

warnings.simplefilter(action="ignore", category=FutureWarning)

# =============================================================================
# CONFIGURAÇÕES GERAIS
# =============================================================================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "dados"
IMG_DIR = BASE_DIR / "images"
ESCUDOS_DIR = IMG_DIR / "escudos"

st.set_page_config(
    page_title="Brasileirão | Olhar estatístico",
    page_icon=str(IMG_DIR / "logo_brasileirao.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# DICIONÁRIOS DIDÁTICOS
# =============================================================================
METRIC_LABELS = {
    "pontos_acum": "Pontos acumulados",
    "vitorias_acum": "Vitórias acumuladas",
    "empates_acum": "Empates acumulados",
    "derrotas_acum": "Derrotas acumuladas",
    "gols_pro_acum": "Gols marcados acumulados",
    "gols_contra_acum": "Gols sofridos acumulados",
    "saldo_gols_acum": "Saldo de gols acumulado",
}

METRIC_EXPLAIN = {
    "pontos_acum": "Mostra quantos pontos o time somou até cada rodada. É a métrica mais direta para acompanhar a corrida pelo título.",
    "vitorias_acum": "Ajuda a entender consistência. Em pontos corridos, vencer pesa mais que apenas evitar derrotas.",
    "empates_acum": "Mostra quantas vezes o time pontuou sem vencer. Muitos empates podem indicar regularidade, mas também dificuldade de decidir jogos.",
    "derrotas_acum": "Ajuda a identificar quedas de desempenho e momentos de instabilidade ao longo da competição.",
    "gols_pro_acum": "Indica força ofensiva. Quanto mais rápido essa curva sobe, maior o volume de gols marcados.",
    "gols_contra_acum": "Indica vulnerabilidade defensiva. Aqui, subir muito nem sempre é boa notícia.",
    "saldo_gols_acum": "Resume ataque e defesa em uma métrica só: gols marcados menos gols sofridos.",
}

COLUMN_LABELS = {
    "ano_campeonato": "Ano",
    "rodada": "Rodada",
    "time": "Time",
    "adversário": "Adversário",
    "pontos_acum": "Pontos",
    "jogos_acum": "Jogos",
    "vitorias_acum": "Vitórias",
    "empates_acum": "Empates",
    "derrotas_acum": "Derrotas",
    "gols_pro": "Gols pró",
    "gols_contra": "Gols contra",
    "gols_pro_acum": "Gols pró acum.",
    "gols_contra_acum": "Gols contra acum.",
    "saldo_gols_acum": "Saldo de gols",
    "classificacao_1o_turno": "Classificação 1º turno",
    "classificacao_final": "Classificação final",
}

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================
@st.cache_data(show_spinner="Carregando dados do Brasileirão...")
def carregar_dados() -> pd.DataFrame:
    """Carrega e prepara a base consolidada do Brasileirão."""
    data_path = DATA_DIR / "df_completo.parquet"
    if not data_path.exists():
        st.error(
            f"Arquivo de dados não encontrado: {data_path}. "
            "Verifique se a pasta 'dados' está no mesmo diretório do app.py."
        )
        st.stop()

    df = pd.read_parquet(data_path)
    df = df.loc[df["ano_campeonato"] >= 2006].copy()
    df = df.dropna(subset=["gols_pro"])

    int_cols = [
        "gols_pro",
        "gols_contra",
        "gols_pro_acum",
        "gols_contra_acum",
        "saldo_gols_acum",
    ]
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype("int64")

    return df


def get_metric_from_label(label: str) -> str:
    return {v: k for k, v in METRIC_LABELS.items()}[label]


def metric_selectbox(label: str, key: str, default: str = "pontos_acum") -> str:
    labels = list(METRIC_LABELS.values())
    default_label = METRIC_LABELS.get(default, labels[0])
    selected_label = st.selectbox(label, labels, index=labels.index(default_label), key=key)
    metric = get_metric_from_label(selected_label)
    st.caption(f"📌 {METRIC_EXPLAIN[metric]}")
    return metric


def safe_image(container, path: Path, width: int = 60, fallback_text: str = "") -> None:
    if path.exists():
        container.image(str(path), width=width)
    elif fallback_text:
        container.caption(fallback_text)


def rodada_max_valida(df_ano: pd.DataFrame) -> int:
    """Retorna a última rodada com jogos completos ou a rodada anterior quando a atual ainda está incompleta."""
    if df_ano.empty:
        return 0
    max_rodada = int(df_ano["rodada"].max())
    if max_rodada == 0:
        return 0
    jogos_por_rodada = df_ano.groupby("rodada")["gols_pro"].count()
    if jogos_por_rodada.get(max_rodada, 0) >= 20:
        return max_rodada
    return max(max_rodada - 1, 0)


def bloco_didatico(pergunta: str, conceito: str, acao: str) -> None:
    c1, c2, c3 = st.columns(3)
    c1.info(f"❓ **Pergunta**\n\n{pergunta}")
    c2.success(f"🎓 **Conceito de dados**\n\n{conceito}")
    c3.warning(f"🕹️ **Explore**\n\n{acao}")


def mostrar_tabela(df: pd.DataFrame, key: str, label: str = "Mostrar tabela de dados") -> None:
    if st.toggle(label, key=key):
        st.caption(f"Formato da tabela: {df.shape[0]} linhas x {df.shape[1]} colunas")
        st.dataframe(df.rename(columns=COLUMN_LABELS), use_container_width=True, hide_index=True)


def add_linha_primeiro_turno(fig: go.Figure) -> go.Figure:
    fig.add_vline(
        x=19,
        line_width=2,
        line_dash="dash",
        annotation_text="Fim do 1º turno",
        annotation_position="top",
    )
    return fig


def filtrar_grupo_times(df: pd.DataFrame, escolha: str, container=st, key_prefix: str = "") -> tuple[pd.DataFrame, object]:
    selecionados = None
    if escolha in ["Campeão", "1º colocado"]:
        return df.loc[df["classificacao_final"] == 1].copy(), selecionados
    if escolha in ["Campeões", "Campeões históricos"]:
        return df.loc[df["classificacao_final"] == 1].copy(), selecionados
    if escolha in ["Campeão do 1º turno", "Campeões do 1º turno"]:
        return df.loc[df["classificacao_1o_turno"] == 1].copy(), selecionados
    if escolha == "G4":
        return df.loc[df["classificacao_final"] <= 4].copy(), selecionados
    if escolha == "G6":
        return df.loc[df["classificacao_final"] <= 6].copy(), selecionados
    if escolha == "Z4":
        return df.loc[df["classificacao_final"] >= 17].copy(), selecionados
    if escolha == "Selecionar":
        times = sorted(df["time"].dropna().unique().tolist())
        default = times[:1]
        selecionados = container.multiselect("Selecionar time(s)", times, default=default, key=f"{key_prefix}_times")
        return df.loc[df["time"].isin(selecionados)].copy(), selecionados
    return df.copy(), selecionados


def dataframe_classificacao(df_ano: pd.DataFrame) -> pd.DataFrame:
    df = df_ano.sort_values(["jogos_acum"], ascending=False).reset_index(drop=True)
    df = df.groupby("time").first().reset_index()
    df = df.sort_values(["pontos_acum", "vitorias_acum", "saldo_gols_acum"], ascending=False).reset_index(drop=True)
    df.insert(0, "posição", np.arange(1, len(df) + 1))
    return df


def calcular_curvas_pos1(df: pd.DataFrame) -> pd.DataFrame:
    df_pos1 = df.groupby(["ano_campeonato", "rodada"])["pontos_acum"].max().reset_index()
    df_pos1 = df_pos1.pivot(index="rodada", columns="ano_campeonato", values="pontos_acum").reset_index()
    df_pos1.index.name = None
    df_pos1.columns.name = None
    return df_pos1


def identificar_curva_pos1_menor_rmse(df_pos1: pd.DataFrame, ano_analisado: int, rodada_max: int):
    df_base = df_pos1.loc[df_pos1["rodada"] <= rodada_max].copy().dropna(axis=1, how="all")
    df_base = df_base.dropna()
    list_cols = [col for col in df_base.columns if col != "rodada"]

    if ano_analisado not in list_cols:
        raise ValueError(f"O ano {ano_analisado} não possui dados suficientes para calcular similaridade.")

    df_turno1 = df_base.loc[df_base["rodada"] <= 19]
    df_turno2 = df_base.loc[df_base["rodada"] > 19]

    valores_rmse = []
    for col in list_cols:
        if col == ano_analisado:
            valores_rmse.append(0.0)
            continue
        if df_turno2.empty:
            valor = rmse(df_turno1[ano_analisado], df_turno1[col])
        else:
            valor_t1 = rmse(df_turno1[ano_analisado], df_turno1[col])
            valor_t2 = rmse(df_turno2[ano_analisado], df_turno2[col])
            valor = (valor_t1 + 3 * valor_t2) / 4
        valores_rmse.append(float(valor))

    df_rmse = pd.DataFrame({"ano_campeonato": list_cols, f"rmse_{ano_analisado}": valores_rmse})
    df_rmse = df_rmse.loc[df_rmse["ano_campeonato"] != ano_analisado]
    df_rmse = df_rmse.sort_values(f"rmse_{ano_analisado}").reset_index(drop=True)

    ano_similar = int(df_rmse.loc[0, "ano_campeonato"])
    min_rmse = float(df_rmse.iloc[0, 1])
    return df_base, df_rmse, ano_similar, min_rmse


def identificar_times_menor_rmse(df: pd.DataFrame, df_pos1: pd.DataFrame, ano_analisado: int, rodada_max: int, ano_similar: int):
    df_times = df.loc[
        (df["ano_campeonato"] == ano_analisado) & (df["rodada"] <= rodada_max),
        ["time", "rodada", "pontos_acum"],
    ].copy()

    df_times = df_times.pivot(index="rodada", columns="time", values="pontos_acum").reset_index()
    df_ref = df_pos1.loc[df_pos1["rodada"] <= rodada_max, ["rodada", ano_similar]].copy()
    df_times = df_times.merge(df_ref, on="rodada", how="inner").dropna()

    time_cols = [col for col in df_times.columns if col not in ["rodada", ano_similar]]
    df_turno1 = df_times.loc[df_times["rodada"] <= 19]
    df_turno2 = df_times.loc[df_times["rodada"] > 19]

    valores_rmse = []
    for time in time_cols:
        if df_turno2.empty:
            valor = rmse(df_turno1[time], df_turno1[ano_similar])
        else:
            valor_t1 = rmse(df_turno1[time], df_turno1[ano_similar])
            valor_t2 = rmse(df_turno2[time], df_turno2[ano_similar])
            valor = (valor_t1 + 3 * valor_t2) / 4
        valores_rmse.append(float(valor))

    rmse_col = f"rmse_{ano_analisado}_{ano_similar}"
    df_rmse_times = pd.DataFrame({"time": time_cols, rmse_col: valores_rmse})
    df_rmse_times = df_rmse_times.sort_values(rmse_col).reset_index(drop=True)
    return df_times, df_rmse_times, rmse_col


def header_app() -> None:
    c1, c2, c3 = st.columns([0.15, 0.72, 0.13])
    safe_image(c1, IMG_DIR / "logo_brasileirao_shadow.png", width=120)
    c2.markdown(
        """
        # Brasileirão sob um olhar estatístico
        ##### Futebol, Estatística e Ciência de Dados em uma experiência interativa
        """,
        unsafe_allow_html=True,
    )
    safe_image(c3, IMG_DIR / "DataIndus_green.png", width=90)


def sidebar_app() -> bool:
    with st.sidebar:
        safe_image(st, IMG_DIR / "DataIndus_green.png", width=150)
        st.markdown("## 🎓 Experiência")
        modo_aprendiz = st.toggle(
            "Modo aprendiz",
            value=True,
            help="Ative para ver explicações simples sobre os conceitos de Data Science usados no app.",
        )

        st.markdown("---")
        st.markdown("## 📚 Glossário rápido")
        with st.expander("Série temporal"):
            st.write("Sequência de dados ao longo do tempo. No app, as rodadas formam essa sequência.")
        with st.expander("Boxplot"):
            st.write("Resumo visual da distribuição. Mostra concentração, dispersão e possíveis valores fora do padrão.")
        with st.expander("Desvio padrão"):
            st.write("Mede o quanto os valores estão espalhados em relação à média.")
        with st.expander("RMSE"):
            st.write("Mede a distância média entre duas curvas. Quanto menor o RMSE, mais parecidas elas são.")
        with st.expander("Similaridade"):
            st.write("No app, similaridade significa comportamento parecido entre curvas. Não significa probabilidade real.")

        st.markdown("---")
        st.markdown(
            """
            **DataIndus**  
            Conteúdo de Python, Estatística, Machine Learning, Engenharia de Dados e aplicações industriais.

            - YouTube: @dataindus
            - LinkedIn: Mario André de Deus
            - Medium: Brasileirão sob um olhar estatístico
            """
        )
    return modo_aprendiz

# =============================================================================
# ABAS
# =============================================================================
def aba_home(df: pd.DataFrame, modo_aprendiz: bool) -> None:
    st.markdown(
        """
        ## 🏟️ Comece por aqui

        Este app transforma o Campeonato Brasileiro em um laboratório divertido de **Estatística** e **Ciência de Dados**.

        Aqui você pode investigar perguntas como:

        - Um campeão precisa liderar desde cedo?
        - Qual campanha foi mais dominante?
        - O G4 de um ano parece com o G4 de outro?
        - O que boxplot, desvio padrão e RMSE têm a ver com futebol?
        - Dá para aprender modelagem olhando para a corrida rodada a rodada?
        """
    )

    st.info(
        """
        💡 **Roteiro sugerido**  
        1. Escolha uma pergunta.  
        2. Mexa nos filtros.  
        3. Observe o gráfico.  
        4. Leia a explicação.  
        5. Tire uma conclusão com os dados.
        """
    )

    st.warning(
        """
        ⚠️ A aba de projeções tem finalidade exclusivamente didática.  
        Ela demonstra comparação de curvas e engenharia de variáveis, mas **não deve ser usada para apostas**.
        """
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temporadas", f"{df.ano_campeonato.min()}–{df.ano_campeonato.max()}")
    c2.metric("Times na base", df["time"].nunique())
    c3.metric("Rodadas registradas", int(df[["ano_campeonato", "rodada"]].drop_duplicates().shape[0]))
    c4.metric("Jogos/time registrados", df.shape[0])

    if modo_aprendiz:
        bloco_didatico(
            pergunta="Como transformar futebol em dados?",
            conceito="Cada rodada vira uma linha de observação; cada métrica vira uma variável.",
            acao="Comece pela aba 'Corrida rodada a rodada' e observe como as curvas contam histórias.",
        )

    st.markdown(
        """
        ### Fontes e recorte
        Os dados consideram o Brasileirão masculino a partir de 2006, quando o campeonato passou a ter 20 times no formato atual de pontos corridos.

        Fontes originais usadas no projeto:
        - Base dos Dados, para temporadas históricas.
        - GE / Globo Esporte, para temporadas mais recentes.
        """
    )


def aba_campeoes(df: pd.DataFrame, modo_aprendiz: bool) -> None:
    st.subheader("🏆 Hall dos campeões")
    st.write("Veja os campeões desde 2006 e compare suas principais métricas finais.")

    if modo_aprendiz:
        bloco_didatico(
            pergunta="Todo campeão tem campanha parecida?",
            conceito="Métricas agregadas: pontos, vitórias, saldo e gols marcados.",
            acao="Compare campeões com pontuações altas e baixas. Depois investigue a curva deles nas outras abas.",
        )

    campeoes = (
        df.loc[(df["classificacao_final"] == 1) & (df["rodada"] == 38)]
        .sort_values("ano_campeonato", ascending=False)
        .reset_index(drop=True)
    )

    for _, row in campeoes.iterrows():
        ano = int(row["ano_campeonato"])
        time = row["time"]
        c0, c1, c2, c3, c4, c5 = st.columns([0.12, 0.34, 0.13, 0.13, 0.14, 0.14])
        safe_image(c0, ESCUDOS_DIR / f"{time}.png", width=52, fallback_text=time)
        c1.metric(str(ano), time)
        c2.metric("Pontos", int(row["pontos_acum"]))
        c3.metric("Vitórias", int(row["vitorias_acum"]))
        c4.metric("Saldo", int(row["saldo_gols_acum"]))
        c5.metric("Gols pró", int(row["gols_pro_acum"]))
        st.divider()


def aba_raio_x(df: pd.DataFrame, modo_aprendiz: bool) -> None:
    st.subheader("📅 Raio-X da temporada")
    st.write("Escolha uma temporada e explore a classificação, os jogos e os resultados com filtros simples.")

    if modo_aprendiz:
        bloco_didatico(
            pergunta="Como ler uma tabela de campeonato como base de dados?",
            conceito="Filtros, ordenação, variáveis acumuladas e classificação.",
            acao="Escolha um ano, abra a classificação e depois filtre os jogos por G4, Z4 ou time específico.",
        )

    c1, c2, c3 = st.columns([0.18, 0.18, 0.64])
    choose_year = c1.number_input(
        "Escolher ano",
        min_value=int(df.ano_campeonato.min()),
        max_value=int(df.ano_campeonato.max()),
        value=int(df.ano_campeonato.max()),
        key="raiox_ano",
    )
    df_ano = df.loc[df["ano_campeonato"] == choose_year].copy()
    rodada_max = rodada_max_valida(df_ano)
    if rodada_max < 38:
        c2.metric("Até a rodada", rodada_max)
    c3.title(f"Brasileirão {choose_year}")

    with st.expander("Classificação geral", expanded=True):
        classificacao = dataframe_classificacao(df_ano)
        cols_show = [
            "posição", "time", "pontos_acum", "jogos_acum", "vitorias_acum",
            "empates_acum", "derrotas_acum", "saldo_gols_acum", "gols_pro_acum", "gols_contra_acum",
        ]
        st.dataframe(
            classificacao[cols_show].rename(columns=COLUMN_LABELS),
            use_container_width=True,
            hide_index=True,
        )

    with st.expander("Tabela de jogos", expanded=False):
        df_jogos = df_ano.sort_values(["rodada", "classificacao_final"]).reset_index(drop=True)
        cols = [
            "rodada", "time", "adversário", "pontos_acum", "gols_pro", "gols_contra",
            "classificacao_1o_turno", "classificacao_final",
        ]
        df_jogos = df_jogos[cols].copy()

        opcoes = ["Todos", "Campeão" if rodada_max == 38 else "1º colocado", "Campeão do 1º turno", "G4", "Z4", "Selecionar"]
        escolha = st.radio("Escolher grupo de times", opcoes, horizontal=True, key="raiox_grupo")
        df_jogos, _ = filtrar_grupo_times(df_jogos, escolha, key_prefix="raiox")
        st.dataframe(df_jogos.rename(columns=COLUMN_LABELS), use_container_width=True, hide_index=True)


def aba_evolucao(df: pd.DataFrame, modo_aprendiz: bool) -> None:
    st.subheader("📈 Corrida rodada a rodada")
    st.markdown(
        """
        Aqui cada linha conta uma história. Imagine que o Brasileirão é uma corrida de 38 voltas: cada rodada é uma volta,
        e cada time vai acumulando pontos, vitórias, gols ou saldo.
        """
    )

    if modo_aprendiz:
        bloco_didatico(
            pergunta="O campeão dispara cedo ou cresce no segundo turno?",
            conceito="Série temporal e comparação de curvas.",
            acao="Compare pontos acumulados de campeões, G4 e Z4. Clique na legenda para isolar curvas.",
        )

    with st.expander("Por times dentro de uma temporada", expanded=True):
        c1, c2, c3 = st.columns([0.3, 0.35, 0.35])
        choose_year = c1.number_input(
            "Escolher ano",
            min_value=int(df.ano_campeonato.min()),
            max_value=int(df.ano_campeonato.max()),
            value=int(df.ano_campeonato.max()),
            key="evol_ano",
        )
        df_plot = df.loc[df["ano_campeonato"] == choose_year].copy()
        rodada_max = rodada_max_valida(df_plot)
        opcoes = ["Todos", "Campeão" if rodada_max == 38 else "1º colocado", "Campeão do 1º turno", "G4", "Z4", "Selecionar"]
        escolha = c2.radio("Escolher grupo", opcoes, horizontal=True, key="evol_grupo")
        choose_metric = metric_selectbox("Escolher métrica", key="evol_metric")
        df_plot, selecionados = filtrar_grupo_times(df_plot, escolha, container=c3, key_prefix="evol")

        fig = px.line(
            df_plot,
            x="rodada",
            y=choose_metric,
            color="time",
            title=f"Brasileirão {choose_year} | {escolha} | {METRIC_LABELS[choose_metric]}",
            hover_data=["adversário", "classificacao_1o_turno", "classificacao_final"],
            labels=COLUMN_LABELS | {choose_metric: METRIC_LABELS[choose_metric]},
        )
        fig = add_linha_primeiro_turno(fig)
        st.plotly_chart(fig, use_container_width=True)
        mostrar_tabela(df_plot, key="evol_tabela")

    with st.expander("Por anos", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        ano_ini = c1.number_input("De ano", min_value=int(df.ano_campeonato.min()), max_value=int(df.ano_campeonato.max()), value=int(df.ano_campeonato.min()), key="evol_ano_ini")
        ano_fim = c2.number_input("Até ano", min_value=int(df.ano_campeonato.min()), max_value=int(df.ano_campeonato.max()), value=int(df.ano_campeonato.max()), key="evol_ano_fim")
        choose_metric = metric_selectbox("Escolher métrica", key="evol_anos_metric")
        escolha = c4.radio("Escolher grupo", ["Campeões", "Campeões do 1º turno", "Selecionar"], key="evol_anos_grupo")

        df_plot = df.loc[df["ano_campeonato"].between(ano_ini, ano_fim)].copy()
        if escolha == "Campeões":
            df_plot = df_plot.loc[df_plot["classificacao_final"] == 1]
            titulo_grupo = "Campeões"
        elif escolha == "Campeões do 1º turno":
            df_plot = df_plot.loc[df_plot["classificacao_1o_turno"] == 1]
            titulo_grupo = "Campeões do 1º turno"
        else:
            chosen_time = c4.selectbox("Time", sorted(df["time"].unique()), key="evol_anos_time")
            df_plot = df_plot.loc[df_plot["time"] == chosen_time]
            titulo_grupo = chosen_time

        fig = px.line(
            df_plot,
            x="rodada",
            y=choose_metric,
            color="ano_campeonato",
            title=f"Brasileirão {ano_ini} a {ano_fim} | {titulo_grupo} | {METRIC_LABELS[choose_metric]}",
            hover_name="time",
            hover_data=["adversário", "classificacao_1o_turno", "classificacao_final"],
            labels=COLUMN_LABELS | {choose_metric: METRIC_LABELS[choose_metric]},
        )
        fig = add_linha_primeiro_turno(fig)
        st.plotly_chart(fig, use_container_width=True)
        mostrar_tabela(df_plot, key="evol_anos_tabela")

    with st.expander("Comparar um time com históricos de campeões ou Z4", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        base_comparacao = c1.selectbox("Comparar com", ["Campeões", "Z4"], key="evol_hist_base")
        ano_ini = c2.number_input("De ano", min_value=int(df.ano_campeonato.min()), max_value=int(df.ano_campeonato.max()), value=int(df.ano_campeonato.min()), key="evol_hist_ini")
        ano_fim = c3.number_input("Até ano", min_value=int(df.ano_campeonato.min()), max_value=int(df.ano_campeonato.max()), value=int(df.ano_campeonato.max()), key="evol_hist_fim")
        choose_metric = metric_selectbox("Escolher métrica", key="evol_hist_metric")

        df_hist = df.loc[df["ano_campeonato"].between(ano_ini, ano_fim)].copy()
        df_hist = df_hist.loc[df_hist["classificacao_final"] == (1 if base_comparacao == "Campeões" else 17)]

        ano_time = c2.number_input("Ano do time analisado", min_value=int(df.ano_campeonato.min()), max_value=int(df.ano_campeonato.max()), value=int(df.ano_campeonato.max()), key="evol_hist_ano_time")
        times_ano = sorted(df.loc[df["ano_campeonato"] == ano_time, "time"].dropna().unique())
        time_analisado = c1.selectbox("Time analisado", times_ano, key="evol_hist_time")
        df_time = df.loc[(df["ano_campeonato"] == ano_time) & (df["time"] == time_analisado)].copy()

        fig = px.line(
            df_hist,
            x="rodada",
            y=choose_metric,
            color="ano_campeonato",
            title=f"{time_analisado} {ano_time} vs histórico de {base_comparacao} | {METRIC_LABELS[choose_metric]}",
            hover_name="time",
            hover_data=["ano_campeonato", "time"],
            labels=COLUMN_LABELS | {choose_metric: METRIC_LABELS[choose_metric]},
        )
        fig.add_scatter(
            x=df_time["rodada"],
            y=df_time[choose_metric],
            mode="lines",
            name=f"{time_analisado} {ano_time}",
            line=dict(width=4),
        )
        fig = add_linha_primeiro_turno(fig)
        st.plotly_chart(fig, use_container_width=True)


def aba_comparativos(df: pd.DataFrame, modo_aprendiz: bool) -> None:
    st.subheader("⚔️ Duelo de campanhas")
    st.write("Compare dois anos distintos, rodada a rodada, usando a métrica que desejar.")

    if modo_aprendiz:
        bloco_didatico(
            pergunta="Duas temporadas podem parecer iguais na tabela final, mas diferentes rodada a rodada?",
            conceito="Facetas, comparação visual e análise de grupos.",
            acao="Escolha dois anos, filtre por G4 ou Z4 e compare o formato das curvas.",
        )

    c1, c2 = st.columns([0.3, 0.7])
    choose_metric = metric_selectbox("Escolher métrica", key="comp_metric")
    escolha = c2.radio("Escolher grupo", ["Todos", "Campeões", "Campeões do 1º turno", "G4", "Z4", "Selecionar"], horizontal=True, key="comp_grupo")

    anos = sorted(df["ano_campeonato"].unique())
    c1, c2, c3 = st.columns([0.35, 0.35, 0.3])
    ano1 = c1.number_input("Ano 1", value=int(anos[-2]), min_value=int(min(anos)), max_value=int(max(anos)), key="comp_ano1")
    ano2 = c2.number_input("Ano 2", value=int(anos[-1]), min_value=int(min(anos)), max_value=int(max(anos)), key="comp_ano2")

    df_plot = df.loc[df["ano_campeonato"].isin([ano1, ano2])].copy()
    df_plot, selecionados = filtrar_grupo_times(df_plot, escolha, container=c3, key_prefix="comp")

    fig = px.line(
        df_plot,
        x="rodada",
        y=choose_metric,
        color="time",
        facet_col="ano_campeonato",
        facet_col_spacing=0.05,
        category_orders={"ano_campeonato": [ano1, ano2]},
        title=f"Brasileirão | {ano1} vs {ano2} | {escolha} | {METRIC_LABELS[choose_metric]}",
        hover_data=["classificacao_final"],
        labels=COLUMN_LABELS | {choose_metric: METRIC_LABELS[choose_metric]},
    )
    fig = add_linha_primeiro_turno(fig)
    st.plotly_chart(fig, use_container_width=True)
    mostrar_tabela(df_plot, key="comp_tabela")


def aba_distribuicoes(df: pd.DataFrame, modo_aprendiz: bool) -> None:
    st.subheader("🎲 Laboratório de estatística")
    st.markdown(
        """
        Aqui o campeonato vira uma sala com 20 alunos. Cada time tem uma nota: seus pontos, vitórias ou saldo final.
        Quando as notas são parecidas, o campeonato foi equilibrado. Quando ficam muito espalhadas, houve maior desigualdade.
        """
    )

    if modo_aprendiz:
        bloco_didatico(
            pergunta="Qual temporada foi mais equilibrada?",
            conceito="Distribuição, boxplot e desvio padrão.",
            acao="Ordene por desvio padrão e observe quais anos tiveram menor ou maior dispersão.",
        )
        with st.expander("🎓 O que é um boxplot?", expanded=True):
            st.markdown(
                """
                Um boxplot resume a distribuição dos dados:
                - a caixa mostra onde está a maior parte dos times;
                - linhas longas indicam maior diferença entre campanhas;
                - pontos muito afastados podem indicar campanhas fora da curva.
                """
            )

    c1, c2, c3, _ = st.columns([0.18, 0.28, 0.18, 0.36])
    df_plot = df.loc[df["rodada"] == 38].copy()
    ordenar_por = c1.radio("Ordenar por", ["Ano", "Desvio padrão"], key="dist_order")
    choose_metric = metric_selectbox("Escolher métrica", key="dist_metric")
    escolha = c3.radio("Grupo", ["Todos", "G4", "G6", "Z4"], key="dist_grupo")
    df_plot, _ = filtrar_grupo_times(df_plot, escolha, key_prefix="dist")

    df_std = (
        df_plot.groupby("ano_campeonato")[choose_metric]
        .std()
        .reset_index()
        .rename(columns={choose_metric: f"{choose_metric}_std"})
    )
    df_plot = df_plot.merge(df_std, on="ano_campeonato", how="left")
    df_plot = df_plot.sort_values("ano_campeonato" if ordenar_por == "Ano" else f"{choose_metric}_std")

    with st.expander("Gráfico Boxplot", expanded=True):
        fig = px.box(
            df_plot,
            x="ano_campeonato",
            y=choose_metric,
            hover_data=["time", "adversário"],
            title=f"Distribuição | {escolha} | {METRIC_LABELS[choose_metric]}",
            labels=COLUMN_LABELS | {choose_metric: METRIC_LABELS[choose_metric]},
        )
        fig.update_xaxes(type="category")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Curva de distribuição", expanded=False):
        group_labels = []
        hist_data = []
        for ano in df_plot["ano_campeonato"].dropna().unique():
            valores = df_plot.loc[df_plot["ano_campeonato"] == ano, choose_metric].dropna().tolist()
            if len(valores) >= 2:
                group_labels.append(str(ano))
                hist_data.append(valores)

        if hist_data:
            fig = ff.create_distplot(hist_data, group_labels, curve_type="normal", show_hist=False, show_rug=False)
            fig.update_layout(title_text=f"Curvas de distribuição | {METRIC_LABELS[choose_metric]} | {escolha}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Não há dados suficientes para construir a curva de distribuição.")

    mostrar_tabela(df_plot, key="dist_tabela")


def aba_mito_verdade(df: pd.DataFrame, modo_aprendiz: bool) -> None:
    st.subheader("🔮 Mito ou verdade? Líder do 1º turno vira campeão?")
    st.write("Use os fluxos abaixo para investigar a relação entre liderança no 1º turno e título ao final do campeonato.")

    if modo_aprendiz:
        bloco_didatico(
            pergunta="Liderar no meio do campeonato garante o título?",
            conceito="Teste de hipótese exploratório e visualização de fluxo.",
            acao="Passe o mouse pelos fluxos e veja para onde foram os líderes do 1º turno e de onde vieram os campeões.",
        )

    c1, c2 = st.columns(2)

    # Líder do 1º turno -> classificação final
    df_turno_final = (
        df.groupby(["ano_campeonato", "time"])[["classificacao_1o_turno", "classificacao_final"]]
        .max()
        .reset_index()
    )
    lideres = df_turno_final.loc[df_turno_final["classificacao_1o_turno"] == 1].copy()
    contagem_final = lideres.groupby("classificacao_final")["time"].count().reset_index()

    labels_final = ["Líder 1º turno"] + [f"Final {int(pos)}º" for pos in contagem_final["classificacao_final"]]
    source = [0] * len(contagem_final)
    target = list(range(1, len(contagem_final) + 1))
    value = contagem_final["time"].tolist()

    fig1 = go.Figure(
        data=[go.Sankey(node=dict(label=labels_final, pad=25, thickness=12), link=dict(source=source, target=target, value=value))]
    )
    fig1.update_layout(title="Destino dos líderes do 1º turno", height=420)
    c1.info("Qual foi a classificação final dos times que lideraram no fim do 1º turno?")
    c1.plotly_chart(fig1, use_container_width=True)

    # Campeões -> classificação no 1º turno
    campeoes = df_turno_final.loc[df_turno_final["classificacao_final"] == 1].copy()
    contagem_turno = campeoes.groupby("classificacao_1o_turno")["time"].count().reset_index()

    labels_turno = ["Campeões"] + [f"Turno {int(pos)}º" for pos in contagem_turno["classificacao_1o_turno"]]
    source = list(range(1, len(contagem_turno) + 1))
    target = [0] * len(contagem_turno)
    value = contagem_turno["time"].tolist()

    fig2 = go.Figure(
        data=[go.Sankey(node=dict(label=labels_turno, pad=25, thickness=12), link=dict(source=source, target=target, value=value))]
    )
    fig2.update_layout(title="Posição dos campeões no 1º turno", height=420)
    c2.info("Em qual posição os campeões estavam no fim do 1º turno?")
    c2.plotly_chart(fig2, use_container_width=True)

    total = len(lideres)
    lideres_campeoes = int((lideres["classificacao_final"] == 1).sum())
    pct = 100 * lideres_campeoes / total if total else 0
    st.success(f"Na base analisada, {lideres_campeoes} de {total} líderes do 1º turno foram campeões: {pct:.1f}%.")


def aba_projecoes(df: pd.DataFrame, modo_aprendiz: bool) -> None:
    st.subheader("🤖 Máquina de palpites didáticos")
    st.markdown(
        """
        Esta seção brinca de comparar campanhas. A lógica é medir a **similaridade** entre curvas de pontos acumulados.

        Quanto menor o RMSE, mais parecidas são as curvas. Isso não significa probabilidade real de título.
        """
    )

    st.error(
        "⚠️ Esta simulação é exclusivamente didática e não deve, em hipótese alguma, ser usada como referência para apostas."
    )

    if modo_aprendiz:
        bloco_didatico(
            pergunta="Como um modelo simples compara campanhas?",
            conceito="Engenharia de variáveis, similaridade de curvas e RMSE ponderado.",
            acao="Escolha um ano e uma rodada. Veja qual ano histórico parece mais com a campanha atual.",
        )
        with st.expander("🎓 Como interpretar o RMSE aqui?", expanded=True):
            st.markdown(
                """
                O RMSE mede distância entre duas curvas.  
                - RMSE baixo: curvas parecidas.  
                - RMSE alto: curvas diferentes.  
                - Peso maior no 2º turno: valoriza mais o desempenho recente da campanha.
                """
            )

    c1, c2, _ = st.columns([0.35, 0.35, 0.3])
    ano_analisado = c1.number_input(
        "Ano a ser analisado",
        min_value=int(df.ano_campeonato.min()),
        max_value=int(df.ano_campeonato.max()),
        value=int(df.ano_campeonato.max()),
        key="proj_ano",
    )
    df_ano = df.loc[df["ano_campeonato"] == ano_analisado].copy()
    max_rodada = max(rodada_max_valida(df_ano), 10)
    rodada_max = c2.number_input("Até a rodada", value=max_rodada, max_value=max_rodada, min_value=10, key="proj_rodada")

    df_pos1 = calcular_curvas_pos1(df)

    layout1, layout2 = st.columns([0.35, 0.65], gap="medium")
    with layout1:
        st.markdown(
            f"""
            ### 1 | Curva da posição 1
            Primeiro, o app identifica a pontuação do líder a cada rodada em cada temporada.

            ### 2 | Ano histórico mais parecido
            Depois, compara a curva do líder de **{ano_analisado}** até a rodada **{rodada_max}** com as demais temporadas.
            """
        )

    with layout2:
        with st.expander("1 | Curvas da posição 1 por ano", expanded=True):
            fig = px.line(
                df_pos1,
                x="rodada",
                y=[col for col in df_pos1.columns if col != "rodada"],
                title="Curvas da posição 1 em cada temporada",
                labels={"value": "Pontos do líder", "rodada": "Rodada", "variable": "Ano"},
            )
            fig = add_linha_primeiro_turno(fig)
            st.plotly_chart(fig, use_container_width=True)

        with st.expander("2 | Similaridades entre curvas da posição 1", expanded=True):
            try:
                df_base, df_rmse, ano_similar, min_rmse = identificar_curva_pos1_menor_rmse(df_pos1, ano_analisado, int(rodada_max))
                fig = px.line(
                    df_base,
                    x="rodada",
                    y=[ano_analisado, ano_similar],
                    title=f"Ano analisado: {ano_analisado} | Ano mais similar: {ano_similar} | RMSE: {min_rmse:.3f}",
                    labels={"value": "Pontos do líder", "rodada": "Rodada", "variable": "Ano"},
                )
                fig = add_linha_primeiro_turno(fig)
                st.plotly_chart(fig, use_container_width=True)
                mostrar_tabela(df_rmse.round(3), key="proj_rmse_anos", label="Mostrar ranking completo de anos similares")
                st.success(f"A curva da posição 1 mais similar a {ano_analisado}, até a rodada {rodada_max}, foi a de {ano_similar}.")
            except Exception as exc:
                st.error(f"Não foi possível calcular a similaridade: {exc}")
                return

    layout1, layout2 = st.columns([0.35, 0.65], gap="medium")
    with layout1:
        st.markdown(
            f"""
            ### 3 | Times mais parecidos com a curva campeã
            Agora o app compara cada time de **{ano_analisado}** com a curva do líder do ano histórico mais parecido: **{ano_similar}**.

            O ranking abaixo indica **similaridade**, não chance real de título.
            """
        )

    with layout2:
        with st.expander("3 | Ranking de similaridade dos times", expanded=True):
            df_times_curvas, df_rmse_times, rmse_col = identificar_times_menor_rmse(df, df_pos1, int(ano_analisado), int(rodada_max), int(ano_similar))
            top_times = df_rmse_times["time"].head(5).tolist()
            fig = px.line(
                df_times_curvas,
                x="rodada",
                y=top_times + [ano_similar],
                title=f"Top 5 times de {ano_analisado} mais similares à curva do líder de {ano_similar}",
                labels={"value": "Pontos acumulados", "rodada": "Rodada", "variable": "Time/Ano referência"},
            )
            fig = add_linha_primeiro_turno(fig)
            st.plotly_chart(fig, use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Ano analisado", int(ano_analisado))
            c2.metric("Até a rodada", int(rodada_max))
            c3.metric("Ano mais similar", int(ano_similar))
            pontuacao_ref = int(df.loc[df["ano_campeonato"] == ano_similar, "pontos_acum"].max())
            c4.metric("Pontuação referência", pontuacao_ref)

            st.info("Times mais similares por RMSE ponderado:")
            st.dataframe(df_rmse_times.rename(columns={rmse_col: "RMSE ponderado"}).round(3), use_container_width=True, hide_index=True)

# =============================================================================
# APP PRINCIPAL
# =============================================================================
def main() -> None:
    df = carregar_dados()
    modo_aprendiz = sidebar_app()
    header_app()

    tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "🏟️ Comece por aqui",
            "🏆 Hall dos campeões",
            "📅 Raio-X da temporada",
            "📈 Corrida rodada a rodada",
            "⚔️ Duelo de campanhas",
            "🎲 Laboratório de estatística",
            "🔮 Mito ou verdade?",
            "🤖 Máquina de palpites didáticos",
        ]
    )

    with tab0:
        aba_home(df, modo_aprendiz)
    with tab1:
        aba_campeoes(df, modo_aprendiz)
    with tab2:
        aba_raio_x(df, modo_aprendiz)
    with tab3:
        aba_evolucao(df, modo_aprendiz)
    with tab4:
        aba_comparativos(df, modo_aprendiz)
    with tab5:
        aba_distribuicoes(df, modo_aprendiz)
    with tab6:
        aba_mito_verdade(df, modo_aprendiz)
    with tab7:
        aba_projecoes(df, modo_aprendiz)


if __name__ == "__main__":
    main()
