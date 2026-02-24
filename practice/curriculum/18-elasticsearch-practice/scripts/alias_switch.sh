#!/usr/bin/env bash
# Exercise 15.4: Atomic alias switch from v1 to v2
set -euo pipefail

ES_URL="${ES_URL:-http://localhost:9200}"

echo "=== Current alias state ==="
curl -sf "$ES_URL/_alias/books_alias" | jq .

echo ""
echo "=== Atomic alias switch: books_alias  v1 -> v2 ==="
curl -sf -X POST "$ES_URL/_aliases" \
  -H 'Content-Type: application/json' \
  -d '{
  "actions": [
    { "remove": { "index": "books_v1", "alias": "books_alias" } },
    { "add":    { "index": "books_v2", "alias": "books_alias" } }
  ]
}' | jq .

echo ""
echo "=== New alias state ==="
curl -sf "$ES_URL/_alias/books_alias" | jq .

echo ""
echo "=== Verify: query via alias returns v2 data (with summary field) ==="
curl -sf "$ES_URL/books_alias/_search?size=1" \
  -H 'Content-Type: application/json' \
  -d '{ "query": { "match_all": {} }, "_source": ["title", "summary"] }' \
  | jq '.hits.hits[]._source'

echo ""
echo "=== Alias switch complete ==="
echo "Optional: delete old index with: curl -X DELETE $ES_URL/books_v1"
