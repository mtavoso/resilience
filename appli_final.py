
import psycopg2
import random
import math
import numpy as np


HOST = "tuxa.sme.utc"
USER = "nf18a045"
PASSWORD = "t7R2VmrxnT9H"
DATABASE = "dbnf18a045"


# lire le fichier .sql
with open("rendu_3.sql", "r", encoding="utf-8") as f:
    rendu_3 = f.read()
with open("rendu_4.sql", "r", encoding="utf-8") as f:
    rendu_4 = f.read()

# Open connection
conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
# Open a cursor to send SQL commands
cur = conn.cursor()

# Validation valeur int
def input_int(prompt, min_val=None, max_val=None, allow_empty=False):
    while True:
        s = input(prompt)
        if allow_empty and s.strip() == "":
            return None
        try:
            v = int(s)
        except Exception:
            print("Entrée invalide, entrez un nombre entier.")
            continue
        if min_val is not None and v < min_val:
            print(f"Valeur trop petite (>= {min_val}).")
            continue
        if max_val is not None and v > max_val:
            print(f"Valeur trop grande (<= {max_val}).")
            continue
        return v

# Validation choix dans une liste de valeurs
def input_choice(prompt, choices):
    # choices: iterable of allowed string values
    while True:
        s = input(prompt).strip()
        if s in choices:
            return s
        print(f"Choix invalide. Valeurs possibles: {', '.join(map(str,choices))}")


# Décomenter la ligne suivante pour initialiser la BDD
#cur.execute(rendu_3)
#conn.commit()

def connexion():
    run = True
    while run:
        print("\nVeuillez vous connecter :")
        prenom = input("Entrez votre prénom : ").strip()
        nom = input("Entrez votre nom : ").strip()


        # Vérifier login
        cur.execute("SELECT id,mot_de_passe FROM Personne WHERE nom = %s AND prenom =%s", (nom,prenom))
        user = cur.fetchone()
        #Décommenter la ligne suivante pour voir le mot de passe
        #print(f"Mot de passe: {user}")

        if user is None:
            choix=input("Cette personne n'est pas présente dans la base. Voulez-vous l'inscrire? (oui ou non)").strip()
            if(choix=="oui"):
                inscription()
                break
            continue
        
        db_password = user[1]


        # Vérifier mot de passe
        password = input("Entrez mot de passe : ").strip()

        if password != db_password:
            print("Mot de passe incorrect.")
            continue
        
        global utilisateur_connecte
        utilisateur_connecte=[user[0],prenom,nom]
        conn.commit()
        # Auth OK → sortir de la boucle login
        print("Connexion réussie !")
        run = False

def inscription():
    print("Inscription")
    prenom=str(input("Entrez prenom de la personne: ").strip())
    nom=str(input("Entrez nom de la personne: ").strip())
    mdp=str(input("Entrez le mot de passe de la personne: ").strip())
    pos=str(input("Entrez la localisation de la personne dans le format longitude,latitude : ").strip()).split(",")

    request1="INSERT INTO Localisation(longitude,latitude) VALUES(%s, %s);"
    cur.execute(request1,(pos[0],pos[1]))
    request2="SELECT num FROM Localisation WHERE longitude=%s AND latitude=%s"
    cur.execute(request2,(pos[0],pos[1]))
    id_loca=cur.fetchone()

    request3="INSERT INTO Personne (prenom, nom, mot_de_passe, loca) VALUES(%s,%s,%s,%s)"
    cur.execute(request3,(prenom,nom,mdp,id_loca))

    cur.execute("SELECT id,mot_de_passe FROM Personne WHERE nom = %s AND prenom =%s", (nom,prenom))
    a=cur.fetchone()
    global utilisateur_connecte
    utilisateur_connecte=[a[0],prenom,nom]
    conn.commit()
    print("Personne créé avec succés")

def voir_liste_personne():
        requete="SELECT prenom, nom, longitude, latitude FROM PERSONNE p JOIN LOCALISATION l ON p.loca=l.num; "
        cur.execute(requete)
        x=cur.fetchall()
        print("Liste des personnes dans l'application")
        for i in x:
            print(f"Prénom: {i[0]} | Nom: {i[1]} | Localisation: https://www.openstreetmap.org/#map=17/{i[2]}/{i[3]}")
        quit=None
        while quit==None:
            quit=input("Appuyez sur entrer pour quitter ")

def creer_communaute():
    nom_commu=str(input("Entrez le nom de la communauté "))
    id_loca=None
    choix=str(input("Voulez-vous ajouter une localisation à votre communauté? (oui ou non) "))
    if choix=="oui":
        pos=str(input("Entrez la localisation de la communauté dans le format longitude,latitude : ").strip()).split(",")
        request1="INSERT INTO Localisation(longitude,latitude) VALUES(%s, %s);"
        cur.execute(request1,(pos[0],pos[1]))
        conn.commit()
        request2="SELECT num FROM Localisation WHERE longitude=%s AND latitude=%s"
        cur.execute(request2,(pos[0],pos[1]))
        id_loca=cur.fetchone()



    requete="INSERT INTO Communaute (nom, loca, createur) VALUES " \
    "(%s, %s, %s)"
    cur.execute(requete,(nom_commu,id_loca,utilisateur_connecte[0]))

    requete="INSERT INTO Membre (personne, communaute) VALUES " \
    "(%s, %s)"
    cur.execute(requete,(utilisateur_connecte[0],nom_commu))
    conn.commit()
    print("Communauté créé avec succés")

#Vue Communauté
def voir_liste_communaute():
    requete = """
        SELECT nom, longitude, latitude, createur
        FROM Communaute c
        LEFT JOIN Localisation l ON c.loca = l.num
    """
    cur.execute(requete)
    x = cur.fetchall()

    print("Liste des communautés dans l'application")

    for i in x:
        # Récupérer le créateur
        request = "SELECT prenom, nom FROM Personne WHERE id = %s"
        cur.execute(request, (i[3],))
        a = cur.fetchone()
        createur = f"{a[0]} {a[1]}"

        # Vérifier si l'utilisateur est membre
        requete = """
            SELECT 1 FROM Membre
            WHERE communaute = %s AND personne = %s
        """
        cur.execute(requete, (i[0], utilisateur_connecte[0]))
        membre = cur.fetchone()

        print(
            f"Nom de la communauté: {i[0]} | "
            f"Localisation: ({i[1]}, {i[2]}) | "
            f"Createur: {createur} | "
            f"{bool(membre)}"
        )

    input("Appuyez sur entrer pour quitter")


def ajouter_savoir_faire():
     print ("Ajouter un savoir a une comunauté dont vous êtes membre[1] ou a vous même[2]?")
     type_savoir = input("Votre choix : ").strip()
     if type_savoir == "1":
        print("Voici la liste des communautés dont vous êtes membre :")

        cur.execute("""
            SELECT Communaute.nom
            FROM Communaute
            JOIN Membre ON Communaute.nom = Membre.communaute
            WHERE Membre.personne = %s
        """, (utilisateur_connecte[0],))

        communautes = cur.fetchall()

        for i, communaute in enumerate(communautes, start=1):
            print(f"{i}) {communaute[0]}")

        choix = input_int("Numéro de la communauté : ", min_val=1)
        nom_communaute = communautes[choix - 1][0]

        savoir = input("Savoir : ")
        niveau = input_int("Niveau (1 à 5) : ", min_val=1, max_val=5)

        # Vérifier si le savoir existe
        cur.execute("SELECT intitule FROM Savoir_faire WHERE intitule = %s", (savoir,))
        result = cur.fetchone()

        if not result:
            cur.execute(
                "INSERT INTO Savoir_faire (intitule) VALUES (%s)",
                (savoir,)
            )

        # Insérer la maîtrise
        cur.execute("""
            INSERT INTO Maitrise_communautaire (communaute, savoir_faire, rang)
            VALUES (%s, %s, %s)
        """, (nom_communaute, savoir, niveau))

        conn.commit()

     elif type_savoir == "2":
        print("Quel est le savoir que vous voulez ajouter?")
        savoir = input("Savoir : ")
        print ("De 1 a 5 quelle est le niveau de maitrise de ce savoir?")
        niveau = input_int("Niveau : ", min_val=1, max_val=5)
        cur.execute("Select * FROM savoir_faire WHERE intitule = %s", (savoir,))
        result = cur.fetchone()
        if result:
            sql = "INSERT INTO Maitrise_personnelle (personne, savoir, rang) VALUES (%s, %s, %s)"
            cur.execute(sql, (utilisateur_connecte[0], savoir, niveau))
            conn.commit()
        else:
            sql = "INSERT INTO Savoir_faire (intitule) VALUES (%s)"
            cur.execute(sql, (savoir,))
            conn.commit()
            sql = "INSERT INTO Maitrise_personnelle (personne, savoir, rang) VALUES (%s, %s, %s)"
            cur.execute(sql, (utilisateur_connecte[0], savoir, niveau))
            conn.commit()

def proposer_service():
    print("Ajout un service que vous proposez")
    nom_service=str(input("Entrez le service que vous proposez: ").strip())
    type_service=input_int("Le service est-il payant (1), gratuit(2) ou contre un autre service(3)? ")

    request="SELECT s.service_id FROM Service s JOIN Proposition_service ps ON s.service_id=ps.service WHERE s.nom=%s AND ps.personne=%s"
    cur.execute(request,[nom_service,utilisateur_connecte[0]])
    id_service=cur.fetchall()
    if(len(id_service)==0):
        #Si il n'existe pas on crée le service et la personne qui le propose veut mettre à jour la contrepartie
        request="INSERT INTO Service (nom) VALUES(%s)"
        cur.execute(request,[nom_service])

        request="SELECT service_id FROM Service WHERE nom=%s"
        cur.execute(request,[nom_service])
        id_service=cur.fetchone()
        if(type_service==1):
            prix=input_int("Fixez un prix à votre service : ", min_val=0)
            request="INSERT INTO Service_commercial (service, somme) VALUES(%s,%s)"
            cur.execute(request,[id_service[0],prix])
        elif type_service==2:
            request="INSERT INTO Service_gratuit (service) VALUES(%s)"
            cur.execute(request,[id_service[0]])
        elif type_service==3:
            nom_service_echange=str(input("Entrez le nom du service avec lequel vous voulez l'échanger (ou rien si pas encore déterminé): ").strip())
            request="SELECT service_id FROM Service WHERE nom=%s"
            cur.execute(request,[nom_service_echange])
            id_service_echange=cur.fetchone()
            if id_service_echange:
                request="INSERT INTO Service_echange (service, contrepartie) VALUES(%s,%s)"
                cur.execute(request,[id_service[0],id_service_echange[0]])
            else:
                request="INSERT INTO Service_echange (service, contrepartie) VALUES(%s,%s)"
                cur.execute(request,[id_service[0],None])
        request="INSERT INTO Proposition_service (personne, service) VALUES(%s,%s)"
        cur.execute(request,(utilisateur_connecte[0],id_service[0] if isinstance(id_service, tuple) else id_service))
        conn.commit()     
    else:
        id_service = id_service[0]

        # Si le service existe, vérifier s'il est un service d'échange et la personne qui le propose veut mettre à jour la somme
        try:
            service_id = id_service[0] if isinstance(id_service, tuple) else id_service
        except Exception:
            service_id = id_service

        cur.execute("SELECT service, contrepartie FROM Service_echange WHERE service = %s", (service_id,))
        service_echange = cur.fetchone()
        if service_echange:
            choix_maj = input("Ce service est un service d'échange. Voulez-vous mettre à jour sa contrepartie ? (oui/non) ").strip().lower()
            if choix_maj == "oui":
                nom_service_echange = input("Entrez le nom du service à mettre comme contrepartie (ou rien pour effacer): ").strip()
                if nom_service_echange == "":
                    cur.execute("UPDATE Service_echange SET contrepartie = %s WHERE service = %s", (None, service_id))
                else:
                    cur.execute("SELECT service_id FROM Service WHERE nom=%s", (nom_service_echange,))
                    id_service_echange = cur.fetchone()
                    if id_service_echange:
                        other_id = id_service_echange[0] if isinstance(id_service_echange, tuple) else id_service_echange
                        cur.execute("UPDATE Service_echange SET contrepartie = %s WHERE service = %s", (other_id, service_id))
                        print("Contrepartie mise à jour.")
                    else:
                        print("Le service de contrepartie n'existe pas. Aucune modification effectuée.")
        conn.commit()
    print("Service proposé avec succés")
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")
   
def declarer_lien():
    print("Lien personel[1] ou lien communautaire[2]?")
    type_lien = input("Votre choix : ").strip()

    if type_lien == "1":
        print("voici la liste des personnes :")
        cur.execute("SELECT id, prenom, nom FROM Personne")
        personnes = cur.fetchall()
        for p in personnes:
            print(f"{p[0]} - {p[1]}) {p[2]}")
        print("Entrez l'ID de la personne avec lequel vous souhaitez créer un lien :")
        id_utilisateur = input_int("ID personne : ", min_val=1)
        
        if id_utilisateur == utilisateur_connecte[0]:
            print("Vous ne pouvez pas créer un lien avec vous-même!")
            return
            
        description_lien = input("Description du lien : ").strip()
        sql = "INSERT INTO Lien_interpersonnel (personne1, personne2, description) VALUES (%s, %s,%s)"
        try:
            cur.execute(sql,(utilisateur_connecte[0], id_utilisateur,description_lien))
            conn.commit()
            print("Lien créé avec succès!")
        except:
            conn.rollback()
            print("Ce lien existe déjà ou une erreur est survenue!")

    elif type_lien == "2":
        print("Depuis quelle communauté voulez vous créer un lien?")
        cur.execute("SELECT nom FROM Communaute WHERE nom IN (SELECT communaute FROM Membre WHERE personne = %s)", (utilisateur_connecte[0],))
        communautes = cur.fetchall()
        for communaute in communautes:
            print(f"{communaute[0]}")
        print("Avec quelle communauté voulez vous créer un lien?")
        id_communauté1 = input("Nom Communaute : ").strip()
        cur.execute("SELECT nom FROM Communaute")
        communautes = cur.fetchall()
        print("Avec quelle autre communauté voulez vous créer un lien?")
        for communaute in communautes:
            print(f"{communaute[0]}")
        id_communauté2 = input("Nom Communaute : ").strip()
        
        if id_communauté1 == id_communauté2:
            print("Vous ne pouvez pas créer un lien entre une communauté et elle-même!")
            return
        
        description_lien = input("Description du lien : ").strip()

        sql = "INSERT INTO Lien_intercommunautaire (communaute1, communaute2, description) VALUES (%s, %s, %s)"
        try:
            cur.execute(sql,(id_communauté1, id_communauté2, description_lien))
            conn.commit()
            print("Lien créé avec succès!")
        except:
            conn.rollback()
            print("Ce lien existe déjà ou une erreur est survenue!")

def rejoindre_communaute():
    print("Voici la liste des communautés :")
    cur.execute("SELECT nom FROM Communaute")
    communautes = cur.fetchall()
    for communaute in communautes:
        print(f"{communaute[0]}) {communaute[0]}")
    print("Entrez le nom de la communauté que vous souhaitez rejoindre :")
    nom_communauté = input("Nom Communauté : ").strip()
    
    sql="SELECT * FROM Membre WHERE personne=%s AND communaute=%s"
    cur.execute(sql,(utilisateur_connecte[0], nom_communauté))
    membre=cur.fetchall()

    if(len(membre)>0):
        print("Vous êtes déjà membre de cette communauté!")
        return
    else:
        sql = "INSERT INTO Membre (personne, communaute) VALUES (%s, %s)"
        cur.execute(sql,(utilisateur_connecte[0], nom_communauté))
        conn.commit()
        print("Vous avez rejoint la communauté avec succès!")
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")
    

def voir_membres_communaute():
    print("Voici la liste des communautés dont vous êtes membre :")
    cur.execute("SELECT communaute FROM Membre WHERE personne = %s", (utilisateur_connecte[0],))
    communautes = cur.fetchall()
    for communaute in communautes:
        print(f"{communaute[0]}")
    print("Entrez le nom de la communauté pour voir ses membres :")
    nom_communauté = input("Nom Communauté : ").strip()
    
    sql = "SELECT p.prenom, p.nom FROM Personne p JOIN Membre m ON p.id = m.personne WHERE m.communaute = %s"
    cur.execute(sql,(nom_communauté,))
    membres = cur.fetchall()
    print(f"Membres de la communauté {nom_communauté} :")
    for membre in membres:
        print(f"{membre[0]} {membre[1]}")
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")

def voir_services_proposes():
    sql = "SELECT p.prenom, p.nom, s.nom, s.service_id FROM Service s JOIN Proposition_service ps ON s.service_id = ps.service JOIN Personne p ON ps.personne = p.id ORDER BY p.nom, s.nom"
    cur.execute(sql)
    services = cur.fetchall()

    print("Services proposés par tous les personnes :")
    for service in services:
        sql="SELECT * FROM Service_commercial WHERE service=%s"
        cur.execute(sql,[service[3]])
        services_commerciaux=cur.fetchall()

        sql="SELECT * FROM Service_gratuit WHERE service=%s"
        cur.execute(sql,[service[3]])
        services_gratuits=cur.fetchall()

        sql="SELECT * FROM Service_echange Where service=%s"
        cur.execute(sql,[service[3]])
        services_echange=cur.fetchall()

        if(len(services_commerciaux)>0):
            print(f"{service[0]} {service[1]} : {service[2]} contre {services_commerciaux[0][1]} euros")
        if(len(services_gratuits)>0):
            print(f"{service[0]} {service[1]} : {service[2]} (service Gratuit)")
        if(len(services_echange)>0):
            #On cherche le nom du service de contrepartie
            sql="SELECT nom FROM Service WHERE service_id=%s"
            cur.execute(sql,[services_echange[0][1]])
            service_contrepartie=cur.fetchone()
            if service_contrepartie==None:
                print(f"{service[0]} {service[1]} : {service[2]} contre aucun service défini")
            else:
                print(f"{service[0]} {service[1]} : {service[2]} contre {service_contrepartie[0]}")
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")

def voir_liens_personnels():
    sql = "SELECT p1.prenom, p1.nom, p2.prenom, p2.nom, li.description FROM Lien_interpersonnel li JOIN Personne p1 ON li.personne1 = p1.id JOIN Personne p2 ON li.personne2 = p2.id ORDER BY p1.nom, p2.nom"
    cur.execute(sql)
    liens = cur.fetchall()
    print("Tous les liens interpersonnels :")
    for lien in liens:
        print(f"{lien[0]} {lien[1]} <-> {lien[2]} {lien[3]} : {lien[4]}")
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")

def voir_liens_communautaires():
    sql = "SELECT li.communaute1, li.communaute2, li.description FROM Lien_intercommunautaire li ORDER BY li.communaute1, li.communaute2"
    cur.execute(sql)
    liens = cur.fetchall()
    print("Tous les liens intercommunautaires :")
    for lien in liens:
        print(f"{lien[0]} <-> {lien[1]} : {lien[2]}")
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")

def envoyer_message():
    type_expediteur=input_int("Envoyer message en tant que personne[1] ou en tant que communauté[2]", min_val=1, max_val=2)
    type_receveur=input_int("Envoyer message à une personne[1] ou à une communauté[2]", min_val=1, max_val=2)
    if(type_expediteur==1):
        #Envoie message Personne-Personne
        if(type_receveur==1):
            print("Envoie message à une personne")
            #On laisse choisir à quel personne envoyer un message
            request="SELECT id, prenom, nom FROM Personne WHERE id != %s"
            cur.execute(request,(utilisateur_connecte[0],))
            personnes=cur.fetchall()
            for personne in personnes:
                print(f"{personne[0]} -  {personne[1]} {personne[2]}")
            personne_receveur=input("Entrez l'id de la personne à laquelle vous voulez envoyer un message: ")

            #On cherche le dernier message
            request="SELECT id FROM Message WHERE expediteur_personne=%s AND receveur_personne=%s ORDER BY id DESC"
            cur.execute(request,[personne_receveur,utilisateur_connecte[0]])
            message_precedent=cur.fetchone()
            message=input("Ecrire votre message: ")

            #On envoie le message
            request="INSERT INTO Message(message,expediteur_personne,receveur_personne,message_precedent) VALUES(%s,%s,%s,%s)"
            cur.execute(request,[message,utilisateur_connecte[0],personne_receveur,message_precedent])
        #Envoie message Personne-Communaute
        elif(type_receveur==2):
            print('Envoie message à une communauté: ')
            #On laisse choisir à quel communauté envoyer un message
            request="SELECT nom FROM Communaute"
            cur.execute(request)
            communautes=cur.fetchall()
            for i in communautes:
                print(i[0])
            communaute_receveur=input("A quelle communauté envoyer un message ?: ")

            #On cherche le dernier message
            request="SELECT id FROM Message WHERE expediteur_commu=%s AND receveur_personne=%s ORDER BY id DESC"
            cur.execute(request,[communaute_receveur,utilisateur_connecte[0]])
            message_precedent=cur.fetchone()
            message=input("Ecrire votre message: ")

            #On envoie le message
            request="INSERT INTO Message(message,expediteur_personne,receveur_commu,message_precedent) VALUES(%s,%s,%s,%s)"
            cur.execute(request,[message,utilisateur_connecte[0],communaute_receveur,message_precedent])


    elif(type_expediteur==2):
        print('Envoie message à une communauté')
        #On laisse choisir sour quel communauté envoyer un message
        request="SELECT communaute FROM Membre m WHERE m.personne=%s"
        cur.execute(request,(utilisateur_connecte[0],))
        communautes=cur.fetchall()
        if(len(communautes)==0):
            print("Vous n'êtes membre d'aucune communauté")
            return
        for i in communautes:
            print(i[0])
        communaute_expediteur=input("Ecrire le nom de la communauté à partir de laquelle vous voulez envoyer un message: ")

        #Envoie message Communaute-Personne
        if(type_receveur==1):
            print("Envoie message à une personne")
            #On laisse choisir à quel personne envoyer un message
            request="SELECT id, prenom, nom FROM Personne WHERE id != %s"
            cur.execute(request,(utilisateur_connecte[0],))
            personnes=cur.fetchall()
            for personne in personnes:
                print(f"{personne[0]} -  {personne[1]} {personne[2]}")
            personne_receveur=input("Entrez l'id de la personne à laquelle vous voulez envoyer un message: ")

            #On cherche le dernier message
            request="SELECT id FROM Message WHERE receveur_commu=%s AND expediteur_personne=%s ORDER BY id DESC"
            cur.execute(request,[communaute_expediteur,personne_receveur])
            message_precedent=cur.fetchone()
            message=input("Ecrire votre message: ")

            #On envoie le message
            request="INSERT INTO Message(message,expediteur_commu,receveur_personne,message_precedent) VALUES(%s,%s,%s,%s)"
            cur.execute(request,[message,communaute_expediteur,personne_receveur,message_precedent])
        #Envoie message Communaute-Communaute
        elif(type_receveur==2):
            #On laisse choisir à quel communauté envoyer un message
            request="SELECT nom FROM Communaute"
            cur.execute(request)
            communautes=cur.fetchall()
            for i in communautes:
                print(i[0])
            communaute_receveur=input("A quelle communauté envoyer un message: ")

            #On cherche le dernier message
            request="SELECT id FROM Message WHERE receveur_commu=%s AND expediteur_commu=%s ORDER BY id DESC"
            cur.execute(request,[communaute_expediteur,communaute_receveur])
            message_precedent=cur.fetchone()
            message=input("Ecrire votre message: ")

            #On envoie le message
            request="INSERT INTO Message(message,expediteur_commu,receveur_commu,message_precedent) VALUES(%s,%s,%s,%s)"
            cur.execute(request,[message,communaute_expediteur,communaute_receveur,message_precedent])
    conn.commit()


#Historique des messages (Vue message) 
def voir_messages():
    type_receveur=input_int("Voir des messages en tant que personne[1] ou en tant que communauté[2]", min_val=1, max_val=2)
    type_expediteur=input_int("Voir les messages envoyes par une personne[1] ou une communaute[2]", min_val=1, max_val=2)
    if type_receveur==1:
        if type_expediteur==1:
            #On laisse choisir les messages envoye par quel personne voir
            request="SELECT id, prenom, nom FROM Personne WHERE id != %s"
            cur.execute(request,(utilisateur_connecte[0],))
            personnes=cur.fetchall()
            for i in personnes:
                print(f"{i[0]} - {i[1]} {i[2]}")
            id_personne_expediteur=input("Entrez le id de la personne que vous voulez voir la conversation: ")

            request="SELECT prenom, nom FROM Personne WHERE id = %s"
            cur.execute(request,(id_personne_expediteur,))
            personne_expediteur=cur.fetchone()


            #On regarde les messages reçu
            request="SELECT id,message FROM Message WHERE expediteur_personne=%s AND receveur_personne=%s ORDER BY id"
            cur.execute(request,[id_personne_expediteur, utilisateur_connecte[0]])
            messages_recu=cur.fetchall()

            #On regarde les messages envoyes
            cur.execute(request,[utilisateur_connecte[0],id_personne_expediteur])
            message_envoye=cur.fetchall()

            #On concatene les 2 listes
            messages_total=messages_recu+message_envoye

            #On trie tout les messages selon les id
            messages_total.sort(key= lambda l:l[0])

            if messages_total==[]:
                print("Aucun message dans cette conversation")
            #On print les messages dans l'ordre d'envoie
            for message in messages_total:
                if(message in messages_recu):
                    print(f"{personne_expediteur[0]} {personne_expediteur[1]} : {message[1]}")
                if message in message_envoye:
                    print(f"{utilisateur_connecte[1]} {utilisateur_connecte[2]} : {message[1]}")

        if type_expediteur==2:
            #On laisse choisir les messages envoye par quel communauté voir
            request="SELECT nom FROM Communaute"
            cur.execute(request)
            communautes=cur.fetchall()
            for i in communautes:
                print(i[0])
            communaute_expediteur=input("Voir les messages envoyés par quelle communaute: ")

            request="SELECT id,message FROM Message WHERE expediteur_commu=%s AND receveur_personne=%s ORDER BY id"
            cur.execute(request,[communaute_expediteur,utilisateur_connecte[0]])
            messages_recu=cur.fetchall()

            request="SELECT id,message FROM Message WHERE expediteur_personne=%s AND receveur_commu=%s ORDER BY id"
            cur.execute(request,[utilisateur_connecte[0],communaute_expediteur])
            message_envoye=cur.fetchall()

            #On concatene les 2 listes
            messages_total=messages_recu+message_envoye

            #On trie tout les messages selon les id
            messages_total.sort(key= lambda l:l[0])

            if messages_total==[]:
                print("Aucun message dans cette conversation")
            #On print les messages dans l'ordre d'envoie
            for message in messages_total:
                if(message in messages_recu):
                    print(f"{communaute_expediteur} : {message[1]}")
                if message in message_envoye:
                    print(f"{utilisateur_connecte[1]} {utilisateur_connecte[2]} : {message[1]}")
            
    elif type_receveur==2:
        print("Voir message commu")
        #On laisse choisir voir les message de quel communaute
        request="SELECT communaute FROM Membre m WHERE m.personne=%s"
        cur.execute(request,(utilisateur_connecte[0],))
        communautes=cur.fetchall()
        for i in communautes:
            print(i[0])
        communaute_receveur=input("Voir les messages de quels communauté?: ")
        if type_expediteur==1:
            #On laisse choisir les messages envoye par quel personne voir
            request="SELECT id, prenom, nom FROM Personne"
            cur.execute(request)
            personnes=cur.fetchall()
            for i in personnes:
                print(f"{i[0]} - {i[1]} {i[2]}")
            id_personne_expediteur=input("Entrez le id de la personne que vous voulez voir la conversation: ")

            request="SELECT prenom, nom FROM Personne WHERE id = %s"
            cur.execute(request,(id_personne_expediteur,))
            personne_expediteur=cur.fetchone()


            request="SELECT id,message FROM Message WHERE expediteur_personne=%s AND receveur_commu=%s ORDER BY id"
            cur.execute(request,[id_personne_expediteur,communaute_receveur])
            messages_recu=cur.fetchall()

            request="SELECT id,message FROM Message WHERE expediteur_commu=%s AND receveur_personne=%s ORDER BY id"
            cur.execute(request,[communaute_receveur,id_personne_expediteur])
            message_envoye=cur.fetchall()

            #On concatene les 2 listes
            messages_total=messages_recu+message_envoye

            #On trie tout les messages selon les id
            messages_total.sort(key= lambda l:l[0])

            #On print les messages dans l'ordre d'envoie
            if messages_total==[]:
                print("Aucun message dans cette conversation")
            for message in messages_total:
                if(message in messages_recu):
                    print(f"{personne_expediteur[0]} {personne_expediteur[1]} : {message[1]}")
                if message in message_envoye:
                    print(f"{communaute_receveur} : {message[1]}")
        if type_expediteur==2:
            #On laisse choisir les messages envoye par quel communauté voir
            request="SELECT nom FROM Communaute"
            cur.execute(request)
            communautes=cur.fetchall()
            for i in communautes:
                print(i[0])
            communaute_expediteur=input("Voir les messages envoyés par quelle communaute: ")

            request="SELECT id,message FROM Message WHERE expediteur_commu=%s AND receveur_commu=%s ORDER BY id"
            cur.execute(request,[communaute_expediteur,communaute_receveur])
            messages_recu=cur.fetchall()

            cur.execute(request,[communaute_receveur,communaute_expediteur])
            message_envoye=cur.fetchall()

            #On concatene les 2 listes
            messages_total=messages_recu+message_envoye

            #On trie tout les messages selon les id
            messages_total.sort(key= lambda l:l[0])
            if messages_total==[]:
                print("Aucun message dans cette conversation")
            #On print les messages dans l'ordre d'envoie
            for message in messages_total:
                if(message in messages_recu):
                    print(f"{communaute_expediteur} : {message[1]}")
                if message in message_envoye:
                    print(f"{communaute_receveur} : {message[1]}")
    conn.commit()
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")
    

def voir_savoirs():
    print("Voir les savoirs-faire")
    request="SELECT sf.intitule, p.prenom, p.nom, mp.rang FROM Savoir_faire sf JOIN Maitrise_personnelle mp ON sf.intitule=mp.savoir JOIN Personne p ON p.id=mp.personne"
    cur.execute(request)
    savoir_faire_personnelle=cur.fetchall()
    request="SELECT sf.intitule, c.nom, mc.rang FROM Savoir_faire sf JOIN Maitrise_communautaire mc ON sf.intitule=mc.savoir_faire JOIN Communaute c ON c.nom=mc.communaute"
    cur.execute(request)
    savoir_faire_communautaire=cur.fetchall()

    print("Savoir des personnes")
    for sf_perso in savoir_faire_personnelle:
        print(f"Savoir {sf_perso[0]} | Personne maitrisant ce savoir: {sf_perso[1]} {sf_perso[2]} | Niveau de maitrise: {sf_perso[3]}")
    print("Savoir des communautés")
    for sf_commu in savoir_faire_communautaire:
        print(f"Savoir {sf_commu[0]} | Personne maitrisant ce savoir: {sf_commu[1]} | Niveau de maitrise: {sf_commu[2]}")
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")

def creer_compteG1():
    print("Création compte G1")
    type_compte=str(input("Entrez le type de compte (personne/communauté): ").strip())
    solde=input_int("Entrez le solde du compte G1: ")
    cle=random.randint(100000,999999)
    if type_compte=="personne":
        request = "INSERT INTO Compte_G1 (proprietaire_personne) VALUES (%s) RETURNING id"
        cur.execute(request, (utilisateur_connecte[0],))
        id_compte = cur.fetchone()[0]

        #Création clé publique
        request="INSERT INTO Cle_publique(cle,solde,compte) VALUES(%s,%s,%s)"
        cur.execute(request,(cle,solde,id_compte))


    elif type_compte=="communaute":
        print("Voici la liste des communautés dont vous êtes membre :")
        cur.execute("SELECT communaute FROM Membre WHERE personne = %s", (utilisateur_connecte[0],))
        communautes_membre = cur.fetchall()
        if not communautes_membre:
            print("Vous n'êtes membre d'aucune communauté!")
            return
            
        for c in communautes_membre:
            print(f"- {c[0]}")
        print("Entrez le nom de la communauté pour laquelle vous souhaitez créer un compte G1 :")
        nom_communaute = input("Nom communauté : ").strip()
        
        # Vérifier que l'utilisateur est bien membre de cette communauté
        cur.execute("SELECT * FROM Membre WHERE personne = %s AND communaute = %s", (utilisateur_connecte[0], nom_communaute))
        if not cur.fetchone():
            print("Vous n'êtes pas membre de cette communauté!")
            return

        request="INSERT INTO Compte_G1(proprietaire_commu) VALUES(%s)"
        cur.execute(request,(nom_communaute,))
        id_compte=cur.lastrowid
        
        #Création clé publique
        request="INSERT INTO Cle_publique(personne,cle,compte) VALUES(%s,%s,%s)"
        cur.execute(request,(solde,cle,id_compte))
    
    print(f"Compte G1 créé avec succès! Votre clé publique est : {cle}")
    conn.commit()

def voir_solde_compteG1():
    print("Voir solde compte G1")
    request="SELECT id, proprietaire_personne, proprietaire_commu FROM Compte_G1 WHERE proprietaire_personne=%s OR proprietaire_commu IN (SELECT communaute FROM Membre WHERE personne=%s)"
    cur.execute(request,(utilisateur_connecte[0],utilisateur_connecte[0]))
    comptes=cur.fetchall()
    if len(comptes)==0:
        print("Vous n'avez pas de compte G1")
        return
    for compte in comptes:
        proprietaire_personne=None
        proprietaire_commu=None
        if(compte[1]!=None):
            request="SELECT prenom, nom FROM Personne WHERE id=%s"
            cur.execute(request,(compte[1],))
            proprietaire_personne=cur.fetchone()
            print(f"Compte ID: {compte[0]} | Proprietaire Personne: {proprietaire_personne[0]} {proprietaire_personne[1]} | Proprietaire Communauté: {None}")
        if(compte[2]!=None):
            request="SELECT nom FROM Communaute WHERE nom=%s"
            cur.execute(request,(compte[2],))
            proprietaire_commu=cur.fetchone()
            print(f"Compte ID: {compte[0]} | Proprietaire Personne: {None} | Proprietaire Communauté: {proprietaire_commu[0]}")

        request="SELECT cle, solde FROM Cle_publique WHERE compte=%s"
        cur.execute(request,(compte[0],))
        cles=cur.fetchall()
        for cle in cles:
            print(f"  Clé: {cle[0]} | Solde: {cle[1]}")
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")


#Exclusion d'un membre par vote 
def voter_contre_un_membre():
    print("Voici les communautés dans lesquelles vous êtes membre :")

    cur.execute("SELECT communaute FROM Membre WHERE personne = %s", (utilisateur_connecte[0],))
    communautes = cur.fetchall()

    for c in communautes:
        print(c[0])

    communaute = input("Voter dans quelle communauté ? ").strip()

    cur.execute("SELECT m.id, p.prenom, p.nom FROM Membre m JOIN Personne p ON m.personne = p.id WHERE m.communaute = %s", (communaute,))
    personnes = cur.fetchall()

    for p in personnes:
        print(f"{p[0]} - {p[1]} {p[2]}")

    personne_contre_qui_voter = input_int("ID du membre contre lequel vous votez : ", min_val=1)

    # id du membre votant
    cur.execute("SELECT id FROM Membre WHERE personne = %s AND communaute = %s", (utilisateur_connecte[0], communaute))
    id_membre_votant = cur.fetchone()[0]

    cur.execute("UPDATE Membre SET vote_contre = %s WHERE id = %s", (personne_contre_qui_voter, id_membre_votant))

    # nombre total de membres
    cur.execute("SELECT COUNT(*) FROM Membre WHERE communaute = %s", (communaute,))
    nombre_de_personne_commu = cur.fetchone()[0]

    # nombre de votes contre cette personne
    cur.execute("SELECT COUNT(*) FROM Membre WHERE communaute = %s AND vote_contre = %s", (communaute, personne_contre_qui_voter))
    votes = cur.fetchone()[0]

    seuil = nombre_de_personne_commu // 2 + 1

    if votes >= seuil:
        cur.execute("UPDATE Membre SET vote_contre = NULL WHERE vote_contre = %s", (personne_contre_qui_voter,))
        cur.execute("DELETE FROM Membre WHERE id = %s", (personne_contre_qui_voter,))
        conn.commit()
        print(f"Membre expulsé de {communaute} ({votes}/{nombre_de_personne_commu})")
    else:
        conn.commit()
        print(f"Vote enregistré ({votes}/{seuil})")
        


#Conversion degrés en radians (utilisé pour la distance)
def convertRad(input):
        return (np.pi * input)/180

#Calcul distance entre deux points géographiques
def distance(lat_a_degre, lon_a_degre, lat_b_degre, lon_b_degre):
    #Rayon de la terre en mètre
    R = 6378000 
 
    lat_a = convertRad(lat_a_degre)
    lon_a = convertRad(lon_a_degre)
    lat_b = convertRad(lat_b_degre)
    lon_b = convertRad(lon_b_degre)
     
    d = R * (np.pi/2 - math.asin( math.sin(lat_b) * math.sin(lat_a) + math.cos(lon_b - lon_a) * math.cos(lat_b) * math.cos(lat_a)))
    d=d/1000 # conversion en km
    return d

#Vue Proches
def vue_proches():
    requete="SELECT prenom,nom,longitude, latitude FROM Personne p JOIN Localisation l ON p.loca=l.num  WHERE id != %s"
    cur.execute(requete,( utilisateur_connecte[0],))
    personnes=cur.fetchall()
    requete="SELECT c.nom,longitude, latitude FROM Communaute c JOIN Localisation l ON c.loca=l.num"
    cur.execute(requete)
    communautes=cur.fetchall()

    requete="SELECT longitude, latitude FROM Localisation l JOIN Personne p ON l.num=p.loca WHERE p.id=%s"
    cur.execute(requete,( utilisateur_connecte[0],))
    loca_utilisateur=cur.fetchone()
    for personne in personnes:
        dist=distance(loca_utilisateur[1],loca_utilisateur[0],personne[3],personne[2])
        if dist<=1:
            print(f"La personne {personne[0]} {personne[1]} est à moins de 1 km de vous")
    for communaute in communautes:
        dist=distance(loca_utilisateur[1],loca_utilisateur[0],communaute[2],communaute[1])
        if dist<=1:
            print(f"La communauté {communaute[0]} est à moins de 1 km de vous")
    quit=None
    while quit==None:
        quit=input("Appuyez sur entrer pour quitter ")
        
    


utilisateur_connecte=None
def start_application():
    # Début de l'interface utilisateur
    print("Bienvenue dans la base de donnée dans l'application de gestion de communauté")
    print("Connectez vous ou inscrivez vous sur la base")
    print("1- Connectez-vous")
    print("2- Inscrivez-vous")  
    print("3- Quitter")  

    try:
        choix=input_int("Faites votre choix: ")
    except ValueError:
        print("Choix invalide, veuillez entrer un nombre")
        return start_application()

    if choix==1:
        connexion()

    if choix==2:
        inscription()

    if(choix==3):
        print("Fermeture application")
        exit()

start_application()


if utilisateur_connecte!=None:
    print(f"Vous êtes bien connecté en tant que {utilisateur_connecte[1]} {utilisateur_connecte[2]}")


    while(True):
        print("Choisissez les actions que vous pouvez effectuez")
        print("1- Voir toutes les personnes dans l'application")
        print("2- Créer une communauté")
        print("3- Voir la liste des communauté dans l'application (Vue communauté)")
        print("4- Ajouter savoir_faire")
        print("5- Proposer un service")
        print("6- Déclarer un lien")
        print("7- Rejoindre une communauté")
        print("8- Voir les membres d'une communauté")
        print("9- Voir les services proposés par tous les personnes")
        print("10- Voir vos liens interpersonnels")
        print("11- Voir vos liens intercommunautaires")
        print("12- Envoyer un message")
        print("13- Voir vos messages (Vue message) (Historique des messages)")
        print("14- Voter contre un membre")
        print("15- Voir les personnes et communautés proches de vous (moins de 1 km) (Vue proches)")
        print("16- Créer un compte G1")
        print("17- Voir le solde de votre(s) compte(s) G1")
        print("18- Voir les savoirs-faire")
        print("19- Se déconnecter")

        choix=input_int("Faites votre choix ")
        if choix==1:
            voir_liste_personne()
        elif choix==2:
            creer_communaute()
        elif choix==3:
            voir_liste_communaute()
        elif choix==4:
            ajouter_savoir_faire()
        elif choix==5:
            proposer_service()
        elif choix==6:
            declarer_lien()
        elif choix==7:
            rejoindre_communaute()
        elif choix==8:
            voir_membres_communaute()
        elif choix==9:
            voir_services_proposes()
        elif choix==10:
            voir_liens_personnels()
        elif choix==11:
            voir_liens_communautaires()
        elif choix==12:
            envoyer_message()
        elif choix==13:
            voir_messages()
        elif choix==14:
            voter_contre_un_membre()
        elif choix==15:
            vue_proches()
        elif choix==16:
            creer_compteG1()
        elif choix==17:
            voir_solde_compteG1()
        elif choix==18:
            voir_savoirs()
        elif choix==19:
            utilisateur_connecte=None
            start_application()








