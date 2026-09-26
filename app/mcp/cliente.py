import asyncio

from mcp import Client, StdioServerParameters


async def consultar_dados_mcp_async():
    """
    Conecta ao MCP Server e consulta os principais
    conjuntos de dados disponíveis.

    Retorna um dicionário com os dados obtidos
    através das ferramentas MCP.
    """

    servidor = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.servidor"],
    )

    async with Client(servidor) as cliente:

        ocorrencias = await cliente.call_tool(
            "consultar_ocorrencias",
            {},
        )

        remessas = await cliente.call_tool(
            "consultar_remessas",
            {},
        )

        rotas = await cliente.call_tool(
            "consultar_rotas",
            {},
        )

        transportadoras = await cliente.call_tool(
            "consultar_transportadoras",
            {},
        )

        return {
            "ocorrencias": ocorrencias.structured_content["result"],
            "remessas": remessas.structured_content["result"],
            "rotas": rotas.structured_content["result"],
            "transportadoras": transportadoras.structured_content["result"],
        }


def consultar_dados_mcp():
    """
    Executa a consulta assíncrona do MCP de forma
    síncrona para facilitar o uso pelo restante
    da aplicação.
    """

    return asyncio.run(
        consultar_dados_mcp_async()
    )


if __name__ == "__main__":

    print("=== CLIENTE MCP V5.6 ===")
    print()

    dados = consultar_dados_mcp()

    print(
        f"Ocorrências: "
        f"{len(dados['ocorrencias'])}"
    )

    print(
        f"Remessas: "
        f"{len(dados['remessas'])}"
    )

    print(
        f"Rotas: "
        f"{len(dados['rotas'])}"
    )

    print(
        f"Transportadoras: "
        f"{len(dados['transportadoras'])}"
    )

    print()
    print("=== CONSULTA MCP CONCLUÍDA ===")