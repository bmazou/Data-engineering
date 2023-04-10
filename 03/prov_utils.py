from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD, PROV, RDFS, SKOS, FOAF

NSR = Namespace("http://example.org/nsr/")
NSP = Namespace("http://example.org/provenance#")


def add_shared_agents(g: Graph):
    author = NSP.BedrichMazourek
    director = NSP.PetrSkoda
    school = NSP.MatematickoFyzikalniFakulta
    urad = NSP.CeskyStatistickyUradAgent
    
    def add_school():
        g.add( (school, RDF.type, PROV.Agent) )
        g.add( (school, RDF.type, PROV.Organization) )
        g.add( (school, FOAF.name, Literal("Matematicko-fyzikální fakulta Univerzity Karlovy", lang="cs")) )
        g.add( (school, FOAF.schoolHomepage, Literal("https://www.mff.cuni.cz", datatype=XSD.anyURI)) )
    
    def add_director():
        g.add( (director, RDF.type, PROV.Agent) )
        g.add( (director, RDF.type, PROV.Person) )
        g.add( (director, FOAF.name, Literal("Petr Skoda", lang="cs")) )
        g.add( (director, FOAF.mbox, URIRef("mailto:petr.skoda@matfyz.cuni.cz")) )
        g.add( (director, FOAF.homepage, Literal("https://github.com/skodapetr", datatype=XSD.anyURI)) )
        g.add( (director, PROV.actedOnBehalfOf, school) )
   
    def add_author():
        g.add( (author, RDF.type, PROV.Agent) )
        g.add( (author, RDF.type, PROV.Person) )
        g.add( (author, FOAF.name, Literal("Bedřich Mazourek", lang="cs")) )
        g.add( (author, FOAF.mbox, URIRef("mailto:codprojmail@gmail.com")) )
        g.add( (author, FOAF.homepage, Literal("https://github.com/bmazou", datatype=XSD.anyURI)) )
        g.add( (author, PROV.actedOnBehalfOf, director) )
    
    def add_urad():
        g.add( (urad, RDF.type, PROV.Agent) )
        g.add( (urad, RDF.type, FOAF.Organization) )
        g.add( (urad, SKOS.prefLabel, Literal("Český statistický úřad", lang="cs")) )
        g.add( (urad, SKOS.prefLabel, Literal("Czech Statistical Office", lang="en")) )
        g.add( (urad, RDFS.seeAlso, URIRef("https://www.czso.cz/")) )
    
    add_school()
    add_director()
    add_author()
    add_urad()
    
def add_qualified_assoc(g: Graph, association, agent):
    g.add( (association, RDF.type, PROV.Association) )
    g.add( (association, PROV.agent, agent) )
    g.add( (association, PROV.hadRole, NSP.CreatorRole) )
    g.add( (association, RDFS.comment, Literal("Python script created the data cube", lang="en")) )

    g.add( (NSP.CreatorRole, RDF.type, PROV.Role) )
    g.add( (NSP.CreatorRole, SKOS.definition, Literal("Datacube creator", lang="en")) )
    g.add( (NSP.CreatorRole, SKOS.definition, Literal("Tvůrce datové kostky", lang="cs")) )
    
    
def save_prov_graph(g: Graph):
    def get_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file_name", help="File name", default=None)
        args = parser.parse_args()
        return args

    args = get_args()
    if args.file_name is not None:
        output_path = "output/" + args.file_name
        g.serialize(destination=output_path, format="trig")
    else:
        print("File name not specified. Data will not be saved.")

    
def bind_namespaces(g: Graph):
    g.bind("prov", PROV)
    g.bind("nsr", NSR)
    g.bind("nsprov", NSP)
    g.bind("rdfs", RDFS)
    g.bind("skos", SKOS)
    g.bind("foaf", FOAF)
    g.bind("xsd", XSD)