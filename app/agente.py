from app.interpretador import interpretar_pergunta
from app.mcp.cliente import consultar_dados_mcp

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
        linhas.append(
            f"- {tipo}: {quantidade}"
        )

    linhas.append("")
    linhas.append("Impacto financeiro por tipo:")

    for tipo, valor in resultado["perdas_por_tipo"].items():
        linhas.append(
            f"- {tipo}: {formatar_moeda(valor)}"
        )

    linhas.append("")

    tipo_frequente = resultado["tipo_mais_frequente"]

    linhas.append(
        f"Tipo mais frequente: "
        f"{tipo_frequente[0]} "
        f"({tipo_frequente[1]} ocorrências)."
    )

    tipo_maior_perda = resultado["tipo_maior_perda"]

    linhas.append(
        f"Maior impacto financeiro: "
        f"{tipo_maior_perda[0]} "
        f"({formatar_moeda(tipo_maior_perda[1])})."
    )

    linhas.append("")

    linhas.append(
        "Observação: os indicadores identificam pontos de atenção "
        "e não constituem, isoladamente, evidência de fraude."
    )

    return "\n".join(linhas)


def formatar_rotas(resultado):
    linhas = [
        "ANÁLISE DAS ROTAS",
        ""
    ]

    for rota in resultado:
        linhas.append(
            f"Rota {rota['rota']}: "
            f"{rota['ocorrencias']} ocorrências "
            f"em {rota['remessas']} remessas."
        )

        linhas.append(
            f"Índice de ocorrência: "
            f"{rota['indice_ocorrencia']:.2f}%."
        )

        linhas.append(
            f"Perdas registradas: "
            f"{formatar_moeda(rota['valor_perdas'])}."
        )

        linhas.append("")

    return "\n".join(linhas).strip()


def formatar_riscos(resultado):
    linhas = []

    riscos_criticos = [
        item
        for item in resultado
        if item["risco"] == "CRÍTICO"
    ]

    riscos_altos = [
        item
        for item in resultado
        if item["risco"] == "ALTO"
    ]

    linhas.append("PRIORIZAÇÃO DE RISCOS")
    linhas.append("")

    linhas.append(
        f"Total de rotas analisadas: {len(resultado)}."
    )

    linhas.append(
        f"Rotas classificadas como risco CRÍTICO: "
        f"{len(riscos_criticos)}."
    )

    linhas.append(
        f"Rotas classificadas como risco ALTO: "
        f"{len(riscos_altos)}."
    )

    linhas.append("")
    linhas.append("CLASSIFICAÇÃO DAS ROTAS")
    linhas.append("")

    for item in resultado:

        linhas.append(
            f"Rota: {item['rota']}"
        )

        linhas.append(
            f"Risco: {item['risco']}"
        )

        linhas.append(
            f"Índice de ocorrência: "
            f"{item['indice_ocorrencia']:.2f}%"
        )

        linhas.append(
            f"Ocorrências: {item['ocorrencias']}"
        )

        linhas.append(
            f"Perdas registradas: "
            f"{formatar_moeda(item['valor_perdas'])}"
        )

        linhas.append("")

    if resultado:

        principal = resultado[0]

        linhas.append("PONTO DE ATENÇÃO")
        linhas.append("")

        linhas.append(
            f"A rota {principal['rota']} "
            f"foi classificada como risco "
            f"{principal['risco']}."
        )

        linhas.append(
            f"Índice de ocorrência: "
            f"{principal['indice_ocorrencia']:.2f}%."
        )

        linhas.append(
            f"Perdas registradas: "
            f"{formatar_moeda(principal['valor_perdas'])}."
        )

        linhas.append("")

        linhas.append(
            "Essa classificação representa um ponto de atenção "
            "baseado nos indicadores analisados e não constitui, "
            "isoladamente, evidência de fraude ou irregularidade."
        )

        linhas.append(
            "Qualquer decisão operacional deve ser validada "
            "pela equipe responsável."
        )

    return "\n".join(linhas)


def formatar_transportadoras(resultado):
    linhas = [
        "ANÁLISE DAS TRANSPORTADORAS",
        ""
    ]

    for transportadora in resultado:

        linhas.append(
            f"Transportadora: "
            f"{transportadora['transportadora']}"
        )

        linhas.append(
            f"Ocorrências: "
            f"{transportadora['ocorrencias']} "
            f"em {transportadora['remessas']} remessas."
        )

        linhas.append(
            f"Índice de ocorrência: "
            f"{transportadora['indice_ocorrencia']:.2f}%."
        )

        linhas.append(
            f"Perdas registradas: "
            f"{formatar_moeda(transportadora['valor_perdas'])}."
        )

        linhas.append(
            f"Média por ocorrência: "
            f"{formatar_moeda(transportadora['valor_medio_perda'])}."
        )

        linhas.append("")

    return "\n".join(linhas).strip()


def formatar_anomalias(resultado):
    linhas = [
        "PONTOS DE ATENÇÃO IDENTIFICADOS"
    ]

    if resultado["rotas"]:

        linhas.append("")
        linhas.append("ROTAS")

        for rota in resultado["rotas"]:

            linhas.append(
                f"- {rota['rota']}: "
                f"nível {rota['nivel']}, "
                f"índice de ocorrência de "
                f"{rota['indice_ocorrencia']:.2f}% "
                f"e perdas de "
                f"{formatar_moeda(rota['valor_perdas'])}."
            )

    else:

        linhas.append(
            "- Nenhum ponto de atenção identificado nas rotas."
        )

    if resultado["transportadoras"]:

        linhas.append("")
        linhas.append("TRANSPORTADORAS")

        for transportadora in resultado["transportadoras"]:

            linhas.append(
                f"- {transportadora['transportadora']}: "
                f"nível {transportadora['nivel']}, "
                f"{transportadora['ocorrencias']} ocorrências "
                f"e perdas de "
                f"{formatar_moeda(transportadora['valor_perdas'])}."
            )

    else:

        linhas.append(
            "- Nenhum ponto de atenção identificado "
            "nas transportadoras."
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


def obter_dados_dashboard():
    dados = consultar_dados_mcp()

    remessas = dados["remessas"]
    ocorrencias = dados["ocorrencias"]

    perdas = analisar_perdas(ocorrencias)

    rotas = analisar_rotas(
        remessas,
        ocorrencias
    )

    transportadoras = analisar_transportadoras(
        remessas,
        ocorrencias
    )

    riscos = priorizar_riscos(
        remessas,
        ocorrencias
    )

    return {
        "perdas": perdas,
        "rotas": rotas,
        "transportadoras": transportadoras,
        "riscos": riscos
    }


def executar_agente(pergunta):

    interpretacao = interpretar_pergunta(pergunta)

    intencao = interpretacao["intencao"]
    entidade = interpretacao["entidade"]

    if intencao == "relatorio":
        return gerar_relatorio()

    # ==========================================================
    # V5.6 — CONSULTA DOS DADOS ATRAVÉS DO MCP
    # ==========================================================

    dados = consultar_dados_mcp()

    remessas = dados["remessas"]
    ocorrencias = dados["ocorrencias"]

    # ==========================================================
    # EXECUÇÃO DAS SKILLS UTILIZANDO OS DADOS DO MCP
    # ==========================================================

    if intencao == "analisar_anomalias":
        return analisar_anomalias(
            remessas,
            ocorrencias
        )

    if intencao == "priorizar" and entidade == "transportadora":
        return analisar_transportadoras(
            remessas,
            ocorrencias
        )

    if intencao == "analisar" and entidade == "transportadora":
        return analisar_transportadoras(
            remessas,
            ocorrencias
        )

    if intencao == "priorizar" and entidade == "rota":
        return priorizar_riscos(
            remessas,
            ocorrencias
        )

    if intencao == "analisar" and entidade == "rota":
        return analisar_rotas(
            remessas,
            ocorrencias
        )

    if intencao == "priorizar":
        return priorizar_riscos(
            remessas,
            ocorrencias
        )

    if intencao == "analisar" and entidade == "perdas":
        return analisar_perdas(
            ocorrencias
        )

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
                "Agente: Não consegui identificar "
                "qual análise devo executar."
            )

            print(
                "Tente perguntar sobre perdas, rotas, "
                "riscos, transportadoras, anomalias ou relatório."
            )

        else:

            print(
                "Agente: Análise executada com sucesso."
            )

            print()

            print(
                formatar_resposta(resultado)
            )

        print()