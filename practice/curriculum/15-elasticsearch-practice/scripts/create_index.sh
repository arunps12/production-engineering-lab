#!/usr/bin/env bash
# Exercise 15.2: Create the 'books' index with explicit mappings
set -euo pipefail

ES_URL="${ES_URL:-http://localhost:9200}"

echo "=== Deleting existing 'books' index (if any) ==="
curl -sf -X DELETE "$ES_URL/books" 2>/dev/null || true

echo ""
echo "=== Creating 'books' index with mappings ==="
curl -sf -X PUT "$ES_URL/books" \
  -H 'Content-Type: application/json' \
  -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "analysis": {
      "analyzer": {
        "custom_text": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "stop", "snowball"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "custom_text",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "author": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "genre": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "description": {
        "type": "text",
        "analyzer": "custom_text"
      },
      "year": { "type": "integer" },
      "pages": { "type": "integer" },
      "rating": { "type": "float" },
      "tags": { "type": "keyword" },
      "published_date": { "type": "date", "format": "yyyy-MM-dd" }
    }
  }
}' | jq .

echo ""
echo "=== Index created successfully ==="
curl -sf "$ES_URL/books/_mapping" | jq .
