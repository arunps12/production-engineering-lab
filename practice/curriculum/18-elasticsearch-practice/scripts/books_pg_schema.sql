-- Exercise 15.3: Books schema for PostgreSQL (same data as ES)
-- Run: docker exec -i pg_lab psql -U labuser -d labdb < scripts/books_pg_schema.sql

BEGIN;

CREATE TABLE IF NOT EXISTS books (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(300) NOT NULL,
    author          VARCHAR(200) NOT NULL,
    genre           VARCHAR(100) NOT NULL,
    description     TEXT,
    year            INTEGER,
    pages           INTEGER,
    rating          NUMERIC(3,1),
    tags            TEXT[],
    published_date  DATE
);

-- Seed the same 10 books
INSERT INTO books (id, title, author, genre, description, year, pages, rating, tags, published_date) VALUES
(1,  'The Art of Computer Programming',        'Donald Knuth',      'Computer Science',     'Comprehensive monograph on algorithms and data structures', 1968, 3168, 4.9, ARRAY['algorithms','programming','mathematics'], '1968-01-01'),
(2,  'Distributed Systems Design',             'Martin Kleppmann',  'Computer Science',     'Guide to designing data-intensive applications with distributed architecture patterns', 2017, 616, 4.8, ARRAY['distributed','systems','architecture'], '2017-03-16'),
(3,  'Clean Code',                             'Robert C. Martin',  'Software Engineering', 'A handbook of agile software craftsmanship and clean programming practices', 2008, 464, 4.5, ARRAY['clean-code','programming','best-practices'], '2008-08-01'),
(4,  'The Pragmatic Programmer',               'David Thomas',      'Software Engineering', 'From journeyman to master programmer through practical tips and techniques', 2019, 352, 4.7, ARRAY['programming','career','best-practices'], '2019-09-20'),
(5,  'Site Reliability Engineering',           'Betsy Beyer',       'DevOps',               'How Google runs production systems with reliability principles', 2016, 552, 4.6, ARRAY['sre','devops','production'], '2016-03-23'),
(6,  'Python Crash Course',                    'Eric Matthes',      'Programming',          'A hands-on project-based introduction to Python programming language', 2023, 544, 4.6, ARRAY['python','beginner','programming'], '2023-01-10'),
(7,  'Database Internals',                     'Alex Petrov',       'Computer Science',     'Deep dive into how distributed data systems work under the hood', 2019, 350, 4.5, ARRAY['database','internals','distributed'], '2019-10-01'),
(8,  'The Linux Command Line',                 'William Shotts',    'Operating Systems',    'Complete introduction to Linux command line and shell scripting', 2019, 480, 4.4, ARRAY['linux','command-line','shell'], '2019-03-07'),
(9,  'Designing Data-Intensive Applications',  'Martin Kleppmann',  'Computer Science',     'The big ideas behind reliable scalable and maintainable systems', 2017, 624, 4.9, ARRAY['data','distributed','architecture'], '2017-04-18'),
(10, 'Docker Deep Dive',                       'Nigel Poulton',     'DevOps',               'Zero to Docker in a single book covering containers images and orchestration', 2023, 368, 4.3, ARRAY['docker','containers','devops'], '2023-06-15')
ON CONFLICT (id) DO NOTHING;

COMMIT;

SELECT count(*) AS books_loaded FROM books;
