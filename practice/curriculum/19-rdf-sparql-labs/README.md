# Module 16 — RDF + SPARQL Labs

## Goals

- Understand RDF triples, namespaces, and Turtle syntax
- Run Apache Jena Fuseki as a SPARQL endpoint in Docker
- Write SPARQL queries: SELECT, FILTER, OPTIONAL, GROUP BY
- Compare SQL and SPARQL approaches for the same dataset

## Prerequisites

- Docker & Docker Compose installed
- `curl` available
- Basic understanding of databases (Module 14 recommended)

## Setup

```bash
cd practice/curriculum/16-rdf-sparql-labs
docker compose up -d
```

Wait for Fuseki to start:

```bash
curl -s http://localhost:3030/$/ping
# Expected: returns timestamp
```

Fuseki UI is available at: http://localhost:3030

---

## Exercise 16.1 — RDF Basics (Turtle)

### Objective

Understand RDF triples (subject-predicate-object) and write a Turtle (.ttl) file by hand.

### Concepts

An RDF triple states a fact:

```
<subject>  <predicate>  <object> .
```

Example:

```turtle
<http://example.org/book/1>  <http://purl.org/dc/terms/title>  "Clean Code" .
```

With **prefixes** (namespaces) to shorten URIs:

```turtle
@prefix ex: <http://example.org/book/> .
@prefix dct: <http://purl.org/dc/terms/> .

ex:1  dct:title  "Clean Code" .
```

### Steps

1. Review the sample data:

```bash
cat data/sample.ttl
```

2. Understand the structure:
   - `@prefix` declarations define namespace shortcuts
   - Each resource (subject) has properties listed with `;` separator
   - Lists of values use `,` separator
   - Each statement ends with `.`

3. The file models: **Books**, **Authors**, **Publishers**, and **Languages**

### Key RDF Concepts

| Concept | Description | Example |
|---------|-------------|---------|
| URI | Unique identifier for a resource | `ex:book/1` |
| Literal | A data value | `"Clean Code"`, `464`^^xsd:integer |
| Triple | Subject-predicate-object fact | `ex:book/1 dct:title "Clean Code"` |
| Prefix | Namespace shortcut | `@prefix ex: <http://example.org/>` |
| Blank node | Anonymous resource | `_:publisher1` |

### Deliverables

- [data/sample.ttl](data/sample.ttl) — hand-crafted Turtle file

---

## Exercise 16.2 — Run Fuseki in Docker + Load Data

### Objective

Start Apache Jena Fuseki and load the TTL data into a dataset.

### Steps

1. Start Fuseki:

```bash
docker compose up -d
```

2. Create a dataset:

```bash
curl -s -X POST http://localhost:3030/$/datasets \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'dbName=books&dbType=tdb2'
```

Expected: `200 OK`

3. Upload the TTL file:

```bash
curl -s -X POST http://localhost:3030/books/data \
  -H 'Content-Type: text/turtle' \
  --data-binary @data/sample.ttl
```

Expected: triples loaded count

4. Verify the data:

```bash
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query=SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }" \
  -H 'Accept: application/json' | jq .
```

### Deliverables

- Running Fuseki with loaded RDF data

---

## Exercise 16.3 — SPARQL Query Practice

### Objective

Write SPARQL queries of increasing complexity.

### Steps

Run each query against Fuseki:

```bash
# General pattern to run a .rq file:
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query@queries/01_all_books.rq" \
  -H 'Accept: application/json' | jq '.results.bindings[] | {title: .title.value, author: .author.value}'
```

### Queries

1. **All books with authors:**

```bash
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query@queries/01_all_books.rq" \
  -H 'Accept: application/json' | jq '.results.bindings[]'
```

2. **Filter by year:**

```bash
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query@queries/02_filter_year.rq" \
  -H 'Accept: application/json' | jq '.results.bindings[]'
```

3. **Optional publisher info:**

```bash
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query@queries/03_optional_publisher.rq" \
  -H 'Accept: application/json' | jq '.results.bindings[]'
```

4. **Count books by language (GROUP BY):**

```bash
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query@queries/04_group_by_language.rq" \
  -H 'Accept: application/json' | jq '.results.bindings[]'
```

5. **Books with multiple authors:**

```bash
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query@queries/05_multi_author.rq" \
  -H 'Accept: application/json' | jq '.results.bindings[]'
```

### Deliverables

- [queries/01_all_books.rq](queries/01_all_books.rq)
- [queries/02_filter_year.rq](queries/02_filter_year.rq)
- [queries/03_optional_publisher.rq](queries/03_optional_publisher.rq)
- [queries/04_group_by_language.rq](queries/04_group_by_language.rq)
- [queries/05_multi_author.rq](queries/05_multi_author.rq)

---

## Exercise 16.4 — SQL vs SPARQL Equivalence

### Objective

Answer the same questions using both SQL and SPARQL to understand modeling differences.

### Steps

1. Load SQL data into Postgres (from Module 14):

```bash
docker exec -i pg_lab psql -U labuser -d labdb < sql/schema.sql
docker exec -i pg_lab psql -U labuser -d labdb < sql/seed.sql
```

2. Run SQL queries:

```bash
docker exec -i pg_lab psql -U labuser -d labdb < sql/queries.sql
```

3. Run equivalent SPARQL queries:

```bash
for f in sparql/*.rq; do
  echo "=== $(basename $f) ==="
  curl -s -G http://localhost:3030/books/query \
    --data-urlencode "query@$f" \
    -H 'Accept: application/json' | jq '.results.bindings[]'
  echo ""
done
```

### Key Modeling Differences

| Aspect | SQL | SPARQL/RDF |
|--------|-----|-----------|
| Schema | Fixed tables + columns | Flexible triples — no fixed schema |
| Joins | Explicit JOIN syntax | Implicit via triple patterns |
| Identity | Primary keys (integers) | URIs (globally unique) |
| Multi-valued | Junction tables | Multiple triples with same predicate |
| NULL values | NULL column | Triple simply doesn't exist |
| Types | Column data types | Optional `^^xsd:type` annotations |
| Querying | SQL against tables | SPARQL against graph |

### Deliverables

- [sql/schema.sql](sql/schema.sql)
- [sql/seed.sql](sql/seed.sql)
- [sql/queries.sql](sql/queries.sql)
- [rdf/books.ttl](rdf/books.ttl) (symlink or copy of data/sample.ttl)
- [sparql/*.rq](sparql/)
- [solutions/comparison.md](solutions/comparison.md)

---

## Cleanup

```bash
docker compose down -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Fuseki not starting | Check `docker compose logs fuseki` |
| Dataset not found | Create it: `curl -X POST localhost:3030/$/datasets -d 'dbName=books&dbType=tdb2'` |
| SPARQL syntax error | Validate at https://sparql.org/query-validator.html |
| Empty results | Verify data loaded: count triples query above |

## Next Steps

- Module 17: REST API CRUD Labs
- Cheatsheet: [SQL vs SPARQL vs Elasticsearch](../../../docs/cheatsheets/sql_vs_sparql_vs_es.md)
