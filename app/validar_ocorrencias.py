import csv

caminho = "dados/ocorrencias.csv"

with open(caminho, mode="r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)
    ocorrencias = list(leitor)

print(f"Total de ocorrências: {len(ocorrencias)}")
print(f"Primeira ocorrência: {ocorrencias[0]}")
print(f"Última ocorrência: {ocorrencias[-1]}")