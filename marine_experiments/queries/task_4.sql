SELECT SP.species_name, E.experiment_id, SP.is_predator, 
CASE
    WHEN SP.is_predator = True THEN ROUND(E.score * 1.2, 1)
    ELSE ROUND(E.score, 1)
    END AS score
FROM experiment as E
JOIN subject as SU
    ON SU.subject_id = E.subject_id
JOIN species as SP
    ON SP.species_id = SU.species_id
ORDER BY score DESC;