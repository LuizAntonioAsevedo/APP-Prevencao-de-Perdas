import csv

caminho = "dados/rotas.csv"

with open(caminho, mode="r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)
    rotas = list(leitor)

print(f"Total de rotas: {len(rotas)}")

print()
print("Rotas cadastradas:")

for rota in rotas:
    print(
        f"- {rota['id_rota']}: "
        f"{rota['origem']} → {rota['destino']} | "
        f"{rota['distancia_km']} km | "
        f"{rota['regiao']}"
    )