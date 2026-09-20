
from app.interpretador import interpretar_pergunta

from app.skills.analisar_perdas import analisar_perdas
from app.skills.analisar_rotas import analisar_rotas
from app.skills.analisar_transportadoras import analisar_transportadoras
from app.skills.analisar_anomalias import analisar_anomalias
from app.skills.priorizar_riscos import priorizar_riscos
from app.skills.gerar_relatorio import gerar_relatorio


def formatar_moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_perdas(resultado):
    linhas = []

    linhas.append(
        f"Foram identificadas {resultado['total_ocorrencias']} ocorrências."
    )

    linhas.append(
        f"Valor total registrado: "
        f"{formatar_moeda(resultado['valor_total'])}."
    )

    linhas.append(
        f"Ocorrências em investigação: "
        f"{resultado['ocorrencias_em_investigacao']}."
    )

    linhas.append("")

    linhas.append("Ocorrências por tipo:")

    for tipo, quantidade in resultado["ocorrencias_por_tipo"].items():
        linhas.append(f"- {tipo}: {quantidade}")

    linhas.append("")

    linhas.append("Impacto financeiro por tipo:")

    for tipo, valor in resultado["perdas_por_tipo"].items():
        linhas.append(f"- {tipo}: {formatar_moeda(valor)}")

    linhas.append("")

    tipo_frequente = resultado["tipo_mais_frequente"]

    linhas.append(
        f"Tipo mais frequente: {tipo_frequente[0]} "
        f"({tipo_frequente[1]} ocorrências)."
    )

    tipo_maior_perda = resultado["tipo_maior_perda"]

    linhas.append(
        f"Maior impacto financeiro: {tipo_maior_perda[0]} "
        f"({formatar_moeda(tipo_maior_perda[1])})."
    )

    linhas.append("")

    linhas.append(
        "Observação: os indicadores identificam pontos de atenção "
        "e não constituem, isoladamente, evidência de fraude."
    )

    return "\n".join(linhas)


def formatar_rotas(resultado):
    linhas = []

    linhas.append("Análise das rotas:")

    for rota in resultado:
        linhas.append(
            f"- {rota['rota']}: "
            f"{rota['ocorrencias']} ocorrências em "
            f"{rota['remessas']} remessas; "
            f"índice de ocorrência de "
            f"{rota['indice_ocorrencia']:.2f}%; "
            f"perdas registradas de "
            f"{formatar_moeda(rota['valor_perdas'])}."
        )

    return "\n".join(linhas)


def formatar_riscos(resultado):
    linhas = []

    riscos_criticos = [
        item for item in resultado
        if item["risco"] == "CRÍTICO"
    ]

    riscos_altos = [
        item for item in resultado
        if item["risco"] == "ALTO"
    ]

    linhas.append(
        f"Foram analisadas {len(resultado)} rotas."
    )

    linhas.append(
        f"Rotas classificadas como risco crítico: "
        f"{len(riscos_criticos)}."
    )

    linhas.append(
        f"Rotas classificadas como risco alto: "
        f"{len(riscos_altos)}."
    )

    linhas.append("")

    linhas.append("Priorização das rotas:")

    for item in resultado:
        linhas.append(
            f"- {item['rota']} | "
            f"Risco: {item['risco']} | "
            f"Índice de ocorrência: "
            f"{item['indice_ocorrencia']:.2f}% | "
            f"Perdas: "
            f"{formatar_moeda(item['valor_perdas'])}."
        )

    if resultado:
        principal = resultado[0]

        linhas.append("")

        linhas.append(
            f"Prioridade de atenção: {principal['rota']}, "
            f"classificada como risco {principal['risco']}, "
            f"com {principal['indice_ocorrencia']:.2f}% de "
            f"índice de ocorrência e "
            f"{formatar_moeda(principal['valor_perdas'])} "
            f"em perdas registradas."
        )

    linhas.append("")

    linhas.append(
        "Observação: a classificação representa um ponto de atenção "
        "e deve ser validada pela equipe responsável antes de "
        "qualquer decisão operacional."
    )

    return "\n".join(linhas)


def formatar_transportadoras(resultado):
    linhas = []

    linhas.append("Análise das transportadoras:")

    for transportadora in resultado:
        linhas.append(
            f"- {transportadora['transportadora']}: "
            f"{transportadora['ocorrencias']} ocorrências em "
            f"{transportadora['remessas']} remessas; "
            f"índice de ocorrência de "
            f"{transportadora['indice_ocorrencia']:.2f}%; "
            f"perdas de "
            f"{formatar_moeda(transportadora['valor_perdas'])}; "
            f"média por ocorrência de "
            f"{formatar_moeda(transportadora['valor_medio_perda'])}."
        )

    return "\n".join(linhas)


def formatar_anomalias(resultado):
    linhas = []

    linhas.append("Pontos de atenção identificados:")

    if resultado["rotas"]:
        linhas.append("")
        linhas.append("Rotas:")

        for rota in resultado["rotas"]:
            linhas.append(
                f"- {rota['rota']}: nível {rota['nivel']}, "
                f"índice de ocorrência de "
                f"{rota['indice_ocorrencia']:.2f}% e "
                f"perdas de "
                f"{formatar_moeda(rota['valor_perdas'])}."
            )
    else:
        linhas.append("- Nenhuma anomalia identificada nas rotas.")

    if resultado["transportadoras"]:
        linhas.append("")
        linhas.append("Transportadoras:")

        for transportadora in resultado["transportadoras"]:
            linhas.append(
                f"- {transportadora['transportadora']}: "
                f"nível {transportadora['nivel']}, "
                f"{transportadora['ocorrencias']} ocorrências e "
                f"perdas de "
                f"{formatar_moeda(transportadora['valor_perdas'])}."
            )
    else:
        linhas.append(
            "- Nenhuma anomalia identificada nas transportadoras."
        )

    linhas.append("")

    linhas.append(
        "Observação: uma anomalia representa um comportamento "
        "que merece análise e não significa, isoladamente, "
        "fraude ou irregularidade."
    )

    return "\n".join(linhas)


def formatar_resposta(resultado):
    if isinstance(resultado, str):
        return resultado

    if not isinstance(resultado, (dict, list)):
        return str(resultado)

    if isinstance(resultado, dict):

        if "total_ocorrencias" in resultado:
            return formatar_perdas(resultado)

        if "rotas" in resultado and "transportadoras" in resultado:
            return formatar_anomalias(resultado)

        return str(resultado)

    if isinstance(resultado, list):

        if not resultado:
            return "Nenhum resultado foi encontrado."

        primeiro = resultado[0]

        if "risco" in primeiro:
            return formatar_riscos(resultado)

        if "indice_ocorrencia" in primeiro:

            if "transportadora" in primeiro:
                return formatar_transportadoras(resultado)

            if "rota" in primeiro:
                return formatar_rotas(resultado)

        return str(resultado)

    return str(resultado)


def executar_agente(pergunta):
    interpretacao = interpretar_pergunta(pergunta)

    intencao = interpretacao["intencao"]
    entidade = interpretacao["entidade"]

    # ==========================================================
    # RELATÓRIO
    # ==========================================================

    if intencao == "relatorio":
        return gerar_relatorio()

    # ==========================================================
    # ANÁLISE DE ANOMALIAS
    # ==========================================================

    if intencao == "analisar_anomalias":
        return analisar_anomalias()

    # ==========================================================
    # PRIORIZAÇÃO DE TRANSPORTADORAS
    # ==========================================================

    if intencao == "priorizar" and entidade == "transportadora":
        return analisar_transportadoras()

    # ==========================================================
    # ANÁLISE DE TRANSPORTADORAS
    # ==========================================================

    if intencao == "analisar" and entidade == "transportadora":
        return analisar_transportadoras()

    # ==========================================================
    # PRIORIZAÇÃO DE ROTAS
    # ==========================================================

    if intencao == "priorizar" and entidade == "rota":
        return priorizar_riscos()

    # ==========================================================
    # ANÁLISE DE ROTAS
    # ==========================================================

    if intencao == "analisar" and entidade == "rota":
        return analisar_rotas()

    # ==========================================================
    # PRIORIZAÇÃO GERAL
    # ==========================================================

    if intencao == "priorizar":
        return priorizar_riscos()

    # ==========================================================
    # ANÁLISE DE PERDAS
    # ==========================================================

    if intencao == "analisar" and entidade == "perdas":
        return analisar_perdas()

    # ==========================================================
    # PERGUNTA NÃO IDENTIFICADA
    # ==========================================================

    return None


if __name__ == "__main__":
    print("=== AGENTE DE PREVENÇÃO DE PERDAS ===")
    print()
    print("Digite uma pergunta para o agente.")
    print("Digite 'sair' para encerrar.")
    print()

    while True:
        pergunta = input("Você: ")

        if pergunta.lower().strip() == "sair":
            print("Agente encerrado.")
            break

        resultado = executar_agente(pergunta)

        print()

        if resultado is None:
            print(
                "Agente: Não consegui identificar qual análise "
                "devo executar."
            )
            print(
                "Tente perguntar sobre perdas, rotas, riscos, "
                "transportadoras, anomalias ou relatório."
            )
        else:
            print("Agente: Análise executada com sucesso.")
            print()
            print(formatar_resposta(resultado))

        print()

