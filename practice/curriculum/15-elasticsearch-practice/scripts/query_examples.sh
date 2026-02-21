#!/usr/bin/env bash
# Exercise 15.2: Query examples for the 'books' index
set -euo pipefail

ES_URL="${ES_URL:-http://localhost:9200}"

echo "============================================"
echo "Q1: Match query — full-text search for 'distributed systems'"
echo "============================================"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "query": {
    "match": {
      "description": "distributed systems"
    }
  }
}' | jq '.hits.hits[] | {id: ._id, title: ._source.title, score: ._score}'

echo ""
echo "============================================"
echo "Q2: Term query — exact match on genre keyword"
echo "============================================"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "query": {
    "term": {
      "genre.keyword": "DevOps"
    }
  }
}' | jq '.hits.hits[] | {id: ._id, title: ._source.title}'

echo ""
echo "============================================"
echo "Q3: Wildcard query — titles starting with 'The'"
echo "============================================"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "query": {
    "wildcard": {
      "title.keyword": "The*"
    }
  }
}' | jq '.hits.hits[] | {id: ._id, title: ._source.title}'

echo ""
echo "============================================"
echo "Q4: Fuzzy query — typo-tolerant ('programing' → 'programming')"
echo "============================================"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "query": {
    "fuzzy": {
      "description": {
        "value": "programing",
        "fuzziness": "AUTO"
      }
    }
  }
}' | jq '.hits.hits[] | {id: ._id, title: ._source.title, score: ._score}'

echo ""
echo "============================================"
echo "Q5: Range query — books published after 2020"
echo "============================================"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "query": {
    "range": {
      "year": { "gte": 2020 }
    }
  }
}' | jq '.hits.hits[] | {id: ._id, title: ._source.title, year: ._source.year}'

echo ""
echo "============================================"
echo "Q6: Bool query — must be DevOps genre + should mention 'production'"
echo "============================================"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "query": {
    "bool": {
      "must": [
        { "term": { "genre.keyword": "DevOps" } }
      ],
      "should": [
        { "match": { "description": "production" } }
      ]
    }
  }
}' | jq '.hits.hits[] | {id: ._id, title: ._source.title, score: ._score}'

echo ""
echo "============================================"
echo "Q7: Aggregation — average rating by genre"
echo "============================================"
curl -sf "$ES_URL/books/_search" \
  -H 'Content-Type: application/json' \
  -d '{
  "size": 0,
  "aggs": {
    "by_genre": {
      "terms": { "field": "genre.keyword" },
      "aggs": {
        "avg_rating": { "avg": { "field": "rating" } }
      }
    }
  }
}' | jq '.aggregations.by_genre.buckets[] | {genre: .key, count: .doc_count, avg_rating: .avg_rating.value}'

echo ""
echo "=== All queries completed ==="
