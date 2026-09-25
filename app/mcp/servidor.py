from mcp.server import MCPServer

from app.tools.dados import (
    obter_ocorrencias,
    obter_remessas,
    obter_rotas,
    obter_transportadoras,
)


mcp = MCPServer("Agente Prevencao de Perdas")


@mcp.tool()
def testar_mcp() -> str:
    """
    Ferramenta simples para validar o funcionamento do MCP Server.
    """
    return "MCP do Agente de Prevencao de Perdas funcionando!"


@mcp.tool()
def consultar_ocorrencias() -> list[dict]:
    """
    Consulta as ocorrências de prevenção de perdas
    armazenadas no banco SQLite.
    """
    return obter_ocorrencias()


@mcp.tool()
def consultar_remessas() -> list[dict]:
    """
    Consulta as remessas armazenadas no banco SQLite.
    """
    return obter_remessas()


@mcp.tool()
def consultar_rotas() -> list[dict]:
    """
    Consulta as rotas armazenadas no banco SQLite.
    """
    return obter_rotas()


@mcp.tool()
def consultar_transportadoras() -> list[dict]:
    """
    Consulta as transportadoras armazenadas no banco SQLite.
    """
    return obter_transportadoras()


if __name__ == "__main__":
    mcp.run()