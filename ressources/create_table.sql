DROP DATABASE IF EXISTS DutilShawn_TPSommatif;
CREATE DATABASE DutilShawn_TPSommatif;

USE DutilShawn_TPSommatif;

#SELECT no_chapitre_destination FROM lien_chapitre lc WHERE no_chapitre_origine = 1;
#SELECT * FROM livre l ;
SELECT * FROM sauvegarde s ;
#DELETE FROM sauvegarde WHERE id_sauvegarde = 70;

CREATE TABLE discipline (
    id_discipline INTEGER PRIMARY KEY AUTO_INCREMENT,
    notes VARCHAR(64)
);

CREATE TABLE armes (
    id_arme INTEGER PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(64)
);

CREATE TABLE objet (
    id_objet INTEGER PRIMARY KEY AUTO_INCREMENT,
    objet TEXT
);

CREATE TABLE repas (
    id_repas INTEGER PRIMARY KEY AUTO_INCREMENT,
    repas TEXT
);

CREATE TABLE objet_speciaux (
    id_objet_speciaux INTEGER PRIMARY KEY AUTO_INCREMENT,
    contenu TEXT
);

CREATE TABLE bourse (
    id_bourse INTEGER PRIMARY KEY AUTO_INCREMENT,
    contenu TEXT
);

CREATE TABLE chapitre (
    id_chapitre INTEGER PRIMARY KEY AUTO_INCREMENT,
    no_chapitre VARCHAR(64) NOT NULL,
    texte TEXT
);


CREATE TABLE livre (
    id_livre INTEGER PRIMARY KEY AUTO_INCREMENT,
    titre VARCHAR(64) NOT NULL
);

CREATE TABLE lien_livre_chapitre (
    id_livre INTEGER,
    id_chapitre INTEGER,
    FOREIGN KEY (id_livre) REFERENCES livre(id_livre),
    FOREIGN KEY (id_chapitre) REFERENCES chapitre(id_chapitre)
);

CREATE TABLE lien_chapitre (
    id_lien_chapitre INTEGER PRIMARY KEY AUTO_INCREMENT,
    no_chapitre_origine INTEGER,
    no_chapitre_destination INTEGER,
    id_chapitre INTEGER,
    FOREIGN KEY (id_chapitre) REFERENCES chapitre(id_chapitre)
);

CREATE TABLE usager (
    id_usager INTEGER PRIMARY KEY AUTO_INCREMENT,
    nom_usager VARCHAR(64) NOT NULL,
    id_livre INTEGER,
    FOREIGN KEY (id_livre) REFERENCES livre(id_livre)
);

CREATE TABLE feuille_aventure (
    id_feuille_aventure INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_discipline INTEGER,
    id_arme INTEGER,
    id_objet INTEGER,
    id_repas INTEGER,
    id_objet_speciaux INTEGER,
    id_bourse INTEGER,
    FOREIGN KEY (id_discipline) REFERENCES discipline(id_discipline),
    FOREIGN KEY (id_arme) REFERENCES armes(id_arme),
    FOREIGN KEY (id_objet) REFERENCES objet(id_objet),
    FOREIGN KEY (id_repas) REFERENCES repas(id_repas),
    FOREIGN KEY (id_objet_speciaux) REFERENCES objet_speciaux(id_objet_speciaux),
    FOREIGN KEY (id_bourse) REFERENCES bourse(id_bourse)
);

CREATE TABLE sauvegarde (
    id_sauvegarde INTEGER PRIMARY KEY AUTO_INCREMENT,
    nom_sauvegarde VARCHAR(64),
    id_usager INTEGER,
    id_livre INTEGER,
    id_chapitre INTEGER,
    id_feuille_aventure INTEGER,
    FOREIGN KEY (id_usager) REFERENCES usager(id_usager),
    FOREIGN KEY (id_livre) REFERENCES livre(id_livre),
    FOREIGN KEY (id_chapitre) REFERENCES chapitre(id_chapitre),
    FOREIGN KEY (id_feuille_aventure) REFERENCES feuille_aventure(id_feuille_aventure)
);

