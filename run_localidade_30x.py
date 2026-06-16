#!/usr/bin/env python3
# run_localidade_30x.py
# Roda o teste de localidade espacial 30 vezes e salva resultados em CSV
# Uso: python3 run_localidade_30x.py

import numpy as np
import time
import csv
import os

REPETICOES = 30
TAMANHO = 3000  # matriz 3000x3000 (~69 MB)
OUTPUT = "data/localidade_resultados.csv"

os.makedirs("data", exist_ok=True)

def loop_sequencial(matriz):
    """Loop A — acesso linha por linha (cache-friendly)"""
    total = 0.0
    n = matriz.shape[0]
    for i in range(n):
        for j in range(n):
            total += matriz[i, j]
    return total

def loop_saltos(matriz):
    """Loop B — acesso coluna por coluna (cache-hostile)"""
    total = 0.0
    n = matriz.shape[0]
    for i in range(n):
        for j in range(n):
            total += matriz[j, i]
    return total

print(f"Rodando teste de localidade espacial — {REPETICOES} repetições")
print(f"Matriz: {TAMANHO}x{TAMANHO} ({TAMANHO*TAMANHO*8/1024/1024:.0f} MB)\n")

resultados = []

# Warm-up: descarta as 3 primeiras execuções
print("Aquecendo (warm-up)...")
matriz_wup = np.random.rand(500, 500)
for _ in range(3):
    loop_sequencial(matriz_wup)
    loop_saltos(matriz_wup)
print("Warm-up concluído.\n")

for i in range(1, REPETICOES + 1):
    # Cria nova matriz a cada repetição para evitar cache quente
    matriz = np.random.rand(TAMANHO, TAMANHO)

    inicio = time.perf_counter()
    loop_sequencial(matriz)
    tempo_a = time.perf_counter() - inicio

    inicio = time.perf_counter()
    loop_saltos(matriz)
    tempo_b = time.perf_counter() - inicio

    razao = tempo_b / tempo_a
    resultados.append((i, tempo_a, tempo_b, razao))

    print(f"  [{i:02d}/{REPETICOES}] Loop A: {tempo_a:.4f}s | Loop B: {tempo_b:.4f}s | Razão B/A: {razao:.3f}")

# Salva CSV
with open(OUTPUT, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["repeticao", "tempo_loop_a_s", "tempo_loop_b_s", "razao_b_a"])
    writer.writerows(resultados)

# Estatísticas finais
tempos_a = [r[1] for r in resultados]
tempos_b = [r[2] for r in resultados]
razoes   = [r[3] for r in resultados]

def ic95(valores):
    import math
    n = len(valores)
    media = sum(valores) / n
    variancia = sum((x - media)**2 for x in valores) / (n - 1)
    desvio = math.sqrt(variancia)
    margem = 1.96 * desvio / math.sqrt(n)
    return media, desvio, margem

ma, da, ea = ic95(tempos_a)
mb, db, eb = ic95(tempos_b)
mr, dr, er = ic95(razoes)

print(f"\n{'='*55}")
print(f"RESULTADOS FINAIS ({REPETICOES} repetições)")
print(f"{'='*55}")
print(f"Loop A (sequencial): {ma:.4f}s ± {da:.4f}s  IC95: [{ma-ea:.4f}, {ma+ea:.4f}]")
print(f"Loop B (saltos):     {mb:.4f}s ± {db:.4f}s  IC95: [{mb-eb:.4f}, {mb+eb:.4f}]")
print(f"Razão B/A:           {mr:.3f} ± {dr:.3f}    IC95: [{mr-er:.3f}, {mr+er:.3f}]")
print(f"\n✅ Resultados salvos em: {OUTPUT}")
