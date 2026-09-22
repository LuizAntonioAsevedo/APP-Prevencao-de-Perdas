from app.agente import obter_dados_dashboard


# ==========================================================
# CARREGAMENTO DOS DADOS DO DASHBOARD
# ==========================================================

def carregar_dashboard():
    """
    Carrega os dados necessários para o Dashboard
    através da camada do Agente.
    """

    dados = obter_dados_dashboard()

    return (
        dados["perdas"],
        dados["rotas"],
        dados["transportadoras"],
        dados["riscos"],
    )


# ==========================================================
# INDICADORES PRINCIPAIS
# ==========================================================

def obter_indicadores_principais(
    perdas,
    rotas,
    riscos
):
    """
    Calcula os principais indicadores exibidos
    no Dashboard.
    """

    total_ocorrencias = perdas["total_ocorrencias"]

    valor_total = perdas["valor_total"]

    ocorrencias_investigacao = (
        perdas["ocorrencias_em_investigacao"]
    )

    total_rotas = len(rotas)

    rotas_criticas = sum(
        1
        for item in riscos
        if item["risco"] == "CRÍTICO"
    )

    return {
        "total_ocorrencias": total_ocorrencias,
        "valor_total": valor_total,
        "ocorrencias_investigacao": ocorrencias_investigacao,
        "total_rotas": total_rotas,
        "rotas_criticas": rotas_criticas,
    }


# ==========================================================
# CLASSIFICAÇÃO DOS RISCOS
# ==========================================================

def contar_riscos(riscos):
    """
    Conta a quantidade de rotas em cada classificação
    de risco.
    """

    quantidade_critico = sum(
        1
        for item in riscos
        if item["risco"] == "CRÍTICO"
    )

    quantidade_alto = sum(
        1
        for item in riscos
        if item["risco"] == "ALTO"
    )

    quantidade_medio = sum(
        1
        for item in riscos
        if item["risco"] == "MÉDIO"
    )

    quantidade_baixo = sum(
        1
        for item in riscos
        if item["risco"] == "BAIXO"
    )

    return {
        "CRÍTICO": quantidade_critico,
        "ALTO": quantidade_alto,
        "MÉDIO": quantidade_medio,
        "BAIXO": quantidade_baixo,
    }


# ==========================================================
# PRINCIPAL PONTO DE ATENÇÃO
# ==========================================================

def obter_principal_ponto_atencao(riscos):
    """
    Retorna a rota classificada como principal ponto
    de atenção.
    """

    if not riscos:
        return None

    return riscos[0]


# ==========================================================
# PREPARAÇÃO — PERDAS POR TIPO
# ==========================================================

def preparar_perdas_por_tipo(perdas):
    """
    Prepara os dados de perdas por tipo para o gráfico.
    """

    return {
        "Tipo": list(
            perdas["perdas_por_tipo"].keys()
        ),
        "Valor": list(
            perdas["perdas_por_tipo"].values()
        ),
    }


# ==========================================================
# PREPARAÇÃO — OCORRÊNCIAS POR TIPO
# ==========================================================

def preparar_ocorrencias_por_tipo(perdas):
    """
    Prepara os dados de ocorrências por tipo
    para o gráfico.
    """

    return {
        "Tipo": list(
            perdas["ocorrencias_por_tipo"].keys()
        ),
        "Ocorrências": list(
            perdas["ocorrencias_por_tipo"].values()
        ),
    }


# ==========================================================
# PREPARAÇÃO — PERDAS POR ROTA
# ==========================================================

def preparar_perdas_por_rota(rotas):
    """
    Prepara os dados de perdas por rota para o gráfico.
    """

    return {
        "Rota": [
            item["rota"]
            for item in rotas
        ],
        "Perdas": [
            item["valor_perdas"]
            for item in rotas
        ],
    }


# ==========================================================
# PREPARAÇÃO — PERDAS POR TRANSPORTADORA
# ==========================================================

def preparar_perdas_por_transportadora(transportadoras):
    """
    Prepara os dados de perdas por transportadora
    para o gráfico.
    """

    return {
        "Transportadora": [
            item["transportadora"]
            for item in transportadoras
        ],
        "Perdas": [
            item["valor_perdas"]
            for item in transportadoras
        ],
    }


# ==========================================================
# PREPARAÇÃO — CLASSIFICAÇÃO DAS ROTAS
# ==========================================================

def preparar_tabela_rotas(riscos):
    """
    Prepara os dados da tabela de classificação
    das rotas.
    """

    dados_rotas = []

    for item in riscos:

        dados_rotas.append(
            {
                "Rota": item["rota"],
                "Risco": item["risco"],
                "Ocorrências": item["ocorrencias"],
                "Índice (%)": (
                    f"{item['indice_ocorrencia']:.2f}"
                ),
                "Perdas (R$)": item["valor_perdas"],
            }
        )

    return dados_rotas


# ==========================================================
# TESTE DA CAMADA DE DASHBOARD
# ==========================================================

if __name__ == "__main__":

    print("=== DASHBOARD ===")
    print()

    (
        perdas,
        rotas,
        transportadoras,
        riscos
    ) = carregar_dashboard()

    indicadores = obter_indicadores_principais(
        perdas,
        rotas,
        riscos
    )

    classificacao = contar_riscos(riscos)

    principal = obter_principal_ponto_atencao(
        riscos
    )

    print(
        f"Ocorrências: "
        f"{indicadores['total_ocorrencias']}"
    )

    print(
        f"Perdas registradas: "
        f"R$ {indicadores['valor_total']:.2f}"
    )

    print(
        f"Em investigação: "
        f"{indicadores['ocorrencias_investigacao']}"
    )

    print(
        f"Rotas críticas: "
        f"{indicadores['rotas_criticas']}"
    )

    print()

    print("Classificação das rotas:")

    print(
        f"CRÍTICO: "
        f"{classificacao['CRÍTICO']}"
    )

    print(
        f"ALTO: "
        f"{classificacao['ALTO']}"
    )

    print(
        f"MÉDIO: "
        f"{classificacao['MÉDIO']}"
    )

    print(
        f"BAIXO: "
        f"{classificacao['BAIXO']}"
    )

    print()

    if principal:

        print(
            f"Principal ponto de atenção: "
            f"{principal['rota']}"
        )

        print(
            f"Risco: "
            f"{principal['risco']}"
        )

        print(
            f"Índice: "
            f"{principal['indice_ocorrencia']:.2f}%"
        )

        print(
            f"Perdas: "
            f"R$ {principal['valor_perdas']:.2f}"
        )