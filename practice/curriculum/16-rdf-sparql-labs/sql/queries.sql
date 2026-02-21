-- Module 16, Exercise 16.4: SQL queries (equivalent to SPARQL queries)

-- Q1: All books with authors (equivalent to 01_all_books.rq)
SELECT b.title, a.name AS author
FROM rdf_books b
JOIN rdf_book_authors ba ON b.id = ba.book_id
JOIN rdf_authors a ON ba.author_id = a.id
ORDER BY b.title;

-- Q2: Books published after 2016 (equivalent to 02_filter_year.rq)
SELECT b.title, b.year
FROM rdf_books b
WHERE b.year >= 2017
ORDER BY b.year;

-- Q3: All books with optional publisher (equivalent to 03_optional_publisher.rq)
SELECT b.title, a.name AS author, p.name AS publisher
FROM rdf_books b
JOIN rdf_book_authors ba ON b.id = ba.book_id
JOIN rdf_authors a ON ba.author_id = a.id
LEFT JOIN rdf_publishers p ON b.publisher_id = p.id
ORDER BY b.title;

-- Q4: Count books by language (equivalent to 04_group_by_language.rq)
SELECT l.name AS language, COUNT(bl.book_id) AS book_count
FROM rdf_languages l
JOIN rdf_book_languages bl ON l.id = bl.language_id
GROUP BY l.name
ORDER BY book_count DESC;

-- Q5: Books with multiple authors (equivalent to 05_multi_author.rq)
SELECT b.title,
       STRING_AGG(a.name, ', ') AS authors,
       COUNT(a.id) AS author_count
FROM rdf_books b
JOIN rdf_book_authors ba ON b.id = ba.book_id
JOIN rdf_authors a ON ba.author_id = a.id
GROUP BY b.title
HAVING COUNT(a.id) > 1
ORDER BY b.title;
