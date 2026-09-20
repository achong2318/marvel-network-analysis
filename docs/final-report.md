# Marvel Hero Network Final Project Report

Andrew Chong and Jake Hauf

B.S. Cyber-Physical Systems Engineering

ENEB355 - Spring 2026

1. Summary

Our project models the complex web of superhero co-appearances in the Marvel Universe using graph theory and advanced data structures. By leveraging the hero-network.csv dataset, we mapped connections between characters, applied graph algorithms (Breadth-First Search and Degree Centrality), and utilized a self-balancing AVL Binary Search Tree to rank hero data. Our results confirm the highly interconnected nature of the Marvel Universe and identify the most central figures in its storytelling.

2. Data Wrangling & Graph Construction

2.1 Data Cleaning & Preparation

The raw dataset consists of hundreds of thousands of comic book co-appearances. To prepare the data for our analysis, we executed several cleaning steps using the Pandas library:

•

Extracted the relevant hero1 and hero2 columns.

•

Dropped rows containing null or empty values.

•

Converted all character names to string format.

•

Filtered out self-loops (instances where a hero is connected to themselves).

2.2 Subgraph Filtering

Visualizing and analyzing the entire Marvel network is computationally expensive and visually cluttered. To create a meaningful and dense subgraph, we filtered the dataset to include only the top 150 most frequently appearing heroes. Edges were only retained if both heroes belonged to this top 150 list. This reduction left us with a highly concentrated graph consisting of 150 nodes and 8,119 edges.

3. Methodology & Mathematical Concepts

We employed several fundamental graph theory concepts and data structures to analyze the relationships within the Marvel Universe.

Key Terminology:

•

Node: Represents a Marvel hero.

•

Edge: Represents a connection between two heroes who appeared together in comics.

•

Graph: The complete Marvel hero network structure we used for traversal and centrality metrics. •

Connected Component: A group where every node can reach every other node. Almost all top Marvel heroes belong to one large connected component.

3.1 Degree Centrality

Degree centrality measures how connected a node is relative to the rest of the network. We calculated it using the formula:

Cd(v) = deg(v) / (n − 1)

Where deg(v) is the number of connections hero v has, and n is the total number of heroes. Values close to 1 indicate that the hero is connected to a large percentage of the network.

3.2 Breadth-First Search (BFS) & Shortest Path

We used BFS to find the shortest connection between two heroes. Our algorithm searches through the graph level-by-level, ensuring the shortest sequence of edges is discovered. The time complexity for this algorithm is:

O(V + E)

Where V is the number of vertices (heroes) and E is the number of edges (connections).

3.3 AVL Tree for Ranking

We integrated an AVL tree, which is a self-balancing binary search tree, to efficiently store and rank hero data. By maintaining balance, our operations such as insertions, searches, and sorting remain extremely fast, operating with a time complexity of:

O(log n)

4. Implementation Details

Our technical stack includes Python, Pandas, NetworkX, and Matplotlib. We structured the Python implementation systematically to load, process, analyze, and visualize the data.

import pandas as pd

import networkx as nx

import matplotlib.pyplot as plt

import time

After importing libraries and loading the CSV, we used the value_counts() method to isolate the top 150 heroes. We initialized an undirected graph and populated connections by iterating over the filtered dataframe.

Our code then isolates specific heroes (e.g., White Queen and Wong) by matching string names to avoid CSV formatting errors. We execute the BFS algorithm, verify a path exists, and calculate the path length (number of edges). Finally, we construct a targeted subgraph isolating just the connection chain.

5. Visual Interpretation

We generated several visualizations to intuitively present the network's topology.

5.1 Main Marvel Network Graph

Plotted using a spring_layout with seed=42, our visualization maps each hero as a node. The dense center of the graph visually confirms that popular heroes appear together frequently, creating overlapping edges and forming a single, highly connected network. Peripheral nodes, pushed outward by the layout algorithm, represent heroes with slightly fewer connections but who still remain part of the main component.

5.2 Degree Centrality Rankings

Our bar chart ranking the top heroes reveals that figures like Captain America and Spider-Man act as major storytelling hubs. The bars appear remarkably similar in height because the top Marvel heroes are all extremely connected. The normalized degree centrality scores are close to 1.0, signifying connections to nearly the entire core network.

5.3 BFS Shortest Path Visualization

This visualization highlights the specific path between two queried heroes (e.g., White Queen to Wong) using a dark line over a faded background of the full graph. This demonstrates that even characters who seem unrelated are connected through a surprisingly small number of steps.

This visualization zooms in on a specific subset of the network to clearly illustrate the shortest connection path between targeted characters discovered through the breadth-first search algorithm.

6. Performance Analysis

Our project highlights the trade-offs between custom implementations and optimized library functions:

•

Filtering the dataset down to 150 nodes allows our degree centrality calculations to run in a matter of milliseconds, demonstrating high efficiency.

•

Our custom BFS implementation successfully demonstrates algorithmic mechanics. While naturally slower than NetworkX's optimized C-backed routines, it proves robust.

•

Using the AVL tree introduces an O(log n) ranking system, which scales far better than executing standard sort() functions on every query across massive datasets.

7. Conclusion

We successfully modeled a real-world dataset as a complex graph. By implementing custom BFS and AVL tree structures, alongside NetworkX's centrality metrics, our analysis confirms that the core Marvel Universe is incredibly tight-knit. Our visualizations clearly demonstrate that graph theory is an exceptional tool for understanding real-world network structures. The top 150 characters form a single connected component, heavily anchored by central storytelling hubs like Captain America, Spider-Man, and Mr. Fantastic.
