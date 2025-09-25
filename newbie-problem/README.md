# Problema do “bixo turista” (USP São Carlos)

## Visão geral

Modelamos o campus como um grafo ponderado. O bixo parte do **ICMC** e precisa **visitar todos os pontos**: `ICMC, EESC, IFSC, CAASO, BANDECO`.

* **UCS (busca cega por custo)**: visita **todos os pontos** com **término livre**.
* **A*** (busca heurística): visita **todos os pontos** e **termina no BANDECO**.
  A solução **só é válida** se, ao final, o bixo estiver no BANDECO.

Ambos os scripts imprimem **cada interação**: nó expandido, custos e **snapshot da fronteira**.

## Arquivos

* `ucs.py` — UCS com logs passo a passo.
* `astar.py` — A* com logs passo a passo.

## Como executar

Pré-requisitos: Python 3.8+

```bash
# UCS: visitar todos (término livre), começa no ICMC
python ucs.py

# A*: visitar todos e TERMINAR no BANDECO, começa no ICMC
python astar.py
```

## Grafo utilizado

Vértices: `ICMC, EESC, IFSC, CAASO, BANDECO`
Arestas não-direcionadas com custo (tempo de caminhada):

* ICMC–EESC: 3
* ICMC–IFSC: 10
* ICMC–CAASO: 6
* EESC–IFSC: 9
* EESC–CAASO: 2
* CAASO–IFSC: 8
* IFSC–BANDECO: 10
* CAASO–BANDECO: 2

> Para alterar o mapa, edite a lista `arestas` em cada arquivo.

## Objetivos e critérios de parada

* **UCS**: parar no **primeiro estado** que tenha `visitados = {todos os pontos}` (término em qualquer nó).
* **A***: parar no **primeiro estado** que tenha `visitados = {todos}` **e** `no_atual = BANDECO`.

## Heurística usada no A*

Admissível e consistente (mantém otimalidade):

* `h(n) = max( faltantes × menor_aresta , distância_mínima(nó_atual -> BANDECO) )`
  (distâncias mínimas pré-calculadas com Dijkstra a partir do BANDECO)

## Estruturas e implementação

* **Estado**: `(no_atual, visitados_bitmask)`
* **Fronteira**: fila de prioridade

  * UCS ordena por `g`
  * A* ordena por `f = g + h`
* **Reconstrução de caminho**: via ponteiros de pai

## Customizações rápidas

* **Mudar ponto inicial**: altere a chamada `ucs_verbose("ICMC")` / `astar_verbose("ICMC","BANDECO")`.
* **Fixar outro ponto final no A***: troque `"BANDECO"` pelo destino desejado.
* **Trocar heurística**: mude a função `h(u, m)` em `astar_verbose.py`.

## Limitações e dicas

* UCS pode expandir muitos nós (tempo/memória) em grafos maiores.
* A* depende da qualidade de `h`: quanto mais informativa (sem superestimar), menos expansões.
* Mnater **todos os custos ≥ 0** para preservar as garantias de otimalidade.
