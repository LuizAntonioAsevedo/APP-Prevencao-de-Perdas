
import sqlite3
from pathlib import Path


# ==========================================================
# CAMINHO DO BANCO DE DADOS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

CAMINHO_BANCO = BASE_DIR / "dados" / "prevencao_perdas.db"


# ==========================================================
# CONEXÃO COM O BANCO
# ==========================================================

def conectar():
    """
    Cria e retorna uma conexão com o banco SQLite.
    """

    conexao = sqlite3.connect(CAMINHO_BANCO)

    return conexao

