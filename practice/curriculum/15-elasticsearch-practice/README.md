# Module 15 — Elasticsearch Practice

## Goals

- Run Elasticsearch and Kibana in Docker
- Create indexes with explicit mappings
- Index, search, and query documents using the REST API
- Compare full-text search (ES) vs SQL pattern matching
- Perform zero-downtime reindexing with aliases

## Prerequisites

- Docker & Docker Compose installed
- `curl` and `jq` available
- Completed Module 14 (for SQL comparison exercise)

## Setup

```bash
cd practice/curriculum/15-elasticsearch-practice
docker compose up -d
```

Wait for Elasticsearch to be healthy (may take 30–60 seconds):

```bash
# Check health
curl -s http://localhost:9200/_cluster/health | jq .
# Expected: "status": "yellow" or "green"
```

Kibana (optional) is available at: http://localhost:5601

---

## Exercise 15.1 — Run Elasticsearch in Docker

### Objective

Start an Elasticsearch cluster and verify it's healthy.

### Steps

1. Start the stack:

```bash
docker compose up -d
```

2. Check Elasticsearch is running:

```bash
curl -s http://localhost:9200 | jq .
```

Expected output:

```json
{
  "name": "es_lab",
  "cluster_name": "docker-cluster",
  "version": {
    "number": "8.12.0"
  },
  "tagline": "You Know, for Search"
}
```

3. Check cluster health:

```bash
curl -s http://localhost:9200/_cluster/health | jq .
```

4. List indices (should be empty initially):

```bash
curl -s http://localhost:9200/_cat/indices?v
```

### Memory Notes

Elasticsearch requires at minimum 512MB heap. The docker-compose.yml sets:
- `ES_JAVA_OPTS=-Xms512m -Xmx512m`
- Container memory limit: 1GB

If your machine has limited RAM, stop other services first.

### Deliverables

- Running Elasticsearch container with health check passing

---

## Exercise 15.2 — Create Index + Mapping + Index Documents

### Objective

Create an index with explicit mappings, insert documents, and run various queries.

### Steps

1. Create the index with mappings:

```bash
bash scripts/create_index.sh
```

2. Index sample documents:

```bash
bash scripts/index_docs.sh
```

3. Verify document count:

```bash
curl -s http://localhost:9200/books/_count | jq .
```

Expected: `"count": 10`

4. Run query examples:

```bash
bash scripts/query_examples.sh
```

### Query Types Demonstrated

| Query Type | Use Case | Example |
|-----------|----------|---------|
| `match` | Full-text search | Find books mentioning "distributed systems" |
| `term` | Exact value match | Find books by exact genre |
| `wildcard` | Pattern match | Find titles starting with "The" |
| `fuzzy` | Typo-tolerant search | Find "programing" → "programming" |
| `range` | Numeric/date range | Books published after 2020 |
| `bool` | Compound queries | Must match genre AND should match keyword |

### Deliverables

- [scripts/create_index.sh](scripts/create_index.sh)
- [scripts/index_docs.sh](scripts/index_docs.sh)
- [scripts/query_examples.sh](scripts/query_examples.sh)

---

## Exercise 15.3 — SQL vs Elasticsearch Comparison

### Objective

Store the same dataset in both Postgres and Elasticsearch. Compare full-text search capabilities.

### Prerequisites

Module 14 Postgres must be running on port 5432.

### Steps

1. Load the books data into Postgres:

```bash
docker exec -i pg_lab psql -U labuser -d labdb < scripts/books_pg_schema.sql
```

2. The same data is already in Elasticsearch from Exercise 15.2.

3. Run the comparison:

```bash
bash scripts/sql_vs_es_comparison.sh
```

### Key Differences

| Feature | PostgreSQL (`LIKE` / `ILIKE`) | Elasticsearch (`match`) |
|---------|-------------------------------|------------------------|
| Prefix search | `WHERE title LIKE 'The%'` | `{"prefix": {"title": "the"}}` |
| Fuzzy search | Not built-in (pg_trgm extension) | `{"fuzzy": {"title": "programing"}}` |
| Full-text | `to_tsvector` + `to_tsquery` | Built-in analyzers + tokenizers |
| Performance at scale | Degrades with `LIKE '%term%'` | Inverted index — fast at any scale |
| Relevance scoring | Manual ranking | Built-in `_score` |
| Exact match | `WHERE genre = 'fiction'` | `{"term": {"genre.keyword": "fiction"}}` |

### Analyzers and Tokenization

Elasticsearch breaks text into tokens:

```bash
curl -s -X POST "http://localhost:9200/books/_analyze" \
  -H 'Content-Type: application/json' \
  -d '{"analyzer": "standard", "text": "Distributed Systems Design"}' | jq .
```

Output: `["distributed", "systems", "design"]` — lowercased, split on whitespace.

### Deliverables

- [scripts/books_pg_schema.sql](scripts/books_pg_schema.sql)
- [scripts/sql_vs_es_comparison.sh](scripts/sql_vs_es_comparison.sh)
- [solutions/comparison.md](solutions/comparison.md)

---

## Exercise 15.4 — Reindex Strategy (v1 → v2 + Alias Switch)

### Objective

Perform a zero-downtime schema migration by reindexing from v1 to v2 and switching an alias.

### Steps

1. Set up the alias on v1:

```bash
bash scripts/reindex_v1_to_v2.sh
```

This script:
- Creates `books_v1` index (copy of existing)
- Sets alias `books_alias` → `books_v1`
- Creates `books_v2` with updated mappings (adds `summary` field)
- Reindexes all documents from v1 → v2

2. Switch the alias:

```bash
bash scripts/alias_switch.sh
```

3. Verify:

```bash
# Alias now points to v2
curl -s http://localhost:9200/_alias/books_alias | jq .

# Queries via alias work
curl -s http://localhost:9200/books_alias/_count | jq .

# Old v1 can be deleted
curl -s -X DELETE http://localhost:9200/books_v1
```

### Why Aliases?

- **Zero downtime** — application always queries the alias, never the real index
- **Atomic switch** — alias update is a single atomic operation
- **Rollback** — if v2 has issues, switch alias back to v1

### Deliverables

- [scripts/reindex_v1_to_v2.sh](scripts/reindex_v1_to_v2.sh)
- [scripts/alias_switch.sh](scripts/alias_switch.sh)

---

## Cleanup

```bash
docker compose down -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `max virtual memory areas vm.max_map_count` | `sudo sysctl -w vm.max_map_count=262144` |
| ES not starting (OOM) | Reduce `ES_JAVA_OPTS` to `-Xms256m -Xmx256m` |
| Connection refused on 9200 | Wait 30s after startup; check `docker compose logs es` |
| Kibana not connecting | Ensure ES is healthy first; Kibana depends on ES |

## Next Steps

- Module 16: RDF + SPARQL Labs
- Cheatsheet: [SQL vs SPARQL vs Elasticsearch](../../../docs/cheatsheets/sql_vs_sparql_vs_es.md)
