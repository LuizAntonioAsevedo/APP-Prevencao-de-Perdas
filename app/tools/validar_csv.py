from app.tools.ler_csv import ler_csv


# ==========================================================
# COLUNAS OBRIGATÓRIAS
# ==========================================================

COLUNAS_OCORRENCIAS = {
    "id_ocorrencia",
    "id_remessa",
    "data",
    "tipo_ocorrencia",
    "rota",
    "transportadora",
    "valor_perda",
    "status",
    "descricao",
}


# ==========================================================
# VALIDAÇÃO DO CSV
# ==========================================================

def validar_csv(caminho_arquivo, colunas_obrigatorias):
    """
    Valida a estrutura e alguns conteúdos básicos de um arquivo CSV.

    Verifica:
    - se o arquivo pode ser lido;
    - se possui registros;
    - se possui todas as colunas obrigatórias;
    - se existem valores vazios nas colunas obrigatórias;
    - se o campo valor_perda possui valor numérico válido.

    Retorna um dicionário com o resultado da validação.
    """

    dados = ler_csv(caminho_arquivo)

    if not dados:
        return {
            "valido": False,
            "mensagem": "O arquivo CSV está vazio.",
            "erros": [
                "Nenhum registro foi encontrado."
            ],
        }

    colunas_encontradas = set(dados[0].keys())

    colunas_faltantes = (
        set(colunas_obrigatorias) - colunas_encontradas
    )

    if colunas_faltantes:
        return {
            "valido": False,
            "mensagem": "O CSV não possui todas as colunas obrigatórias.",
            "erros": [
                f"Colunas faltantes: {', '.join(sorted(colunas_faltantes))}"
            ],
        }

    erros = []

    for numero_linha, registro in enumerate(dados, start=2):

        # --------------------------------------------------
        # VERIFICA CAMPOS OBRIGATÓRIOS
        # --------------------------------------------------

        for coluna in colunas_obrigatorias:

            valor = registro.get(coluna)

            if valor is None or str(valor).strip() == "":
                erros.append(
                    f"Linha {numero_linha}: "
                    f"coluna '{coluna}' está vazia."
                )

        # --------------------------------------------------
        # VALIDA VALOR DA PERDA
        # --------------------------------------------------

        valor_perda = registro.get("valor_perda")

        if valor_perda is not None and str(valor_perda).strip() != "":
            try:
                float(valor_perda)
            except ValueError:
                erros.append(
                    f"Linha {numero_linha}: "
                    f"valor_perda '{valor_perda}' não é numérico."
                )

    if erros:
        return {
            "valido": False,
            "mensagem": "O CSV possui dados inválidos.",
            "erros": erros,
        }

    return {
        "valido": True,
        "mensagem": "CSV validado com sucesso.",
        "erros": [],
        "quantidade_registros": len(dados),
    }


# ==========================================================
# TESTE
# ==========================================================

if __name__ == "__main__":

    caminho = "dados/teste_externo.csv"

    resultado = validar_csv(
        caminho,
        COLUNAS_OCORRENCIAS,
    )

    print("=== VALIDAÇÃO DO CSV ===")
    print()

    print(f"Arquivo: {caminho}")
    print(f"Válido: {resultado['valido']}")
    print(f"Mensagem: {resultado['mensagem']}")

    if "quantidade_registros" in resultado:
        print(
            f"Registros encontrados: "
            f"{resultado['quantidade_registros']}"
        )

    if resultado["erros"]:
        print()
        print("Erros encontrados:")

        for erro in resultado["erros"]:
            print(f"- {erro}")