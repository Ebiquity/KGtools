from SPARQLWrapper import SPARQLWrapper, JSON, POST

def number_of_triples(endpoint):
    """ returns the number of triples in the endpoint """
    return ask(endpoint, "SELECT (COUNT(*) AS ?n) WHERE {?s ?p ?o}")

def ask(endpoint, query):
    """ sends query to the endpoint and returns a stream of tuples
        with the values of the query's variables """
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        yield (tuple([v['value'] for v in result.values()]))

def update(endpoint, query):
    """ insert, delete and update queries should be sent using a post method and don't return a useful value """
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setMethod(POST)
    results = sparql.query().convert()
    return results
        
def number_of_triples(endpoint):
    """ returns the number of triples in the endpoint """
    return int(next(ask(endpoint, "SELECT (COUNT(*) AS ?n) WHERE {?s ?p ?o}"))[0])
    
