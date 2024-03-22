import sqlite3
connexion = sqlite3.connect('etudiants.db')
cursor = connexion.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS etudiants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT,
                    prenom TEXT,
                    age INTEGER,
                    classe TEXT
                )''')

cursor.execute("INSERT INTO etudiants (nom, prenom, age, classe) VALUES ('Hoki ', 'Clement', 22, 'EID0')")
cursor.execute("INSERT INTO etudiants (nom, prenom, age, classe) VALUES ('Tac', 'Alex', 23, 'EID0')")
cursor.execute("INSERT INTO etudiants (nom, prenom, age, classe) VALUES ('Genetier ', 'Laura', 19, 'EID2')")
cursor.execute("INSERT INTO etudiants (nom, prenom, age, classe) VALUES ('Benjamin', 'Nicolas', 18, 'EID2')")
cursor.execute("INSERT INTO etudiants (nom, prenom, age, classe) VALUES ('Galland', 'Margaux', 17, 'EID3')")
cursor.execute("INSERT INTO etudiants (nom, prenom, age, classe) VALUES ('Pérou', 'Michel', 22, 'EID3')")

# Pour afficher les resultats d'une requete
def afficher_resultats_requete(requete, parametres=None):
    if parametres:
        cursor.execute(requete, parametres)
    else:
        cursor.execute(requete)
    for row in cursor.fetchall():
        print(row)

# Pour afficher tous les étudiants de la base de données.
def afficher_tous_etudiants():
    requete = "SELECT * FROM etudiants"
    afficher_resultats_requete(requete)

# Pour afficher les étudiants d'une classe spécifique.
def affi_classe(classe):
    requete = "SELECT * FROM etudiants WHERE classe=?"
    afficher_resultats_requete(requete, (classe,))

# Pour afficher les étudiants dont l'âge est supérieur à une valeur donnée.
def affi_age_sup(age):
    requete = "SELECT * FROM etudiants WHERE age > ?"
    afficher_resultats_requete(requete, (age,))

# Pour afficher les étudiants dont le nom commence par une lettre spécifique.
def afficher_nom(lettre):
    requete = "SELECT * FROM etudiants WHERE nom LIKE ?"
    afficher_resultats_requete(requete, (lettre + '%',))

# Pour afficher les étudiants dont le nom et le prénom commencent par des lettres spécifiques.
def afficher_nom_prenom(lettre_nom, lettre_prenom):
    requete = "SELECT * FROM etudiants WHERE nom LIKE ? AND prenom LIKE ?"
    afficher_resultats_requete(requete, (lettre_nom + '%', lettre_prenom + '%'))

# Menu principal
while True : 
    print("____Nous sommes capables de repondre à ces questions____.")
    print("1. Afficher tous les étudiants de la base de données.")
    print("2. Afficher les étudiants d'une classe spécifique.")
    print("3. Afficher les étudiants dont l'âge est supérieur à une valeur donnée.")
    print("4. Afficher les étudiants dont le nom commence par une lettre spécifique.")
    print("5. Afficher les étudiants dont le nom et le prénom commencent par des lettres spécifiques.")
    print("0. Quitter.")

    choix = input("Saisissez votre choix: ")

    if choix == '1':
        afficher_tous_etudiants()
    elif choix == '2':
        classe = input("Entrez la classe: ")
        affi_classe(classe)
    elif choix == '3':
        age = int(input("Entrez l'âge minimum: "))
        affi_age_sup(age)
    elif choix == '4':
        lettre = input("Entrez la lettre: ")
        afficher_nom(lettre)
    elif choix == '5':
        lettre_nom = input("Entrez la première lettre du nom: ")
        lettre_prenom = input("Entrez la première lettre du prénom: ")
        afficher_nom_prenom(lettre_nom, lettre_prenom)
    elif choix == '0':
        print("Au revoir !")
        connexion.close()
        exit()
    else:
        print("Choix invalide, veuillez réessayer.")


