import bz2
import json
from pathlib import Path
from typing import Dict

import pydash
from rdflib import RDFS, Graph, Literal, Namespace, XSD
from rdflib.term import Identifier
from tqdm import tqdm


def wikidata(filename: str, progress_label="Wikidata"):
    with bz2.open(filename, mode="rt") as file_obj:
        # TODO: Hard-coded since we need the uncompressed size
        # is there a way to get this without full decompression?
        with tqdm(desc=progress_label, total=1523565366625) as pbar:
            file_obj.read(2)  # We expect the file to start with "{\n"
            pbar.update(2)
            for line in file_obj:
                yield json.loads(line.rstrip(",\n"))
                pbar.update(len(line))


WD = Namespace("http://www.wikidata.org/entity/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")


def snak2object(snak: Dict) -> Identifier:
    match pydash.get(snak, "mainsnak.datavalue.type"):
        case "string":
            return Literal(pydash.get(snak, "mainsnak.datavalue.value"))
        case "time":
            return Literal(pydash.get(snak, "mainsnak.datavalue.time"), datatype=XSD.dateTime)
        case "wikibase-entityid":
            return WD[pydash.get(snak, "mainsnak.datavalue.value.id")]


def main():
    for entity in wikidata("latest-all.json.bz2", progress_label=f"Wikidata"):
        label = pydash.get(entity, "labels.en.value")
        if not label:  # English-only to keep size down
            continue

        g = Graph()
        g.add(
            (
                WD[entity["id"]],
                RDFS.label,
                Literal(label),
            )
        )

        for prop, snaks in entity["claims"].items():
            prop_uri = WDT[prop]
            for snak in snaks:
                g.add(
                    (
                        WD[entity["id"]],
                        prop_uri,
                        snak2object(snak),
                    )
                )

        print(g.serialize(format="nt"))


if __name__ == "__main__":
    main()
