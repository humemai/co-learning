# Graph Learning

## typedb-schema-and-data

This data is stored in [`../typedb-schema-and-data/`](../typedb-schema-and-data/).
Originally both schema and the data were made with TypeDB, which is a key-value pair
pair sort of data. This data is not necessarily a graph type of data. So I convert it to
RDF data.

**TODO-1: The excel files had more than one sheet per file. pandas dataframe only use
the first sheet. Ask Emma if it's necessary to use other sheets as well.**

**TODO-2: Next time I get this data, find a way to get it raw TypeDB data, not an excel
file. It wasn't so eays to parse the excel spreadsheets.**

## OWL/RDF ontology (schema)

Before creating the data, we need to define an ontology (schema). It's created at
[`./co-learning-OWL-ontology.ttl`](./co-learning-OWL-ontology.ttl). The used format is
Turtle. I tried to follow the original [TypeDB schema made by
Emma](../typedb-schema-and-data/CP_ontology_schema_corrected.tql) as much as possible,
but of course some changes are made.

**TODO-3: Get feedback from Emma on what she thinks about the new OWL/RDF ontology.**

## RDF data

The [TypeDB data in the excel files](../typedb-schema-and-data/CPs%20exp%202a%20data/)
are converted to RDF Triples. Again Turtle was used as syntaxing. Check out the [Jupyter
Notebook](./typedb2rdf.ipynb). There isn't magic here. It's mostly hand-engineering.
Again, converting raw TypeDB data to RDF data must be a better choice.

[The newly created RDF files are saved here](./data/). Every `.ttl` file contains the
triples of each participant.

### Example

Let's take a look at the participant `p01` and its situation `s00`.

```ttl
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix colearn: <http://example.org/colearn#> .

# Define a participant
colearn:p01 a colearn:Participant ;
    rdfs:label "Participant p01" .

# A new situation p01_s00 starts
colearn:p01 colearn:hasSituation colearn:p01_s00 .

# Define a situation.
colearn:p01_s00 a colearn:Situation ;
    rdfs:label "Participant p01, Situation s00" ;
    colearn:isSituationOf colearn:p01 ;
    colearn:objectType "large rock" ;
    colearn:objectType "large rock" ;
    colearn:locationType "top of rock pile" ;
    colearn:locationType "bottom of rock pile" ;
    colearn:hasHumanAction colearn:p01_s00_h00 ;
    colearn:hasRobotAction colearn:p01_s00_r00 .

# Define the Human actions.
colearn:p01_s00_h00 a colearn:HumanAction ;
    rdfs:label "Participant p01, Situation s00, Human-Action h00" ;
    colearn:actorType "human" ;
    colearn:actionType "move to object" ;
    colearn:objectType "large rock" ;
    colearn:isActionOf colearn:p01_s00 ;
    colearn:hasNextAction colearn:p01_s00_h01 .

colearn:p01_s00_h01 a colearn:HumanAction ;
    rdfs:label "Participant p01, Situation s00, Human-Action h01" ;
    colearn:actorType "human" ;
    colearn:actionType "pick up object in location" ;
    colearn:objectType "small rock" ;
    colearn:locationType "top of rock pile" ;
    colearn:isActionOf colearn:p01_s00 ;
    colearn:hasPreviousAction colearn:p01_s00_h00 .

# Define the Robot actions.
colearn:p01_s00_r00 a colearn:RobotAction ;
    rdfs:label "Participant p01, Situation s00, Robot-Action r00" ;
    colearn:actorType "robot" ;
    colearn:actionType "move to object" ;
    colearn:objectType "large rock" ;
    colearn:isActionOf colearn:p01_s00 ;
    colearn:hasNextAction colearn:p01_s00_r01 .

colearn:p01_s00_r01 a colearn:RobotAction ;
    rdfs:label "Participant p01, Situation s00, Robot-Action r01" ;
    colearn:actorType "robot" ;
    colearn:actionType "break object in location" ;
    colearn:objectType "large rock" ;
    colearn:locationType "right side of rock pile" ;
    colearn:isActionOf colearn:p01_s00 ;
    colearn:hasNextAction colearn:p01_s00_r02 ;
    colearn:hasPreviousAction colearn:p01_s00_r00 .

colearn:p01_s00_r02 a colearn:RobotAction ;
    rdfs:label "Participant p01, Situation s00, Robot-Action r02" ;
    colearn:actorType "robot" ;
    colearn:actionType "break object in location" ;
    colearn:objectType "large rock" ;
    colearn:locationType "bottom of rock pile" ;
    colearn:isActionOf colearn:p01_s00 ;
    colearn:hasNextAction colearn:p01_s00_r03 ;
    colearn:hasPreviousAction colearn:p01_s00_r01 .

colearn:p01_s00_r03 a colearn:RobotAction ;
    rdfs:label "Participant p01, Situation s00, Robot-Action r03" ;
    colearn:actorType "robot" ;
    colearn:actionType "pick up object in location" ;
    colearn:objectType "small rock" ;
    colearn:locationType "top of rock pile" ;
    colearn:isActionOf colearn:p01_s00 ;
    colearn:hasPreviousAction colearn:p01_s00_r02 .

# A new situation p01_s01 starts
colearn:p01 colearn:hasSituation colearn:p01_s01 .

# Define a situation.
colearn:p01_s01 a colearn:Situation ;
    rdfs:label "Participant p01, Situation s01" ;
    colearn:isSituationOf colearn:p01 ;
    colearn:objectType "small rock" ;
    colearn:locationType "top of rock pile" ;
    colearn:hasHumanAction colearn:p01_s01_h00 ;
    colearn:hasRobotAction colearn:p01_s01_r00 .

# Define the Human actions.
colearn:p01_s01_h00 a colearn:HumanAction ;
    rdfs:label "Participant p01, Situation s01, Human-Action h00" ;
    colearn:actorType "human" ;
    colearn:actionType "move back and forth in location" ;
    colearn:locationType "top of rock pile" ;
    colearn:isActionOf colearn:p01_s01 ;
    colearn:hasNextAction colearn:p01_s01_h01 .

colearn:p01_s01_h01 a colearn:HumanAction ;
    rdfs:label "Participant p01, Situation s01, Human-Action h01" ;
    colearn:actorType "human" ;
    colearn:actionType "pick up object in location" ;
    colearn:objectType "small rock" ;
    colearn:locationType "top of rock pile" ;
    colearn:isActionOf colearn:p01_s01 ;
    colearn:hasPreviousAction colearn:p01_s01_h00 .

# Define the Robot actions.
colearn:p01_s01_r00 a colearn:RobotAction ;
    rdfs:label "Participant p01, Situation s01, Robot-Action r00" ;
    colearn:actorType "robot" ;
    colearn:actionType "move to object" ;
    colearn:objectType "small rock" ;
    colearn:isActionOf colearn:p01_s01 .
```

We first load the necessary namespaces. `colearn:` is designed by ourselves for our
project. The rest of the lines are nothing but writing out RDF triples in Turtle. As
defined in the ontology, the four data type properties, `colearn:actorType`,
`colearn:actionType`, `colearn:objectType`, and `colearn:locationType` are extensively
used. All of these four properties take a string value, i.e., literal, as their tails.
The literal values that they can take are finite. The above example can be represented
as a graph as below.

![alt text](<co-learning p01_s00 example graph.png>)

The properties (relations) whose range is literal are displayed under a node, while the
properties whose range is an instance are displayed with an edge.

One problem here is that some participants have specified multiple DatatypeProperties.
For example, the sitaution node `p01_s00` has two `objectType` and two `locationType`.
At the moemnt, there is no order in them, so the RDF doesn't know which `locationType`
was used with which `objectType`.

**TODO-4: Ask Emma if the above can be problemantic.**

As far as I know, the human actions and the robot actions that share the same suffix are
supposed to happen at the same time. For example, `p01_s00_h00` happens while
`p01_s00_r00` is happening, and `p01_s00_h01` happens while `p01_s00_r01` happens. In
this example, there are two human actions and four robot actions. This happened since
this data was collected in 2022, but the new data in 2024 won't have this problem. That
is, the number of human actions is always equal to that of robot acitons.

**TODO-5: Ask Emma if the above is true.**

## Graph learning

The above data can be considered as tuples. That is, for every situation, there is a
tuple _(situation, human-robot actions)_, where _situation_ is a node and _human-robot
actions_ is a sequence of nodes. As elaborated above, each node is a set of key-value
pairs. These key-value pairs can also be understood as graphs. Below is a graph
representation of the node `p01_s00_h00`.

![alt text](<p01_s00 as a graph.png>)

Now the keys are relations and the values are entities. This is completely fine, since
in RDF, properties with their literal values can also be represented as relations and
literal entities.

The data used here is from 2022. This data does not include reward. However, the 2024
data will have a reward. That is, the tuples can be _(situation, human-robot actions,
reward)_. From the contextual bandit point of view, these tuples can be considered as
(state, action, reward), and we can learn an optimal policy from them.

**TODO-5: Double check with Emma if obtaining (situation, human-robot actions, reward)
is easy.**

_(situation, human-robot actions)_ pairs are very likely to be duplicate. However, it's
likely that the participants have described the same situation and human-robot actions
differently. This is indeed inevitable, since they were asked to describe their
situations and human-robot actions by drag-dropping boxes. In order to find common
_(situation, human-robot actions)_ tuples, we can perform graph learning. There are two
ways to achieve this:

### 1. Symbolic Inductive Reasoning

Symbolic inductive reasoning involves using logic-based techniques to infer new
knowledge from known facts. This approach is particularly suited for knowledge graphs
because they inherently represent facts and relationships in a formal structure. Here's
how you can use symbolic inductive reasoning for comparing knowledge graphs:

- Canonicalization: Normalize the graphs by renaming blank nodes or variables so that
  equivalent entities across different graphs have the same identifier. This step helps
  in aligning the graphs structurally.
- Subgraph Isomorphism: Determine if one graph is isomorphic to a subgraph of another,
  which would imply a structural similarity or exact match between them. Tools like
  SPARQL can be used to query if one set of RDF triples can be found within another.
- Graph Matching Algorithms: Apply algorithms that can find similarities in graph
  structures. Techniques such as the Weisfeiler-Lehman graph kernel or other kernel
  methods can be effective. These algorithms treat graphs in a way that allows for a
  similarity score to be computed, comparing node and edge labels (properties and
  relationships in RDF terms).
- Rule-based Matching: Develop or use existing ontological rules that can logically
  deduce relationships or entity equivalences across graphs. For example, if two graphs
  contain different triples that can be logically inferred to mean the same thing
  through a set of rules, they can be considered similar.

### 2. Sub-symbolic Graph Neural Network (GNN) Approach

Graph neural networks (GNNs) are a powerful tool for learning on graph-structured data.
They can automatically learn to encode graph structure into low-dimensional embeddings,
which can then be used to compare graphs. Here’s how to use GNNs for this purpose:

- Graph Embedding: Use a GNN model to create embeddings for each knowledge graph. Each
  graph is processed as a whole, with node features (if available) and the adjacency
  matrix serving as input to the network. The GNN learns to embed nodes in a way that
  captures both their features and their connectivity.
- Graph Similarity: Once embeddings for the graphs are obtained, compare these
  embeddings to measure graph similarity. Techniques like cosine similarity or Euclidean
  distance between the aggregated node embeddings of two graphs can be used to quantify
  similarity.
- Training the GNN: Depending on the specific task, you might train the GNN in a
  supervised manner (if labels for graph similarity are available) or use unsupervised
  methods to learn embeddings that reflect structural and semantic similarities. For
  instance, autoencoder architectures can be adapted for graphs (Graph Autoencoders) to
  learn embeddings by reconstructing the adjacency matrix.
- Graph Classification or Clustering: After training, use the embeddings for downstream
  tasks like graph classification or clustering. Graphs that cluster together can be
  considered similar based on the learned features.

I didn't do any of the above two approaches yet. I'll try soon when I get the reward
values. (state, action) tuples with high rewards are probably more useful.