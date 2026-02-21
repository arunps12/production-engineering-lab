#!/usr/bin/env bash
# Exercise 15.2: Index sample documents into the 'books' index
set -euo pipefail

ES_URL="${ES_URL:-http://localhost:9200}"

echo "=== Indexing 10 sample books ==="

curl -sf -X POST "$ES_URL/books/_bulk" \
  -H 'Content-Type: application/x-ndjson' \
  -d '
{"index": {"_id": "1"}}
{"title": "The Art of Computer Programming", "author": "Donald Knuth", "genre": "Computer Science", "description": "Comprehensive monograph on algorithms and data structures", "year": 1968, "pages": 3168, "rating": 4.9, "tags": ["algorithms", "programming", "mathematics"], "published_date": "1968-01-01"}
{"index": {"_id": "2"}}
{"title": "Distributed Systems Design", "author": "Martin Kleppmann", "genre": "Computer Science", "description": "Guide to designing data-intensive applications with distributed architecture patterns", "year": 2017, "pages": 616, "rating": 4.8, "tags": ["distributed", "systems", "architecture"], "published_date": "2017-03-16"}
{"index": {"_id": "3"}}
{"title": "Clean Code", "author": "Robert C. Martin", "genre": "Software Engineering", "description": "A handbook of agile software craftsmanship and clean programming practices", "year": 2008, "pages": 464, "rating": 4.5, "tags": ["clean-code", "programming", "best-practices"], "published_date": "2008-08-01"}
{"index": {"_id": "4"}}
{"title": "The Pragmatic Programmer", "author": "David Thomas", "genre": "Software Engineering", "description": "From journeyman to master programmer through practical tips and techniques", "year": 2019, "pages": 352, "rating": 4.7, "tags": ["programming", "career", "best-practices"], "published_date": "2019-09-20"}
{"index": {"_id": "5"}}
{"title": "Site Reliability Engineering", "author": "Betsy Beyer", "genre": "DevOps", "description": "How Google runs production systems with reliability principles", "year": 2016, "pages": 552, "rating": 4.6, "tags": ["sre", "devops", "production"], "published_date": "2016-03-23"}
{"index": {"_id": "6"}}
{"title": "Python Crash Course", "author": "Eric Matthes", "genre": "Programming", "description": "A hands-on project-based introduction to Python programming language", "year": 2023, "pages": 544, "rating": 4.6, "tags": ["python", "beginner", "programming"], "published_date": "2023-01-10"}
{"index": {"_id": "7"}}
{"title": "Database Internals", "author": "Alex Petrov", "genre": "Computer Science", "description": "Deep dive into how distributed data systems work under the hood", "year": 2019, "pages": 350, "rating": 4.5, "tags": ["database", "internals", "distributed"], "published_date": "2019-10-01"}
{"index": {"_id": "8"}}
{"title": "The Linux Command Line", "author": "William Shotts", "genre": "Operating Systems", "description": "Complete introduction to Linux command line and shell scripting", "year": 2019, "pages": 480, "rating": 4.4, "tags": ["linux", "command-line", "shell"], "published_date": "2019-03-07"}
{"index": {"_id": "9"}}
{"title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "genre": "Computer Science", "description": "The big ideas behind reliable scalable and maintainable systems", "year": 2017, "pages": 624, "rating": 4.9, "tags": ["data", "distributed", "architecture"], "published_date": "2017-04-18"}
{"index": {"_id": "10"}}
{"title": "Docker Deep Dive", "author": "Nigel Poulton", "genre": "DevOps", "description": "Zero to Docker in a single book covering containers images and orchestration", "year": 2023, "pages": 368, "rating": 4.3, "tags": ["docker", "containers", "devops"], "published_date": "2023-06-15"}
' | jq '{ took: .took, errors: .errors, indexed: (.items | length) }'

echo ""
echo "=== Refresh index ==="
curl -sf -X POST "$ES_URL/books/_refresh" | jq .

echo ""
echo "=== Document count ==="
curl -sf "$ES_URL/books/_count" | jq .
