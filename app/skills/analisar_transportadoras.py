from collections import defaultdict

from app.tools.dados import obter_remessas, obter_ocorrencias


def carregar_remessas():
    """
    Carrega as remessas utilizando a Tool de dados.
    """

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


def carregar_ocorrencias():
    """
    Carrega as ocorrências utilizando a Tool de dados.
    """

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


def analisar_transportadoras():
    """
    Analisa as transportadoras utilizando os dados fornecidos pela Tool.
    """

    remessas = carregar_remessas()
    ocorrencias = carregar_ocorrencias()

    remessas_por_transportadora = defaultdict(int)
    ocorrencias_por_transportadora = defaultdict(int)
    perdas_por_transportadora = defaultdict(float)

    for remessa in remessas:
        transportadora = remessa["transportadora"]
        remessas_por_transportadora[transportadora] += 1

    for ocorrencia in ocorrencias:
        transportadora = ocorrencia["transportadora"]

        ocorrencias_por_transportadora[transportadora] += 1

        perdas_por_transportadora[transportadora] += float(
            ocorrencia["valor_perda"]
        )

    resultados = []

    for transportadora in sorted(remessas_por_transportadora):
        total_remessas = remessas_por_transportadora[transportadora]
        total_ocorrencias = ocorrencias_por_transportadora[transportadora]
        valor_perdas = perdas_por_transportadora[transportadora]

        indice_ocorrencia = (
            total_ocorrencias / total_remessas
        ) * 100

        valor_medio_perda = (
            valor_perdas / total_ocorrencias
            if total_ocorrencias > 0
            else 0
        )

        resultados.append({
            "transportadora": transportadora,
            "remessas": total_remessas,
            "ocorrencias": total_ocorrencias,
            "indice_ocorrencia": indice_ocorrencia,
            "valor_perdas": valor_perdas,
            "valor_medio_perda": valor_medio_perda
        })

    return resultados


if __name__ == "__main__":
    resultados = analisar_transportadoras()

    print("=== SKILL: ANALISAR TRANSPORTADORAS ===")
    print()

    for resultado in resultados:
        print(f"Transportadora: {resultado['transportadora']}")
        print(f"  Remessas: {resultado['remessas']}")
        print(f"  Ocorrências: {resultado['ocorrencias']}")
        print(
            f"  Índice de ocorrência: "
            f"{resultado['indice_ocorrencia']:.2f}%"
        )
        print(
            f"  Valor das perdas: "
            f"R$ {resultado['valor_perdas']:,.2f}"
        )
        print(
            f"  Valor médio por ocorrência: "
            f"R$ {resultado['valor_medio_perda']:,.2f}"
        )
        print()