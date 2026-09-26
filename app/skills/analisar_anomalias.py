from collections import defaultdict

from app.tools.dados import obter_remessas, obter_ocorrencias


def carregar_remessas(registros=None):
    """
    Carrega as remessas.

    Quando registros são fornecidos, utiliza esses dados
    diretamente.

    Quando registros não são fornecidos, utiliza a Tool
    de dados como comportamento de compatibilidade.
    """

    if registros is None:
        registros = obter_remessas()

    remessas = []

    for registro in registros:
        remessas.append({
            "id_remessa": registro["id_remessa"],
            "data": registro["data"],
            "origem": registro["origem"],
            "destino": registro["destino"],
            "rota": registro["rota"],
            "transportadora": registro["transportadora"],
            "valor_mercadoria": registro["valor_mercadoria"],
            "status": registro["status"],
        })

    return remessas


def carregar_ocorrencias(registros=None):
    """
    Carrega as ocorrências.

    Quando registros são fornecidos, utiliza esses dados
    diretamente.

    Quando registros não são fornecidos, utiliza a Tool
    de dados como comportamento de compatibilidade.
    """

    if registros is None:
        registros = obter_ocorrencias()

    ocorrencias = []

    for registro in registros:
        ocorrencias.append({
            "id_ocorrencia": registro["id_ocorrencia"],
            "id_remessa": registro["id_remessa"],
            "data": registro["data"],
            "tipo_ocorrencia": registro["tipo_ocorrencia"],
            "rota": registro["rota"],
            "transportadora": registro["transportadora"],
            "valor_perda": registro["valor_perda"],
            "status": registro["status"],
            "descricao": registro["descricao"],
        })

    return ocorrencias


def analisar_anomalias(
    remessas=None,
    ocorrencias=None
):
    """
    Identifica pontos de atenção em rotas e transportadoras.

    Se os dados forem fornecidos, a Skill utiliza esses registros.

    Caso contrário, mantém o comportamento anterior utilizando
    as Tools de dados.
    """

    remessas = carregar_remessas(remessas)
    ocorrencias = carregar_ocorrencias(ocorrencias)

    remessas_por_rota = defaultdict(int)
    ocorrencias_por_rota = defaultdict(int)
    perdas_por_rota = defaultdict(float)

    ocorrencias_por_transportadora = defaultdict(int)
    perdas_por_transportadora = defaultdict(float)

    for remessa in remessas:
        remessas_por_rota[remessa["rota"]] += 1

    for ocorrencia in ocorrencias:
        rota = ocorrencia["rota"]
        transportadora = ocorrencia["transportadora"]
        valor = float(ocorrencia["valor_perda"])

        ocorrencias_por_rota[rota] += 1
        perdas_por_rota[rota] += valor

        ocorrencias_por_transportadora[transportadora] += 1
        perdas_por_transportadora[transportadora] += valor

    anomalias_rotas = []

    for rota in sorted(remessas_por_rota):
        total_remessas = remessas_por_rota[rota]
        total_ocorrencias = ocorrencias_por_rota[rota]
        valor_perdas = perdas_por_rota[rota]

        indice = (
            total_ocorrencias / total_remessas
        ) * 100

        if indice >= 75 or valor_perdas >= 8000:
            anomalias_rotas.append({
                "rota": rota,
                "indice_ocorrencia": indice,
                "valor_perdas": valor_perdas,
                "nivel": "ALTO"
            })

        elif indice >= 50 or valor_perdas >= 5000:
            anomalias_rotas.append({
                "rota": rota,
                "indice_ocorrencia": indice,
                "valor_perdas": valor_perdas,
                "nivel": "MÉDIO"
            })

    anomalias_transportadoras = []

    for transportadora in sorted(ocorrencias_por_transportadora):
        total_ocorrencias = ocorrencias_por_transportadora[
            transportadora
        ]
        valor_perdas = perdas_por_transportadora[transportadora]

        if total_ocorrencias >= 10 or valor_perdas >= 15000:
            anomalias_transportadoras.append({
                "transportadora": transportadora,
                "ocorrencias": total_ocorrencias,
                "valor_perdas": valor_perdas,
                "nivel": "ALTO"
            })

        elif total_ocorrencias >= 8 or valor_perdas >= 12000:
            anomalias_transportadoras.append({
                "transportadora": transportadora,
                "ocorrencias": total_ocorrencias,
                "valor_perdas": valor_perdas,
                "nivel": "MÉDIO"
            })

    return {
        "rotas": anomalias_rotas,
        "transportadoras": anomalias_transportadoras
    }


if __name__ == "__main__":
    resultado = analisar_anomalias()

    print("=== SKILL: ANALISAR ANOMALIAS ===")
    print()

    print("Pontos de atenção em rotas:")

    if resultado["rotas"]:
        for rota in resultado["rotas"]:
            print(
                f"- {rota['rota']} "
                f"| Nível: {rota['nivel']}"
            )
            print(
                f"  Índice de ocorrência: "
                f"{rota['indice_ocorrencia']:.2f}%"
            )
            print(
                f"  Valor das perdas: "
                f"R$ {rota['valor_perdas']:,.2f}"
            )

    else:
        print("- Nenhuma anomalia identificada.")

    print()
    print("Pontos de atenção em transportadoras:")

    if resultado["transportadoras"]:
        for transportadora in resultado["transportadoras"]:
            print(
                f"- {transportadora['transportadora']} "
                f"| Nível: {transportadora['nivel']}"
            )
            print(
                f"  Ocorrências: "
                f"{transportadora['ocorrencias']}"
            )
            print(
                f"  Valor das perdas: "
                f"R$ {transportadora['valor_perdas']:,.2f}"
            )

    else:
        print("- Nenhuma anomalia identificada.")