import csv

from my_utils.population_loader import load_data
from rdflib import BNode, Graph, Literal, Namespace, URIRef
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
COUNTRY = Namespace("http://example.org/country/")


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
    collector.bind("country", COUNTRY)


def create_okres_kraj(collector: Graph):
    okres = NS.okres
    collector.add((okres, RDF.type, RDFS.Property))
    collector.add((okres, RDF.type, QB.DimensionProperty))
    collector.add((okres, RDFS.subPropertyOf, SDMX_DIMENSION.refArea))
    collector.add((okres, SKOS.prefLabel, Literal("CZ-NUTS kód okresu", lang="cs")))
    collector.add((okres, SKOS.prefLabel, Literal("CZ-NUTS code of county", lang="en")))
    collector.add((okres, RDFS.range, OKRES.county))
    collector.add((okres, QB.concept, SDMX_CONCEPT.refArea))
    
    kraj = NS.kraj
    collector.add((kraj, RDF.type, RDFS.Property))
    collector.add((kraj, RDF.type, QB.DimensionProperty))
    collector.add((kraj, RDFS.subPropertyOf, SDMX_DIMENSION.refArea))
    collector.add((kraj, SKOS.prefLabel, Literal("CZ-NUTS kód kraje", lang="cs")))
    collector.add((kraj, SKOS.prefLabel, Literal("CZ-NUTS code of region", lang="en")))
    collector.add((kraj, RDFS.range, KRAJ.region))
    collector.add((kraj, QB.concept, SDMX_CONCEPT.refArea))

    return [okres, kraj]


def add_metadata(collector: Graph, data_cube_instance, en_prefLabel, cz_prefLabel, en_title, cz_title, en_description, cz_description, en_subject, cz_subject):
    # Add skos:prefLabel
    collector.add((data_cube_instance, SKOS.prefLabel, Literal(en_prefLabel, lang="en")))
    collector.add((data_cube_instance, SKOS.prefLabel, Literal(cz_prefLabel, lang="cs")))

    # Add dct:issued
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    collector.add((data_cube_instance, DCT.issued, Literal(now, datatype=XSD.date)))

    # Add dct:modified
    collector.add((data_cube_instance, DCT.modified, Literal(now, datatype=XSD.date)))
    
    # Add dct:publisher
    collector.add((data_cube_instance, DCT.publisher, NSR.czech_statistical_organization))

    # Add dct:source
    collector.add((data_cube_instance, DCT.source, Literal("Český statistický úřad", lang="cs")))
    collector.add((data_cube_instance, DCT.source, Literal("Czech Statistical Office", lang="en")))

    # Add dct:license
    collector.add((data_cube_instance, DCT.license, Literal("https://creativecommons.org/licenses/by/4.0/", datatype=XSD.anyURI)))
    
    
    # Add dct:subject
    collector.add((data_cube_instance, DCT.subject, Literal(en_subject, lang="en")))
    collector.add((data_cube_instance, DCT.subject, Literal(cz_subject, lang="cs")))
        
    # Add dct:title
    collector.add((data_cube_instance, DCT.title, Literal(en_title, lang="en")))
    collector.add((data_cube_instance, DCT.title, Literal(cz_title, lang="cs")))
    
    # Add dct:label
    collector.add((data_cube_instance, DCT.label, Literal(en_title, lang="en")))
    collector.add((data_cube_instance, DCT.label, Literal(cz_title, lang="cs")))

    # Add dct:description
    collector.add((data_cube_instance, DCT.description, Literal(en_description, lang="en")))
    collector.add((data_cube_instance, DCT.description, Literal(cz_description, lang="cs")))
    
    # Add dct:comment
    collector.add((data_cube_instance, DCT.comment, Literal(en_description, lang="en")))
    collector.add((data_cube_instance, DCT.comment, Literal(cz_description, lang="cs")))
    

def save_data_cube(data_cube, file_name):
    import os
    if not os.path.exists("output"):
        os.makedirs("output")
    
    path = "output/" + file_name
    with open(path, "w", encoding="utf8") as f:
        f.write(data_cube.serialize(format="ttl"))

def get_okres_name_dicti(path):
    """Creates a dictionary of NUTS codes and their names from a csv file.
    
    Args:
        path (str): Path to the csv file.
        
    Returns:
        dict: Dictionary of NUTS codes and their names.
    """
    okres_name = {}
    with open(path, "r", encoding="utf8") as stream:
        reader = csv.reader(stream)
        header = next(reader)  
        for line in reader:
            end_of_file = len(line) == 0
            if end_of_file: break
            

            nuts_pos = 4
            nuts = line[nuts_pos]
            
            name_pos = -1
            name = line[name_pos]
                        
            okres_name[nuts] = name
    
    return okres_name

def get_kraj_okres_dict(data):
    """ Creates a dictionary of regions and their counties.
    
    Args:
        data (list): List of strings in the format "okres---kraj".
    
    Returns:
        dict: Dictionary of regions and their counties.
    """
    okres_name = get_okres_name_dicti("data/ciselnik-okresu.csv")
    
    kraj_okres = {}
    for row in data:
        okres, kraj = row.split("---")
        if kraj not in kraj_okres:
            kraj_okres[kraj] = []

        kraj_okres[kraj].append((okres, okres_name[okres]))

    return kraj_okres
        
def create_skos_hierarchy(collector: Graph):
    """ Creates a SKOS hierarchy. It contains a top-level concept for the Czech republic, concepts for regions and their counties.

    Args:
        collector (Graph): RDF graph to which the data will be added.
    """
    
    def create_concept_scheme():
        hierarchy = NS.czech_republic_regions_and_counties
        collector.add( ( hierarchy, RDF.type, SKOS.ConceptScheme ) )
        collector.add( ( hierarchy, SKOS.hasTopConcept, COUNTRY.CZ ) )
        collector.add( ( hierarchy, SKOS.prefLabel, Literal("Czech republic regions and counties scheme", lang="en") ) )
        collector.add( ( hierarchy, SKOS.prefLabel, Literal("Schéma regionů a okresů České republiky", lang="cs") ) )
        
        collector.add( ( COUNTRY.CZ, RDF.type, SKOS.Concept ) )
        collector.add( ( COUNTRY.CZ, SKOS.prefLabel, Literal("Česká republika", lang="cs") ) )
        collector.add( ( COUNTRY.CZ, SKOS.prefLabel, Literal("Czech republic", lang="en") ) )

    def add_kraj_instances():
        data = load_data("data/pohyb-obyvatel.csv")
        kraj_okres = get_kraj_okres_dict(data)
        kraj_name = {"CZ020": "Středočeský kraj", "CZ031": "Jihočeský kraj", "CZ032": "Plzeňský kraj", "CZ041": "Karlovarský kraj", "CZ042": "Ústecký kraj", "CZ051": "Liberecký kraj", "CZ052": "Královéhradecký kraj", "CZ053": "Pardubický kraj", "CZ063": "Kraj Vysočina", "CZ064": "Jihomoravský kraj", "CZ071": "Olomoucký kraj", "CZ072": "Zlínský kraj", "CZ080": "Moravskoslezský kraj"}
        for kraj in kraj_okres:
            collector.add((KRAJ[kraj], RDF.type, SKOS.Concept))
            collector.add((COUNTRY.CZ, SKOS.narrower, KRAJ[kraj]))
            collector.add((KRAJ[kraj], SKOS.broader, COUNTRY.CZ))
            collector.add((KRAJ[kraj], SKOS.prefLabel, Literal(kraj_name[kraj], lang="cs")))
            

            for okres in kraj_okres[kraj]:
                nuts_code = okres[0]
                name = okres[1]
                collector.add((OKRES[nuts_code], RDF.type, SKOS.Concept))
                collector.add((OKRES[nuts_code], SKOS.prefLabel, Literal(name, lang="cs")))
                collector.add((KRAJ[kraj], SKOS.narrower, OKRES[nuts_code]))
                collector.add((OKRES[nuts_code], SKOS.broader, KRAJ[kraj]))

    create_concept_scheme()
    add_kraj_instances()
