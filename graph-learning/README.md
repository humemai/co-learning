# Graph Learning

## [`process-raw-data`](./process-raw-data.ipynb)

This jupyter notebook processes the raw data that Emma gave me. It processes them and saves `raw-data.json`.

### [`raw-data.json`](./raw-data.json)

This is a list of CPs. A CP is a `dict` object. An example CP looks like:

```json
{
  "cp_num": 0,
  "participant": 4069,
  "round": 3,
  "cp_name": "Label",
  "ticks_lasted": 117,
  "time_score": 2336,
  "situation": [[], []],
  "actionHuman": [
    [
      {
        "type": "actor",
        "content": "Human"
      },
      {
        "type": "action",
        "content": "Stand still in <location>"
      },
      {
        "type": "location",
        "content": "<Left> side of field"
      }
    ],
    [],
    []
  ],
  "actionRobot": [
    [
      {
        "type": "action",
        "content": "Break <object> in <location>"
      },
      {
        "type": "object",
        "content": "Brown rock"
      }
    ],
    [],
    []
  ]
}
```

## [`make-rdf-data.ipynb`](./make-rdf-data.ipynb)

This makes them into RDF-turtle files and saves them at [`user-raw-data`](./user-raw-data). There are in total of 192 CPs (graphs) saved. Also take a look at [`ontology.ttl`](./ontology.ttl).
