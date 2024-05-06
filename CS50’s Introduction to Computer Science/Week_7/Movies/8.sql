SELECT name from people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WhERE movies.title = 'Toy Story';
