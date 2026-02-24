-- Module 16, Exercise 16.4: SQL schema for books comparison
-- Relational model equivalent of the RDF data

BEGIN;

CREATE TABLE IF NOT EXISTS rdf_authors (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    birth_date  DATE,
    nationality VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS rdf_publishers (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(200) NOT NULL,
    location VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS rdf_languages (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS rdf_books (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(300) NOT NULL,
    publisher_id    INTEGER REFERENCES rdf_publishers(id),
    year            INTEGER,
    pages           INTEGER,
    genre           VARCHAR(100),
    description     TEXT
);

-- Junction table for many-to-many: books <-> authors
CREATE TABLE IF NOT EXISTS rdf_book_authors (
    book_id   INTEGER NOT NULL REFERENCES rdf_books(id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES rdf_authors(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

-- Junction table for many-to-many: books <-> languages
CREATE TABLE IF NOT EXISTS rdf_book_languages (
    book_id     INTEGER NOT NULL REFERENCES rdf_books(id) ON DELETE CASCADE,
    language_id INTEGER NOT NULL REFERENCES rdf_languages(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, language_id)
);

COMMIT;
