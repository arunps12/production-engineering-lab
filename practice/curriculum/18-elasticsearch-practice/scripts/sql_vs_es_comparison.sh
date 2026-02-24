#!/usr/bin/env bash
# Exercise 15.3: SQL vs Elasticsearch comparison
set -euo pipefail

ES_URL="${ES_URL:-http://localhost:9200}"
PG_CMD="docker exec -i pg_lab psql -U labuser -d labdb -t -A"

echo "============================================"
echo "COMPARISON 1: Prefix search — titles starting with 'The'"
echo "============================================"

echo "--- PostgreSQL (LIKE) ---"
echo "SELECT title FROM books WHERE title LIKE 'The%';" | $PG_CMD

echo ""
echo "--- Elasticsearch (prefix) ---"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "query": { "prefix": { "title.keyword": "The" } },
  "_source": ["title"]
}' | jq -r '.hits.hits[]._source.title'

echo ""
echo "============================================"
echo "COMPARISON 2: Fuzzy search — 'programing' (typo)"
echo "============================================"

echo "--- PostgreSQL (ILIKE — no fuzzy) ---"
echo "SELECT title FROM books WHERE description ILIKE '%programing%';" | $PG_CMD
echo "(No results — SQL LIKE doesn't handle typos)"

echo ""
echo "--- Elasticsearch (fuzzy) ---"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "query": { "fuzzy": { "description": { "value": "programing", "fuzziness": "AUTO" } } },
  "_source": ["title"]
}' | jq -r '.hits.hits[]._source.title'

echo ""
echo "============================================"
echo "COMPARISON 3: Full-text search — 'reliable scalable systems'"
echo "============================================"

echo "--- PostgreSQL (to_tsvector/to_tsquery) ---"
echo "SELECT title FROM books WHERE to_tsvector('english', description) @@ to_tsquery('english', 'reliable & scalable & systems');" | $PG_CMD

echo ""
echo "--- Elasticsearch (match) ---"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "query": { "match": { "description": "reliable scalable systems" } },
  "_source": ["title"]
}' | jq -r '.hits.hits[]._source.title'

echo ""
echo "============================================"
echo "COMPARISON 4: Aggregation — average rating by genre"
echo "============================================"

echo "--- PostgreSQL ---"
echo "SELECT genre, ROUND(AVG(rating), 2) AS avg_rating, COUNT(*) FROM books GROUP BY genre ORDER BY avg_rating DESC;" | $PG_CMD

echo ""
echo "--- Elasticsearch ---"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "size": 0,
  "aggs": {
    "by_genre": {
      "terms": { "field": "genre.keyword" },
      "aggs": { "avg_rating": { "avg": { "field": "rating" } } }
    }
  }
}' | jq '.aggregations.by_genre.buckets[] | "\(.key)|\(.avg_rating.value)|\(.doc_count)"'

echo ""
echo "=== Comparison complete ==="
echo "See solutions/comparison.md for detailed analysis."
