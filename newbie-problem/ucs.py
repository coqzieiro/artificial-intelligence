
from heapq import heappush, heappop
from collections import defaultdict
import math

# Grafo não-direcionado da modelagem
NOMES = ["ICMC", "EESC", "IFSC", "CAASO", "BANDECO"]
idx = {n:i for i,n in enumerate(NOMES)}
arestas = [
    ("ICMC","EESC",3),
    ("ICMC","IFSC",10),
    ("ICMC","CAASO",6),
    ("EESC","IFSC",9),
    ("EESC","CAASO",2),
    ("CAASO","IFSC",8),
    ("IFSC","BANDECO",10),
    ("CAASO","BANDECO",2),
]
G = [[] for _ in NOMES]
for a,b,c in arestas:
    u,v = idx[a], idx[b]
    G[u].append((v,c)); G[v].append((u,c))
ALL_MASK = (1<<len(NOMES)) - 1

def nomes_visitados(mask):
    return [NOMES[i] for i in range(len(NOMES)) if mask & (1<<i)]


def ucs_verbose(inicio="ICMC"):
    s = (idx[inicio], 1<<idx[inicio])
    pq=[(0, s, [inicio])]
    best=defaultdict(lambda: math.inf); best[s]=0
    passo=0
    print("== UCS: visitar TODOS (término livre) ==")
    while pq:
        g,(u,m),path = heappop(pq)
        passo+=1
        print(f"\nPasso {passo} — EXPANDE: {{no:{NOMES[u]}, g:{g}, visitados:{nomes_visitados(m)}}}")
        if m==ALL_MASK:
            print(">> OBJETIVO atingido (todos visitados).")
            print("Caminho:", " -> ".join(path))
            print("Custo total:", g)
            return g, path, passo-1
        # expansão
        for v,w in G[u]:
            m2=m|(1<<v); g2=g+w; estado2=(v,m2)
            if g2<best[estado2]:
                best[estado2]=g2
                novo_path = path+[NOMES[v]]
                heappush(pq,(g2, estado2, novo_path))
        # snapshot da fronteira (ordenada por g)
        if pq:
            snapshot=sorted([(g2,NOMES[estado[0]],nomes_visitados(estado[1])) for g2,estado,_ in pq])
            print("Fronteira (g, nó, visitados):")
            for item in snapshot:
                print("  ", item)
    print("Sem solução.")
    return None

if __name__=="__main__":
    ucs_verbose("ICMC")