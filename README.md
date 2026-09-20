
# Marvel Hero Network Analysis

A graph-analysis project that models Marvel character co-appearances as a network. The project applies graph algorithms and a self-balancing AVL tree to identify central characters, find shortest connection paths, and examine the structure of a dense real-world network.

## Highlights

- Cleans and filters a large hero co-appearance dataset with pandas
- Builds a 150-node undirected graph using NetworkX
- Implements Breadth-First Search for shortest paths
- Calculates and visualizes degree centrality
- Implements an AVL self-balancing binary search tree
- Measures algorithm execution time
- Produces network, shortest-path, centrality, and performance visualizations

## Repository structure

- `marvel_network_analysis.ipynb` - portable Jupyter/Colab notebook
- `src/analysis.py` - script export of the notebook workflow
- `data/README.md` - dataset placement instructions
- `docs/final-report.md` - project report
- `requirements.txt` - Python dependencies

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Place `hero-network.csv` in `data/`, then run the notebook from the repository root.

## Results

For the analyzed top-150-character subgraph, the project produced 8,119 edges and one connected component. Captain America had the highest measured degree centrality, and the custom BFS found a two-hop path from White Queen to Wong through Professor X.

## Authors

Andrew Chong and Jake Hauf

This repository preserves the original group-project attribution.
