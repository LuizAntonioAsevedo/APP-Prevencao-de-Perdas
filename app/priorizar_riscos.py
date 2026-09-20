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


def classificar_risco(indice_ocorrencia, valor_perdas):
    if indice_ocorrencia >= 75 and valor_perdas >= 8000:
        return "CRÍTICO"

    if indice_ocorrencia >= 50 or valor_perdas >= 5000:
        return "ALTO"

    if indice_ocorrencia >= 25 or valor_perdas >= 2500:
        return "MÉDIO"

    return "BAIXO"


resultados = []

for rota in sorted(remessas_por_rota):
    total_remessas = remessas_por_rota[rota]
    total_ocorrencias = ocorrencias_por_rota[rota]
    valor_perdas = perdas_por_rota[rota]

    indice_ocorrencia = (total_ocorrencias / total_remessas) * 100

    nivel_risco = classificar_risco(
        indice_ocorrencia,
        valor_perdas
    )

    resultados.append({
        "rota": rota,
        "remessas": total_remessas,
        "ocorrencias": total_ocorrencias,
        "indice": indice_ocorrencia,
        "perdas": valor_perdas,
        "risco": nivel_risco
    })


ordem_risco = {
    "CRÍTICO": 1,
    "ALTO": 2,
    "MÉDIO": 3,
    "BAIXO": 4
}

resultados.sort(
    key=lambda item: (
        ordem_risco[item["risco"]],
        -item["indice"],
        -item["perdas"]
    )
)


print("=== PRIORIZAÇÃO DE RISCOS POR ROTA ===")
print()

for resultado in resultados:
    print(f"Rota: {resultado['rota']}")
    print(f"  Nível de risco: {resultado['risco']}")
    print(f"  Índice de ocorrência: {resultado['indice']:.2f}%")
    print(f"  Valor das perdas: R$ {resultado['perdas']:,.2f}")
    print(f"  Ocorrências: {resultado['ocorrencias']}")
    print()