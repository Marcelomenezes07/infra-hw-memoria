#!/usr/bin/env python3
# analise_estatistica.py
# Lê os CSVs gerados e calcula média, desvio-padrão, IC 95% e gera gráficos
# Uso: python3 analise_estatistica.py

import csv
import math
import os

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib não encontrado. Instale com: pip3 install matplotlib --break-system-packages")
    print("    Continuando apenas com estatísticas em texto...\n")

os.makedirs("results", exist_ok=True)

# ─────────────────────────────────────────────
# Funções estatísticas
# ─────────────────────────────────────────────

def carregar_csv(caminho):
    with open(caminho, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def media(valores):
    return sum(valores) / len(valores)

def desvio_padrao(valores):
    m = media(valores)
    return math.sqrt(sum((x - m)**2 for x in valores) / (len(valores) - 1))

def ic95(valores):
    n = len(valores)
    m = media(valores)
    s = desvio_padrao(valores)
    margem = 1.96 * s / math.sqrt(n)
    return m, s, margem

def teste_t(grupo_a, grupo_b):
    """Teste t de Student (duas amostras independentes)"""
    na, nb = len(grupo_a), len(grupo_b)
    ma, mb = media(grupo_a), media(grupo_b)
    sa, sb = desvio_padrao(grupo_a), desvio_padrao(grupo_b)
    ep = math.sqrt(sa**2/na + sb**2/nb)
    t = (ma - mb) / ep
    return t, ep

# ─────────────────────────────────────────────
# Análise MBW
# ─────────────────────────────────────────────

print("=" * 60)
print("ANÁLISE — MBW (Largura de Banda de Memória)")
print("=" * 60)

mbw_dados = carregar_csv("data/mbw_resultados.csv")

grupos_mbw = {}
for row in mbw_dados:
    tam = int(row["tamanho_mib"])
    val = float(row["vazao_mibs"])
    grupos_mbw.setdefault(tam, []).append(val)

niveis = {16: "L2/L3", 128: "L3/RAM", 1024: "RAM"}

mbw_stats = {}
for tam in sorted(grupos_mbw):
    vals = grupos_mbw[tam]
    m, s, e = ic95(vals)
    mbw_stats[tam] = (m, s, e)
    print(f"\n  {tam} MiB ({niveis[tam]}):")
    print(f"    n          = {len(vals)}")
    print(f"    Média      = {m:.2f} MiB/s")
    print(f"    Desvio-pad = {s:.2f} MiB/s")
    print(f"    IC 95%     = [{m-e:.2f}, {m+e:.2f}] MiB/s")

# Teste t entre 128 MiB e 1024 MiB (queda esperada ao passar do L3)
t_stat, ep = teste_t(grupos_mbw[128], grupos_mbw[1024])
print(f"\n  Teste t (128 MiB vs 1024 MiB):")
print(f"    t = {t_stat:.3f}  |  EP = {ep:.2f}")
print(f"    {'Diferença estatisticamente significativa (|t| > 2)' if abs(t_stat) > 2 else 'Diferença NÃO significativa'}")

# ─────────────────────────────────────────────
# Análise Localidade
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("ANÁLISE — Localidade Espacial")
print("=" * 60)

loc_dados = carregar_csv("data/localidade_resultados.csv")

tempos_a = [float(r["tempo_loop_a_s"]) for r in loc_dados]
tempos_b = [float(r["tempo_loop_b_s"]) for r in loc_dados]
razoes   = [float(r["razao_b_a"])      for r in loc_dados]

ma, sa, ea = ic95(tempos_a)
mb, sb, eb = ic95(tempos_b)
mr, sr, er = ic95(razoes)

print(f"\n  Loop A (sequencial / cache-friendly):")
print(f"    n          = {len(tempos_a)}")
print(f"    Média      = {ma:.4f}s")
print(f"    Desvio-pad = {sa:.4f}s")
print(f"    IC 95%     = [{ma-ea:.4f}, {ma+ea:.4f}]s")

print(f"\n  Loop B (saltos / cache-hostile):")
print(f"    n          = {len(tempos_b)}")
print(f"    Média      = {mb:.4f}s")
print(f"    Desvio-pad = {sb:.4f}s")
print(f"    IC 95%     = [{mb-eb:.4f}, {mb+eb:.4f}]s")

print(f"\n  Razão B/A:")
print(f"    Média      = {mr:.3f}x")
print(f"    Desvio-pad = {sr:.3f}")
print(f"    IC 95%     = [{mr-er:.3f}, {mr+er:.3f}]x")

t_loc, ep_loc = teste_t(tempos_b, tempos_a)
print(f"\n  Teste t (Loop B vs Loop A):")
print(f"    t = {t_loc:.3f}  |  EP = {ep_loc:.6f}")
print(f"    {'Diferença estatisticamente significativa (|t| > 2)' if abs(t_loc) > 2 else 'Diferença NÃO significativa'}")

# ─────────────────────────────────────────────
# Gráficos
# ─────────────────────────────────────────────

if HAS_MATPLOTLIB:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Hierarquia de Memória — Análise Experimental", fontsize=14, fontweight="bold")

    # Gráfico 1 — MBW com barras de erro
    ax1 = axes[0]
    tamanhos = sorted(mbw_stats.keys())
    medias   = [mbw_stats[t][0] for t in tamanhos]
    erros    = [mbw_stats[t][2] for t in tamanhos]
    rotulos  = [f"{t} MiB\n({niveis[t]})" for t in tamanhos]
    cores    = ["#2196F3", "#4CAF50", "#FF9800"]

    bars = ax1.bar(rotulos, medias, yerr=erros, capsize=6,
                   color=cores, edgecolor="black", linewidth=0.8)
    ax1.set_title("Largura de Banda por Nível de Hierarquia (MBW)")
    ax1.set_ylabel("Vazão média (MiB/s)")
    ax1.set_xlabel("Tamanho do array")
    for bar, m, e in zip(bars, medias, erros):
        ax1.text(bar.get_x() + bar.get_width()/2, m + e + 50,
                 f"{m:.0f}", ha="center", va="bottom", fontsize=9)
    ax1.set_ylim(0, max(medias) * 1.2)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # Gráfico 2 — Localidade: boxplot
    ax2 = axes[1]
    bp = ax2.boxplot([tempos_a, tempos_b],
                     labels=["Loop A\n(sequencial)", "Loop B\n(saltos)"],
                     patch_artist=True,
                     medianprops=dict(color="black", linewidth=2))
    bp["boxes"][0].set_facecolor("#2196F3")
    bp["boxes"][1].set_facecolor("#FF9800")
    ax2.set_title("Localidade Espacial — Tempo de Execução")
    ax2.set_ylabel("Tempo (s)")
    ax2.set_xlabel("Padrão de acesso")
    ax2.text(0.5, 0.95, f"Razão B/A: {mr:.3f}x (IC95: [{mr-er:.3f}, {mr+er:.3f}])",
             transform=ax2.transAxes, ha="center", va="top",
             fontsize=9, bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    caminho_grafico = "results/grafico_hierarquia_memoria.png"
    plt.savefig(caminho_grafico, dpi=150, bbox_inches="tight")
    print(f"\n✅ Gráfico salvo em: {caminho_grafico}")
    plt.close()
else:
    print("\nInstale matplotlib para gerar os gráficos:")
    print("  pip3 install matplotlib --break-system-packages")

print("\n✅ Análise concluída!")
