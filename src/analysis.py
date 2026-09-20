# Import the libraries used in this project
from pathlib import Path
from collections import deque
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time

print("Libraries imported successfully.")

# %%

# Place hero-network.csv in the data directory before running the notebook
DATA_FILE = Path("data/hero-network.csv")
if not DATA_FILE.exists():
    raise FileNotFoundError("Download hero-network.csv and place it in data/.")
print(f"Using dataset: {DATA_FILE}")

# %%

# Load the CSV file into pandas

file_name = DATA_FILE

df = pd.read_csv(file_name)

# Show the first 5 rows of data
print("First 5 rows:")
display(df.head())

# Show column names
print("\nColumns:")
print(df.columns)

# Show total number of rows
print("\nNumber of rows:", len(df))

# %%

# Keep only the first two columns

df = df.iloc[:, 0:2]

# Rename the columns
df.columns = ["hero1", "hero2"]

# Remove empty rows
df = df.dropna()

# Convert everything to text
df["hero1"] = df["hero1"].astype(str)
df["hero2"] = df["hero2"].astype(str)

# Remove rows where the same hero appears twice
df = df[df["hero1"] != df["hero2"]]

print("Cleaned data:")
display(df.head())

# %%

# Use only the top 150 heroes
# makes the graph easier to visualize

TOP_N = 150

# Combine both hero columns together
all_heroes = pd.concat([df["hero1"], df["hero2"]])

# Find the heroes that appear the most
top_heroes = all_heroes.value_counts().head(TOP_N).index

# Keep only rows that contain top heroes
small_df = df[
    df["hero1"].isin(top_heroes) &
    df["hero2"].isin(top_heroes)
]

print("Rows after filtering:", len(small_df))

display(small_df.head())

# %%

# Create an empty graph

G = nx.Graph()

# Add hero connections to the graph
for index, row in small_df.iterrows():

    hero1 = row["hero1"]
    hero2 = row["hero2"]

    # Add an edge between the two heroes
    G.add_edge(hero1, hero2)

print("Graph created.")

# Show graph information
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# %%

# Find the number of connections each hero has

degrees = dict(G.degree())

# Sort heroes by number of connections
top_degree = sorted(
    degrees.items(),
    key=lambda x: x[1],
    reverse=True
)

print("Top 10 most connected heroes:")

for hero, degree in top_degree[:10]:
    print(hero, "-", degree)

# %%

# Marvel Network Visualization

plt.figure(figsize=(16,12))

# Spacing between nodes
pos = nx.spring_layout(
    G,
    seed=42,
    k=0.6
)

# Node sizes
node_sizes = []

for node in G.nodes():

    node_sizes.append(degrees[node] * 8)

# Draw nodes
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=node_sizes,
    alpha=0.7
)

nx.draw_networkx_edges(
    G,
    pos,
    alpha=0.03
)

# Only label top 10 heroes
top_heroes_names = []

for hero, degree in top_degree[:10]:

    top_heroes_names.append(hero)

labels = {}

for node in G.nodes():

    if node in top_heroes_names:

        labels[node] = node

# Draw labels
nx.draw_networkx_labels(
    G,
    pos,
    labels,
    font_size=10
)

plt.title("Marvel Hero Interaction Network")

plt.axis("off")

plt.show()

# %%

# Breadth-First Search for the shortest unweighted path
def bfs_shortest_path(graph, start, goal):
    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None

# %%

# Show some hero names from the graph

print(list(G.nodes())[:30])

# Pick two heroes
hero_a = list(G.nodes())[0]
hero_b = list(G.nodes())[25]

# Find shortest path
path = bfs_shortest_path(G, hero_a, hero_b)

print("Hero A:", hero_a)
print("Hero B:", hero_b)

print("\nShortest Path:")

print(" -> ".join(path))

# %%

# Visualize the shortest path

if path is not None:

    path_edges = list(zip(path, path[1:]))

    plt.figure(figsize=(12,8))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=80,
        alpha=0.2
    )

    nx.draw_networkx_edges(
        G,
        pos,
        alpha=0.05
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=path,
        node_size=500
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=path_edges,
        width=3
    )

    nx.draw_networkx_labels(
        G,
        pos,
        labels={node: node for node in path},
        font_size=9
    )

    plt.title("Shortest Path Between Heroes")

    plt.axis("off")

    plt.show()

else:

    print("No path found, so no graph can be drawn.")

# %%

# Clean Shortest Path Visualization
# White Queen to Wong

# Find name from graph
hero_a = [hero for hero in G.nodes() if "WHITE QUEEN/EMMA FRO" in hero][0]
hero_b = [hero for hero in G.nodes() if "WONG" in hero][0]

print("Using hero names:")
print(hero_a)
print(hero_b)

path = bfs_shortest_path(G, hero_a, hero_b)

if path is not None:

    print("\nShortest Path:")
    print(" -> ".join(path))
    print("\nPath Length:", len(path) - 1)

    path_graph = nx.Graph()

    for i in range(len(path) - 1):
        path_graph.add_edge(path[i], path[i + 1])

    plt.figure(figsize=(12,6))

    pos = nx.spring_layout(path_graph, seed=42)

    nx.draw(
        path_graph,
        pos,
        with_labels=True,
        node_size=3500,
        font_size=10
    )

    plt.title("Shortest Path: White Queen to Wong")
    plt.show()

else:
    print("No path found.")

# %%

# Degree centrality measures how connected a hero is

centrality = nx.degree_centrality(G)

# Sort heroes by centrality score
top_centrality = sorted(
    centrality.items(),
    key=lambda x: x[1],
    reverse=True
)

print("Top 10 Heroes by Degree Centrality:")

for hero, score in top_centrality[:10]:
    print(hero, "-", round(score, 4))

# %%

# Create a bar chart of the top heroes

heroes = []
scores = []

for hero, score in top_centrality[:10]:
    heroes.append(hero)
    scores.append(score)

plt.figure(figsize=(12,6))

plt.bar(heroes, scores)

plt.title("Top Heroes by Degree Centrality")

plt.xlabel("Hero")
plt.ylabel("Centrality Score")

plt.xticks(rotation=45)

plt.show()

# %%

# Find connected components in the graph
# This checks if the graph has separate groups

components = list(nx.connected_components(G))

print("Number of Connected Components:")
print(len(components))

largest = max(components, key=len)

print("Largest Component Size:")
print(len(largest))

# %%

# AVL Tree
#self-balancing Binary Search Tree

class AVLNode:

    def __init__(self, key):

        self.key = key

        self.left = None
        self.right = None

        self.height = 1


class AVLTree:

    # Get height of a node
    def get_height(self, node):

        if not node:
            return 0

        return node.height

    # Get balance factor
    def get_balance(self, node):

        if not node:
            return 0

        return self.get_height(node.left) - self.get_height(node.right)

    # Right rotation
    def right_rotate(self, y):

        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        y.height = 1 + max(
            self.get_height(y.left),
            self.get_height(y.right)
        )

        x.height = 1 + max(
            self.get_height(x.left),
            self.get_height(x.right)
        )

        return x

    # Left rotation
    def left_rotate(self, x):

        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        x.height = 1 + max(
            self.get_height(x.left),
            self.get_height(x.right)
        )

        y.height = 1 + max(
            self.get_height(y.left),
            self.get_height(y.right)
        )

        return y

    # Insert a value into the tree
    def insert(self, root, key):

        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)

        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(
            self.get_height(root.left),
            self.get_height(root.right)
        )

        balance = self.get_balance(root)

        # Balance the tree if needed
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Inorder traversal
    def inorder(self, root):

        if not root:
            return []

        return (
            self.inorder(root.left)
            + [root.key]
            + self.inorder(root.right)
        )

# %%

# Create the AVL Tree

tree = AVLTree()

root = None

# Use only unique degree values
used_values = []

for hero, degree in top_degree[:20]:

    if degree not in used_values:

        root = tree.insert(root, degree)

        used_values.append(degree)

print("AVL Tree Created")

print("Inorder Traversal:")

print(tree.inorder(root))

# %%

# Measure performance time for degree centrality

start = time.time()

test = nx.degree_centrality(G)

end = time.time()

print("Degree Centrality Time:")

print(end - start)

# %%

# Create performance chart

operations = ["Centrality"]

times = [end - start]

plt.figure(figsize=(6,4))

plt.bar(operations, times)

plt.title("Performance Analysis")

plt.ylabel("Time in Seconds")

plt.show()
