# SQL vs SPARQL — Modeling Comparison

## Dataset

7 books, 7 authors, 4 publishers, 3 languages — with multi-valued relationships.

## Modeling Differences

### Multi-valued Attributes

**SQL:** Requires a junction table (`book_authors`, `book_languages`).

```sql
-- Junction table approach
CREATE TABLE book_authors (
    book_id   INTEGER REFERENCES books(id),
    author_id INTEGER REFERENCES authors(id),
    PRIMARY KEY (book_id, author_id)
);
```

**RDF:** Simply add multiple triples with the same predicate.

```turtle
book:4  schema:author  author:thomas, author:hunt .
```

No extra tables needed. The graph naturally handles multi-valued properties.

### NULL vs Missing Triples

**SQL:** A book without a publisher has `publisher_id = NULL`. You use `LEFT JOIN` to include it.

```sql
SELECT b.title, p.name
FROM books b
LEFT JOIN publishers p ON b.publisher_id = p.id;
```

**SPARQL:** The triple simply doesn't exist. You use `OPTIONAL` (equivalent to LEFT JOIN).

```sparql
SELECT ?title ?publisherName
WHERE {
    ?book dct:title ?title .
    OPTIONAL {
        ?book schema:publisher ?pub .
        ?pub schema:name ?publisherName .
    }
}
```

### Identity

**SQL:** Integer primary keys. Identity is local to the database.

**RDF:** URIs. Identity is globally unique and can be linked across datasets (Linked Data).

```
SQL:  id = 1
RDF:  <http://example.org/book/1>
```

### Schema

**SQL:** Schema must be defined upfront (CREATE TABLE). Adding a column requires ALTER TABLE.

**RDF:** Schema-free. Any resource can have any property. You can add new predicates without schema changes.

### Joins

**SQL:** Explicit JOIN syntax with ON conditions.

```sql
SELECT b.title, a.name
FROM books b
JOIN book_authors ba ON b.id = ba.book_id
JOIN authors a ON ba.author_id = a.id;
```

**SPARQL:** Implicit joins via shared variables in triple patterns.

```sparql
SELECT ?title ?author
WHERE {
    ?book dct:title ?title ;
          schema:author ?authorNode .
    ?authorNode schema:name ?author .
}
```

The variable `?authorNode` acts as the join condition — simpler syntax for graph traversal.

## When to Use Each

| Use Case | Best Choice | Reason |
|----------|-------------|--------|
| Structured business data | SQL | ACID transactions, well-defined schema |
| Knowledge graphs | SPARQL/RDF | Flexible schema, linked data, reasoning |
| Multi-source integration | SPARQL/RDF | URIs enable cross-dataset linking |
| CRUD applications | SQL | Mature tooling, ORM support |
| Ontology / taxonomy | SPARQL/RDF | Built-in class hierarchy (rdfs:subClassOf) |
| Analytics / reporting | SQL | Advanced aggregations, window functions |
