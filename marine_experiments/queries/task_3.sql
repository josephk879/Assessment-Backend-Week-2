SELECT ET.type_name, SP.species_name, ROUND(AVG(E.score), 1) AS average_score
FROM experiment AS E
JOIN subject as SU
    ON SU.subject_id = E.subject_id
JOIN species as SP
    ON SP.species_id = SU.species_id
JOIN experiment_type as ET
    ON ET.experiment_type_id = E.experiment_type_id
GROUP BY ET.type_name, SP.species_name
HAVING ROUND(AVG(E.score), 1) > 5
ORDER BY ROUND(AVG(E.score), 1) DESC;