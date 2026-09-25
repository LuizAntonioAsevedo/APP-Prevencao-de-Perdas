import asyncio

from mcp import Client, StdioServerParameters


async def main():
    servidor = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.servidor"],
    )

    async with Client(servidor) as cliente:

        resultado = await cliente.list_tools()

        print("\nFerramentas disponíveis:")

        for ferramenta in resultado.tools:
            print(f"- {ferramenta.name}")

        print("\n=== TESTANDO OCORRÊNCIAS ===")

        ocorrencias = await cliente.call_tool(
            "consultar_ocorrencias",
            {},
        )

        print(f"Erro: {ocorrencias.is_error}")
        print(f"Quantidade de ocorrências: {len(ocorrencias.structured_content['result'])}")

        print("\n=== TESTANDO REMESSAS ===")

        remessas = await cliente.call_tool(
            "consultar_remessas",
            {},
        )

        print(f"Erro: {remessas.is_error}")
        print(f"Quantidade de remessas: {len(remessas.structured_content['result'])}")

        print("\n=== TESTANDO ROTAS ===")

        rotas = await cliente.call_tool(
            "consultar_rotas",
            {},
        )

        print(f"Erro: {rotas.is_error}")
        print(f"Quantidade de rotas: {len(rotas.structured_content['result'])}")

        print("\n=== TESTANDO TRANSPORTADORAS ===")

        transportadoras = await cliente.call_tool(
            "consultar_transportadoras",
            {},
        )

        print(f"Erro: {transportadoras.is_error}")
        print(
            f"Quantidade de transportadoras: "
            f"{len(transportadoras.structured_content['result'])}"
        )

        print("\n=== TESTE CONCLUÍDO ===")


if __name__ == "__main__":
    asyncio.run(main())