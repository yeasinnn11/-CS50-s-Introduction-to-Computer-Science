SELECT name from people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WhERE movies.year = 2004
ORDER BY birth;
