#!/bin/bash
REPETICOES=30
OUTPUT="data/mbw_resultados.csv"

mkdir -p data

echo "tamanho_mib,repeticao,vazao_mibs" > "$OUTPUT"

for TAMANHO in 16 128 1024; do
    echo "Rodando MBW para ${TAMANHO} MiB — ${REPETICOES} repetições..."
    for i in $(seq 1 $REPETICOES); do
        RESULTADO=$(mbw -t0 -n 1 $TAMANHO 2>/dev/null | grep "^AVG" | awk '{print $(NF-1)}')
        echo "${TAMANHO},${i},${RESULTADO}" >> "$OUTPUT"
        echo "  [${i}/${REPETICOES}] ${TAMANHO} MiB → ${RESULTADO} MiB/s"
    done
done

echo ""
echo "✅ Concluído! Resultados salvos em: $OUTPUT"
