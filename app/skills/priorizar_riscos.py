from collections import defaultdict

from app.tools.dados import obter_remessas, obter_ocorrencias


def carregar_remessas():
    registros = obter_remessas()

    remessas = []

    for registro in registros:
        remessas.append({
            "id_remessa": registro[0],
            "data": registro[1],
            "origem": registro[2],
            "destino": registro[3],
            "rota": registro[4],
            "transportadora": registro[5],
            "valor_mercadoria": registro[6],
            "status": registro[7],
        })

    return remessas


def carregar_ocorrencias():
    registros = obter_ocorrencias()

    ocorrencias = []

    for registro in registros:
        ocorrencias.append({
            "id_ocorrencia": registro[0],
            "id_remessa": registro[1],
            "data": registro[2],
            "tipo_ocorrencia": registro[3],
            "rota": registro[4],
            "transportadora": registro[5],
            "valor_perda": registro[6],
            "status": registro[7],
            "descricao": registro[8],
        })

    return ocorrencias


def classificar_risco(indice_ocorrencia, valor_perdas):
    """
    Classifica o risco considerando dois fatores:
    - frequência das ocorrências
    - impacto financeiro das perdas
    """

    frequencia_alta = indice_ocorrencia >= 75
    frequencia_media = indice_ocorrencia >= 50

    impacto_alto = valor_perdas >= 8000
    impacto_medio = valor_perdas >= 5000

    if frequencia_alta and impacto_alto:
        return "CRÍTICO"

    if frequencia_alta or impacto_alto:
        return "ALTO"

    if frequencia_media or impacto_medio:
        return "MÉDIO"

    return "BAIXO"


def priorizar_riscos():
    remessas = carregar_remessas()
    ocorrencias = carregar_ocorrencias()

    remessas_por_rota = defaultdict(int)
    ocorrencias_por_rota = defaultdict(int)
    perdas_por_rota = defaultdict(float)

    for remessa in remessas:
        rota = remessa["rota"]
        remessas_por_rota[rota] += 1

    for ocorrencia in ocorrencias:
        rota = ocorrencia["rota"]

        ocorrencias_por_rota[rota] += 1
        perdas_por_rota[rota] += float(
            ocorrencia["valor_perda"]
        )

    resultados = []

    for rota in sorted(remessas_por_rota):
        total_remessas = remessas_por_rota[rota]
        total_ocorrencias = ocorrencias_por_rota[rota]
        valor_perdas = perdas_por_rota[rota]

        indice_ocorrencia = (
            total_ocorrencias / total_remessas
        ) * 100

        risco = classificar_risco(
            indice_ocorrencia,
            valor_perdas
        )

        resultados.append({
            "rota": rota,
            "remessas": total_remessas,
            "ocorrencias": total_ocorrencias,
            "indice_ocorrencia": indice_ocorrencia,
            "valor_perdas": valor_perdas,
            "risco": risco
        })

    ordem_risco = {
        "CRÍTICO": 1,
        "ALTO": 2,
        "MÉDIO": 3,
        "BAIXO": 4
    }

    resultados.sort(
        key=lambda item: (
            ordem_risco[item["risco"]],
            -item["valor_perdas"],
            -item["indice_ocorrencia"]
        )
    )

    return resultados


if __name__ == "__main__":
    resultados = priorizar_riscos()

    print("=== SKILL: PRIORIZAR RISCOS ===")
    print()

    for resultado in resultados:
        print(f"Rota: {resultado['rota']}")
        print(f"  Risco: {resultado['risco']}")
        print(
            f"  Índice de ocorrência: "
            f"{resultado['indice_ocorrencia']:.2f}%"
        )
        print(
            f"  Valor das perdas: "
            f"R$ {resultado['valor_perdas']:,.2f}"
        )
        print(
            f"  Ocorrências: "
            f"{resultado['ocorrencias']}"
        )
        print()