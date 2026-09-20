import csv
from collections import Counter


def carregar_csv(caminho):
    with open(caminho, mode="r", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))


remessas = carregar_csv("dados/remessas.csv")
ocorrencias = carregar_csv("dados/ocorrencias.csv")

ids_remessas = {remessa["id_remessa"] for remessa in remessas}

ocorrencias_invalidas = [
    ocorrencia
    for ocorrencia in ocorrencias
    if ocorrencia["id_remessa"] not in ids_remessas
]

tipos = Counter(
    ocorrencia["tipo_ocorrencia"]
    for ocorrencia in ocorrencias
)

transportadoras = Counter(
    ocorrencia["transportadora"]
    for ocorrencia in ocorrencias
)

valor_total_perdas = sum(
    float(ocorrencia["valor_perda"])
    for ocorrencia in ocorrencias
)

print("=== ANÁLISE INICIAL DE OCORRÊNCIAS ===")
print()
print(f"Total de remessas: {len(remessas)}")
print(f"Total de ocorrências: {len(ocorrencias)}")
print(f"Valor total das perdas: R$ {valor_total_perdas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

print()
print("Ocorrências por tipo:")

for tipo, quantidade in tipos.items():
    print(f"- {tipo}: {quantidade}")

print()
print("Ocorrências por transportadora:")

for transportadora, quantidade in transportadoras.items():
    print(f"- {transportadora}: {quantidade}")

print()
print(f"Ocorrências com remessa inexistente: {len(ocorrencias_invalidas)}")

if ocorrencias_invalidas:
    print("ATENÇÃO: existem ocorrências vinculadas a remessas inexistentes.")
else:
    print("Integridade dos vínculos: OK")