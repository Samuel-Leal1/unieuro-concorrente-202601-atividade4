"""
processar_paralelo.py
---------------------
Processa cada parte da pasta 'partes/' em paralelo,
chamando conversoremescalacinza.py como caixa-preta.
Os resultados vão para a pasta 'partes_cinza/'.

Para alterar o número de threads, mude a variável abaixo:
"""

# =============================================
#   ALTERE AQUI O NÚMERO DE THREADS
#   Valores sugeridos: 2, 4, 8, 12
# =============================================
NUM_THREADS = 12
# =============================================

import os
import subprocess
import sys
import threading
import time

PASTA_ENTRADA = "partes"
PASTA_SAIDA   = "partes_cinza"


def processar_parte(idx, entrada, saida, tempos, erros):
    """Executa conversoremescalacinza.py em um subprocesso e mede o tempo."""
    print(f"  [Thread {idx:02d}] Iniciando → {os.path.basename(entrada)}")
    t0 = time.time()

    resultado = subprocess.run(
        [sys.executable, "conversoremescalacinza.py", entrada, saida],
        capture_output=True,
        text=True
    )

    t1 = time.time()
    tempos[idx] = t1 - t0

    if resultado.returncode != 0:
        erros[idx] = resultado.stderr
        print(f"  [Thread {idx:02d}] ❌ ERRO! ({tempos[idx]:.2f}s)")
    else:
        print(f"  [Thread {idx:02d}] ✅ Concluído em {tempos[idx]:.2f}s")


def main():
    # Coleta os arquivos de entrada ordenados
    arquivos = sorted([
        f for f in os.listdir(PASTA_ENTRADA)
        if f.endswith(".ppm")
    ])

    if not arquivos:
        print(f"❌ Nenhum arquivo .ppm encontrado em '{PASTA_ENTRADA}/'")
        print("   Execute dividir.py primeiro.")
        sys.exit(1)

    os.makedirs(PASTA_SAIDA, exist_ok=True)

    print(f"\n{'='*55}")
    print(f"  PROCESSAMENTO PARALELO")
    print(f"  Threads : {NUM_THREADS}")
    print(f"  Entrada : {PASTA_ENTRADA}/  ({len(arquivos)} arquivos)")
    print(f"  Saída   : {PASTA_SAIDA}/")
    print(f"{'='*55}\n")

    # Monta pares entrada/saída
    pares = []
    for nome in arquivos:
        entrada = os.path.join(PASTA_ENTRADA, nome)
        saida   = os.path.join(PASTA_SAIDA, nome.replace("parte_", "cinza_"))
        pares.append((entrada, saida))

    tempos = {}
    erros  = {}

    print("Disparando threads...\n")

    # ── INÍCIO DA MEDIÇÃO ──
    t_inicio = time.time()

    # Processa em lotes do tamanho de NUM_THREADS
    for lote_ini in range(0, len(pares), NUM_THREADS):
        lote    = pares[lote_ini : lote_ini + NUM_THREADS]
        threads = []

        for idx, (entrada, saida) in enumerate(lote, start=lote_ini):
            t = threading.Thread(
                target=processar_parte,
                args=(idx, entrada, saida, tempos, erros),
                daemon=True
            )
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # ── FIM DA MEDIÇÃO ──
    t_fim = time.time()
    tempo_total = t_fim - t_inicio

    # ── Relatório final ──
    print(f"\n{'='*55}")
    print(f"  RESULTADO FINAL")
    print(f"{'='*55}")
    print(f"  Threads utilizadas : {NUM_THREADS}")
    print(f"  Partes processadas : {len(tempos)}")
    print()
    for i, dur in sorted(tempos.items()):
        print(f"  Thread {i:02d}: {dur:.2f}s")

    if erros:
        print(f"\n  ⚠️  Erros em {len(erros)} thread(s):")
        for idx, msg in erros.items():
            print(f"    Thread {idx:02d}: {msg[:200]}")

    print(f"\n  ⏱️  Tempo total de processamento: {tempo_total:.2f} segundos")
    print(f"  ⏱️  Tempo total de processamento: {tempo_total / 60:.2f} minutos")
    print(f"  🧵  Threads utilizadas           : {NUM_THREADS}")
    print(f"{'='*55}\n")

    print("✅ Processamento paralelo concluído!")
    print(f"   Partes salvas em '{PASTA_SAIDA}/'")
    print("   Execute juntar.py para gerar a imagem final.\n")


if __name__ == "__main__":
    main()
