SELECT DISTINCT name from people As p
JOIN directors AS d ON p.id = d.person_id
JOIN movies ON d.movie_id = movies.id
JOIN ratings ON movies.id = ratings.movie_id
WhERE ratings.rating >= 9.0;
