SELECT COUNT(*) AS Number_of_Movies_WIth_10_Rating FROM movies
JOIN ratings ON movies.id=ratings.movie_id
WHERE rating = 10.0;
