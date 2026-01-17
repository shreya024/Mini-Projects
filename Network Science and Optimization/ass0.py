
import pandas as pd
import networkx as nx
from itertools import combinations

# Load CSV (adjust path if needed)
df = pd.read_csv("IMDB-Movie-Dataset(2023-1951).csv")

# Prepare an undirected graph
G = nx.Graph()

for _, row in df.iterrows():
    # Parse cast list — splitting by comma (strip whitespace)
    if pd.notna(row["cast"]):
        actors = [a.strip() for a in row["cast"].split(",")]
    else:
        actors = []

    # Add nodes
    for a in actors:
        if not G.has_node(a):
            G.add_node(a)

    # Add edges for every pair of actors in this movie
    for a1, a2 in combinations(actors, 2):
        if G.has_edge(a1, a2):
            # Optionally count multiple co-stars by weight
            G[a1][a2]["weight"] += 1
        else:
            G.add_edge(a1, a2, weight=1)

print(f"Graph built: {G.number_of_nodes()} actors, {G.number_of_edges()} co-starring edges")

# Export to a file Gephi can import
nx.write_gexf(G, "bollywood_co_starring_network.gexf")
print("Exported to bollywood_co_starring_network.gexf")
