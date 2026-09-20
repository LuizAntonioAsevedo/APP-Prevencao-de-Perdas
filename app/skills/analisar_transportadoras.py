from collections import defaultdict

from app.database.consultas import consultar_remessas, consultar_ocorrencias


def carregar_remessas():
    """
    Carrega as remessas diretamente do banco SQLite.
    """

    registros = consultar_remessas()

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
    """
    Carrega as ocorrências diretamente do banco SQLite.
    """

    registros = consultar_ocorrencias()

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


def analisar_transportadoras():
    """
    Analisa as transportadoras utilizando os dados do SQLite.
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