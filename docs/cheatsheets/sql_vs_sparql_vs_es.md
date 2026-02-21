# SQL vs SPARQL vs Elasticsearch — Cheatsheet

## Quick Comparison

| Feature | SQL (PostgreSQL) | SPARQL (RDF/Fuseki) | Elasticsearch |
|---------|-----------------|---------------------|---------------|
| **Data Model** | Tables + rows | Triples (graph) | JSON documents |
| **Schema** | Fixed (DDL) | Flexible (ontology) | Dynamic mappings |
| **Query Language** | SQL | SPARQL | Query DSL (JSON) |
| **Joins** | `JOIN` keyword | Triple pattern matching | Nested/parent-child |
| **Transactions** | Full ACID | Limited | No |
| **Full-text Search** | `tsvector`/`tsquery` | `CONTAINS` (limited) | Built-in analyzers |
| **Fuzzy Search** | `pg_trgm` extension | `REGEX` | Built-in `fuzzy` |
| **Aggregations** | `GROUP BY`, window funcs | `GROUP BY`, `HAVING` | Aggs framework |
| **Scalability** | Vertical (read replicas) | Triple stores vary | Horizontal (shards) |
| **Best For** | Structured data, CRUD | Knowledge graphs, linked data | Search, analytics, logs |

---

## Same Question, Three Languages

### "Find all books by author 'Kleppmann'"

**SQL:**
```sql
SELECT b.title, a.name
FROM books b
JOIN book_authors ba ON b.id = ba.book_id
JOIN authors a ON ba.author_id = a.id
WHERE a.name = 'Martin Kleppmann';
```

**SPARQL:**
```sparql
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX schema: <http://schema.org/>

SELECT ?title ?author
WHERE {
    ?book a schema:Book ;
          dct:title ?title ;
          schema:author ?authorNode .
    ?authorNode schema:name ?author .
    FILTER (?author = "Martin Kleppmann")
}
```

**Elasticsearch:**
```json
{
  "query": {
    "term": { "author.keyword": "Martin Kleppmann" }
  }
}
```

---

### "Books published after 2016, sorted by year"

**SQL:**
```sql
SELECT title, year FROM books
WHERE year > 2016
ORDER BY year;
```

**SPARQL:**
```sparql
SELECT ?title ?year
WHERE {
    ?book dct:title ?title ;
          schema:datePublished ?year .
    FILTER (?year > "2016"^^xsd:gYear)
}
ORDER BY ?year
```

**Elasticsearch:**
```json
{
  "query": { "range": { "year": { "gt": 2016 } } },
  "sort": [{ "year": "asc" }]
}
```

---

### "Count books by genre"

**SQL:**
```sql
SELECT genre, COUNT(*) AS count
FROM books
GROUP BY genre
ORDER BY count DESC;
```

**SPARQL:**
```sparql
SELECT ?genre (COUNT(?book) AS ?count)
WHERE {
    ?book a schema:Book ;
          schema:genre ?genre .
}
GROUP BY ?genre
ORDER BY DESC(?count)
```

**Elasticsearch:**
```json
{
  "size": 0,
  "aggs": {
    "by_genre": {
      "terms": { "field": "genre.keyword" }
    }
  }
}
```

---

### "Fuzzy search: find 'programing' (typo)"

**SQL:**
```sql
-- Requires pg_trgm extension
CREATE EXTENSION IF NOT EXISTS pg_trgm;
SELECT title FROM books
WHERE description % 'programing';
-- Or similarity function:
SELECT title, similarity(description, 'programing') AS sim
FROM books
WHERE similarity(description, 'programing') > 0.3
ORDER BY sim DESC;
```

**SPARQL:**
```sparql
-- SPARQL has no built-in fuzzy search
-- Use REGEX as a workaround (not typo-tolerant):
SELECT ?title
WHERE {
    ?book dct:title ?title ;
          schema:description ?desc .
    FILTER REGEX(?desc, "program", "i")
}
```

**Elasticsearch:**
```json
{
  "query": {
    "fuzzy": {
      "description": {
        "value": "programing",
        "fuzziness": "AUTO"
      }
    }
  }
}
```

---

## When to Use Each

| Use Case | Best Choice | Why |
|----------|-------------|-----|
| CRUD application | **SQL** | ACID transactions, well-defined schema, ORM support |
| Full-text search | **Elasticsearch** | Analyzers, scoring, fuzzy, autocomplete |
| Knowledge graph | **SPARQL** | Flexible schema, linked data, reasoning |
| Log analysis | **Elasticsearch** | Fast aggregations, time-series, Kibana |
| Multi-source integration | **SPARQL** | URIs enable cross-dataset linking |
| Analytics / reporting | **SQL** | Window functions, CTEs, advanced joins |
| Real-time search | **Elasticsearch** | Near-real-time indexing, sub-second queries |
| Ontology / taxonomy | **SPARQL** | OWL reasoning, class hierarchy |

## Architecture Pattern

In production, combine them:

```
App → PostgreSQL (source of truth, ACID)
  ↓ (sync)
  Elasticsearch (search index)
  ↓ (enrichment)
  RDF/SPARQL (knowledge graph, semantic layer)
```

- **PostgreSQL**: Write path, transactional data
- **Elasticsearch**: Read path for search, analytics
- **SPARQL**: Semantic queries, data integration
