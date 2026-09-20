import csv
from collections import defaultdict


def carregar_csv(caminho):
    with open(caminho, mode="r", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))


remessas = carregar_csv("dados/remessas.csv")
ocorrencias = carregar_csv("dados/ocorrencias.csv")

remessas_por_rota = defaultdict(int)
ocorrencias_por_rota = defaultdict(int)
perdas_por_rota = defaultdict(float)

for remessa in remessas:
    remessas_por_rota[remessa["rota"]] += 1

for ocorrencia in ocorrencias:
    rota = ocorrencia["rota"]

    ocorrencias_por_rota[rota] += 1
    perdas_por_rota[rota] += float(ocorrencia["valor_perda"])


print("=== ANÁLISE DE PERDAS POR ROTA ===")
print()

for rota in sorted(remessas_por_rota):
    total_remessas = remessas_por_rota[rota]
    total_ocorrencias = ocorrencias_por_rota[rota]
    valor_perdas = perdas_por_rota[rota]

    indice_ocorrencia = (total_ocorrencias / total_remessas) * 100

    print(f"Rota: {rota}")
    print(f"  Remessas: {total_remessas}")
    print(f"  Ocorrências: {total_ocorrencias}")
    print(f"  Índice de ocorrência: {indice_ocorrencia:.2f}%")
    print(f"  Valor das perdas: R$ {valor_perdas:,.2f}")
    print()