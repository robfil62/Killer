from os import remove
import random, sqlite3
from datetime import datetime

VAL_CONTRAT_REALISE = 1
VAL_CONTRAT_EN_COURS = 0
VAL_CONTRAT_ECHOUE = -1
VAL_PARTIE_INIT = 0
VAL_PARTIE_EN_COURS = 1
VAL_PARTIE_FINIE = 2

def getNomJoueurFromId(id):
    commande = "SELECT nom FROM joueurs WHERE id = "+str(id)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    joueur=rows
    return joueur[0][0]


def getNomArmeFromId(id):
    commande = "SELECT nom FROM armes WHERE id = "+str(id)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    arme=rows
    return arme[0][0]

def getNomLieuFromId(id):
    commande = "SELECT nom FROM lieux WHERE id = "+str(id)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    lieu=rows
    return lieu[0][0]

def getIdJoueurFromNom(nom):
    commande = "SELECT id FROM joueurs WHERE nom = '"+nom+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    id=rows
    return id[0][0]

def getNmbMaxJoueursFromIdPartie(id_partie):
    commande = "SELECT nmbJoueurs FROM parties WHERE id = "+str(id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    nmb=rows
    return nmb[0][0]

def getNmbJoueursInPartieFromIdPartie(id_partie):
    commande = "SELECT COUNT(*) FROM contrats WHERE id_partie = ? AND realise = ?"
    val = (id_partie, VAL_CONTRAT_EN_COURS)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    rows = cur.fetchall()
    conn.close

    nmb=rows
    return nmb[0][0]

def getIdContratFromIdAssassin(id_partie, id_assassin):
    commande = "SELECT id_contrat FROM contrats WHERE id_partie = ? AND id_assassin = ? AND realise = ?"
    val = (id_partie, id_assassin, VAL_CONTRAT_EN_COURS)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande, val)
    rows = cur.fetchall()
    conn.close

    if len(rows)==0:
        return -1

    id_contrat = rows[0][0]
    return id_contrat

def getIdCibleFromIdContrat(id_contrat):
    commande = "SELECT id_cible FROM contrats WHERE id_contrat = "+str(id_contrat)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close
    id_cible = rows[0][0]

    return id_cible

def getIdArmeFromIdContrat(id_contrat):
    commande = "SELECT id_arme FROM contrats WHERE id_contrat = "+str(id_contrat)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close
    id_arme = rows[0][0]

    return id_arme

def getIdLieuFromIdContrat(id_contrat):
    commande = "SELECT id_lieu FROM contrats WHERE id_contrat = "+str(id_contrat)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close
    id_lieu = rows[0][0]

    return id_lieu

def addContrat(id_partie, id_assassin, id_cible, id_arme, id_lieu):
    commande = "INSERT INTO contrats (id_partie, id_assassin, id_cible, id_arme, id_lieu) VALUES (?,?,?,?,?)"
    val = (id_partie, id_assassin, id_cible, id_arme, id_lieu)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

def setUpdateEtatContrat(etat, id_contrat):
    commande = "UPDATE contrats SET realise = ?, date_realisation = ? WHERE id_contrat = ?"
    val = (etat, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), id_contrat)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

def setContratRempli(id_partie, id_assassin):
    id_contrat_realise = getIdContratFromIdAssassin(id_partie, id_assassin)
    if id_contrat_realise != -1:
        id_cible = getIdCibleFromIdContrat(id_contrat_realise)
        id_contrat_cible = getIdContratFromIdAssassin(id_partie, id_cible)
        id_cible_cible = getIdCibleFromIdContrat(id_contrat_cible)

        if (id_cible_cible == id_assassin):
            setUpdateEtatContrat(VAL_CONTRAT_REALISE, id_contrat_realise)
            setUpdateEtatContrat(VAL_CONTRAT_ECHOUE, id_contrat_cible)
            print("FIN DE PARTIE")
            print('Gagnant : '+getNomJoueurFromId(id_assassin)) 
            finPartie(id_partie)

        else:
            id_arme_cible = getIdArmeFromIdContrat(id_contrat_cible)
            id_lieu_cible = getIdLieuFromIdContrat(id_contrat_cible)
            setUpdateEtatContrat(VAL_CONTRAT_REALISE, id_contrat_realise)
            setUpdateEtatContrat(VAL_CONTRAT_ECHOUE, id_contrat_cible)
            addContrat(id_partie, id_assassin, id_cible_cible, id_arme_cible, id_lieu_cible)
            print(printContrat(getIdContratFromIdAssassin(id_partie,id_assassin)))

def printContrat(id_contrat):
    if (id_contrat != -1) :
        id_cible = getIdCibleFromIdContrat(id_contrat)
        id_arme = getIdArmeFromIdContrat(id_contrat)
        id_lieu = getIdLieuFromIdContrat(id_contrat)
        nom_cible = getNomJoueurFromId(id_cible)
        nom_arme = getNomArmeFromId(id_arme)
        nom_lieu = getNomLieuFromId(id_lieu)
        print('Contrat : '+nom_cible+', '+nom_arme+', '+nom_lieu)

    else:
        print('Pas de contrat associe')

def finPartie(id_partie):
    commande = "UPDATE parties SET etat = ? WHERE id = ?"
    val = (VAL_PARTIE_FINIE, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

def addPartie(nom, nmb):
    commande = "INSERT INTO parties (nom, nmbJoueurs) VALUES (?,?)"
    val = (nom, nmb)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

def triIds(ids):
    nmbJoueurs = len(ids)
    idsTries = []
    for i in range(nmbJoueurs):
        place=random.randint(0,nmbJoueurs-i-1)
        idsTries.append(ids[place])
        ids.remove(ids[place])

    return idsTries

def joinPartie(nom_joueur, nom_partie):
    commande = "SELECT id FROM joueurs WHERE nom = ?"
    val = (nom_joueur,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    joueur = cur.fetchall()
    conn.close

    if(len(joueur)!=1):
        return "joueur inconnu"

    commande = "SELECT id FROM parties WHERE nom = ?"
    val = (nom_partie,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    partie = cur.fetchall()
    conn.close

    if(len(partie)!=1):
        return "partie inconnue"

    id_partie = partie[0][0]
    id_joueur = joueur[0][0]

    commande = "SELECT id_assassin FROM contrats WHERE id_assassin = ? AND id_partie = ?"
    val = (id_joueur, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    id = cur.fetchall()
    conn.close

    if(len(id)!=0):
        return "joueur deja dans la partie"

    commande = "INSERT INTO contrats (id_partie, id_assassin) VALUES (?,?)"
    val = (id_partie, id_joueur)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'joueur ajoute a la partie'


def getAllIdJoueursFromIdPartie(id_partie):
    commande = "SELECT id_assassin FROM contrats WHERE id_partie = ? AND realise = ?"
    val = (id_partie, VAL_CONTRAT_EN_COURS)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    rows = cur.fetchall()
    conn.close

    liste_id=rows
    return liste_id

def printAllContrats(id_partie):
    liste_id_joueurs = getAllIdJoueursFromIdPartie(id_partie)
    nmb_joueurs=len(liste_id_joueurs)
    for i in range(0,nmb_joueurs):
        printContrat(getIdContratFromIdAssassin(id_partie, liste_id_joueurs[i][0]))

def addJoueur(nom_joueur):
    commande = "SELECT id FROM joueurs WHERE nom = ?"
    val = (nom_joueur,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    joueur = cur.fetchall()
    conn.close

    if(len(joueur)!=0):
        return "Le joueur existe deja"


    commande = "INSERT INTO joueurs (nom) VALUES (?)"
    val = (nom_joueur,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'Joueur cree'

def startPartie(id_partie):
    #Check si la partie n'est pas deja commencee
    commande = "SELECT etat FROM parties WHERE id = ?"
    val = (id_partie,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    etat = cur.fetchall()
    conn.close

    if(etat[0][0]!= VAL_PARTIE_INIT):
        return "La partie est deja en cours"
    
    #Check si tous les joueurs sont la
    nmb_joueur = getNmbJoueursInPartieFromIdPartie(id_partie)
    max_joueur = getNmbMaxJoueursFromIdPartie(id_partie)
    if(nmb_joueur!=max_joueur):
        return "Tous les joueurs ne sont pas prets"

    #Preparation des joueurs
    commande = "SELECT id_assassin FROM contrats WHERE id_partie = ?"
    val = (id_partie,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    ids_joueurs = cur.fetchall()
    conn.close

    liste_joueurs=[]
    for i in range(len(ids_joueurs)):
        liste_joueurs.append(ids_joueurs[i][0])

    for i in range(30):
        liste_joueurs=triIds(liste_joueurs)

    print(liste_joueurs)
    #Preparation des armes
    commande = "SELECT id FROM armes"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    ids_armes = cur.fetchall()
    conn.close

    liste_armes=[]
    for i in range(len(ids_armes)):
        liste_armes.append(ids_armes[i][0])

    for i in range(30):
        liste_armes=triIds(liste_armes)

    if (max_joueur < len(liste_armes)):
        for i in range(0, len(liste_armes) - max_joueur):
            liste_armes.pop()
    
    print(liste_armes)
    #Preparation des lieux
    commande = "SELECT id FROM lieux"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    ids_lieux = cur.fetchall()
    conn.close

    liste_lieux=[]
    for i in range(len(ids_lieux)):
        liste_lieux.append(ids_lieux[i][0])

    for i in range(30):
        liste_lieux=triIds(liste_lieux)

    if (max_joueur < len(liste_lieux)):
        for i in range(0, len(liste_lieux) - max_joueur):
            liste_lieux.pop()
 
    print(liste_lieux)

    #Attribution des contrats
    for i in range(0, max_joueur-1):
        removeContratNul(id_partie,liste_joueurs[i])
        addContrat(id_partie,liste_joueurs[i],liste_joueurs[i+1],liste_armes[i],liste_lieux[i])

    removeContratNul(id_partie, liste_joueurs[max_joueur-1])
    addContrat(id_partie, liste_joueurs[max_joueur-1],liste_joueurs[0],liste_armes[max_joueur-1],liste_lieux[max_joueur-1])

    printAllContrats(id_partie)

    #Changement de l'etat de la partie
    commande = "UPDATE parties SET etat = ? WHERE id = ?"
    val = (VAL_PARTIE_EN_COURS, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close
    
def removeContratNul(id_partie, id_assassin):
    commande = "DELETE FROM contrats WHERE id_partie = ? AND id_assassin = ? AND id_cible IS NULL"
    val = (id_partie, id_assassin)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

def addPartie(nom_partie, nmb_joueur):
    commande = "SELECT id FROM parties WHERE nom = ?"
    val = (nom_partie,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    partie = cur.fetchall()
    conn.close

    if(len(partie)!=0):
        return "Une partie porte deja le meme nom"


    commande = "INSERT INTO parties (nom,nmbJoueurs) VALUES (?,?)"
    val = (nom_partie,nmb_joueur)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'Partie creee'

#----------------Creation des joueurs----------------------
#IHM : nom_joueur
#addJoueur(nom_joueur)

#------------------Creation de la partie-------------------
#IHM : nom_partie, nmb_joueurs
#addPartie(nom_partie,nmb_joueurs)

#--------------------Join partie-------------------------
#IHM : nom_joueur, nom_partie
#print(joinPartie('Robin','TEST'))

#--------------------Start partie-----------------------
#IHM : bouton start, nom_partie
#print(startPartie(2))