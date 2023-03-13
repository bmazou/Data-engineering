from rdflib import Graph, BNode, Literal, Namespace
from rdflib.namespace import QB, RDF, XSD

SDMX_CONCEPT = Namespace("http://purl.org/linked-data/sdmx/2009/concept#")
SDMX_DIMENSION = Namespace("http://purl.org/linked-data/sdmx/2009/dimension#")
SDMX_MEASURE = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")
DCT = Namespace("http://purl.org/dc/terms/")
NS = Namespace("http://example.org/ns/")
NSR = Namespace("http://example.org/nsr/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


def create_structure(collector: Graph, dimensions, measures):
    structure = NS.structure
    collector.add( ( structure, RDF.type, QB.DataStructureDefinition ) )
    
    for dimension in dimensions:
        component = BNode()
        collector.add((structure, QB.component, component))
        collector.add((component, QB.dimension, dimension))

    for measure in measures:
        component = BNode()
        collector.add((structure, QB.component, component))
        collector.add((component, QB.measure, measure))

    return structure

def bind_namespaces(collector: Graph):
    collector.bind("nsr", NSR)
    collector.bind("ns", NS)
    collector.bind("skos", SKOS)
    collector.bind("qb", QB)
    collector.bind("xsd", XSD)
    collector.bind("rdfs", RDFS)
    collector.bind("rdf", RDF)
    collector.bind("sdmx-concept", SDMX_CONCEPT)
    collector.bind("sdmx-dimension", SDMX_DIMENSION)
    collector.bind("sdmx-measure", SDMX_MEASURE)
    collector.bind("dct", DCT)

def create_okres_kraj(collector: Graph):
    okres = NS.okres
    collector.add((okres, RDF.type, RDFS.Property))
    collector.add((okres, RDF.type, QB.DimensionProperty))
    collector.add((okres, RDFS.subPropertyOf, SDMX_DIMENSION.refArea))
    collector.add((okres, SKOS.prefLabel, Literal("CZ-NUTS kód okresu", lang="cs")))
    collector.add((okres, SKOS.prefLabel, Literal("CZ-NUTS code of county", lang="en")))
    collector.add((okres, RDFS.range, XSD.string))
    collector.add((okres, QB.concept, SDMX_CONCEPT.refArea))
    
    kraj = NS.kraj
    collector.add((kraj, RDF.type, RDFS.Property))
    collector.add((kraj, RDF.type, QB.DimensionProperty))
    collector.add((kraj, RDFS.subPropertyOf, SDMX_DIMENSION.refArea))
    collector.add((kraj, SKOS.prefLabel, Literal("CZ-NUTS kód kraje", lang="cs")))
    collector.add((kraj, SKOS.prefLabel, Literal("CZ-NUTS code of region", lang="en")))
    collector.add((kraj, RDFS.range, XSD.string))
    collector.add((kraj, QB.concept, SDMX_CONCEPT.refArea))

    return [okres, kraj]


def add_shared_metadata(collector: Graph):
    # Add dct:source
    collector.add((NSR.data, DCT.source, Literal("Český statistický úřad", lang="cs")))
    collector.add((NSR.data, DCT.source, Literal("Czech Statistical Office", lang="en")))

    # Add dct:issued
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    collector.add((NSR.data, DCT.issued, Literal(now, datatype=XSD.date)))
    
    # Add dct:modified
    collector.add((NSR.data, DCT.modified, Literal(now, datatype=XSD.date)))
    
    # Add dct:subject
    collector.add((NSR.data, DCT.subject, Literal("Population", lang="en")))
    collector.add((NSR.data, DCT.subject, Literal("Populace", lang="cs")))
    
    # Add dct:publisher
    collector.add((NSR.data, DCT.publisher, NSR.czech_statistical_organization))
    
    # Add dct:license
    collector.add((NSR.data, DCT.license, Literal("https://creativecommons.org/licenses/by/4.0/", datatype=XSD.anyURI)))
    

def save_data_cube(data_cube, path):
    with open(path, "w", encoding="utf8") as f:
        f.write(data_cube.serialize(format="ttl"))