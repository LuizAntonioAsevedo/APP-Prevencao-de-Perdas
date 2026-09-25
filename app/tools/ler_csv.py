import csv
from pathlib import Path


def ler_csv(caminho_arquivo):
    """
    Lê um arquivo CSV e retorna seus dados como uma lista de dicionários.

    Cada linha do CSV representa um dicionário.
    """

    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado: {caminho}"
        )

    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        dados = list(leitor)

    return dados


if __name__ == "__main__":
    print("=== TESTE DO LEITOR CSV ===")
    print()

    caminho = Path("dados") / "ocorrencias.csv"

    dados = ler_csv(caminho)

    print(f"Arquivo: {caminho}")
    print(f"Registros encontrados: {len(dados)}")

    if dados:
        print()
        print("Primeiro registro:")
        print(dados[0])