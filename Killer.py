import random, sqlite3
from datetime import datetime

VAL_CONTRAT_REALISE = 1
VAL_CONTRAT_EN_COURS = 0
VAL_CONTRAT_ECHOUE = -1

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
            #finPartie(id_partie)

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


def addPartie(nom, nmb):
    commande = "INSERT INTO parties (nom, nmbJoueurs) VALUES (?,?)"
    val = (nom, nmb)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

def triJoueurs(joueurs):
    nmbJoueurs = len(joueurs)
    joueursTries = []
    for i in range(nmbJoueurs):
        place=random.randint(0,nmbJoueurs-i-1)
        joueursTries.append(joueurs[place])
        joueurs.remove(joueurs[place])

    return joueursTries

def newPartie(nom, nmb):
    addPartie(nom, nmb)

def joinPartie(id_joueur,id_partie):
    commande = "INSERT INTO contrats (id_partie, id_assassin) VALUES (?,?)"
    val = (id_joueur, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close


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
    print(nmb_joueurs)
    for i in range(0,nmb_joueurs-1):
        printContrat(getIdContratFromIdAssassin(id_partie, liste_id_joueurs[i][0]))

printAllContrats(1)
