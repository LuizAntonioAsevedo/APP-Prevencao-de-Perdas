import sqlite3

from app.database.conexao import conectar


# ==========================================================
# CRIAÇÃO DAS TABELAS
# ==========================================================

def criar_tabelas():
    """
    Cria as tabelas do banco de dados SQLite.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    # ======================================================
    # TABELA DE REMESSAS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS remessas (
            id_remessa TEXT PRIMARY KEY,
            data TEXT,
            origem TEXT,
            destino TEXT,
            rota TEXT,
            transportadora TEXT,
            valor_mercadoria REAL,
            status TEXT
        )
    """)

    # ======================================================
    # TABELA DE OCORRÊNCIAS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id_ocorrencia TEXT PRIMARY KEY,
            id_remessa TEXT,
            data TEXT,
            tipo_ocorrencia TEXT,
            rota TEXT,
            transportadora TEXT,
            valor_perda REAL,
            status TEXT,
            descricao TEXT,
            FOREIGN KEY (id_remessa)
                REFERENCES remessas (id_remessa)
        )
    """)

    # ======================================================
    # TABELA DE ROTAS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rotas (
            id_rota TEXT PRIMARY KEY,
            origem TEXT,
            destino TEXT,
            distancia_km REAL,
            regiao TEXT
        )
    """)

    # ======================================================
    # TABELA DE TRANSPORTADORAS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transportadoras (
            id_transportadora TEXT PRIMARY KEY,
            nome TEXT,
            tipo_operacao TEXT,
            regiao TEXT
        )
    """)

    # Salva as alterações
    conexao.commit()

    # Fecha a conexão
    conexao.close()

    print("Tabelas criadas com sucesso!")


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    criar_tabelas()