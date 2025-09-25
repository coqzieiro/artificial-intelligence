from heapq import heappush, heappop
from collections import defaultdict
from itertools import count
import math

# ===== Grafo (não-direcionado) =====
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
# manter ordem previsível dos vizinhos no print
for u in range(len(G)):
    G[u].sort(key=lambda vw: (vw[1], NOMES[vw[0]]))

ALL_MASK = (1<<len(NOMES)) - 1
MIN_EDGE = min(c for _,_,c in arestas)

def nomes_visitados(mask):
    return [NOMES[i] for i in range(len(NOMES)) if mask & (1<<i)]

# ----- Dijkstra a partir do BANDECO (dist mín p/ h consistente) -----
def dijkstra_from(t):
    n=len(G); D=[math.inf]*n; D[t]=0; pq=[(0,t)]
    while pq:
        d,u=heappop(pq)
        if d!=D[u]: continue
        for v,w in G[u]:
            nd=d+w
            if nd<D[v]: D[v]=nd; heappush(pq,(nd,v))
    return D
DIST_TO_BAN = dijkstra_from(idx["BANDECO"])

# ----- Heurística admissível (lower bounds combinados via max) -----
def h(u, m):
    faltantes = bin(ALL_MASK ^ m).count("1")
    return max(faltantes*MIN_EDGE, DIST_TO_BAN[u])

# ===== A* VERBOSE (formatação dos slides) =====
def astar_verbose(inicio="ICMC", destino="BANDECO"):
    s=(idx[inicio], 1<<idx[inicio]); goal=idx[destino]
    tie = count()  # desempate FIFO
    pq=[(h(*s), 0, next(tie), s, [inicio])]  # (f, g, fifo, (u,m), path)
    best=defaultdict(lambda: math.inf); best[s]=0
    passo=0

    while pq:
        f,g,_,(u,m),path=heappop(pq)
        passo+=1
        print(f"\nPasso {passo} - EXPANDE {NOMES[u]} | g={g}  h={h(u,m)}  f={g+h(u,m)}")
        print(f"Visitados: {nomes_visitados(m)}")

        if m==ALL_MASK and u==goal:
            print("\n>> OBJETIVO atingido (todos visitados e no BANDECO).")
            print("Caminho:", " -> ".join(path))
            print("Custo total:", g)
            return g, path

        # --- gerar apenas filhos ainda não visitados e imprimir no formato do slide ---
        linhas=[]
        for v,w in G[u]:
            if m & (1<<v):             # não voltar para nós já visitados
                continue
            m2 = m | (1<<v)
            g2 = g + w
            st2 = (v, m2)
            if g2 < best[st2]:
                best[st2] = g2
                hv = h(v, m2); fv = g2 + hv
                heappush(pq, (fv, g2, next(tie), st2, path+[NOMES[v]]))
                linhas.append((NOMES[v], w, g2, hv, fv))

        # ordenar por f (como na prioridade da A*) para bater com a visual dos slides
        linhas.sort(key=lambda t: (t[4], t[2], t[0]))
        if linhas:
            print("Gerados deste nó  ->  (vizinho | c | g' | h' | f'):")
            for nome_v, c, g2, h2, f2 in linhas:
                print(f"  {nome_v:7s} | {c:>2} | {g2:>2} | {h2:>2} | {f2:>2}")

    print("Sem solução.")
    return None

if __name__=="__main__":
    astar_verbose("ICMC","BANDECO")
