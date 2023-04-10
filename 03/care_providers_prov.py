from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD, PROV, RDFS, SKOS, FOAF

import prov_utils

NSR = Namespace("http://example.org/nsr/")
NSP = Namespace("http://example.org/provenance#")

def create_agents(g: Graph):
    author = NSP.BedrichMazourek
    creation_script = NSP.CareProvidersCreatorAgent
    
    def add_creation_script():
        g.add( (creation_script, RDF.type, PROV.SoftwareAgent) )
        g.add( (creation_script, SKOS.definition, Literal("Script for creating care providers data cube", lang="en")) )
        g.add( (creation_script, SKOS.definition, Literal("Skript pro vytvoření datové kostky o poskytovatelích péče", lang="cs")) )
        g.add( (creation_script, PROV.actedOnBehalfOf, author) )

        location = URIRef("file://../../01/care_providers.py")
        g.add( (creation_script, PROV.atLocation, location) )
        g.add( (location, RDF.type, PROV.Location) )
    
    add_creation_script()
    prov_utils.add_shared_agents(g)

def create_activities(g: Graph):
    providers_creating = NSP.CareProvidersCreatingActivity
    script_association = BNode()

    def add_providers_creating():
        g.add( (providers_creating, RDF.type, PROV.Activity) )
        g.add( (providers_creating, PROV.qualifiedAssociation, script_association) )
        g.add( (providers_creating, PROV.used, NSR.CareProvidersDatasetEntity) )
        g.add( (providers_creating, PROV.generated, NSR.CareProvidersDataCube) )
        g.add( (providers_creating, PROV.startedAtTime, Literal("2021-04-09T14:42:00", datatype=XSD.dateTime)) )
        g.add( (providers_creating, PROV.endedAtTime, Literal("2021-04-09T14:43:00", datatype=XSD.dateTime)) )
    
    add_providers_creating()
    prov_utils.add_qualified_assoc(g, script_association, NSP.CareProvidersCreatorAgent)
            

def create_entities(g: Graph):
    data_cube = NSR.CareProvidersDataCube
    providers_dataset = NSR.CareProvidersDatasetEntity
    
    def add_providers_dataset():
        g.add( (providers_dataset, RDF.type, PROV.Entity) )
        g.add( (providers_dataset, PROV.wasAttributedTo, NSP.CeskyStatistickyUradAgent) )
        g.add( (providers_dataset, SKOS.definition, Literal("Národní registr poskytovatelů zdravotních služeb", lang="cs")) )
        g.add( (providers_dataset, SKOS.definition, Literal("National Register of Health Service Providers", lang="en")) )
        g.add( (providers_dataset, RDFS.seeAlso, URIRef("https://data.gov.cz/datov%C3%A1-sada?iri=https://data.gov.cz/zdroj/datov%C3%A9-sady/https---opendata.mzcr.cz-api-3-action-package_show-id-nrpzs")) )
        
        location = URIRef("file://../../01/data/care_providers.csv")
        g.add( (providers_dataset, PROV.atLocation, location) )
        g.add( (location, RDF.type, PROV.Location) )

    def add_data_cube():
        g.add( (data_cube, RDF.type, PROV.Entity) )
        g.add( (data_cube, PROV.wasDerivedFrom, providers_dataset) )
        g.add( (data_cube, PROV.wasAttributedTo, NSP.CareProvidersCreatorAgent) )
        g.add( (data_cube, PROV.wasGeneratedBy, NSP.CareProvidersCreatingActivity) )
        g.add( (data_cube, SKOS.definition, Literal("Number of given care providers in each county and region of the Czech republic", lang="en")) )
        g.add( (data_cube, SKOS.definition, Literal("Počet daných poskytovatelů péče v jednotlivých okresech a krajích ČR", lang="cs")) )
        
        location = URIRef("file://../../01/output/care_providers.ttl")
        g.add( (data_cube, PROV.atLocation, location) )
        g.add( (location, RDF.type, PROV.Location) )
        
    add_providers_dataset()
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