from app.database.conexao import conectar


# ==========================================================
# CONSULTAR REMESSAS
# ==========================================================

def consultar_remessas():
    """
    Retorna todas as remessas cadastradas no banco.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_remessa,
            data,
            origem,
            destino,
            rota,
            transportadora,
            valor_mercadoria,
            status
        FROM remessas
        ORDER BY id_remessa
    """)

    resultados = cursor.fetchall()

    conexao.close()

    return resultados


# ==========================================================
# CONSULTAR OCORRÊNCIAS
# ==========================================================

def consultar_ocorrencias():
    """
    Retorna todas as ocorrências cadastradas no banco.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_ocorrencia,
            id_remessa,
            data,
            tipo_ocorrencia,
            rota,
            transportadora,
            valor_perda,
            status,
            descricao
        FROM ocorrencias
        ORDER BY id_ocorrencia
    """)

    resultados = cursor.fetchall()

    conexao.close()

    return resultados


# ==========================================================
# CONSULTAR ROTAS
# ==========================================================

def consultar_rotas():
    """
    Retorna todas as rotas cadastradas no banco.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_rota,
            origem,
            destino,
            distancia_km,
            regiao
        FROM rotas
        ORDER BY id_rota
    """)

    resultados = cursor.fetchall()

    conexao.close()

    return resultados


# ==========================================================
# CONSULTAR TRANSPORTADORAS
# ==========================================================

def consultar_transportadoras():
    """
    Retorna todas as transportadoras cadastradas no banco.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_transportadora,
            nome,
            tipo_operacao,
            regiao
        FROM transportadoras
        ORDER BY id_transportadora
    """)

    resultados = cursor.fetchall()

    conexao.close()

    return resultados