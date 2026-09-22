import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# ==========================================================
# CONFIGURAÇÃO DO CAMINHO DO PROJETO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from app.agente import executar_agente, formatar_resposta
from app.dashboard import (
    carregar_dashboard,
    obter_indicadores_principais,
    contar_riscos,
    obter_principal_ponto_atencao,
    preparar_perdas_por_tipo,
    preparar_ocorrencias_por_tipo,
    preparar_perdas_por_rota,
    preparar_perdas_por_transportadora,
    preparar_tabela_rotas,
)


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Agente Inteligente de Prevenção de Perdas",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================================
# FUNÇÃO PARA FORMATAR MOEDA
# ==========================================================

def formatar_moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ==========================================================
# CABEÇALHO
# ==========================================================

st.title("🛡️ Agente Inteligente de Prevenção de Perdas")

st.write(
    "Sistema de apoio à análise de perdas, riscos, rotas, "
    "transportadoras e anomalias."
)

st.info(
    "Os indicadores apresentados representam pontos de atenção "
    "e devem ser validados pela equipe responsável antes de "
    "qualquer decisão operacional."
)


# ==========================================================
# DASHBOARD PRINCIPAL
# ==========================================================

st.header("📊 Dashboard de Prevenção de Perdas")

with st.spinner("Carregando indicadores..."):

    (
        perdas_dashboard,
        rotas_dashboard,
        transportadoras_dashboard,
        riscos_dashboard
    ) = carregar_dashboard()


# ==========================================================
# INDICADORES PRINCIPAIS
# ==========================================================

indicadores = obter_indicadores_principais(
    perdas_dashboard,
    rotas_dashboard,
    riscos_dashboard
)

total_ocorrencias = indicadores["total_ocorrencias"]

valor_total = indicadores["valor_total"]

ocorrencias_investigacao = (
    indicadores["ocorrencias_investigacao"]
)

rotas_criticas = indicadores["rotas_criticas"]


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Ocorrências",
        total_ocorrencias
    )

with col2:
    st.metric(
        "Perdas registradas",
        formatar_moeda(valor_total)
    )

with col3:
    st.metric(
        "Em investigação",
        ocorrencias_investigacao
    )

with col4:
    st.metric(
        "Rotas críticas",
        rotas_criticas
    )


st.divider()


# ==========================================================
# GRÁFICOS — OCORRÊNCIAS E PERDAS
# ==========================================================

st.header("📈 Indicadores financeiros e operacionais")


col1, col2 = st.columns(2)


# ==========================================================
# GRÁFICO — PERDAS POR TIPO
# ==========================================================

with col1:

    st.subheader("💰 Perdas por tipo de ocorrência")

    dados_perdas_tipo = pd.DataFrame(
        preparar_perdas_por_tipo(
            perdas_dashboard
        )
    )

    dados_perdas_tipo = dados_perdas_tipo.set_index(
        "Tipo"
    )

    st.bar_chart(
        dados_perdas_tipo,
        y="Valor"
    )


# ==========================================================
# GRÁFICO — OCORRÊNCIAS POR TIPO
# ==========================================================

with col2:

    st.subheader("📦 Ocorrências por tipo")

    dados_ocorrencias_tipo = pd.DataFrame(
        preparar_ocorrencias_por_tipo(
            perdas_dashboard
        )
    )

    dados_ocorrencias_tipo = (
        dados_ocorrencias_tipo.set_index(
            "Tipo"
        )
    )

    st.bar_chart(
        dados_ocorrencias_tipo,
        y="Ocorrências"
    )


# ==========================================================
# GRÁFICOS — ROTAS E TRANSPORTADORAS
# ==========================================================

st.divider()

st.header("🛣️ Análise de rotas e transportadoras")


col1, col2 = st.columns(2)


# ==========================================================
# GRÁFICO — PERDAS POR ROTA
# ==========================================================

with col1:

    st.subheader("💰 Perdas por rota")

    dados_perdas_rota = pd.DataFrame(
        preparar_perdas_por_rota(
            rotas_dashboard
        )
    )

    dados_perdas_rota = dados_perdas_rota.set_index(
        "Rota"
    )

    st.bar_chart(
        dados_perdas_rota,
        y="Perdas"
    )


# ==========================================================
# GRÁFICO — PERDAS POR TRANSPORTADORA
# ==========================================================

with col2:

    st.subheader("🚚 Perdas por transportadora")

    dados_perdas_transportadora = pd.DataFrame(
        preparar_perdas_por_transportadora(
            transportadoras_dashboard
        )
    )

    dados_perdas_transportadora = (
        dados_perdas_transportadora.set_index(
            "Transportadora"
        )
    )

    st.bar_chart(
        dados_perdas_transportadora,
        y="Perdas"
    )


# ==========================================================
# CLASSIFICAÇÃO DE RISCOS
# ==========================================================

st.divider()

st.header("⚠️ Classificação de riscos")


classificacao_riscos = contar_riscos(
    riscos_dashboard
)


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "CRÍTICO",
        classificacao_riscos["CRÍTICO"]
    )

with col2:
    st.metric(
        "ALTO",
        classificacao_riscos["ALTO"]
    )

with col3:
    st.metric(
        "MÉDIO",
        classificacao_riscos["MÉDIO"]
    )

with col4:
    st.metric(
        "BAIXO",
        classificacao_riscos["BAIXO"]
    )


# ==========================================================
# TABELA DE ROTAS
# ==========================================================

st.subheader("📋 Classificação das rotas")


dados_rotas = preparar_tabela_rotas(
    riscos_dashboard
)


for item in dados_rotas:

    item["Perdas (R$)"] = formatar_moeda(
        item["Perdas (R$)"]
    )


st.table(dados_rotas)


# ==========================================================
# PONTO DE ATENÇÃO
# ==========================================================

principal = obter_principal_ponto_atencao(
    riscos_dashboard
)


if principal:

    st.subheader("🔎 Principal ponto de atenção")

    st.write("Rota analisada:")

    st.header(
        principal["rota"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.write("Classificação")

        st.write(
            principal["risco"]
        )

    with col2:

        st.write("Índice de ocorrência")

        st.write(
            f"{principal['indice_ocorrencia']:.2f}%"
        )

    with col3:

        st.write("Perdas registradas")

        st.write(
            formatar_moeda(
                principal["valor_perdas"]
            )
        )

    st.info(
        "A classificação representa um ponto de atenção "
        "baseado nos indicadores analisados. Ela não "
        "constitui, isoladamente, evidência de fraude "
        "ou irregularidade."
    )


# ==========================================================
# PERGUNTE AO AGENTE
# ==========================================================

st.divider()

st.header("🔎 Pergunte ao agente")

pergunta = st.text_input(
    "Digite sua pergunta:",
    placeholder="Ex.: Qual rota merece mais atenção?"
)


if st.button(
    "🔎 Analisar",
    type="primary"
):

    if not pergunta.strip():

        st.warning(
            "Digite uma pergunta antes de realizar a análise."
        )

    else:

        with st.spinner("Analisando os dados..."):

            resultado = executar_agente(pergunta)

        st.divider()

        st.subheader("📊 Resultado da análise")

        if resultado is None:

            st.warning(
                "Não consegui identificar qual análise "
                "deve ser executada."
            )

            st.write(
                "Experimente perguntas sobre perdas, rotas, "
                "riscos, transportadoras, anomalias ou relatório."
            )

        else:

            # ==================================================
            # RESULTADO DE RISCOS
            # ==================================================

            if (
                isinstance(resultado, list)
                and resultado
                and "risco" in resultado[0]
            ):

                st.write(
                    "A análise de riscos foi concluída."
                )

                st.write(
                    formatar_resposta(resultado)
                )

            # ==================================================
            # OUTROS RESULTADOS
            # ==================================================

            else:

                st.write(
                    formatar_resposta(resultado)
                )


# ==========================================================
# RODAPÉ
# ==========================================================

st.divider()

st.caption(
    "Agente Inteligente de Prevenção de Perdas | "
    "Sistema de apoio à decisão | "
    "Validação humana obrigatória"
)