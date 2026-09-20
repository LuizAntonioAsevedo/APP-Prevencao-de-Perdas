from app.database.conexao import conectar


# ==========================================================
# VALIDAÇÃO DO BANCO DE DADOS
# ==========================================================

def validar_banco():
    """
    Consulta as principais informações do banco SQLite
    e compara com os valores esperados.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    # ======================================================
    # CONTAGEM DOS REGISTROS
    # ======================================================

    cursor.execute("SELECT COUNT(*) FROM remessas")
    total_remessas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ocorrencias")
    total_ocorrencias = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM rotas")
    total_rotas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transportadoras")
    total_transportadoras = cursor.fetchone()[0]

    # ======================================================
    # VALOR TOTAL DAS PERDAS
    # ======================================================

    cursor.execute("""
        SELECT COALESCE(SUM(valor_perda), 0)
        FROM ocorrencias
    """)

    total_perdas = cursor.fetchone()[0]

    conexao.close()

    # ======================================================
    # RESULTADO
    # ======================================================

    print("=" * 50)
    print("VALIDAÇÃO DO BANCO SQLITE")
    print("=" * 50)

    print(f"Remessas:          {total_remessas}")
    print(f"Ocorrências:       {total_ocorrencias}")
    print(f"Rotas:             {total_rotas}")
    print(f"Transportadoras:   {total_transportadoras}")
    print(f"Valor das perdas:  R$ {total_perdas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    print("=" * 50)

    # ======================================================
    # VALIDAÇÃO DOS RESULTADOS ESPERADOS
    # ======================================================

    banco_valido = (
        total_remessas == 30
        and total_ocorrencias == 18
        and total_rotas == 4
        and total_transportadoras == 2
        and total_perdas == 28360
    )

    if banco_valido:
        print("VALIDAÇÃO: OK")
        print("O banco SQLite contém os dados esperados.")
    else:
        print("VALIDAÇÃO: ATENÇÃO")
        print("Os dados encontrados não correspondem aos valores esperados.")


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    validar_banco()