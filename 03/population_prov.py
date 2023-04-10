from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD, PROV, RDFS, SKOS, FOAF

import prov_utils

NSR = Namespace("http://example.org/nsr/")
NSP = Namespace("http://example.org/provenance#")

def create_agents(g: Graph):
    author = NSP.BedrichMazourek
    creation_script = NSP.PopulationCreatorAgent
    
    def add_creation_script():
        g.add( (creation_script, RDF.type, PROV.SoftwareAgent) )
        g.add( (creation_script, SKOS.definition, Literal("Script for creating population data cube", lang="en")) )
        g.add( (creation_script, SKOS.definition, Literal("Skript pro vytvoření datové kostky o pohybu obyvatel", lang="cs")) )
        g.add( (creation_script, PROV.actedOnBehalfOf, author) )

        location = URIRef("file://../../01/population.py")
        g.add( (creation_script, PROV.atLocation, location) )
        g.add( (location, RDF.type, PROV.Location) )
        
    add_creation_script()
    prov_utils.add_shared_agents(g)

def create_activities(g: Graph):
    population_creating = NSP.PopulationCreatingActivity
    script_association = BNode()

    def add_population_creating():
        g.add( (population_creating, RDF.type, PROV.Activity) )
        g.add( (population_creating, PROV.qualifiedAssociation, script_association) )
        g.add( (population_creating, PROV.used, NSR.NutsCodesDatasetEntity) )
        g.add( (population_creating, PROV.used, NSR.PopulationDatasetEntity) )
        g.add( (population_creating, PROV.generated, NSR.PopulationDataCube) )
        g.add( (population_creating, PROV.startedAtTime, Literal("2021-04-09T14:40:00", datatype=XSD.dateTime)) )
        g.add( (population_creating, PROV.endedAtTime, Literal("2021-04-09T14:41:00", datatype=XSD.dateTime)) )
    
    add_population_creating()
    prov_utils.add_qualified_assoc(g, script_association, NSP.PopulationCreatorAgent)
            

def create_entities(g: Graph):
    data_cube = NSR.PopulationDataCube
    code_dataset = NSR.NutsCodesDatasetEntity
    population_dataset = NSR.PopulationDatasetEntity
    
    def add_population_dataset():
        g.add( (population_dataset, RDF.type, PROV.Entity) )
        g.add( (population_dataset, PROV.wasAttributedTo, NSP.CeskyStatistickyUradAgent) )
        g.add( (population_dataset, SKOS.definition, Literal("Pohyb obyvatel za ČR, kraje, okresy, SO ORP a obce - rok 2021", lang="cs")) )
        g.add( (population_dataset, SKOS.definition, Literal("Population movement for Czech republic, regions, counties, SO ORP and municipalities - year 2021", lang="en")) )
        g.add( (population_dataset, RDFS.seeAlso, URIRef("https://data.gov.cz/datov%C3%A1-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatov%C3%A9-sady%2F00025593%2F12032e1445fd74fa08da79b14137fc29")) )
        
        location = URIRef("file://../../01/data/pohyb-obyvatel.csv")
        g.add( (population_dataset, PROV.atLocation, location) )
        g.add( (location, RDF.type, PROV.Location) )
        
    def add_code_dataset():
        g.add( (code_dataset, RDF.type, PROV.Entity) )
        g.add( (code_dataset, PROV.wasAttributedTo, NSP.CeskyStatistickyUradAgent) )
        g.add( (code_dataset, SKOS.definition, Literal("Kódování okresů a krajů v ČR", lang="cs")) )
        g.add( (code_dataset, SKOS.definition, Literal("Coding of counties and regions in Czech republic", lang="en")) )
        
        location = URIRef("file://../../01/data/ciselnik-okresu.csv")
        g.add( (code_dataset, PROV.atLocation, location) )
        g.add( (location, RDF.type, PROV.Location) )

    def add_data_cube():
        g.add( (data_cube, RDF.type, PROV.Entity) )
        g.add( (data_cube, PROV.wasDerivedFrom, population_dataset) )
        g.add( (data_cube, PROV.wasDerivedFrom, code_dataset) )
        g.add( (data_cube, PROV.wasAttributedTo, NSP.PopulationCreatorAgent) )
        g.add( (data_cube, PROV.wasGeneratedBy, NSP.PopulationCreatingActivity) )
        g.add( (data_cube, SKOS.definition, Literal("Mean population for Czech republic in 2021", lang="en")) )
        g.add( (data_cube, SKOS.definition, Literal("Střední stav obyvatel okrsků a krajů v roce 2021", lang="cs")) )
        
        location = URIRef("file://../../01/output/population.ttl")
        g.add( (data_cube, PROV.atLocation, location) )
        g.add( (location, RDF.type, PROV.Location) )

    add_population_dataset()
    add_code_dataset()
    add_data_cube()


def create_prov():
    g = Graph(bind_namespaces="rdflib")
    
    create_entities(g)
    create_activities(g)
    create_agents(g)
    prov_utils.bind_namespaces(g)

    return g

def main():
    data = create_prov()
    prov_utils.save_prov_graph(data)

if __name__ == "__main__":
    main()