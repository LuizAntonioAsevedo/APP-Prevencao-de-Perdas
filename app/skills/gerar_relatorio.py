from datetime import datetime

from .analisar_perdas import analisar_perdas
from .analisar_rotas import analisar_rotas
from .analisar_transportadoras import analisar_transportadoras
from .analisar_anomalias import analisar_anomalias
from .priorizar_riscos import priorizar_riscos


def formatar_moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def gerar_relatorio():
    perdas = analisar_perdas()
    rotas = analisar_rotas()
    transportadoras = analisar_transportadoras()
    anomalias = analisar_anomalias()
    riscos = priorizar_riscos()

    linhas = []

    linhas.append("=" * 60)
    linhas.append("RELATÓRIO DE PREVENÇÃO DE PERDAS")
    linhas.append("=" * 60)
    linhas.append("")

    linhas.append(
        f"Data de geração: "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    linhas.append("")

    linhas.append("1. RESUMO EXECUTIVO")
    linhas.append("-" * 60)

    linhas.append(
        f"Total de ocorrências: {perdas['total_ocorrencias']}"
    )

    linhas.append(
        f"Valor total registrado em perdas: "
        f"{formatar_moeda(perdas['valor_total'])}"
    )

    linhas.append(
        f"Ocorrências em investigação: "
        f"{perdas['ocorrencias_em_investigacao']}"
    )

    linhas.append(
        f"Tipo de ocorrência mais frequente: "
        f"{perdas['tipo_mais_frequente'][0]} "
        f"({perdas['tipo_mais_frequente'][1]} ocorrências)"
    )

    linhas.append(
        f"Tipo com maior impacto financeiro: "
        f"{perdas['tipo_maior_perda'][0]} "
        f"({formatar_moeda(perdas['tipo_maior_perda'][1])})"
    )

    linhas.append("")

    linhas.append("2. ROTAS PRIORITÁRIAS")
    linhas.append("-" * 60)

    for risco in riscos:
        linhas.append(
            f"{risco['rota']} | "
            f"Risco: {risco['risco']} | "
            f"Índice: {risco['indice_ocorrencia']:.2f}% | "
            f"Perdas: {formatar_moeda(risco['valor_perdas'])}"
        )

    linhas.append("")

    linhas.append("3. PONTOS DE ATENÇÃO")
    linhas.append("-" * 60)

    for rota in anomalias["rotas"]:
        linhas.append(
            f"Rota {rota['rota']}: nível {rota['nivel']}, "
            f"índice de ocorrência de "
            f"{rota['indice_ocorrencia']:.2f}% e "
            f"{formatar_moeda(rota['valor_perdas'])} "
            f"em perdas registradas."
        )

    for transportadora in anomalias["transportadoras"]:
        linhas.append(
            f"Transportadora {transportadora['transportadora']}: "
            f"nível {transportadora['nivel']}, "
            f"{transportadora['ocorrencias']} ocorrências e "
            f"{formatar_moeda(transportadora['valor_perdas'])} "
            f"em perdas registradas."
        )

    linhas.append("")

    linhas.append("4. ANÁLISE DAS TRANSPORTADORAS")
    linhas.append("-" * 60)

    for transportadora in transportadoras:
        linhas.append(
            f"{transportadora['transportadora']} | "
            f"Ocorrências: {transportadora['ocorrencias']} | "
            f"Índice: {transportadora['indice_ocorrencia']:.2f}% | "
            f"Perdas: {formatar_moeda(transportadora['valor_perdas'])} | "
            f"Média/ocorrência: "
            f"{formatar_moeda(transportadora['valor_medio_perda'])}"
        )

    linhas.append("")

    linhas.append("5. RECOMENDAÇÕES")
    linhas.append("-" * 60)

    if riscos:
        principal = riscos[0]

        linhas.append(
            f"- Priorizar a investigação da rota {principal['rota']}, "
            f"classificada como risco {principal['risco']}."
        )

    linhas.append(
        "- Avaliar as ocorrências de maior impacto financeiro "
        "e verificar suas causas operacionais."
    )

    linhas.append(
        "- Aprofundar a análise das rotas com elevada frequência "
        "de ocorrências."
    )

    linhas.append(
        "- Verificar possíveis padrões recorrentes por rota, "
        "transportadora e tipo de ocorrência."
    )

    linhas.append(
        "- Validar os resultados com a equipe responsável antes "
        "de qualquer decisão operacional."
    )

    linhas.append("")

    linhas.append("6. OBSERVAÇÃO DE CONTROLE")
    linhas.append("-" * 60)

    linhas.append(
        "Os indicadores apresentados identificam pontos de atenção "
        "e possíveis anomalias. Eles não constituem, isoladamente, "
        "evidência de fraude ou irregularidade."
    )

    linhas.append(
        "Decisões críticas devem ser submetidas à validação humana "
        "e à investigação dos registros operacionais."
    )

    linhas.append("")

    linhas.append("=" * 60)

    return "\n".join(linhas)


if __name__ == "__main__":
    relatorio = gerar_relatorio()

    print(relatorio)