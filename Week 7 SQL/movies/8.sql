SELECT name FROM people WHERE id IN
(SELECT person_id FROM stars LEFT JOIN movies ON movies.id = stars.movie_id WHERE title = 'Toy Story');