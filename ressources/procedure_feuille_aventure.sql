USE DutilShawn_TPSommatif;

DROP PROCEDURE IF EXISTS feuille_aventure_sauvegarde;
DELIMITER $$
CREATE PROCEDURE feuille_aventure_sauvegarde()
BEGIN
    DECLARE last_id_discipline, last_id_arme, last_id_objet, last_id_repas, last_id_objet_speciaux, last_id_bourse INT;

    #SELECT GROUP_CONCAT(id_discipline ORDER BY id_discipline DESC LIMIT 5) INTO last_id_discipline
    #FROM discipline;

    #SELECT GROUP_CONCAT(id_arme ORDER BY id_arme DESC LIMIT 2) INTO last_id_arme
    #FROM armes;

    SELECT id_objet INTO last_id_objet
    FROM objet
    ORDER BY id_objet DESC
    LIMIT 1;

    SELECT id_repas INTO last_id_repas
    FROM repas
    ORDER BY id_repas DESC
    LIMIT 1;

    SELECT id_objet_speciaux INTO last_id_objet_speciaux
    FROM objet_speciaux
    ORDER BY id_objet_speciaux DESC
    LIMIT 1;

    SELECT id_bourse INTO last_id_bourse
    FROM bourse
    ORDER BY id_bourse DESC
    LIMIT 1;

    INSERT INTO feuille_aventure (id_discipline, id_arme, id_objet, id_repas, id_objet_speciaux, id_bourse)
    VALUES (last_id_discipline, last_id_arme, last_id_objet, last_id_repas, last_id_objet_speciaux, last_id_bourse);

END $$

DELIMITER ;


