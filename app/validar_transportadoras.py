import csv

caminho = "dados/transportadoras.csv"

with open(caminho, mode="r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)
    transportadoras = list(leitor)

print(f"Total de transportadoras: {len(transportadoras)}")

print()
print("Transportadoras cadastradas:")

for transportadora in transportadoras:
    print(
        f"- {transportadora['id_transportadora']}: "
        f"{transportadora['nome']} | "
        f"{transportadora['tipo_operacao']} | "
        f"{transportadora['regiao']}"
    )