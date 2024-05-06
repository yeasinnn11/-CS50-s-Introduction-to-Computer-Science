SELECT title from movies As m
JOIN stars ON m.id = stars.movie_id
JOIN people ON stars.person_id = people.id
JOIN ratings ON people.id = ratings.movie_id
WhERE people.name = 'Chadwick Boseman'
ORDER BY ratings.rating ASC
LIMIT 5;
