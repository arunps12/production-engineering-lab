# SECTION 15 — ELASTICSEARCH PRACTICE

---

## PART A — CONCEPT EXPLANATION

### What is Elasticsearch?

Elasticsearch is a distributed search and analytics engine built on Apache Lucene. It stores documents as JSON and provides near-real-time full-text search.

```
Application → Elasticsearch → Returns ranked results
              ┌─────────────────────────────┐
              │         Cluster             │
              │  ┌───────┐    ┌───────┐     │
              │  │Node 1 │    │Node 2 │     │
              │  │Shard 0│    │Shard 1│     │
              │  │Shard 2│    │Replica│     │
              │  └───────┘    └───────┘     │
              └─────────────────────────────┘
```

**Key differences from relational databases:**

| Feature | PostgreSQL | Elasticsearch |
|---------|-----------|---------------|
| Data model | Tables + rows | JSON documents |
| Schema | Fixed (DDL) | Dynamic mappings |
| Query language | SQL | Query DSL (JSON) |
| Joins | Native JOIN | Limited (nested, parent-child) |
| Transactions | Full ACID | No |
| Full-text search | Basic (`tsvector`) | Advanced (analyzers, scoring) |
| Scalability | Vertical | Horizontal (shards) |
| Best for | CRUD, transactions | Search, analytics, logs |

### Core Concepts

**Index** — A collection of documents (like a database table):
```
Index: "books"
├── Document 1: {"title": "Clean Code", "author": "Robert Martin", "year": 2008}
├── Document 2: {"title": "DDIA", "author": "Martin Kleppmann", "year": 2017}
└── Document 3: {"title": "The Pragmatic Programmer", "year": 2019}
```

**Mapping** — Defines field types (like a table schema):
```json
{
  "mappings": {
    "properties": {
      "title":  { "type": "text", "analyzer": "standard" },
      "author": { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "year":   { "type": "integer" },
      "genre":  { "type": "keyword" }
    }
  }
}
```

**`text` vs `keyword`:**
- `text` — Analyzed, tokenized, for full-text search ("Clean Code" → ["clean", "code"])
- `keyword` — Exact match only, not analyzed ("Clean Code" stays as "Clean Code")

### Analyzers — How Text Search Works

When you index a `text` field, Elasticsearch runs it through an **analyzer**:

```
Input: "The Pragmatic Programmer: 20th Anniversary Edition"
         ↓
┌─────────────────────┐
│   Character Filter   │  → Strip HTML, character mapping
├─────────────────────┤
│     Tokenizer        │  → Split into tokens: ["The", "Pragmatic", "Programmer", ...]
├─────────────────────┤
│    Token Filters     │  → Lowercase: ["the", "pragmatic", "programmer", ...]
│                      │  → Stop words: ["pragmatic", "programmer", ...]
│                      │  → Stemming: ["pragmat", "programm", ...]
└─────────────────────┘
```

**Built-in analyzers:**
- `standard` — Tokenize on word boundaries, lowercase, remove punctuation
- `simple` — Split on non-letters, lowercase
- `whitespace` — Split on whitespace only
- `english` — Standard + English stop words + stemming

### Query DSL — The Query Language

Elasticsearch queries are JSON objects. Key query types:

**Match (full-text):**
```json
{ "query": { "match": { "title": "distributed systems" } } }
```

**Term (exact):**
```json
{ "query": { "term": { "genre.keyword": "computer-science" } } }
```

**Range:**
```json
{ "query": { "range": { "year": { "gte": 2015, "lte": 2020 } } } }
```

**Bool (compound):**
```json
{
  "query": {
    "bool": {
      "must":   [{ "match": { "title": "programming" } }],
      "filter": [{ "range": { "year": { "gte": 2015 } } }],
      "should": [{ "term": { "genre.keyword": "software" } }]
    }
  }
}
```

**Fuzzy (typo-tolerant):**
```json
{ "query": { "fuzzy": { "title": { "value": "programing", "fuzziness": "AUTO" } } } }
```

### Aggregations — Analytics

Aggregations are like SQL `GROUP BY` but more powerful:

```json
{
  "size": 0,
  "aggs": {
    "by_genre": {
      "terms": { "field": "genre.keyword" }
    },
    "avg_year": {
      "avg": { "field": "year" }
    }
  }
}
```

### Aliases and Reindexing

You can't change a field's mapping after indexing. To change mappings, you **reindex**:

```
1. Create new index (books_v2) with updated mappings
2. Reindex: POST _reindex { "source": "books_v1", "dest": "books_v2" }
3. Switch alias: books → books_v2  (zero-downtime cutover)
4. Delete old index (books_v1)
```

An **alias** is a pointer to one or more indexes — your application always queries the alias, never the real index name.

### Common Beginner Misunderstandings

1. **"Elasticsearch replaces my database"** — ES is a search engine, not a primary data store. Keep your source of truth in PostgreSQL.
2. **"text and keyword are the same"** — `text` is analyzed for search, `keyword` is exact match only. Use both with `multi-fields`.
3. **"I can update mappings"** — You cannot change a field's type. You must reindex into a new index.
4. **"Relevance scoring is magic"** — ES uses BM25 scoring. Understanding it helps you tune search quality.
5. **"More shards = faster"** — Each shard has overhead. Start with 1 shard per index for small datasets.

---

## PART B — BEGINNER PRACTICE

### Exercise 15.B.1 — Run Elasticsearch in Docker

Start Elasticsearch and Kibana, verify cluster health:

```bash
cd practice/curriculum/15-elasticsearch-practice
docker compose up -d
curl -s http://localhost:9200 | jq .
curl -s http://localhost:9200/_cluster/health | jq .
```

**Practice file:** `practice/curriculum/15-elasticsearch-practice/docker-compose.yml`

### Exercise 15.B.2 — Create Index with Mappings

Create a `books` index with explicit mappings and a custom analyzer:

```bash
bash scripts/create_index.sh
```

Verify the mapping:

```bash
curl -s http://localhost:9200/books/_mapping | jq .
```

**Practice file:** `practice/curriculum/15-elasticsearch-practice/scripts/create_index.sh`

### Exercise 15.B.3 — Index Documents

Index 10 sample book documents using the Bulk API:

```bash
bash scripts/index_docs.sh
curl -s http://localhost:9200/books/_count | jq .  # Should return 10
```

**Practice file:** `practice/curriculum/15-elasticsearch-practice/scripts/index_docs.sh`

### Exercise 15.B.4 — Run Queries

Execute match, term, wildcard, fuzzy, range, bool, and aggregation queries:

```bash
bash scripts/query_examples.sh
```

Study each query type and its output to understand when to use each.

**Practice file:** `practice/curriculum/15-elasticsearch-practice/scripts/query_examples.sh`

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 15.C.1 — SQL vs Elasticsearch Comparison

Set up the same `books` dataset in PostgreSQL and Elasticsearch, then compare:

| Operation | SQL | Elasticsearch |
|-----------|-----|---------------|
| Exact match | `WHERE genre = 'fiction'` | `term: { genre.keyword: "fiction" }` |
| Full-text search | `WHERE title ILIKE '%systems%'` | `match: { title: "systems" }` |
| Fuzzy search | Requires `pg_trgm` extension | Built-in `fuzzy` query |
| Aggregation | `GROUP BY genre` | `terms` aggregation |

```bash
# Create the PostgreSQL table
docker compose exec -T postgres psql -U labuser -d labdb < scripts/books_pg_schema.sql

# Run comparisons
bash scripts/sql_vs_es_comparison.sh
```

**Practice files:**
- `practice/curriculum/15-elasticsearch-practice/scripts/books_pg_schema.sql`
- `practice/curriculum/15-elasticsearch-practice/scripts/sql_vs_es_comparison.sh`

**Solution:** `practice/curriculum/15-elasticsearch-practice/solutions/comparison.md`

### Exercise 15.C.2 — Relevance Tuning

Experiment with boosting and scoring:

```bash
# Boost title matches higher than description
curl -s -X GET "http://localhost:9200/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "multi_match": {
        "query": "programming",
        "fields": ["title^3", "description"],
        "type": "best_fields"
      }
    }
  }' | jq '.hits.hits[] | {title: ._source.title, score: ._score}'
```

The `^3` gives title matches 3x more weight than description matches.

### Exercise 15.C.3 — Custom Analyzers

Create an index with custom analyzer for better search quality:

```json
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "stop", "snowball"]
        }
      }
    }
  }
}
```

Test the analyzer:

```bash
curl -s -X POST "http://localhost:9200/books/_analyze" \
  -H 'Content-Type: application/json' \
  -d '{"analyzer": "standard", "text": "The Pragmatic Programmer 2nd Edition"}' | jq '.tokens[].token'
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 15.D.1 — Debug: Index Mapping Conflict

**Symptom:** Indexing a document fails with `mapper_parsing_exception`.

**Task:**
1. Try indexing `{"year": "twenty-twenty"}` into the `books` index
2. Read the error — `year` is mapped as `integer` but value is a string
3. Understand why dynamic mapping can cause this
4. Fix: Use explicit mappings and validate data before indexing

### Exercise 15.D.2 — Debug: Search Returning No Results

**Symptom:** `term` query for "Clean Code" returns zero hits, but the document exists.

**Task:**
1. Understand that `text` fields are analyzed (lowercased, tokenized)
2. `term` query on a `text` field won't match because "Clean Code" ≠ "clean" or "code"
3. Fix: Use `match` query for `text` fields, or query the `.keyword` sub-field

### Exercise 15.D.3 — Debug: High Memory Usage

**Symptom:** Elasticsearch container keeps getting OOM-killed.

**Task:**
1. Check JVM heap settings (`ES_JAVA_OPTS`)
2. Verify container memory limits vs JVM heap (heap should be ≤ 50% of container memory)
3. Check for too many open indexes or large aggregations
4. Fix: Set proper memory limits in `docker-compose.yml`

### Exercise 15.D.4 — Debug: Slow Queries

**Symptom:** Search latency > 5 seconds.

**Task:**
1. Enable slow query log: `PUT /books/_settings {"index.search.slowlog.threshold.query.warn": "2s"}`
2. Check index size and shard count
3. Use `_profile` API to see query execution breakdown
4. Optimize: Use `filter` context instead of `query` context for non-scoring clauses

---

## PART E — PRODUCTION SIMULATION

### Scenario: Building a Book Search Service

Build and operate a search service for a catalog of 10,000+ books:

1. **Index setup** — Create the `books` index with explicit mappings and custom analyzers
2. **Bulk indexing** — Index 10,000 documents using the Bulk API
3. **Search API** — Build queries for: full-text search, filtered search, autocomplete
4. **Aggregations** — Genre distribution, year histogram, top authors
5. **Monitoring** — Check `_cat/indices`, `_cat/shards`, `_cluster/health`
6. **Reindexing** — Change mappings and do zero-downtime reindex with aliases
7. **Sync strategy** — Design how changes in PostgreSQL sync to Elasticsearch

```bash
# Monitor cluster
curl -s http://localhost:9200/_cat/indices?v
curl -s http://localhost:9200/_cat/shards?v
curl -s http://localhost:9200/_nodes/stats/jvm?filter_path=nodes.*.jvm.mem | jq .

# Index stats
curl -s http://localhost:9200/books/_stats | jq '.indices.books.total'
```

---

## Key Takeaways

1. **Elasticsearch is a search engine, not a database** — Keep PostgreSQL as your source of truth.
2. **Understand `text` vs `keyword`** — Use `text` for full-text search, `keyword` for exact match/aggregations.
3. **Explicit mappings are essential** — Don't rely on dynamic mapping in production.
4. **Use aliases** — Never let your application query index names directly.
5. **Memory matters** — JVM heap should be ≤ 50% of container memory, and ≤ 32GB total.
6. **Analyzers determine search quality** — The default `standard` analyzer works for most cases; customize when needed.

---
*Next: [Section 16 — RDF & SPARQL Labs](16-rdf-sparql-labs.md)*
