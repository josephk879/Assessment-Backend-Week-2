SELECT E.experiment_id, E.subject_id, SP.species_name AS species, 
TO_CHAR(E.experiment_date, 'YYYY-MM-DD') AS experiment_date, ET.type_name AS experiment_type, 
ROUND((E.score/ET.max_score)*100, 2) || '%' AS score
FROM experiment as E
JOIN subject as SU
    ON SU.subject_id = E.subject_id
JOIN species as SP
    ON SP.species_id = SU.species_id
JOIN experiment_type as ET
    ON ET.experiment_type_id = E.experiment_type_id
ORDER BY experiment_date DESC;
