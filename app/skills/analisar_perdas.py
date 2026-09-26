from collections import Counter

from app.tools.dados import obter_ocorrencias


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


def analisar_perdas(registros=None):
    """
    Analisa as perdas utilizando os dados fornecidos.

    Se registros forem fornecidos, a Skill utiliza esses dados.
    Caso contrário, mantém o comportamento anterior utilizando
    a Tool de dados.
    """

    ocorrencias = carregar_ocorrencias(registros)

    total_ocorrencias = len(ocorrencias)

    valor_total = sum(
        float(ocorrencia["valor_perda"])
        for ocorrencia in ocorrencias
    )

    ocorrencias_por_tipo = Counter(
        ocorrencia["tipo_ocorrencia"]
        for ocorrencia in ocorrencias
    )

    perdas_por_tipo = Counter()

    for ocorrencia in ocorrencias:
        tipo = ocorrencia["tipo_ocorrencia"]
        valor = float(ocorrencia["valor_perda"])

        perdas_por_tipo[tipo] += valor

    ocorrencias_em_investigacao = sum(
        1
        for ocorrencia in ocorrencias
        if ocorrencia["status"] == "EM_INVESTIGACAO"
    )

    tipo_mais_frequente = ocorrencias_por_tipo.most_common(1)[0]

    tipo_maior_perda = max(
        perdas_por_tipo.items(),
        key=lambda item: item[1]
    )

    return {
        "total_ocorrencias": total_ocorrencias,
        "valor_total": valor_total,
        "ocorrencias_por_tipo": ocorrencias_por_tipo,
        "perdas_por_tipo": perdas_por_tipo,
        "ocorrencias_em_investigacao": ocorrencias_em_investigacao,
        "tipo_mais_frequente": tipo_mais_frequente,
        "tipo_maior_perda": tipo_maior_perda,
    }


if __name__ == "__main__":
    resultado = analisar_perdas()

    print("=== SKILL: ANALISAR PERDAS ===")
    print()

    print(f"Total de ocorrências: {resultado['total_ocorrencias']}")
    print(
        f"Valor total das perdas: "
        f"R$ {resultado['valor_total']:,.2f}"
    )
    print(
        f"Ocorrências em investigação: "
        f"{resultado['ocorrencias_em_investigacao']}"
    )

    print()
    print("Ocorrências por tipo:")

    for tipo, quantidade in resultado["ocorrencias_por_tipo"].items():
        print(f"- {tipo}: {quantidade}")

    print()
    print("Valor das perdas por tipo:")

    for tipo, valor in resultado["perdas_por_tipo"].items():
        print(f"- {tipo}: R$ {valor:,.2f}")

    print()
    print(
        f"Tipo mais frequente: "
        f"{resultado['tipo_mais_frequente'][0]} "
        f"({resultado['tipo_mais_frequente'][1]} ocorrências)"
    )

    print(
        f"Tipo com maior valor de perda: "
        f"{resultado['tipo_maior_perda'][0]} "
        f"(R$ {resultado['tipo_maior_perda'][1]:,.2f})"
    )