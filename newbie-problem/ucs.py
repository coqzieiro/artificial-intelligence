from heapq import heappush, heappop
from collections import defaultdict
from itertools import count  # <<-- AQUI
import math

# Grafo (não-direcionado)
NOMES = ["ICMC", "EESC", "IFSC", "CAASO", "BANDECO"]
idx = {n:i for i,n in enumerate(NOMES)}
arestas = [
    ("ICMC","EESC",3),
    ("ICMC","IFSC",10),
    ("ICMC","BANDECO",6),
    ("EESC","IFSC",9),
    ("EESC","CAASO",2),
    ("CAASO","IFSC",8),
    ("CAASO","BANDECO",2),
    ("IFSC","BANDECO",10),
]
G = [[] for _ in NOMES]
for a,b,c in arestas:
    u,v = idx[a], idx[b]
    G[u].append((v,c)); G[v].append((u,c))
for u in range(len(G)):
    G[u].sort(key=lambda vw: (vw[1], NOMES[vw[0]]))  # estabilidade opcional

ALL_MASK = (1<<len(NOMES)) - 1
def nomes(mask): return [NOMES[i] for i in range(len(NOMES)) if mask & (1<<i)]

def ucs_verbose(inicio="ICMC"):
    start = idx[inicio]
    s = (start, 1<<start)
    tie = count()                                  # contador FIFO p/ desempate
    pq = [(0, next(tie), s, [inicio])]             # (g, fifo, (u,mask), path)
    best = defaultdict(lambda: math.inf); best[s]=0
    passo = 0
    print("== UCS: visitar TODOS (término livre) — sem voltar a visitados ==")
    while pq:
        g, _, (u,m), path = heappop(pq)
        passo += 1
        print(f"\nPasso {passo} - EXPANDE: {{no:{NOMES[u]}, g:{g}, visitados:{nomes(m)}}}")
        if m == ALL_MASK:
            print(">> OBJETIVO atingido (todos visitados).")
            print("Caminho:", " -> ".join(path))
            print("Custo total:", g)
            return g, path, passo-1

        gerados = []
        for v,w in G[u]:
            if m & (1<<v):               # não gerar nós já visitados
                continue
            m2 = m | (1<<v); g2 = g + w; st2 = (v, m2)
            if g2 < best[st2]:
                best[st2] = g2
                novo_path = path + [NOMES[v]]
                heappush(pq, (g2, next(tie), st2, novo_path))
                gerados.append((g2, NOMES[v], nomes(m2)))

        if gerados:
            print("Gerados deste nó (g, nó, visitados):")
            for item in sorted(gerados):
                print("  ", item)

    print("Sem solução.")
    return None

if __name__ == "__main__":
    ucs_verbose("ICMC")
