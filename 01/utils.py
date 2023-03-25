from rdflib import Graph, BNode, Literal, Namespace
from rdflib.namespace import QB, RDF, XSD

SDMX_CONCEPT = Namespace("http://purl.org/linked-dataCubeInstance/sdmx/2009/concept#")
SDMX_DIMENSION = Namespace("http://purl.org/linked-dataCubeInstance/sdmx/2009/dimension#")
SDMX_MEASURE = Namespace("http://purl.org/linked-dataCubeInstance/sdmx/2009/measure#")
DCT = Namespace("http://purl.org/dc/terms/")
NS = Namespace("http://example.org/ns/")
NSR = Namespace("http://example.org/nsr/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
KRAJ = Namespace("http://ruian.linked.opendata.cz/resource/region/")
OKRES = Namespace("http://ruian.linked.opendata.cz/resource/okres/")


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
    collector.bind("kraj", KRAJ)
    collector.bind("okres", OKRES)


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


def add_metadata(collector: Graph, en_prefLabel, cz_prefLabel, en_title, cz_title, en_description, cz_description, en_subject, cz_subject):
    # Add skos:prefLabel
    collector.add((NSR.dataCubeInstance, SKOS.prefLabel, Literal(en_prefLabel, lang="en")))
    collector.add((NSR.dataCubeInstance, SKOS.prefLabel, Literal(cz_prefLabel, lang="cs")))

    # Add dct:issued
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    collector.add((NSR.dataCubeInstance, DCT.issued, Literal(now, datatype=XSD.date)))

    # Add dct:modified
    collector.add((NSR.dataCubeInstance, DCT.modified, Literal(now, datatype=XSD.date)))
    
    # Add dct:publisher
    collector.add((NSR.dataCubeInstance, DCT.publisher, NSR.czech_statistical_organization))

    # Add dct:source
    collector.add((NSR.dataCubeInstance, DCT.source, Literal("Český statistický úřad", lang="cs")))
    collector.add((NSR.dataCubeInstance, DCT.source, Literal("Czech Statistical Office", lang="en")))

    # Add dct:license
    collector.add((NSR.dataCubeInstance, DCT.license, Literal("https://creativecommons.org/licenses/by/4.0/", datatype=XSD.anyURI)))
    
    
    # Add dct:subject
    collector.add((NSR.dataCubeInstance, DCT.subject, Literal(en_subject, lang="en")))
    collector.add((NSR.dataCubeInstance, DCT.subject, Literal(cz_subject, lang="cs")))
        
    # Add dct:title
    collector.add((NSR.dataCubeInstance, DCT.title, Literal(en_title, lang="en")))
    collector.add((NSR.dataCubeInstance, DCT.title, Literal(cz_title, lang="cs")))
    
    # Add dct:label
    collector.add((NSR.dataCubeInstance, DCT.label, Literal(en_title, lang="en")))
    collector.add((NSR.dataCubeInstance, DCT.label, Literal(cz_title, lang="cs")))

    # Add dct:description
    collector.add((NSR.dataCubeInstance, DCT.description, Literal(en_description, lang="en")))
    collector.add((NSR.dataCubeInstance, DCT.description, Literal(cz_description, lang="cs")))
    
    # Add dct:comment
    collector.add((NSR.dataCubeInstance, DCT.comment, Literal(en_description, lang="en")))
    collector.add((NSR.dataCubeInstance, DCT.comment, Literal(cz_description, lang="cs")))
    

def save_data_cube(data_cube, path):
    with open(path, "w", encoding="utf8") as f:
        f.write(data_cube.serialize(format="ttl"))