import population_loader
import utils
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import QB, RDF, XSD

SDMX_CONCEPT = Namespace("http://purl.org/linked-data/sdmx/2009/concept#")
SDMX_DIMENSION = Namespace("http://purl.org/linked-data/sdmx/2009/dimension#")
SDMX_MEASURE = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")
DCT = Namespace("http://purl.org/dc/terms/")
NS = Namespace("http://example.org/ns/")
NSR = Namespace("http://example.org/nsr/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
KRAJ = Namespace("http://ruian.linked.opendata.cz/resource/region/")
OKRES = Namespace("http://ruian.linked.opendata.cz/resource/okres/")

def create_dimensions(collector: Graph):
    return utils.create_okres_kraj(collector)


def create_measure(collector: Graph):
    mean_population = NS.mean_population
    collector.add( ( mean_population, RDF.type, RDFS.Property))
    collector.add( ( mean_population, RDF.type, QB.MeasureProperty ) )
    collector.add( ( mean_population, SKOS.prefLabel, Literal("Počet obyvatel", lang="cs") ) )
    collector.add( ( mean_population, SKOS.prefLabel, Literal("Population count", lang="en") ) )
    collector.add( ( mean_population, RDFS.range, XSD.integer ) )
    collector.add( ( mean_population, RDFS.subPropertyOf, SDMX_MEASURE.obsValue ) )

    return [mean_population]


def create_dataset(collector: Graph, structure):
    dataset = NSR.PopulationDataCube
    collector.add((dataset, RDF.type, QB.DataSet))
    collector.add((dataset, QB.structure, structure))
    
    utils.add_metadata(collector,
                        dataset,
                        "Mean population",
                        "Střední stav obyvatel",
                        "Mean population of czech counties and regions", 
                        "Střední stav obyvatel okrsků a krajů",
                        "Mean population, depending on the county and region",
                        "Střední stav obyvatel, v závislosti na okrese a kraji",
                        "Population",
                        "Populace")
    

    return dataset


def create_observations(collector: Graph, dataset, data):
    for index, (dimension, count) in enumerate(data.items()):
        g = NSR["observation-" + str(index).zfill(3)]
        create_observation(collector, dataset, g, dimension, count) 


def create_observation(collector: Graph, dataset, g, dimension, count):
    collector.add((g, RDF.type, QB.Observation))
    collector.add((g, QB.dataSet, dataset))
    
    collector.add((g, NS.mean_population, Literal(count, datatype=XSD.integer)))

    okres, kraj = dimension.split("---")
    kraj_iri = KRAJ[kraj]
    okres_iri = OKRES[okres]
    collector.add((g, NS.kraj, URIRef(kraj_iri)))
    collector.add((g, NS.okres, URIRef(okres_iri)))


def as_data_cube(data):
    g = Graph()
    dimensions = create_dimensions(g)
    measures = create_measure(g)
    structure = utils.create_structure(g, dimensions, measures)
    dataset = create_dataset(g, structure)
    utils.create_skos_hierarchy(g)
    create_observations(g, dataset, data)
    utils.bind_namespaces(g)
    
    return g


def main():
    data = population_loader.load_data("data/pohyb-obyvatel.csv")
    data_cube = as_data_cube(data)
    utils.save_data_cube(data_cube, "output/population.ttl")
    

if __name__ == "__main__":
    main()