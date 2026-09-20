from app.database.consultas import (
    consultar_remessas,
    consultar_ocorrencias,
    consultar_rotas,
    consultar_transportadoras,
)


def obter_remessas():
    """
    Tool para consultar as remessas disponíveis no banco.
    """
    return consultar_remessas()


def obter_ocorrencias():
    """
    Tool para consultar as ocorrências disponíveis no banco.
    """
    return consultar_ocorrencias()


def obter_rotas():
    """
    Tool para consultar as rotas disponíveis no banco.
    """
    return consultar_rotas()


def obter_transportadoras():
    """
    Tool para consultar as transportadoras disponíveis no banco.
    """
    return consultar_transportadoras()


if __name__ == "__main__":
    print("=== TOOL: DADOS ===")
    print()

    remessas = obter_remessas()
    ocorrencias = obter_ocorrencias()
    rotas = obter_rotas()
    transportadoras = obter_transportadoras()

    print(f"Remessas disponíveis: {len(remessas)}")
    print(f"Ocorrências disponíveis: {len(ocorrencias)}")
    print(f"Rotas disponíveis: {len(rotas)}")
    print(f"Transportadoras disponíveis: {len(transportadoras)}")