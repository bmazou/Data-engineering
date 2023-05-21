import my_utils.utils as utils
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCAT, FOAF, RDF, XSD

DCT = Namespace("http://purl.org/dc/terms/")
NS = Namespace("http://example.org/ns/")
NSR = Namespace("http://example.org/nsr/")
SPDX = Namespace("http://spdx.org/rdf/terms#")


def create_dcat(collector: Graph):
    def add_label():
        collector.add((dataset, DCT.label, Literal("Mean population of Czech regions and counties", lang="en")))
        collector.add((dataset, DCT.label, Literal("Průměrná populace českých krajů a okresů", lang="cs")))

    def add_description():
        collector.add((dataset, DCT.description, Literal("Mean population, depending on the county and region", lang="en")))
        collector.add((dataset, DCT.description, Literal("Průměrná populace, v závislosti na okrese a kraji", lang="cs")))
    
    def add_themes():
        demography_theme = URIRef("http://eurovoc.europa.eu/385")
        collector.add((dataset, DCAT.theme, demography_theme))
        
        human_geography_theme = URIRef("http://eurovoc.europa.eu/6388")
        collector.add((dataset, DCAT.theme, human_geography_theme))
    
    def add_publisher():
        publisher = NSR.BedrichMazourek
        collector.add((publisher, RDF.type, FOAF.Person))
        collector.add((publisher, FOAF.name, Literal("Bedřich Mazourek", lang="cs")))
        collector.add((publisher, FOAF.mbox, URIRef("mailto:codprojmail@gmail.com")))
        collector.add((publisher, FOAF.homepage, Literal("https://github.com/bmazou", datatype=XSD.anyURI)))
        collector.add((dataset, DCT.publisher, publisher))

    def add_spatial():
        czech_republic = URIRef("http://publications.europa.eu/resource/authority/country/CZE")
        collector.add((dataset, DCT.spatial, czech_republic))
    
    def add_keywords():
        keywords_en = ["population", "Czech Republic", "regions", "counties"]
        keywords_cs = ["populace", "Česká republika", "kraje", "okresy"]
        for en_key, cs_key in zip(keywords_en, keywords_cs):
            collector.add((dataset, DCT.keyword, Literal(en_key, lang="en")))
            collector.add((dataset, DCT.keyword, Literal(cs_key, lang="cs")))
    
    def add_distribution():
        distribution = NSR.PopulationDataCubeDistribution
        collector.add((distribution, RDF.type, DCAT.Distribution))
        collector.add((distribution, DCT.title, Literal("Population data cube")))
        collector.add((distribution, DCAT.accessURL, URIRef("https://github.com/bmazou/Data-engineering-hw/blob/main/05/output/population.ttl")))
        collector.add((distribution, DCAT.mediaType, URIRef("http://publications.europa.eu/resource/authority/file-type/RDF_TURTLE")))

        # Add SPDX checksum information
        checksum = BNode()
        collector.add((distribution, SPDX.checksum, checksum))
        collector.add((checksum, RDF.type, SPDX.Checksum))
        collector.add((checksum, SPDX.algorithm, SPDX.checksumAlgorithm_sha1))
        fileHash = utils.get_file_hash("output/population.ttl")
        collector.add((checksum, SPDX.checksumValue, Literal(fileHash, datatype=XSD.hexBinary)))
        
    def add_accrual_periodicity():
        collector.add((dataset, DCT.accrualPeriodicity, URIRef("http://publications.europa.eu/resource/authority/frequency/NEVER")))
        
        
    dataset = NSR.PopulationDataCube
    collector.add((dataset, RDF.type, DCAT.Dataset))
    add_label()
    add_description()
    add_themes()
    add_publisher()
    add_spatial()
    add_keywords()
    add_distribution()
    add_accrual_periodicity()


def bind_namespaces(collector: Graph):
    collector.bind("dcat", DCAT)
    collector.bind("dct", DCT)
    collector.bind("foaf", FOAF)
    collector.bind("ns", NS)
    collector.bind("nsr", NSR)
    collector.bind("rdf", RDF)
    collector.bind("spdx", SPDX)


def main():
    g = Graph()
    create_dcat(g)    
    bind_namespaces(g)
    
    utils.save_data_cube(g, "population_dcat.ttl")

if __name__ == "__main__":
    main()