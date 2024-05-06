SELECT title from movies As m
JOIN stars ON m.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WhERE people.name IN('Bradley Cooper','Jennifer Lawrence')
GROUP BY title
HAVING COUNT(DISTINCT people.name) = 2;
