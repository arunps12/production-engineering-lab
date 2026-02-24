# SECTION 19 — RDF & SPARQL LABS

---

## PART A — CONCEPT EXPLANATION

### What is RDF?

RDF (Resource Description Framework) is a W3C standard for representing knowledge as a graph of interconnected facts. Every fact is a **triple**: subject → predicate → object.

```
Subject          Predicate          Object
──────────       ──────────         ──────
ex:book/1   →   dct:title     →   "Clean Code"
ex:book/1   →   schema:author →   ex:author/1
ex:author/1 →   schema:name   →   "Robert C. Martin"
```

This creates a **knowledge graph**:

```
            dct:title
ex:book/1 ──────────→ "Clean Code"
    │
    │ schema:author
    ↓
ex:author/1 ──→ "Robert C. Martin"
                  schema:name
```

### RDF vs Relational Databases

| Feature | SQL (Tables) | RDF (Graph) |
|---------|-------------|-------------|
| Data unit | Row | Triple (S-P-O) |
| Schema | Fixed (DDL) | Flexible (ontology) |
| Relationships | Foreign keys + JOINs | Direct edges in graph |
| Identity | Integer IDs | URIs (globally unique) |
| Multi-valued | Junction tables | Multiple triples |
| Schema changes | ALTER TABLE (migration) | Just add triples |
| Query language | SQL | SPARQL |

**Key insight:** In RDF, relationships are first-class citizens. In SQL, they require extra tables and JOINs.

### Turtle Syntax (.ttl)

Turtle is the most human-readable RDF format:

```turtle
@prefix ex:     <http://example.org/> .
@prefix dct:    <http://purl.org/dc/terms/> .
@prefix schema: <http://schema.org/> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .

ex:book/1
    a schema:Book ;                           # rdf:type
    dct:title "Clean Code" ;                  # string literal
    schema:author ex:author/1 ;               # link to another resource
    schema:numberOfPages 464 ;                # integer literal
    schema:datePublished "2008"^^xsd:gYear .  # typed literal

ex:author/1
    a schema:Person ;
    schema:name "Robert C. Martin" .
```

**Syntax rules:**
- `@prefix` — Namespace shortcuts (like SQL aliases)
- `;` — Same subject, different predicate
- `,` — Same subject + predicate, different objects
- `.` — End of statement
- `a` — Shorthand for `rdf:type`
- `"value"^^xsd:type` — Typed literal

### URIs — Global Identifiers

Unlike integer IDs in SQL, RDF uses URIs:

```
SQL:  id = 42                      (only unique within one table)
RDF:  http://example.org/book/42   (globally unique across the web)
```

This enables **linked data** — connecting datasets from different sources:

```turtle
ex:book/1 schema:author <http://dbpedia.org/resource/Robert_C._Martin> .
```

Your local book data links to DBpedia (Wikipedia's RDF twin) without any JOIN.

### SPARQL — The Query Language

SPARQL queries use **triple patterns** with variables (`?var`):

```sparql
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX schema: <http://schema.org/>

SELECT ?title ?authorName
WHERE {
    ?book a schema:Book ;
          dct:title ?title ;
          schema:author ?author .
    ?author schema:name ?authorName .
}
ORDER BY ?title
```

**How it works:**
1. Each line in `WHERE` is a triple pattern
2. `?book`, `?title`, `?author` are variables
3. The engine finds all triples matching the pattern
4. Variables get bound to matching values

**SPARQL vs SQL equivalence:**

| SQL | SPARQL |
|-----|--------|
| `SELECT col FROM table` | `SELECT ?var WHERE { ?s :pred ?var }` |
| `WHERE col = 'val'` | `FILTER (?var = "val")` |
| `JOIN` | Triple pattern chaining |
| `LEFT JOIN` | `OPTIONAL { }` |
| `GROUP BY` | `GROUP BY` |
| `COUNT(*)` | `COUNT(?var)` |
| `ORDER BY` | `ORDER BY` |
| `LIMIT` | `LIMIT` |

### OPTIONAL — The LEFT JOIN of SPARQL

```sparql
SELECT ?title ?publisher
WHERE {
    ?book dct:title ?title .
    OPTIONAL { ?book schema:publisher ?pub . ?pub schema:name ?publisher }
}
```

Books without a publisher still appear (with `?publisher` unbound) — like a SQL `LEFT JOIN`.

### Apache Jena Fuseki

Fuseki is a SPARQL server that provides:
- **SPARQL endpoint** — HTTP API for queries (`/dataset/query`)
- **SPARQL Update** — Insert/delete data (`/dataset/update`)
- **Graph Store** — Upload RDF files (`/dataset/data`)
- **Web UI** — Browser-based query editor (port 3030)

### Common Beginner Misunderstandings

1. **"RDF is just another database format"** — RDF is a data model for knowledge representation. It excels at linking heterogeneous data.
2. **"I need RDF for everything"** — Use SQL for CRUD apps. Use RDF for knowledge graphs, linked data, and semantic web applications.
3. **"SPARQL is like SQL"** — SPARQL matches graph patterns, not table rows. Think in triples, not tables.
4. **"URIs must be web URLs"** — URIs are identifiers. They don't need to resolve to a web page (but it's nice if they do).
5. **"RDF has no schema"** — RDF is schema-flexible, not schema-less. Ontologies (OWL/RDFS) define structure and constraints.

---

## PART B — BEGINNER PRACTICE

### Exercise 16.B.1 — Understand RDF Triples and Turtle

Read the sample Turtle file and identify subjects, predicates, and objects:

```bash
cd practice/curriculum/16-rdf-sparql-labs
cat data/sample.ttl
```

For each resource, list its properties. Identify:
- Which resources are Books? Authors? Publishers?
- Which properties link resources together (object properties)?
- Which properties have literal values (data properties)?

**Practice file:** `practice/curriculum/16-rdf-sparql-labs/data/sample.ttl`

### Exercise 16.B.2 — Run Fuseki in Docker + Load Data

Start Fuseki, create a dataset, and upload the TTL data:

```bash
docker compose up -d
curl -s http://localhost:3030/$/ping

# Create dataset
curl -s -X POST http://localhost:3030/$/datasets \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'dbName=books&dbType=tdb2'

# Upload data
curl -s -X POST http://localhost:3030/books/data \
  -H 'Content-Type: text/turtle' \
  --data-binary @data/sample.ttl

# Verify triple count
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query=SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }" \
  -H 'Accept: application/json' | jq .
```

### Exercise 16.B.3 — Basic SPARQL Queries

Run queries of increasing complexity:

```bash
# All books with titles
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query@queries/01_all_books.rq" \
  -H 'Accept: application/json' | jq .
```

**Practice files:**
- `practice/curriculum/16-rdf-sparql-labs/queries/01_all_books.rq`
- `practice/curriculum/16-rdf-sparql-labs/queries/02_filter_year.rq`
- `practice/curriculum/16-rdf-sparql-labs/queries/03_optional_publisher.rq`
- `practice/curriculum/16-rdf-sparql-labs/queries/04_group_by_language.rq`
- `practice/curriculum/16-rdf-sparql-labs/queries/05_multi_author.rq`

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 16.C.1 — SQL vs SPARQL Comparison

Model the same book dataset in PostgreSQL and compare query approaches:

```bash
# Set up PostgreSQL schema
docker compose exec -T postgres psql -U labuser -d labdb < sql/schema.sql
docker compose exec -T postgres psql -U labuser -d labdb < sql/seed.sql

# Run SQL queries
docker compose exec -T postgres psql -U labuser -d labdb < sql/queries.sql
```

Then run the equivalent SPARQL queries and compare:

```bash
for f in sparql/*.rq; do
  echo "=== $f ==="
  curl -s -G http://localhost:3030/books/query \
    --data-urlencode "query@$f" \
    -H 'Accept: application/json' | jq '.results.bindings'
done
```

**Key differences to note:**
- SQL needs junction tables for multi-valued relationships; RDF just adds triples
- SPARQL uses `OPTIONAL` instead of `LEFT JOIN`
- RDF handles schema evolution without migrations

**Solution:** `practice/curriculum/16-rdf-sparql-labs/solutions/comparison.md`

### Exercise 16.C.2 — SPARQL UPDATE Operations

Insert, update, and delete data using SPARQL Update:

```sparql
# Insert a new book
INSERT DATA {
    ex:book/8 a schema:Book ;
              dct:title "New Book" ;
              schema:datePublished "2025"^^xsd:gYear .
}

# Update (delete old value, insert new)
DELETE { ex:book/8 dct:title ?old }
INSERT { ex:book/8 dct:title "Updated Book Title" }
WHERE  { ex:book/8 dct:title ?old }

# Delete
DELETE WHERE { ex:book/8 ?p ?o }
```

### Exercise 16.C.3 — Named Graphs

Organize data into separate graphs for provenance tracking:

```sparql
# Insert into a named graph
INSERT DATA {
    GRAPH <http://example.org/graph/reviews> {
        ex:book/1 schema:reviewRating "5"^^xsd:integer .
        ex:book/1 schema:reviewBody "Excellent book on clean code." .
    }
}

# Query a specific graph
SELECT ?title ?rating
WHERE {
    ?book dct:title ?title .
    GRAPH <http://example.org/graph/reviews> {
        ?book schema:reviewRating ?rating .
    }
}
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 16.D.1 — Debug: SPARQL Query Returns Empty

**Symptom:** Query returns zero results despite data being loaded.

**Task:**
1. Verify data is loaded: `SELECT (COUNT(*) AS ?c) WHERE { ?s ?p ?o }`
2. Check namespace prefixes — a typo in the prefix URI means no pattern matches
3. Compare URI in query vs data: `http://example.org/` vs `http://example.org` (trailing slash matters!)
4. Fix prefix URIs and re-run

### Exercise 16.D.2 — Debug: Fuseki Won't Start

**Symptom:** Fuseki container exits immediately.

**Task:**
1. Check logs: `docker compose logs fuseki`
2. Common causes: port conflict, volume permissions, invalid config
3. Fix and restart

### Exercise 16.D.3 — Debug: Malformed Turtle File

**Symptom:** Data upload fails with parse error.

**Task:**
1. Read the error message — it tells you the line number
2. Common mistakes: missing `.` at end of statement, unclosed quotes, invalid URI
3. Fix the Turtle syntax and re-upload

### Exercise 16.D.4 — Debug: OPTIONAL Produces Duplicates

**Symptom:** Query returns more rows than expected because of multiple OPTIONAL bindings.

**Task:**
1. Understand that each `OPTIONAL` creates a LEFT JOIN — multiple matches multiply rows
2. Use sub-queries or `GROUP BY` with `SAMPLE()` to deduplicate
3. Restructure query to avoid Cartesian products

---

## PART E — PRODUCTION SIMULATION

### Scenario: Building a Knowledge Graph Service

Build and operate a semantic data service:

1. **Data modeling** — Design an RDF ontology for a domain (books, authors, publishers, reviews)
2. **Data loading** — Create Turtle files and load into Fuseki
3. **SPARQL API** — Write queries for: list, filter, aggregate, traverse relationships
4. **Integration** — Compare with the equivalent SQL model to understand tradeoffs
5. **Named graphs** — Separate data by source (catalog, reviews, user data)
6. **SPARQL Update** — Insert, update, and delete triples via the HTTP API
7. **Backup** — Export the dataset as Turtle/N-Triples for backup

```bash
# Export all data
curl -s http://localhost:3030/books/data \
  -H 'Accept: text/turtle' > backup.ttl

# Count triples
curl -s -G http://localhost:3030/books/query \
  --data-urlencode "query=SELECT (COUNT(*) AS ?triples) WHERE { ?s ?p ?o }" \
  -H 'Accept: application/json' | jq .
```

---

## Key Takeaways

1. **RDF models knowledge as a graph** — Think in triples (subject-predicate-object), not rows and columns.
2. **URIs are global identifiers** — They enable linking data across datasets without foreign keys.
3. **SPARQL matches patterns** — Triple patterns with variables replace SQL JOINs.
4. **OPTIONAL = LEFT JOIN** — Use it to include results even when some triples don't exist.
5. **RDF is schema-flexible** — Adding new properties doesn't require migrations.
6. **Use RDF for the right problems** — Knowledge graphs, linked data, and semantic integration — not CRUD apps.

---
*Next: [Section 20 — Capstone Project](20-capstone-project.md)*
