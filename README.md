# Wikidata Tools

A collection of scripts for working with Wikidata dumps.

## wd2rdf.py

This script takes the JSON dump format and extracts out a subset of the
information as RDF data.

The output is NTriples format so it works well with unix pipes.
The script is designed to avoid ever loading the full dataset in memory.

The file can be imported into things like GraphDB or indeed subsets can be
extracted via grep to make smaller chunks of data.

The script depends on:

- rdflib
- pydash
- tqdm

Usage:

```bash
python wd2rdf.py <latest-all.json.bz2 >output.nt
```

Limitations:

- Only English labels are extracted. All literals become language-less with English presumed.
- Therefore, only entities that have an English label are extracted
- Only pure s/p/o triples are created, so all the rich attributes qualifying properties will be lost

This produces just under 150GB of data at time of writing.

What works:

- Dates are marked as XSD date types
- Entities are extracted as URIs, all other strings are just string literals
