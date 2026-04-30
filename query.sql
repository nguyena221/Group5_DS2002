USE recipes;

SELECT *
FROM recipes.file_processing_log
WHERE Status = 'SUCCESS';
