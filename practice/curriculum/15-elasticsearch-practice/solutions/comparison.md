# SQL vs Elasticsearch — Comparison

## Dataset

10 books with: title, author, genre, description, year, pages, rating, tags.

## Prefix Search

### PostgreSQL
```sql
SELECT title FROM books WHERE title LIKE 'The%';
```
- Uses sequential scan or B-tree index (only for prefix `LIKE 'X%'`)
- Case-sensitive (use `ILIKE` for case-insensitive, but no index support without `pg_trgm`)

### Elasticsearch
```json
{ "query": { "prefix": { "title.keyword": "The" } } }
```
- Uses inverted index — efficient at any scale
- Can combine with analyzers for case-insensitive matching

## Fuzzy Search (Typo Tolerance)

### PostgreSQL
```sql
-- No built-in fuzzy search
-- Requires pg_trgm extension:
CREATE EXTENSION IF NOT EXISTS pg_trgm;
SELECT title FROM books WHERE description % 'programing';
```
- Requires extension installation
- Trigram similarity — works but limited control

### Elasticsearch
```json
{ "query": { "fuzzy": { "description": { "value": "programing", "fuzziness": "AUTO" } } } }
```
- Built-in Levenshtein distance
- `AUTO` fuzziness: 0 edits for 1-2 chars, 1 for 3-5, 2 for 6+
- Fast with automaton-based implementation

## Full-Text Search

### PostgreSQL
```sql
SELECT title FROM books
WHERE to_tsvector('english', description) @@ to_tsquery('english', 'reliable & scalable');
```
- Requires `tsvector` and `tsquery` functions
- Can add GIN index for performance
- Limited relevance scoring

### Elasticsearch
```json
{ "query": { "match": { "description": "reliable scalable" } } }
```
- Built-in analyzer pipeline: tokenize → lowercase → stop words → stem
- Automatic relevance scoring (`_score`)
- Configurable analyzers per field

## When to Use Each

| Criterion | PostgreSQL | Elasticsearch |
|-----------|-----------|---------------|
| ACID transactions | Yes | No |
| Joins / relations | Yes | Limited (nested/parent-child) |
| Full-text search | Limited (tsvector) | Excellent |
| Fuzzy / typo search | Extension needed | Built-in |
| Aggregations | GROUP BY | Powerful agg framework |
| Real-time analytics | Limited | Excellent |
| Data consistency | Strong | Eventually consistent |
| Schema flexibility | Fixed schema | Dynamic mappings |
| Write-heavy workloads | Excellent | Good (bulk API) |
| Complex queries | SQL (very expressive) | Query DSL (JSON-based) |

## Verdict

- Use **PostgreSQL** as your source of truth for relational data
- Use **Elasticsearch** as a secondary search index for full-text, fuzzy, and analytics queries
- Sync data from Postgres → ES using change data capture (Debezium) or application-level writes
