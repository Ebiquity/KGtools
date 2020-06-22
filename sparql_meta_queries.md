# Adapted from [Sparql Playground](http://sparql-playground.sib.swiss/) and other sources

## Add the following prefixes or others to the queries as needed

```
PREFIX  rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
```

## what the data look like?

```
SELECT * WHERE {?subject ?predicate ?object . }
LIMIT 10
```

## How many triples in the dataset?

```
SELECT (COUNT(*) AS ?no)  WHERE { ?s ?p ?o  }
```

## What classes are defined?

```
SELECT distinct ?class
WHERE { {?class a rdfs:Class} UNION {?class a owl:Class} }
order by ?class
```

## Number of immediate instances of  class XXX

```
SELECT (COUNT(?s) AS ?totalNumberOfInstances)
WHERE { ?s a XXX}
```

## Number of immediate or indirect instances of class XXX

```
SELECT (COUNT(?s) AS ?totalNumberOfInstances)
WHERE { ?s rdfs:type/rdfs:subclassOf* XXX}
```

## Number of immediate instances of all classes

```
SELECT ?class (count(?instance) as ?numberOfInstances)
WHERE { ?instance a ?class . }
group by ?class
order by desc(?numberOfInstances)
```

## What properties are used?

```
SELECT DISTINCT ?property
WHERE { ?s ?property ?o . }
```

## Which classes use property XXX?

```
SELECT DISTINCT ?class
WHERE {
    ?subject XYZZY ?o .
    ?subject a ?class . }
```

## How often is a property XXX used

```
SELECT (COUNT(*) AS ?total)
WHERE { ?s XXX ?o }
```

# How often has each property been used?

```
SELECT ?property (COUNT(?property) AS ?propTotal)
WHERE { ?s ?property ?o . }
GROUP BY ?property
ORDER BY DESC(?propTotal)
```
