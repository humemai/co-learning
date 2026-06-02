# Co-Learning for the ROMAN 2026 Paper

This repository is the curated artifact for the accepted ROMAN 2026 paper, "Improving Human-Robot Teamwork in Urban Search and Rescue Through Episodic Memory of Prior Collaboration."

It is organized around four top-level areas:

- `runtime/`: MATRX USAR experiment code, assets, visualizer, schema, and runtime configuration
- `data/`: processed dataset and raw CSV inputs used for the paper analyses
- `analysis/`: graph-learning notebooks, helper code, and generated analysis figures
- `paper/`: accepted paper source and supplementary material

The `humemai-research` package is not vendored here. Install it from PyPI when you need the JanusGraph-based analysis workflow.

## Repository layout

- `main.py`
  Thin entrypoint for launching the interactive MATRX experiment from the repo root.
- `runtime/`
  Runtime package for the MATRX USAR experiment.
- `runtime/custom_visualizer/`
  Flask-based visualizer used by the experiment UI.
- `runtime/images/`
  Images used by the MATRX environment and visualizer.
- `runtime/loggers/`
  Runtime logging helpers.
- `runtime/typedb-schema/`
  TypeDB schema and seed data for collaboration-pattern storage.
- `runtime/latin_square_list.csv`
  Participant-to-scenario ordering used by the experiment runner.
- `data/raw-data.json`
  Processed collaboration-pattern dataset used by the paper analyses.
- `data/user-raw-data/new/`
  Raw CSV inputs used to regenerate `data/raw-data.json`.
- `analysis/graph_learning.py`
  Utilities for parsing raw data and generating RDF-style graph artifacts.
- `analysis/process-raw-data.ipynb`
  Notebook that regenerates `data/raw-data.json` from the raw CSV files.
- `analysis/graph-learning-humemai.ipynb`
  Notebook for the HumemAI / JanusGraph / RGCN analysis workflow used for the paper figures.
- `analysis/figures/`
  Generated analysis figures referenced by the supplementary material.
- `paper/roman-2026/`
  Accepted paper source, references, figures, and compiled PDF.
- `paper/supplementary-material/`
  Supplementary markdown, figures, and PDF.

## Python dependencies

Create a virtual environment and install the Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The analysis notebook also uses the published package:

```bash
pip install humemai-research
```

## External services

The MATRX runtime still uses TypeDB for collaboration-pattern storage during the interactive experiment.

- Install TypeDB Server / Console / Studio separately.
- Start the server on `localhost:1729`.
- Create the `CP_ontology` database.
- Load the schema from `runtime/typedb-schema/CP_ontology_schema_corrected.tql`.
- Load any required seed data from `runtime/typedb-schema/Basic_Instances.tql` if your experiment setup expects it.

## Reproducing the paper assets

### 1. Rebuild the processed dataset

Open `analysis/process-raw-data.ipynb` and run it against the CSV files in `data/user-raw-data/new/`.

The output is `data/raw-data.json`.

### 2. Run the graph-learning analysis

Open `analysis/graph-learning-humemai.ipynb`.

This notebook:

- writes the collaboration patterns into JanusGraph through `humemai-research`
- constructs the graph representation of each collaboration pattern
- trains the RGCN used in the paper analysis
- produces the clustering and training figures used in the manuscript and supplementary material

`analysis/graph_learning.py` contains the reusable parsing and graph-construction helpers used by that workflow.

### 3. Run the interactive MATRX experiment

```bash
python main.py
```

You will be prompted for:

- the starting scenario number
- the participant number, which also determines the visualizer port

Then open the visualizer in a browser at:

```text
http://localhost:<participant-number>/human-agent/human_selector
```

Keyboard controls:

- Arrow keys: move
- `b`: pick up / select
- `n`: drop
