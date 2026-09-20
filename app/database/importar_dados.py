import csv
from pathlib import Path

from app.database.conexao import conectar


# ==========================================================
# CAMINHO DOS ARQUIVOS CSV
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

CAMINHO_DADOS = BASE_DIR / "dados"


# ==========================================================
# FUNÇÕES DE IMPORTAÇÃO
# ==========================================================

def importar_remessas(cursor):
    caminho = CAMINHO_DADOS / "remessas.csv"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            cursor.execute("""
                INSERT OR IGNORE INTO remessas (
                    id_remessa,
                    data,
                    origem,
                    destino,
                    rota,
                    transportadora,
                    valor_mercadoria,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                linha["id_remessa"],
                linha["data"],
                linha["origem"],
                linha["destino"],
                linha["rota"],
                linha["transportadora"],
                float(linha["valor_mercadoria"]),
                linha["status"]
            ))


def importar_ocorrencias(cursor):
    caminho = CAMINHO_DADOS / "ocorrencias.csv"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            cursor.execute("""
                INSERT OR IGNORE INTO ocorrencias (
                    id_ocorrencia,
                    id_remessa,
                    data,
                    tipo_ocorrencia,
                    rota,
                    transportadora,
                    valor_perda,
                    status,
                    descricao
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                linha["id_ocorrencia"],
                linha["id_remessa"],
                linha["data"],
                linha["tipo_ocorrencia"],
                linha["rota"],
                linha["transportadora"],
                float(linha["valor_perda"]),
                linha["status"],
                linha["descricao"]
            ))


def importar_rotas(cursor):
    caminho = CAMINHO_DADOS / "rotas.csv"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            cursor.execute("""
                INSERT OR IGNORE INTO rotas (
                    id_rota,
                    origem,
                    destino,
                    distancia_km,
                    regiao
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                linha["id_rota"],
                linha["origem"],
                linha["destino"],
                float(linha["distancia_km"]),
                linha["regiao"]
            ))


def importar_transportadoras(cursor):
    caminho = CAMINHO_DADOS / "transportadoras.csv"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            cursor.execute("""
                INSERT OR IGNORE INTO transportadoras (
                    id_transportadora,
                    nome,
                    tipo_operacao,
                    regiao
                )
                VALUES (?, ?, ?, ?)
            """, (
                linha["id_transportadora"],
                linha["nome"],
                linha["tipo_operacao"],
                linha["regiao"]
            ))


# ==========================================================
# IMPORTAÇÃO COMPLETA
# ==========================================================

def importar_dados():
    """
    Importa todos os dados dos arquivos CSV para o SQLite.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    importar_remessas(cursor)
    importar_ocorrencias(cursor)
    importar_rotas(cursor)
    importar_transportadoras(cursor)

    conexao.commit()
    conexao.close()

    print("Dados importados com sucesso!")


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    importar_dados()