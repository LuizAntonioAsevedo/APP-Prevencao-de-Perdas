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


def analisar_rotas():
    """
    Analisa as rotas utilizando os dados fornecidos pela Tool.
    """

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

        resultados.append({
            "rota": rota,
            "remessas": total_remessas,
            "ocorrencias": total_ocorrencias,
            "indice_ocorrencia": indice_ocorrencia,
            "valor_perdas": valor_perdas
        })

    return resultados


if __name__ == "__main__":
    resultados = analisar_rotas()

    print("=== SKILL: ANALISAR ROTAS ===")
    print()

    for resultado in resultados:
        print(f"Rota: {resultado['rota']}")
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
        print()