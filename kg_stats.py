## print statistics for the data on an endpoint
## call like:
##   python print_stats.py <endpoint> [output_file_path]
##   python print_stats.py http://localhost:9090/test/query/ stats.txt
##   python print_stats.py http://localhost:9090/test/query/ 


from SPARQLWrapper import SPARQLWrapper, JSON
import sys
import argparse

# some sparql endpoints
dbpedia = "http://dbpedia.org/sparql"
ckg_local = "http://localhost:9090/ckg/query/"
ckg = "http://eb4.cs.umbc.edu:9090/ckg/query/"
default_endpoint = ckg_local

#####  Queries to gather information about a dataset #####

class_query = """
# find classes and their number instances
select ?class (count(?instance) as ?instances) where {
    ?instance a ?class
}
group by ?class
order by desc(?instances)"""

object_predicate_query = """
# find predicates that have an object as a value
select ?predicate (count(?object) as ?objects) where {
    ?subject ?predicate ?object
    filter (! isliteral(?object)).
}
group by ?predicate
order by desc(?objects)"""

data_predicate_query = """
# find predicates that have literal values
select ?predicate (count(?object) as ?objects) where {
    ?subject ?predicate ?object
    filter (isliteral(?object)).
}
group by ?predicate
order by desc(?objects) """

##### common namespaces we use to make the printout easier to read #####

namespaces = []
for line in open('namespaces.txt'):
    _, prefix, uri, _ = line.strip().split(' ')
    prefix = prefix[:-1]  # strip final :
    uri = uri[1:-1]       # strip angle brackets
    namespaces.append((prefix, uri))

def qnamify(url, prefixes=namespaces):
    """ returns a qualified URI if the url states with a prefix we recongnize, else the url"""
    if url.startswith('http'):
        for prefix, ns in prefixes:
            if url.startswith(ns):
                return prefix + ':' + url.split(ns)[1]
    return url

def ask(query, endpoint=default_endpoint):
    """ send a query to the endpoint and use namespaces to make results more compact
    """
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        yield([qnamify(v['value']) for v in result.values()])

def get_stats(endpoint=default_endpoint, fileout=sys.stdout):
    if fileout == sys.stdout:
        out = fileout
    else:
        out = open(fileout, 'w')

    out.write("ENDPOINT: {}\n\n".format(endpoint))
            
    out.write("DATA PROPERTIES\n\n")
    for item, number in ask(data_predicate_query, ckg):
        out.write("{}\t{}\n".format(item, number))

    out.write("\n\nOBJECT PROPERTIES\n\n")
    for item, number in ask(object_predicate_query, ckg):
        out.write("{}\t{}\n".format(item, number))

    out.write("\n\nCLASSES\n\n")    
    for item, number in ask(class_query, ckg):
        out.write("{}\t{}\n".format(item, number))

    if out != sys.stdout:
        out.close

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'print basic statistics about a kb at an endpoint')
    parser.add_argument('endpoint', help='url of SPARQL endpoint for the rdf knowledge graph ')
    parser.add_argument('output', nargs='?', default=sys.stdout, help='file for output, defaults to stdout')
    args = parser.parse_args()
    get_stats(args.endpoint, args.output)
    
