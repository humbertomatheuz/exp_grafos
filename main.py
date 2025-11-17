import osmnx as ox
import networkx as nx
import time
import re
import os
import matplotlib.pyplot as plt
from math import sqrt

LOCAL_FIXO = "Recife, Brazil"
ARQUIVO_MAPA = "recife.graphml"

def extrair_lat_lon(entrada):
    numeros = re.findall(r'-?\d+\.\d+', entrada)
    if len(numeros) >= 2:
        lat = float(numeros[0])
        lon = float(numeros[1])
        if lat > 0 and lon > 0:
            print("⚠️ Aviso: Coordenadas positivas. Recife costuma ser negativo (-8, -34).")
        return lat, lon
    return None

def carregar_grafo_cidade():
    if os.path.exists(ARQUIVO_MAPA):
        print(f"\n📂 Arquivo de cache '{ARQUIVO_MAPA}' encontrado.")
        try:
            G = ox.load_graphml(ARQUIVO_MAPA)
            print(f"✅ Mapa carregado! {len(G.nodes)} nós.")
            return G
        except:
            print("⚠️ Cache inválido. Baixando novamente.")

    print(f"\n🔄 Baixando mapa de: {LOCAL_FIXO}")
    print("⏳ Aguarde... (Pode demorar 1-2 minutos)")
    
    try:
        G = ox.graph_from_place(LOCAL_FIXO, network_type='drive')
        
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        
        print(f"💾 Salvando novo cache '{ARQUIVO_MAPA}'...")
        ox.save_graphml(G, ARQUIVO_MAPA)
        
        return G
    except Exception as e:
        print(f"❌ Erro fatal ao baixar: {e}")
        exit()

def calcular_distancia_caminho(G, caminho):
    distancia = 0
    if not caminho or len(caminho) < 2: return 0
    for u, v in zip(caminho[:-1], caminho[1:]):
        arestas = G[u][v]
        menor = min(d.get('length', 0) for d in arestas.values())
        distancia += menor
    return distancia

def executar_algoritmos(G, origem, destino):
    resultados = []
    
    def h(u, v):
        try:
            dx = float(G.nodes[u]['x']) - float(G.nodes[v]['x'])
            dy = float(G.nodes[u]['y']) - float(G.nodes[v]['y'])
            dist_graus = sqrt(dx**2 + dy**2)
            return dist_graus * 111319
        except: return 0

    print(f"\n🚦 Calculando rotas...")

    testes = [
        ("BFS", nx.shortest_path, None, None),
        ("Dijkstra", nx.dijkstra_path, 'length', None),
        ("A*", nx.astar_path, 'length', h)
    ]

    rota_visual = []

    for nome, func, peso, heur in testes:
        inicio = time.time()
        try:
            kwargs = {'weight': peso}
            if heur: kwargs['heuristic'] = heur
            
            caminho = func(G, source=origem, target=destino, **kwargs)
            tempo = time.time() - inicio
            dist = calcular_distancia_caminho(G, caminho)
            
            resultados.append([nome, f"{tempo:.5f}", len(caminho), f"{dist:.1f}"])
            if nome == "Dijkstra": rota_visual = caminho
        except:
            resultados.append([nome, "Erro", "-", "-"])

    return resultados, rota_visual

if __name__ == "__main__":
    G = carregar_grafo_cidade()
    G_scc = G.subgraph(max(nx.strongly_connected_components(G), key=len))

    print("\n" + "="*60)
    print("📍 Insira as coordenadas (ex: -8.039, -34.927)")
    print("="*60)

    coords_a = None
    while not coords_a:
        entrada = input(">> Ponto A (Origem): ").strip()
        coords_a = extrair_lat_lon(entrada)
        if not coords_a: print("❌ Formato inválido.")

    coords_b = None
    while not coords_b:
        entrada = input(">> Ponto B (Destino): ").strip()
        coords_b = extrair_lat_lon(entrada)
        if not coords_b: print("❌ Formato inválido.")

    print(f"\n🔍 Mapeando no grafo...")
    origem = ox.nearest_nodes(G_scc, X=coords_a[1], Y=coords_a[0])
    destino = ox.nearest_nodes(G_scc, X=coords_b[1], Y=coords_b[0])

    tabela, rota = executar_algoritmos(G_scc, origem, destino)

    print("\n" + "="*65)
    print(f"{'Algoritmo':<15} | {'Tempo (s)':<12} | {'Nós na Rota':<12} | {'Distância (m)':<15}")
    print("-" * 65)
    for l in tabela:
        print(f"{l[0]:<15} | {l[1]:<12} | {l[2]:<12} | {l[3]:<15}")
    print("="*65)
    
    if rota:
        print("\n🗺️ Abrindo mapa...")
        fig, ax = ox.plot_graph_route(G, rota, route_color='cyan', node_size=0, figsize=(10,10), show=False, close=False)
        
        ax.scatter(G.nodes[origem]['x'], G.nodes[origem]['y'], c='lime', s=200, label='A (Origem)', zorder=10, edgecolors='black')
        ax.scatter(G.nodes[destino]['x'], G.nodes[destino]['y'], c='red', s=200, label='B (Destino)', zorder=10, edgecolors='black')
        
        plt.legend()
        plt.title(f"Rota Calculada: {tabela[1][3]}m")
        plt.show()
    else:
        print("⚠️ Nenhuma rota encontrada.")