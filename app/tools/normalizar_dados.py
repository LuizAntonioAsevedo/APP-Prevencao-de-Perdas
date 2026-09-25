from app.tools.ler_csv import ler_csv
from app.tools.validar_csv import (
    validar_csv,
    COLUNAS_OCORRENCIAS,
)


# ==========================================================
# NORMALIZAÇÃO DE OCORRÊNCIAS
# ==========================================================

def normalizar_ocorrencias(dados):
    """
    Normaliza os dados de ocorrências.

    Converte:
    - valor_perda de texto para número decimal.

    Retorna uma nova lista de registros,
    sem alterar a lista original.
    """

    dados_normalizados = []

    for registro in dados:

        novo_registro = registro.copy()

        novo_registro["valor_perda"] = float(
            novo_registro["valor_perda"]
        )

        dados_normalizados.append(novo_registro)

    return dados_normalizados


# ==========================================================
# TESTE DE INTEGRAÇÃO
# ==========================================================

if __name__ == "__main__":

    caminho = "dados/teste_externo.csv"

    print("=== TESTE DO FLUXO COMPLETO ===")
    print()

    # ------------------------------------------------------
    # 1. LEITURA
    # ------------------------------------------------------

    dados = ler_csv(caminho)

    print("1. Leitura do CSV:")
    print(f"   Registros encontrados: {len(dados)}")

    # ------------------------------------------------------
    # 2. VALIDAÇÃO
    # ------------------------------------------------------

    resultado_validacao = validar_csv(
        caminho,
        COLUNAS_OCORRENCIAS,
    )

    print()
    print("2. Validação do CSV:")
    print(f"   Válido: {resultado_validacao['valido']}")
    print(f"   Mensagem: {resultado_validacao['mensagem']}")

    # ------------------------------------------------------
    # 3. NORMALIZAÇÃO
    # ------------------------------------------------------

    if resultado_validacao["valido"]:

        dados_normalizados = normalizar_ocorrencias(
            dados
        )

        print()
        print("3. Normalização:")

        print(
            f"   Registros normalizados: "
            f"{len(dados_normalizados)}"
        )

        print(
            f"   Tipo de valor_perda: "
            f"{type(dados_normalizados[0]['valor_perda']).__name__}"
        )

        print()
        print("Primeiro registro normalizado:")
        print(dados_normalizados[0])

        print()
        print("=== FLUXO CONCLUÍDO COM SUCESSO ===")

    else:

        print()
        print("=== FLUXO INTERROMPIDO ===")
        print("O arquivo não foi normalizado porque falhou na validação.")

        print()
        print("Erros encontrados:")

        for erro in resultado_validacao["erros"]:
            print(f"- {erro}")