# Brasileirão sob um Olhar Estatístico ⚽📊

Uma aplicação interativa para explorar o Campeonato Brasileiro de pontos corridos com estatística, visualização de dados e conceitos de Ciência de Dados.

O projeto transforma campanhas do Brasileirão em uma experiência analítica e didática: o usuário pode acompanhar a evolução rodada a rodada, comparar campeões, investigar padrões de pontuação, observar distribuições estatísticas e entender como métricas de similaridade podem ser usadas para comparar campanhas de futebol.

> Futebol como laboratório para aprender Data Science.

---

## Acesse o app

Aplicação publicada no Streamlit:

**https://brasileirao-olhar-estatistico.streamlit.app/**

---

## Objetivo do projeto

O objetivo deste projeto é usar o Brasileirão como um ambiente simples, familiar e divertido para explorar conceitos de análise de dados.

A partir de dados históricos do Campeonato Brasileiro, o app permite responder perguntas como:

- Um campeão costuma liderar desde o início?
- O líder do primeiro turno normalmente termina campeão?
- Qual campanha foi mais dominante?
- Quantos pontos costumam separar campeões, G4, meio de tabela e rebaixados?
- O Brasileirão está ficando mais equilibrado?
- É possível comparar campanhas atuais com campanhas históricas?
- Como métricas como RMSE e similaridade vetorial podem ajudar a medir semelhança entre campanhas?

---

## Por que futebol e Data Science?

Futebol é um tema popular, intuitivo e cheio de dados.

Cada campeonato gera uma sequência de eventos: vitórias, empates, derrotas, gols, pontos, saldo, posições e variações rodada a rodada. Isso torna o Brasileirão um ótimo exemplo para estudar:

- análise exploratória de dados;
- séries temporais;
- visualização de dados;
- estatística descritiva;
- comparação de distribuições;
- métricas de erro;
- similaridade entre vetores;
- storytelling com dados;
- construção de dashboards interativos.

A proposta não é prever o futuro com precisão absoluta, mas mostrar como uma pergunta esportiva pode virar uma investigação orientada por dados.

---

## Funcionalidades principais

### 🚀 Tour de 3 minutos

Uma entrada rápida para quem deseja entender o app sem precisar configurar filtros complexos.

A ideia é apresentar provocações simples e mostrar como futebol pode ser analisado por meio de dados.

---

### 🔥 Histórias dos dados

Seção com narrativas prontas sobre campanhas marcantes e padrões históricos do Brasileirão.

Exemplos de perguntas exploradas:

- O que torna uma campanha fora da curva?
- Como uma liderança pode se sustentar ou desaparecer?
- O que os dados dizem sobre equilíbrio entre os times?
- Que padrões aparecem quando comparamos diferentes temporadas?

---

### 📈 Corrida rodada a rodada

Visualização da evolução dos times ao longo do campeonato.

Cada campanha é tratada como uma série temporal. O usuário pode observar a progressão de pontos, vitórias, saldo de gols e outras métricas acumuladas.

Essa seção ajuda a entender conceitos como:

- séries temporais;
- trajetória acumulada;
- comparação de curvas;
- ritmo de pontuação;
- desempenho por turno.

---

### 🏆 Hall dos campeões

Análise dos campeões brasileiros no formato de pontos corridos.

Permite comparar campanhas vencedoras e observar como diferentes campeões chegaram ao título.

---

### 📅 Raio-X da temporada

Exploração de temporadas específicas do Brasileirão.

O usuário pode analisar estatísticas por ano, posições finais, pontuação e desempenho dos clubes.

---

### ⚔️ Comparativos

Área dedicada à comparação entre anos, clubes, campanhas e grupos de interesse.

Útil para observar diferenças entre campeões, classificados ao G4, times intermediários e equipes rebaixadas.

---

### 🎲 Laboratório estatístico

Seção voltada à análise de distribuições.

Aqui entram conceitos como:

- média;
- mediana;
- dispersão;
- desvio padrão;
- boxplot;
- outliers;
- equilíbrio competitivo.

O objetivo é mostrar que a tabela final do campeonato não é apenas uma lista de posições, mas uma distribuição estatística de desempenho.

---

### 🤖 Similaridade de campanhas

Seção didática para comparar campanhas atuais com campanhas históricas.

A abordagem considera a evolução rodada a rodada e mede o quanto uma campanha se parece com outra.

A métrica final utilizada é o RMSE, que calcula a distância ponto a ponto entre duas curvas.

---

### 🧠 Futebol, Vetores e IA

Uma seção conceitual que conecta futebol com ideias modernas de Ciência de Dados.

A lógica é simples:

Uma campanha pode ser representada como uma sequência de números.

Exemplo simplificado:

```text
Campanha A = [3, 6, 9, 12, 15, 18, ...]
Campanha B = [1, 4, 7, 10, 13, 16, ...]
````

Essas sequências podem ser interpretadas como vetores de desempenho.

A partir disso, surge uma pergunta:

> Campanhas parecidas ocupam regiões próximas em um espaço vetorial?

Essa é uma ponte conceitual com temas como:

* embeddings;
* sistemas de recomendação;
* busca semântica;
* similaridade vetorial;
* modelos de linguagem;
* representação numérica de objetos complexos.

Importante: o app não usa LLMs nem transformers para prever resultados. A conexão é conceitual e didática: transformar informação em vetores e medir proximidade entre eles.

---

## Abordagem estatística

O projeto parte da ideia de que a campanha de um time pode ser analisada como uma trajetória.

Em vez de olhar apenas para a pontuação final, o app observa como essa pontuação foi construída rodada a rodada.

Isso permite comparar não apenas o resultado final, mas o caminho percorrido.

---

## RMSE

A métrica principal usada na comparação de campanhas é o RMSE.

RMSE significa Root Mean Squared Error, ou raiz do erro quadrático médio.

No contexto do app, ele mede a distância entre duas curvas de desempenho.

Se duas campanhas têm pontuação acumulada muito parecida rodada a rodada, o RMSE tende a ser menor.

Se as campanhas se afastam muito ao longo das rodadas, o RMSE tende a ser maior.

Em termos práticos:

```text
RMSE baixo  -> campanhas mais parecidas
RMSE alto   -> campanhas mais diferentes
```

---

## Similaridade de cosseno

Durante a idealização da abordagem, também foi considerada a similaridade de cosseno.

Essa métrica mede o ângulo entre dois vetores. Ela é muito usada em problemas de similaridade vetorial, especialmente em contextos como embeddings, busca semântica e recomendação.

A similaridade de cosseno poderia responder a uma pergunta como:

> As campanhas têm uma direção parecida?

No entanto, para o problema específico deste app, ela não foi mantida como métrica final.

O motivo é que a similaridade de cosseno mede principalmente a direção dos vetores, não necessariamente a distância absoluta entre as campanhas.

No futebol, isso pode ser uma limitação.

Duas campanhas podem ter formato parecido, mas níveis muito diferentes de pontuação. Por exemplo, dois times podem crescer em ritmo semelhante ao longo do campeonato, mas um terminar com 82 pontos e outro com 68.

Como a proposta do app é comparar a proximidade rodada a rodada, o RMSE se mostrou mais adequado.

---

## RMSE vs Similaridade de Cosseno

| Métrica                 | O que mede                           | Boa para                                         | Limitação no contexto do Brasileirão                                |
| ----------------------- | ------------------------------------ | ------------------------------------------------ | ------------------------------------------------------------------- |
| RMSE                    | Distância ponto a ponto entre curvas | Comparar campanhas rodada a rodada               | Pode penalizar fortemente diferenças absolutas                      |
| Similaridade de cosseno | Direção entre vetores                | Comparar formato ou orientação geral da campanha | Pode considerar parecidas campanhas com pontuações muito diferentes |

Lição de Ciência de Dados:

> A melhor métrica não é necessariamente a mais famosa ou moderna. É a que melhor responde à pergunta do problema.

---

## Estrutura esperada dos dados

O app utiliza uma base consolidada em formato Parquet, contendo dados históricos do Brasileirão.

Arquivo esperado:

```text
dados/df_completo.parquet
```

Algumas colunas utilizadas pelo app incluem:

```text
ano_campeonato
rodada
time
posicao
pontos
pontos_acum
vitorias_acum
empates_acum
derrotas_acum
gols_pro_acum
gols_contra_acum
saldo_gols_acum
```

A estrutura exata pode variar conforme novas versões da base sejam atualizadas.

---

## Tecnologias utilizadas

* Python
* Pandas
* NumPy
* Plotly
* Streamlit
* Scikit-learn
* PyArrow / Parquet

---

## Como executar localmente

Clone o repositório:

```bash
git clone https://github.com/marioandrededeus/estatisticas-brasileirao-masc.git
```

Acesse a pasta do projeto:

```bash
cd estatisticas-brasileirao-masc
```

Crie e ative um ambiente virtual, se desejar:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/Mac:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o app:

```bash
streamlit run app.py
```

---

## Estrutura sugerida do projeto

```text
estatisticas-brasileirao-masc/
│
├── app.py
├── requirements.txt
├── README.md
│
├── dados/
│   └── df_completo.parquet
│
├── images/
│   └── arquivos de imagem e logos
│
└── notebooks/
    └── análises exploratórias e estudos auxiliares
```

---

## Limitações

Este projeto tem finalidade analítica e educacional.

As projeções e comparações de campanhas não devem ser interpretadas como previsão garantida de resultados esportivos.

O futebol envolve muitos fatores que não estão necessariamente representados na base de dados, como:

* lesões;
* troca de técnicos;
* calendário;
* competições paralelas;
* mando de campo;
* contexto financeiro;
* decisões de arbitragem;
* desempenho individual de atletas;
* fatores psicológicos e táticos.

Portanto, os resultados devem ser vistos como apoio à exploração estatística, não como modelo preditivo definitivo.

---

## Possíveis melhorias futuras

Algumas ideias para evolução do projeto:

* incluir dados de mando de campo;
* separar desempenho como mandante e visitante;
* incluir força ofensiva e defensiva por rodada;
* comparar campanhas por janela móvel;
* testar outras métricas de similaridade;
* adicionar clustering de campanhas;
* criar embeddings de campanhas;
* incluir dados de mercado, elenco ou técnicos;
* criar ranking de campanhas mais parecidas;
* permitir exportação de gráficos;
* melhorar ainda mais a experiência mobile;
* criar versão multipágina com `pages/` do Streamlit;
* adicionar testes automatizados para funções principais.

---

## Ideias de análises possíveis

Este projeto pode ser usado para explorar perguntas como:

* O campeão costuma ter melhor ataque ou melhor defesa?
* Existe uma pontuação mínima segura contra rebaixamento?
* A diferença entre campeão e vice está aumentando ou diminuindo?
* O Brasileirão ficou mais equilibrado ao longo dos anos?
* O G4 costuma se definir cedo ou apenas nas rodadas finais?
* Qual campanha teve a maior arrancada no segundo turno?
* Qual campanha perdeu mais desempenho depois da rodada 19?
* Quais campeões tiveram trajetórias mais parecidas?

---

## Sobre o projeto

Este projeto foi desenvolvido com o objetivo de aproximar futebol, estatística e Ciência de Dados.

A proposta é mostrar que conceitos técnicos podem ser explorados de forma acessível quando aplicados a temas familiares.

Futebol, nesse contexto, funciona como uma porta de entrada para discutir dados, hipóteses, métricas, visualizações e interpretação crítica.

---

## Autor

Desenvolvido por Mario André de Deus.

* LinkedIn: [https://www.linkedin.com/in/marioandrededeus/](https://www.linkedin.com/in/marioandrededeus/)
* GitHub: [https://github.com/marioandrededeus](https://github.com/marioandrededeus)
* Repositório do projeto: [https://github.com/marioandrededeus/estatisticas-brasileirao-masc](https://github.com/marioandrededeus/estatisticas-brasileirao-masc)


---

## Contribuições

Sugestões, melhorias e novas análises são bem-vindas.

Algumas formas de contribuir:

* abrir uma issue com sugestão de análise;
* propor melhoria de visualização;
* revisar textos didáticos;
* sugerir novas métricas;
* enviar pull request com melhorias no código.

---

## Disclaimer

Este projeto é experimental, educacional e voltado à análise estatística do futebol.

As análises apresentadas não representam recomendação de aposta, previsão garantida de resultado ou avaliação definitiva sobre clubes, atletas ou campeonatos.
