SELECT SU.subject_id, SU.subject_name, SP.species_name, 
TO_CHAR(SU.date_of_birth, 'YYYY-MM') AS date_of_birth
FROM subject AS SU
JOIN species AS SP
    ON SP.species_id = SU.species_id
ORDER BY date_of_birth DESC;