USE DutilShawn_TPSommatif;

DROP PROCEDURE IF EXISTS sauvegarde;
DELIMITER $$

CREATE PROCEDURE sauvegarde(IN last_id_chapitre INT, IN last_nom_sauvegarde VARCHAR(64))
BEGIN
    DECLARE last_id_usager, last_id_livre, last_id_feuille_aventure INT;

    SELECT id_usager INTO last_id_usager
    FROM usager
    ORDER BY id_usager DESC
    LIMIT 1;

    SELECT id_livre INTO last_id_livre
    FROM livre
    ORDER BY id_livre DESC
    LIMIT 1;

    SELECT id_feuille_aventure INTO last_id_feuille_aventure
    FROM feuille_aventure
    ORDER BY id_feuille_aventure DESC
    LIMIT 1;

    INSERT INTO sauvegarde (nom_sauvegarde, id_usager, id_livre, id_chapitre, id_feuille_aventure)
    VALUES (last_nom_sauvegarde, last_id_usager, last_id_livre, last_id_chapitre, last_id_feuille_aventure);

END $$

DELIMITER ;