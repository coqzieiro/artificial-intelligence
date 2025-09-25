
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


MIN_EDGE = min(c for _,_,c in arestas)

# Dijkstra a partir do BANDECO para dist mínimas (para h consistente)
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

def h(u, m):
    faltantes = bin(ALL_MASK ^ m).count("1")
    return max(faltantes*MIN_EDGE, DIST_TO_BAN[u])

def astar_verbose(inicio="ICMC", destino="BANDECO"):
    s=(idx[inicio], 1<<idx[inicio]); goal=idx[destino]
    pq=[(h(*s), 0, s, [inicio])]
    best=defaultdict(lambda: math.inf); best[s]=0
    passo=0
    print("== A*: visitar TODOS e TERMINAR no BANDECO ==")
    while pq:
        f,g,(u,m),path=heappop(pq)
        passo+=1
        print(f"\nPasso {passo} — EXPANDE: {{no:{NOMES[u]}, g:{g}, h:{h(u,m)}, f:{g+h(u,m)}, visitados:{nomes_visitados(m)}}}")
        if m==ALL_MASK and u==goal:
            print(">> OBJETIVO atingido (todos visitados e no BANDECO).")
            print("Caminho:", " -> ".join(path))
            print("Custo total:", g)
            return g, path, passo-1
        for v,w in G[u]:
            m2=m|(1<<v); g2=g+w; estado2=(v,m2)
            if g2<best[estado2]:
                best[estado2]=g2
                novo_path = path+[NOMES[v]]
                heappush(pq,(g2+h(v,m2), g2, estado2, novo_path))
        # snapshot da fronteira (ordenada por f)
        if pq:
            snapshot=sorted([(f2, g2, NOMES[e[0]], nomes_visitados(e[1])) for f2,g2,e,_ in pq])
            print("Fronteira (f, g, nó, visitados):")
            for item in snapshot:
                print("  ", item)
    print("Sem solução.")
    return None

if __name__=="__main__":
    astar_verbose("ICMC","BANDECO")