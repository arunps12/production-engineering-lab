-- Module 16, Exercise 16.4: Seed data (same as sample.ttl)

BEGIN;

-- Authors
INSERT INTO rdf_authors (id, name, birth_date, nationality) VALUES
    (1, 'Donald Knuth',      '1938-01-10', 'American'),
    (2, 'Martin Kleppmann',  '1985-04-22', 'German'),
    (3, 'Robert C. Martin',  NULL,         'American'),
    (4, 'David Thomas',      NULL,         'British'),
    (5, 'Andrew Hunt',       NULL,         'American'),
    (6, 'Betsy Beyer',       NULL,         'American'),
    (7, 'Eric Matthes',      NULL,         'American')
ON CONFLICT (id) DO NOTHING;

-- Publishers
INSERT INTO rdf_publishers (id, name, location) VALUES
    (1, 'Addison-Wesley',   'Boston, MA'),
    (2, 'O''Reilly Media',  'Sebastopol, CA'),
    (3, 'Prentice Hall',    'Upper Saddle River, NJ'),
    (4, 'No Starch Press',  'San Francisco, CA')
ON CONFLICT (id) DO NOTHING;

-- Languages
INSERT INTO rdf_languages (id, name) VALUES
    (1, 'English'),
    (2, 'German'),
    (3, 'French')
ON CONFLICT (name) DO NOTHING;

-- Books
INSERT INTO rdf_books (id, title, publisher_id, year, pages, genre, description) VALUES
    (1, 'The Art of Computer Programming',       1, 1968, 3168, 'Computer Science',     'Comprehensive monograph on algorithms and data structures'),
    (2, 'Designing Data-Intensive Applications',  2, 2017, 624,  'Computer Science',     'The big ideas behind reliable scalable and maintainable systems'),
    (3, 'Clean Code',                             3, 2008, 464,  'Software Engineering', 'A handbook of agile software craftsmanship'),
    (4, 'The Pragmatic Programmer',               1, 2019, 352,  'Software Engineering', 'From journeyman to master programmer'),
    (5, 'Site Reliability Engineering',           2, 2016, 552,  'DevOps',               'How Google runs production systems'),
    (6, 'Python Crash Course',                    4, 2023, 544,  'Programming',          'A hands-on project-based introduction to Python'),
    (7, 'Database Internals',                     2, 2019, 350,  'Computer Science',     'Deep dive into how distributed data systems work')
ON CONFLICT (id) DO NOTHING;

-- Book-Author relationships
INSERT INTO rdf_book_authors (book_id, author_id) VALUES
    (1, 1), -- Art of Programming - Knuth
    (2, 2), -- DDIA - Kleppmann
    (3, 3), -- Clean Code - Martin
    (4, 4), -- Pragmatic Programmer - Thomas
    (4, 5), -- Pragmatic Programmer - Hunt (multi-author!)
    (5, 6), -- SRE - Beyer
    (6, 7), -- Python Crash Course - Matthes
    (7, 2)  -- Database Internals - Kleppmann
ON CONFLICT DO NOTHING;

-- Book-Language relationships
INSERT INTO rdf_book_languages (book_id, language_id) VALUES
    (1, 1), -- English
    (2, 1), (2, 2), -- English + German
    (3, 1), (3, 3), -- English + French
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1)
ON CONFLICT DO NOTHING;

COMMIT;

SELECT 'Seed complete' AS status,
       (SELECT count(*) FROM rdf_books) AS books,
       (SELECT count(*) FROM rdf_authors) AS authors;
