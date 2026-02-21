#!/usr/bin/env bash
# Exercise 15.4: Reindex from v1 to v2 with updated mappings
set -euo pipefail

ES_URL="${ES_URL:-http://localhost:9200}"

echo "=== Step 1: Create books_v1 (copy from books) ==="

# Create v1 with same mappings
curl -sf -X PUT "$ES_URL/books_v1" \
  -H 'Content-Type: application/json' \
  -d '{
  "settings": { "number_of_shards": 1, "number_of_replicas": 0 },
  "mappings": {
    "properties": {
      "title": { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "author": { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "genre": { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "description": { "type": "text" },
      "year": { "type": "integer" },
      "pages": { "type": "integer" },
      "rating": { "type": "float" },
      "tags": { "type": "keyword" },
      "published_date": { "type": "date", "format": "yyyy-MM-dd" }
    }
  }
}' | jq .

echo ""
echo "=== Step 2: Reindex books -> books_v1 ==="
curl -sf -X POST "$ES_URL/_reindex" \
  -H 'Content-Type: application/json' \
  -d '{
  "source": { "index": "books" },
  "dest": { "index": "books_v1" }
}' | jq '{ took: .took, total: .total, created: .created }'

echo ""
echo "=== Step 3: Create alias 'books_alias' -> books_v1 ==="
curl -sf -X POST "$ES_URL/_aliases" \
  -H 'Content-Type: application/json' \
  -d '{
  "actions": [
    { "add": { "index": "books_v1", "alias": "books_alias" } }
  ]
}' | jq .

echo ""
echo "=== Step 4: Create books_v2 with NEW mapping (added 'summary' field) ==="
curl -sf -X PUT "$ES_URL/books_v2" \
  -H 'Content-Type: application/json' \
  -d '{
  "settings": { "number_of_shards": 1, "number_of_replicas": 0 },
  "mappings": {
    "properties": {
      "title": { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "author": { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "genre": { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "description": { "type": "text" },
      "summary": { "type": "text", "analyzer": "english" },
      "year": { "type": "integer" },
      "pages": { "type": "integer" },
      "rating": { "type": "float" },
      "tags": { "type": "keyword" },
      "published_date": { "type": "date", "format": "yyyy-MM-dd" }
    }
  }
}' | jq .

echo ""
echo "=== Step 5: Reindex books_v1 -> books_v2 (with script to populate summary) ==="
curl -sf -X POST "$ES_URL/_reindex" \
  -H 'Content-Type: application/json' \
  -d '{
  "source": { "index": "books_v1" },
  "dest": { "index": "books_v2" },
  "script": {
    "source": "ctx._source.summary = ctx._source.title + ' by ' + ctx._source.author + '. ' + ctx._source.description",
    "lang": "painless"
  }
}' | jq '{ took: .took, total: .total, created: .created }'

echo ""
echo "=== Reindex complete. Now run alias_switch.sh to cut over. ==="
curl -sf "$ES_URL/books_v2/_count" | jq .
