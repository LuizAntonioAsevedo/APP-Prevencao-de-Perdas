import csv

caminho = "dados/remessas.csv"

with open(caminho, mode="r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)
    remessas = list(leitor)

print(f"Total de remessas: {len(remessas)}")
print(f"Primeira remessa: {remessas[0]}")
print(f"Última remessa: {remessas[-1]}")