SELECT AVG(rating) AS containing_the_average_rating FROM movies
JOIN ratings ON movies.id=ratings.movie_id
WHERE year = 2012;

