
def interpretar_pergunta(pergunta):
    """
    Interpreta a pergunta do usuário e identifica:

    - intenção da pergunta
    - entidade principal envolvida

    Retorna um dicionário com essas informações.
    """

    pergunta = pergunta.lower().strip()

    # ==========================================================
    # TERMOS DE CONTEXTO
    # ==========================================================

    palavras_transportadoras = [
        "transportadora",
        "transportadoras",
        "empresa de transporte",
        "empresas de transporte",
    ]

    palavras_rotas = [
        "rota",
        "rotas",
        "trajeto",
        "trajetos",
    ]

    palavras_perdas = [
        "perda",
        "perdas",
        "prejuízo",
        "prejuizo",
        "prejuízos",
        "prejuizos",
        "impacto financeiro",
        "valor perdido",
        "valores perdidos",
    ]

    palavras_anomalias = [
        "anomalia",
        "anomalias",
        "comportamento anormal",
        "comportamentos anormais",
        "comportamento fora do padrão",
        "fora do padrão",
        "fora do padrao",
        "pontos de atenção",
        "pontos de atencao",
        "ponto de atenção",
        "ponto de atencao",
        "irregularidade",
        "irregularidades",
        "sinais de alerta",
        "sinal de alerta",
    ]

    palavras_relatorio = [
        "relatório",
        "relatorio",
        "relatório completo",
        "relatorio completo",
        "gere um relatório",
        "gerar relatório",
        "faça um relatório",
        "fazer relatório",
    ]

    palavras_priorizacao = [
        "maior risco",
        "maiores riscos",
        "mais crítico",
        "mais critica",
        "mais crítica",
        "mais críticos",
        "mais criticos",
        "maior atenção",
        "mais atenção",
        "maior prioridade",
        "mais prioridade",
        "prioridade de investigação",
        "prioridade para investigação",
        "priorizar",
        "prioridade",
        "merece mais atenção",
        "merecem mais atenção",
        "devo investigar primeiro",
        "investigar primeiro",
        "deve ser investigada primeiro",
        "pior rota",
        "rotas críticas",
        "rotas criticas",
        "rota crítica",
        "rota critica",
    ]

    # ==========================================================
    # 1. RELATÓRIO
    # ==========================================================

    if any(item in pergunta for item in palavras_relatorio):
        return {
            "intencao": "relatorio",
            "entidade": "geral",
        }

    # ==========================================================
    # 2. ANOMALIAS
    # ==========================================================

    if any(item in pergunta for item in palavras_anomalias):
        return {
            "intencao": "analisar_anomalias",
            "entidade": "geral",
        }

    # ==========================================================
    # 3. TRANSPORTADORA
    # ==========================================================

    tem_transportadora = any(
        item in pergunta
        for item in palavras_transportadoras
    )

    if tem_transportadora:

        if any(
            item in pergunta
            for item in palavras_priorizacao
        ):
            return {
                "intencao": "priorizar",
                "entidade": "transportadora",
            }

        return {
            "intencao": "analisar",
            "entidade": "transportadora",
        }

    # ==========================================================
    # 4. ROTA
    # ==========================================================

    tem_rota = any(
        item in pergunta
        for item in palavras_rotas
    )

    if tem_rota:

        if any(
            item in pergunta
            for item in palavras_priorizacao
        ):
            return {
                "intencao": "priorizar",
                "entidade": "rota",
            }

        return {
            "intencao": "analisar",
            "entidade": "rota",
        }

    # ==========================================================
    # 5. PRIORIZAÇÃO GERAL
    # ==========================================================

    if any(
        item in pergunta
        for item in palavras_priorizacao
    ):
        return {
            "intencao": "priorizar",
            "entidade": "geral",
        }

    # ==========================================================
    # 6. PERDAS
    # ==========================================================

    if any(
        item in pergunta
        for item in palavras_perdas
    ):
        return {
            "intencao": "analisar",
            "entidade": "perdas",
        }

    # ==========================================================
    # 7. PERGUNTA NÃO IDENTIFICADA
    # ==========================================================

    return {
        "intencao": "desconhecida",
        "entidade": "desconhecida",
    }
