import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow
from TP_sommatif_verifier import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *




class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)


        self.setupUi(self)

        self.id_chapitre=1
        id_usager_sauvegarde=None

        # Insertion/afficher de les disciplines
        self.liste_utilisateur.currentTextChanged.connect(self.afficher_discipline)
        self.liste_descipline_1.currentTextChanged.connect(self.insertion_discipline1)
        self.liste_descipline_2.currentTextChanged.connect(self.insertion_discipline2)
        self.liste_descipline_3.currentTextChanged.connect(self.insertion_discipline3)
        self.liste_descipline_4.currentTextChanged.connect(self.insertion_discipline4)
        self.liste_descipline_5.currentTextChanged.connect(self.insertion_discipline5)

        # Insertion/afficher de les armes
        self.liste_utilisateur.currentTextChanged.connect(self.afficher_armes)
        self.liste_arme_1.currentTextChanged.connect(self.insertion_arme1)
        self.liste_arme_2.currentTextChanged.connect(self.insertion_arme2)

        # Insertion objet / repas / objet_speiaux / bourse
        self.contenu_objet.textChanged.connect(self.insertion_objet)
        self.contenu_repas.textChanged.connect(self.insertion_repas)
        self.contenu_objet_speciaux.textChanged.connect(self.insertion_objet_sepciaux)
        self.spinBox_bourse.valueChanged.connect(self.insertion_bourse)


        # afficher usager / livre / contexte / usage / texte / chapitre
        self.afficher_usager(id_usager_sauvegarde)
        self.afficher_livre()
        self.afficher_contexte()
        self.liste_utilisateur.currentTextChanged.connect(lambda: self.afficher_chapitre(self.id_chapitre))
        self.btn_execution_chapitre.clicked.connect(self.chapitre_selectionne_et_affiche)
        self.liste_utilisateur.currentTextChanged.connect(self.afficher_texte)
        
        # Creation usager / feuille d'aventure / sauvegarde 
        self.btn_creation_usager.clicked.connect(self.creation_usager)
        self.btn_feuille_aventure.clicked.connect(self.enregistrer_feuille_aventure)
        self.btn_creation_sauvegarde.clicked.connect(self.creation_sauvegarde)
        self.afficher_sauvegarde()
        self.btn_supprimer_sauvegarde.clicked.connect(self.supprimer_sauvegarde_selectionnee)
        self.btn_afficher_sauvegarde.clicked.connect(self.charger_sauvegarde)

    ##########################################
    #              Livre                     #
    ##########################################

    def afficher_livre(self):
        cnx = mysql.connector.connect(
        user='shawn',
        password='shawn',
        host='localhost',
        database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT titre FROM livre;"

        cursor.execute(query)
        livres = cursor.fetchall()

        for livre in livres:
            self.liste_livre.addItem(livre['titre'])
            
        cursor.close()
        cnx.close()  

    ##########################################
    #              Sauvegarde                #
    ##########################################

    def charger_sauvegarde(self):
        print("Entering charger_sauvegarde")
        nom_sauvegarde = self.liste_sauvegarde.currentText()

        if nom_sauvegarde != "Choisissez une sauvegarde...":
            print("Selected Sauvegarde:", nom_sauvegarde)

            cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

            cursor = cnx.cursor(dictionary=True)

            try:
                query_select_sauvegarde = "SELECT id_usager,id_chapitre,id_feuille_aventure FROM sauvegarde WHERE nom_sauvegarde = %s;"
                values_select_sauvegarde = (nom_sauvegarde,)
                cursor.execute(query_select_sauvegarde, values_select_sauvegarde)
                
                sauvegarde_ids = cursor.fetchall()

                if sauvegarde_ids:
                    print("Sauvegarde IDs:", sauvegarde_ids)
                    self.afficher_usager(sauvegarde_ids[0]['id_usager'])
                    self.id_chapitre = (sauvegarde_ids[0]['id_chapitre'] - 1)
                    print("ID Chapitre:", sauvegarde_ids[0]['id_chapitre'])
                    self.afficher_texte(self.id_chapitre)
                    self.afficher_feuille_aventure(sauvegarde_ids[0]['id_feuille_aventure'])
                    print("salut",sauvegarde_ids[0]['id_feuille_aventure'])

            except mysql.connector.errors.InternalError as err:
                import traceback
                traceback.print_exc()
                print(f"Erreur lors de la récupération des données de la sauvegarde : {err}")

            finally:
                cursor.close()
                cnx.close()

    def supprimer_sauvegarde_selectionnee(self):
        index = self.liste_sauvegarde.currentIndex()

        if index > 0:
            sauvegarde_id = self.chercher_id_sauvegarde(index)
        if sauvegarde_id is not None:
            self.supprimer_sauvegarde(sauvegarde_id)

    def chercher_id_sauvegarde(self, index):
        item_text = self.liste_sauvegarde.itemText(index)

        if item_text != "Choisissez une sauvegarde...":
            cnx = mysql.connector.connect(
                user='shawn',
                password='shawn',
                host='localhost',
                database='DutilShawn_TPSommatif'
            )
            cursor = cnx.cursor(dictionary=True)

            try:
                query_select_sauvegarde = "SELECT id_sauvegarde FROM sauvegarde WHERE nom_sauvegarde = %s;"
                values_select_sauvegarde = (item_text,)
                cursor.execute(query_select_sauvegarde, values_select_sauvegarde)

                sauvegarde_id = cursor.fetchall()
                return sauvegarde_id[0]['id_sauvegarde'] if sauvegarde_id else None

            except mysql.connector.errors.InternalError as err:
                import traceback
                traceback.print_exc()
                print(f"Erreur lors de la récupération de l'id de la sauvegarde : {err}")

            finally:
                cursor.close()
                cnx.close()

        return None

    def supprimer_sauvegarde(self,sauvegarde_id):

        cnx = mysql.connector.connect(
        user='shawn',
        password='shawn',
        host='localhost',
        database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        try:
            query = "DELETE FROM sauvegarde WHERE id_sauvegarde = %s"
            values = (sauvegarde_id,)
            cursor.execute(query, values)
            cnx.commit()

            self.liste_sauvegarde.clear()
            self.afficher_sauvegarde()

        except mysql.connector.Error as err:
            print(f"Erreur lors de la suppression de la sauvegarde : {err}")

        finally:
            cursor.close()
            cnx.close()
    
    def afficher_sauvegarde(self):
        cnx = mysql.connector.connect(
        user='shawn',
        password='shawn',
        host='localhost',
        database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT nom_sauvegarde FROM sauvegarde;"

        cursor.execute(query)
        sauvegardes = cursor.fetchall()

        self.liste_sauvegarde.clear()
        self.liste_sauvegarde.addItem("Choisissez une sauvegarde...")
        self.liste_sauvegarde.setCurrentIndex(0)

        for sauvegarde in sauvegardes:
            self.liste_sauvegarde.addItem(sauvegarde['nom_sauvegarde'])

        cursor.close()
        cnx.close()

    def creation_sauvegarde_sans_sauvegarder(self, idChapitre):
        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.input_sauvegarde.text()

        try:
            self.idchapitre = idChapitre

        except mysql.connector.Error as err:
            print(f"Error during creation_sauvegarde_sans_sauvegarder: {err}")
        finally:
            cursor.close()
            cnx.close()

    def creation_sauvegarde(self, idChapitre):
        idChapitre = self.idchapitre
        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.input_sauvegarde.text()

        try:
            # Appel de la procédure stockée avec le nom de la sauvegarde et l'id du chapitre
            query_call_sauvegarde = "CALL sauvegarde(%s, %s);"
            values_call_sauvegarde = (idChapitre,texte_saisi)
            cursor.execute(query_call_sauvegarde, values_call_sauvegarde)
            cnx.commit()
            print("Procédure stockée exécutée avec succès!")

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de la procédure stockée : {err}")
        finally:
            cursor.close()
            cnx.close()

        self.afficher_sauvegarde()
    
    ##########################################
    #            feuille aventure            #
    ##########################################
    def afficher_feuille_aventure(self,id_feuille_aventure):
        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT id_objet, id_repas, id_objet_speciaux, id_bourse FROM feuille_aventure WHERE id_feuille_aventure = %s;"
        values = (id_feuille_aventure,)
        cursor.execute(query, values)
                
        feuille_aventure_ids = cursor.fetchall()

        if feuille_aventure_ids:
            self.afficher_objet(feuille_aventure_ids[0]['id_objet'])
            self.afficher_repas(feuille_aventure_ids[0]['id_repas'])
            self.afficher_objet_speciaux(feuille_aventure_ids[0]['id_objet_speciaux'])
            self.afficher_bourse(feuille_aventure_ids[0]['id_bourse'])

    def enregistrer_feuille_aventure(self):
        cnx = mysql.connector.connect(
        user='shawn',
        password='shawn',
        host='localhost',
        database='DutilShawn_TPSommatif')

        try:
            cursor = cnx.cursor()
            cursor.callproc('feuille_aventure_sauvegarde')
            cnx.commit()
            print("Stored procedure executed successfully!")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            cnx.close()

    ##########################################
    #               Bourse                   #
    ##########################################
    
    def afficher_bourse(self,id_bourse):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT contenu FROM bourse WHERE id_bourse = %s;"
        values = (id_bourse,)

        cursor.execute(query,values)

        bourse = cursor.fetchone()
        self.spinBox_bourse.setValue(int(bourse['contenu']))

        cnx.commit()

        cursor.close()
        cnx.close()

    def insertion_bourse(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        nombre = self.spinBox_bourse.value()

        query = "INSERT INTO bourse(contenu) VALUES(%s);"
        values = (nombre,)

        cursor.execute(query,values)
        cnx.commit()

        cursor.close()
        cnx.close()

    ##########################################
    #            Objet speciaux              #
    ##########################################

    def afficher_objet_speciaux(self,id_objet_speciaux):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT contenu FROM objet_speciaux WHERE id_objet_speciaux = %s;"
        values = (id_objet_speciaux,)

        cursor.execute(query,values)
        objet_speciaux = cursor.fetchone()
        self.contenu_objet_speciaux.setPlainText(objet_speciaux['contenu'])
        cnx.commit()

        cursor.close()
        cnx.close()

    def insertion_objet_sepciaux(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.contenu_objet_speciaux.toPlainText()

        query = "INSERT INTO objet_speciaux(contenu) VALUES(%s);"
        values = (texte_saisi,)

        cursor.execute(query,values)
        cnx.commit()

        cursor.close()
        cnx.close()

    ##########################################
    #               Repas                    #
    ##########################################

    def afficher_repas(self,id_repas):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT repas FROM repas WHERE id_repas = %s;"
        values = (id_repas,)

        cursor.execute(query,values)
        _repas = cursor.fetchone()
        self.contenu_repas.setPlainText(_repas['repas'])
        cnx.commit()

        cursor.close()
        cnx.close()


    def insertion_repas(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.contenu_repas.toPlainText()

        query = "INSERT INTO repas(repas) VALUES(%s);"
        values = (texte_saisi,)

        cursor.execute(query,values)
        cnx.commit()

        cursor.close()
        cnx.close()

    ##########################################
    #               Objet                    #
    ##########################################

    def afficher_objet(self,id_objet):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT objet FROM objet WHERE id_objet = %s;"
        values = (id_objet,)

        cursor.execute(query,values)
        _objet = cursor.fetchone()
        self.contenu_objet.setPlainText(_objet['objet'])
        cnx.commit()

        cursor.close()
        cnx.close()

    def insertion_objet(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.contenu_objet.toPlainText()

        query = "INSERT INTO objet(objet) VALUES(%s);"
        values = (texte_saisi,)

        cursor.execute(query,values)

        cnx.commit()
        cursor.close()
        cnx.close()

            
    ##########################################
    #               Armes                    #
    ##########################################

    def afficher_armes(self):
        self.liste_arme_1.clear()
        self.liste_arme_2.clear()

        nom_usager = self.liste_utilisateur.currentText()

        if nom_usager:
            cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

            cursor = cnx.cursor(dictionary=True)

            query = "SELECT nom FROM armes;"

            cursor.execute(query)
            armes = cursor.fetchall()
            self.liste_arme_1.addItem("Choisissez une arme...")
            self.liste_arme_1.setCurrentIndex(0)
            self.liste_arme_2.addItem("Choisissez une arme...")
            self.liste_arme_2.setCurrentIndex(0)

            compteur = 0
            for arme in armes:
                compteur += 1
                self.liste_arme_1.addItem(arme['nom'])
                self.liste_arme_2.addItem(arme['nom'])
                if compteur >= 10:
                    break

            cursor.close()
            cnx.close()



    def insertion_arme1(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.liste_arme_1.currentText()

        query = "INSERT INTO armes(nom) VALUES(%s);"
        values = (texte_saisi,)

        cursor.execute(query, values)
        cnx.commit()

        cursor.close()
        cnx.close()

    def insertion_arme2(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.liste_arme_2.currentText()

        query = "INSERT INTO armes(nom) VALUES(%s);"
        values = (texte_saisi,)

        cursor.execute(query, values)
        cnx.commit()

        cursor.close()
        cnx.close()

        
    ##########################################
    #              Discipline                #
    ##########################################
    def afficher_discipline(self):
        nom_usager = self.liste_utilisateur.currentText()

        if nom_usager:
            cnx = mysql.connector.connect(
                user='shawn',
                password='shawn',
                host='localhost',
                database='DutilShawn_TPSommatif'
            )

            cursor = cnx.cursor(dictionary=True)

            query = "SELECT notes FROM discipline;"

            cursor.execute(query)

            self.liste_descipline_1.addItem("Choisissez une discipline...")
            self.liste_descipline_1.setCurrentIndex(0)
            self.liste_descipline_2.addItem("Choisissez une discipline...")
            self.liste_descipline_2.setCurrentIndex(0)
            self.liste_descipline_3.addItem("Choisissez une discipline...")
            self.liste_descipline_3.setCurrentIndex(0)
            self.liste_descipline_4.addItem("Choisissez une discipline...")
            self.liste_descipline_4.setCurrentIndex(0)
            self.liste_descipline_5.addItem("Choisissez une discipline...")
            self.liste_descipline_5.setCurrentIndex(0)

            disciplines = cursor.fetchall()

            for discipline in disciplines:
                self.liste_descipline_1.addItem(discipline['notes'])
                self.liste_descipline_2.addItem(discipline['notes'])
                self.liste_descipline_3.addItem(discipline['notes'])
                self.liste_descipline_4.addItem(discipline['notes'])
                self.liste_descipline_5.addItem(discipline['notes'])

            cursor.close()
            cnx.close()

    def insertion_discipline1(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.liste_descipline_1.currentText()

        query = "INSERT INTO discipline(notes) VALUES(%s);"
        values = (texte_saisi,)

        cursor.execute(query, values)
        cnx.commit()

        cursor.close()
        cnx.close()


    def insertion_discipline2(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.liste_descipline_2.currentText()

        query = "INSERT INTO discipline(notes) VALUES(%s);"
        values = (texte_saisi,)

        cursor.execute(query, values)
        cnx.commit()

        cursor.close()
        cnx.close()


    def insertion_discipline3(self):
        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.liste_descipline_3.currentText()

        query = "INSERT INTO discipline(notes) VALUES(%s);"
        values = (texte_saisi,)

        cursor.execute(query, values)

        cnx.commit()
        cursor.close()
        cnx.close()

    def insertion_discipline4(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.liste_descipline_4.currentText()

        query = "INSERT INTO discipline(notes) VALUES(%s);"

        values = (texte_saisi,)
        cursor.execute(query, values)

        cnx.commit()
        cursor.close()
        cnx.close()



    def insertion_discipline5(self):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        texte_saisi = self.liste_descipline_5.currentText()

        query = "INSERT INTO discipline(notes) VALUES(%s);"

        values = (texte_saisi,)
        cursor.execute(query, values)

        cnx.commit()
        cursor.close()
        cnx.close()

    ##########################################
    #               Texte                    #
    ##########################################

    def afficher_texte(self,id_chapitre):

        id_chapitre = self.id_chapitre + 1

        nom_usager = self.liste_utilisateur.currentText()

        if nom_usager:
            
            cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

            cursor = cnx.cursor(dictionary=True)

            query = "SELECT DISTINCT chapitre.texte \
                        FROM chapitre \
                        INNER JOIN lien_livre_chapitre ON chapitre.id_chapitre = lien_livre_chapitre.id_chapitre \
                        INNER JOIN livre ON lien_livre_chapitre.id_livre = livre.id_livre \
                        INNER JOIN usager ON usager.id_livre = livre.id_livre \
                        WHERE chapitre.id_chapitre = %s AND usager.nom_usager = %s;"
            
            values = (id_chapitre, nom_usager)

            self.creation_sauvegarde_sans_sauvegarder(id_chapitre)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                texte = result['texte']
                self.contenu_texte.setPlainText(texte)
            else:
                self.contenu_texte.clear()

            self.afficher_chapitre(id_chapitre - 1)

            cnx.commit()
            cursor.close()
            cnx.close()
 
    def afficher_contexte(self):
        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT texte FROM chapitre WHERE id_chapitre = 1;"

        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            texte = result['texte']
            self.contenu_texte.setPlainText(texte)
        else:
            self.contenu_texte.clear()

        cursor.close()
        cnx.close()

    ##########################################
    #               Chapitre                 #
    ##########################################

    def afficher_chapitre(self,id_chapitre):
        self.liste_chapitres.clear()

        nom_usager = self.liste_utilisateur.currentText()

        if nom_usager:

            cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

            cursor = cnx.cursor(dictionary=True)

            query = "SELECT DISTINCT no_chapitre_destination FROM lien_chapitre WHERE no_chapitre_origine = %s;"
            values = (id_chapitre,)

            cursor.execute(query, values)

            chapitres = cursor.fetchall()

            for chapitre in chapitres:
                self.liste_chapitres.addItem(str(chapitre['no_chapitre_destination']))

            cnx.commit()
            cursor.close()
            cnx.close()


    def chapitre_selectionne_et_affiche(self):

        nouvelle_valeur = int(self.liste_chapitres.currentText())

        self.id_chapitre = nouvelle_valeur
        self.afficher_texte(self.id_chapitre)


    ##########################################
    #               Usager                   #
    ##########################################
    def creation_usager(self):
        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)


        texte_saisi = self.input_usager.text()

        query = "INSERT INTO usager(nom_usager,id_livre) VALUES(%s,1);"
        values = (texte_saisi,)

        cursor.execute(query,values)
        cnx.commit()

        cursor.close()
        cnx.close()

        self.liste_utilisateur.addItem(texte_saisi)

    def afficher_usager(self, id_usager_sauvegarde=None):

        cnx = mysql.connector.connect(
            user='shawn',
            password='shawn',
            host='localhost',
            database='DutilShawn_TPSommatif')

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT id_usager, nom_usager FROM usager;"

        cursor.execute(query)
        usagers = cursor.fetchall()

        self.liste_utilisateur.clear()
        self.liste_utilisateur.addItem("Choisissez un usager...")
        self.liste_utilisateur.setCurrentIndex(0)

        for usager in usagers:
            self.liste_utilisateur.addItem(usager['nom_usager'])

            if id_usager_sauvegarde is not None and usager['id_usager'] == id_usager_sauvegarde:
                #print("id usager dsadsadadsadasd",id_usager_sauvegarde)
                self.liste_utilisateur.setCurrentIndex(id_usager_sauvegarde)

        cursor.close()
        cnx.close()

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()