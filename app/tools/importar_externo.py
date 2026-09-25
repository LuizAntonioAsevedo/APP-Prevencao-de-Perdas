from app.database.conexao import conectar

from app.tools.ler_csv import ler_csv
from app.tools.validar_csv import (
    validar_csv,
    COLUNAS_OCORRENCIAS,
)
from app.tools.normalizar_dados import normalizar_ocorrencias


# ==========================================================
# IMPORTAÇÃO DE OCORRÊNCIAS EXTERNAS
# ==========================================================

def importar_ocorrencias_externas(caminho_arquivo):
    """
    Lê, valida, normaliza e importa ocorrências
    de um arquivo CSV externo para o SQLite.

    Retorna a quantidade de registros processados.
    """

    # ------------------------------------------------------
    # 1. LEITURA
    # ------------------------------------------------------

    dados = ler_csv(caminho_arquivo)

    # ------------------------------------------------------
    # 2. VALIDAÇÃO
    # ------------------------------------------------------

    resultado_validacao = validar_csv(
        caminho_arquivo,
        COLUNAS_OCORRENCIAS,
    )

    if not resultado_validacao["valido"]:
        raise ValueError(
            "CSV inválido: "
            + " | ".join(resultado_validacao["erros"])
        )

    # ------------------------------------------------------
    # 3. NORMALIZAÇÃO
    # ------------------------------------------------------

    dados_normalizados = normalizar_ocorrencias(
        dados
    )

    # ------------------------------------------------------
    # 4. CONEXÃO COM O BANCO
    # ------------------------------------------------------

    conexao = conectar()
    cursor = conexao.cursor()

    # ------------------------------------------------------
    # 5. IMPORTAÇÃO
    # ------------------------------------------------------

    registros_importados = 0

    for registro in dados_normalizados:

        cursor.execute(
            """
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
            """,
            (
                registro["id_ocorrencia"],
                registro["id_remessa"],
                registro["data"],
                registro["tipo_ocorrencia"],
                registro["rota"],
                registro["transportadora"],
                registro["valor_perda"],
                registro["status"],
                registro["descricao"],
            ),
        )

        if cursor.rowcount > 0:
            registros_importados += 1

    # ------------------------------------------------------
    # 6. CONFIRMAÇÃO
    # ------------------------------------------------------

    conexao.commit()
    conexao.close()

    return registros_importados


# ==========================================================
# TESTE
# ==========================================================

if __name__ == "__main__":

    caminho = "dados/teste_externo.csv"

    print("=== IMPORTAÇÃO DE DADOS EXTERNOS ===")
    print()

    quantidade = importar_ocorrencias_externas(
        caminho
    )

    print(
        f"Registros importados: {quantidade}"
    )

    print()
    print("=== IMPORTAÇÃO CONCLUÍDA ===")