from os import remove
import random, sqlite3
from datetime import datetime
from flask import Flask

VAL_CONTRAT_REALISE = 1
VAL_CONTRAT_EN_COURS = 0
VAL_CONTRAT_ECHOUE = -1
VAL_PARTIE_INIT = 0
VAL_PARTIE_EN_COURS = 1
VAL_PARTIE_FINIE = 2


app = Flask(__name__)

@app.route("/home")
def hello_world():
    return "ICI Rappel des liens utiles USERS ONLY"


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
    if(len(id)==0):
        return -1

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

def getNmbArmesInPartieFromIdPartie(id_partie):
    commande = "SELECT listeIdArmes FROM parties WHERE id = ?"
    val = (id_partie,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    rows = cur.fetchall()
    conn.close

    if(rows[0][0] is None):
        return 0

    else:
        ids_armes=str(rows[0][0])
        liste_id=ids_armes.split(",")
        return len(liste_id)

def getNmbLieuxInPartieFromIdPartie(id_partie):
    commande = "SELECT listeIdLieux FROM parties WHERE id = ?"
    val = (id_partie,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    rows = cur.fetchall()
    conn.close

    if(rows[0][0] is None):
        return 0

    else:
        ids_lieux=str(rows[0][0])
        liste_id=ids_lieux.split(",")
        return len(liste_id)
   

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

    if len(rows)==0:
        return -1

    id_cible = rows[0][0]
    return id_cible

def getIdArmeFromIdContrat(id_contrat):
    commande = "SELECT id_arme FROM contrats WHERE id_contrat = "+str(id_contrat)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close
    
    if len(rows)==0:
        return -1
    
    id_arme = rows[0][0]
    return id_arme

def getIdLieuFromIdContrat(id_contrat):
    commande = "SELECT id_lieu FROM contrats WHERE id_contrat = "+str(id_contrat)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close
    
    if len(rows)==0:
        return -1

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

def setUpdateEtatPartie(etat, id_partie):
    commande = "UPDATE parties SET etat = ? WHERE id = ?"
    val = (etat, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

def getMdpFromIdJoueur(id_joueur):
    commande = "SELECT mdp FROM joueurs WHERE id = '"+str(id_joueur)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close
    mdp = rows[0][0]

    return mdp

@app.route('/contratDone/<nom_partie>/<nom_assassin>/<mdp>/<mdp_victime>')
def setContratRempli(nom_assassin, nom_partie, mdp, mdp_victime):
    id_partie=getIdPartieFromNomPartie(nom_partie)
    id_assassin = getIdJoueurFromNom(nom_assassin)
    
    id_contrat_realise = getIdContratFromIdAssassin(id_partie, id_assassin)
    if id_contrat_realise != -1:
        if (str(getMdpFromIdJoueur(id_assassin))!=str(mdp)):
            return "Mot de passe de l'assassin incorrect"

        id_cible = getIdCibleFromIdContrat(id_contrat_realise)
        if (str(getMdpFromIdJoueur(id_cible))!=str(mdp_victime)):
            return "Mot de passe de la victime incorrect"

        id_contrat_cible = getIdContratFromIdAssassin(id_partie, id_cible)
        id_cible_cible = getIdCibleFromIdContrat(id_contrat_cible)

        if (id_cible_cible == id_assassin):
            setUpdateEtatContrat(VAL_CONTRAT_REALISE, id_contrat_realise)
            setUpdateEtatContrat(VAL_CONTRAT_ECHOUE, id_contrat_cible)
            setUpdateEtatPartie(VAL_PARTIE_FINIE, id_partie)
            return('FIN DE PARTIE ------------------ Gagnant : '+ nom_assassin) 

        else:
            id_arme_cible = getIdArmeFromIdContrat(id_contrat_cible)
            id_lieu_cible = getIdLieuFromIdContrat(id_contrat_cible)
            setUpdateEtatContrat(VAL_CONTRAT_REALISE, id_contrat_realise)
            setUpdateEtatContrat(VAL_CONTRAT_ECHOUE, id_contrat_cible)
            addContrat(id_partie, id_assassin, id_cible_cible, id_arme_cible, id_lieu_cible)
            return(nom_assassin + ", votre nouveau contrat : "+getContrat(getIdContratFromIdAssassin(id_partie,id_assassin)))

def getContrat(id_contrat):
    if (id_contrat != -1) :
        id_cible = getIdCibleFromIdContrat(id_contrat)
        id_arme = getIdArmeFromIdContrat(id_contrat)
        id_lieu = getIdLieuFromIdContrat(id_contrat)
        nom_cible = getNomJoueurFromId(id_cible)
        nom_arme = getNomArmeFromId(id_arme)
        nom_lieu = getNomLieuFromId(id_lieu)
        return (nom_cible+', '+nom_arme+', '+nom_lieu)

    else:
        return('Pas de contrat associe')

def finPartie(id_partie):
    commande = "UPDATE parties SET etat = ? WHERE id = ?"
    val = (VAL_PARTIE_FINIE, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

@app.route('/newParty/<nom>/<nmb>')
def addPartie(nom, nmb):
    commande = "SELECT nom FROM parties WHERE nom = ?"
    val = (nom,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    partie = cur.fetchall()
    conn.close

    if(len(partie)!=0):
        return "Le partie existe deja"

    commande = "INSERT INTO parties (nom, nmbJoueurs) VALUES (?,?)"
    val = (nom, nmb)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return "Partie creee"

def removeContratNul(id_partie, id_assassin):
    commande = "DELETE FROM contrats WHERE id_partie = ? AND id_assassin = ? AND id_cible IS NULL"
    val = (id_partie, id_assassin)
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

@app.route('/join/<nom_partie>/<nom_joueur>/<mdp>')
def joinPartie(nom_joueur, nom_partie, mdp):
    commande = "SELECT id,mdp FROM joueurs WHERE nom = ?"
    val = (nom_joueur,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    joueur = cur.fetchall()
    conn.close

    if(len(joueur)!=1):
        return "Joueur inconnu"

    if(str(joueur[0][1])!=str(mdp)):
        return "Mot de passe incorrect"

    commande = "SELECT id FROM parties WHERE nom = ?"
    val = (nom_partie,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    partie = cur.fetchall()
    conn.close

    if(len(partie)!=1):
        return "Partie inconnue"

    id_partie = partie[0][0]
    id_joueur = joueur[0][0]

    nmb_max = getNmbMaxJoueursFromIdPartie(id_partie)
    nmb_joueurs = getNmbJoueursInPartieFromIdPartie(id_partie)

    if(nmb_max == nmb_joueurs):
        return "Le nombre maximal de joueurs a ete atteint"

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
        print(getContrat(getIdContratFromIdAssassin(id_partie, liste_id_joueurs[i][0])))

@app.route('/myContrat/<nom_partie>/<nom_joueur>/<mdp>')
def printContratFromJoueur(nom_joueur,nom_partie,mdp):
    id_partie = getIdPartieFromNomPartie(nom_partie)
    id_joueur = getIdJoueurFromNom(nom_joueur)
    if(str(getMdpFromIdJoueur(id_joueur))!=str(mdp)):
        return "Mot de passe incorrect"

    return nom_joueur + ", votre contrat : " + getContrat(getIdContratFromIdAssassin(id_partie,id_joueur))

@app.route('/newWeapon/<nom_arme>/<descr>')
def addArme(nom_arme, descr):
    commande = "SELECT id FROM armes WHERE nom = ?"
    val = (nom_arme,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    arme = cur.fetchall()
    conn.close

    if(len(arme)!=0):
        return "L'arme existe deja"


    commande = "INSERT INTO armes (nom, description) VALUES (?, ?)"
    val = (nom_arme,descr)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'Arme creee'

@app.route('/newPlace/<nom_lieu>/<descr>')
def addLieu(nom_lieu, descr):
    commande = "SELECT id FROM lieux WHERE nom = ?"
    val = (nom_lieu,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    lieu = cur.fetchall()
    conn.close

    if(len(lieu)!=0):
        return "Le lieu existe deja"


    commande = "INSERT INTO lieux (nom, description) VALUES (?, ?)"
    val = (nom_lieu,descr)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'Lieu cree'


@app.route('/newPlayer/<nom_joueur>/<mdp>')
def addJoueur(nom_joueur, mdp):
    commande = "SELECT id FROM joueurs WHERE nom = ?"
    val = (nom_joueur,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    joueur = cur.fetchall()
    conn.close

    if(len(joueur)!=0):
        return "Le joueur existe deja"


    commande = "INSERT INTO joueurs (nom, mdp) VALUES (?, ?)"
    val = (nom_joueur,mdp)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'Joueur cree'

def getIdPartieFromNomPartie(nom_partie):
    commande = "SELECT id FROM parties WHERE nom = '"+nom_partie+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    if len(rows)==0:
        return -1

    id=rows
    return id[0][0]

def getIdArmeFromNomArme(nom_arme):
    commande = "SELECT id FROM armes WHERE nom = '"+nom_arme+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    if len(rows)==0:
        return -1

    id=rows
    return id[0][0]

def getIdLieuFromNomArme(nom_lieu):
    commande = "SELECT id FROM lieux WHERE nom = '"+nom_lieu+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    if len(rows)==0:
        return -1

    id=rows
    return id[0][0]


@app.route('/addWeapon/<nom_arme>/<nom_partie>')
def addWeapon(nom_arme,nom_partie):
    id_arme = getIdArmeFromNomArme(nom_arme)
    if (id_arme==-1):
        return "Arme inconnue"

    id_partie = getIdPartieFromNomPartie(nom_partie)
    if (id_partie == -1):
        return "Partie inconnue"

    commande = "SELECT listeIdArmes FROM parties WHERE id = '"+str(id_partie)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    if(rows[0][0] is None):
        ids_armes=str(id_arme)

    else:
        ids_armes=str(rows[0][0])
        liste_id=ids_armes.split(",")
 
        if(len(liste_id)==getNmbMaxJoueursFromIdPartie(id_partie)):
            return "Le nombre maximal d'arme a ete selectionne"

        for i in range(0,len(liste_id)):
            if (str(liste_id[i])==str(id_arme)):
                return "Arme deja ajoutee"

        ids_armes=ids_armes+","+str(id_arme)

    commande = "UPDATE parties SET listeIdArmes = ? WHERE id = ?"
    val = (ids_armes, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'Arme ajoutee'


@app.route('/addPlace/<nom_lieu>/<nom_partie>')
def addPlace(nom_lieu,nom_partie):
    id_lieu = getIdLieuFromNomArme(nom_lieu)
    if (id_lieu==-1):
        return "Lieu inconnu"

    id_partie = getIdPartieFromNomPartie(nom_partie)
    if (id_partie == -1):
        return "Partie inconnue"

    commande = "SELECT listeIdLieux FROM parties WHERE id = '"+str(id_partie)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    if(rows[0][0] is None):
        ids_lieux=str(id_lieu)

    else:
        ids_lieux=str(rows[0][0])
        liste_id=ids_lieux.split(",")
 
        if(len(liste_id)==getNmbMaxJoueursFromIdPartie(id_partie)):
            return "Le nombre maximal de lieu a ete selectionne"

        for i in range(0,len(liste_id)):
            if (str(liste_id[i])==str(id_lieu)):
                return "Lieu deja ajoute"

        ids_lieux=ids_lieux+","+str(id_lieu)

    commande = "UPDATE parties SET listeIdLieux = ? WHERE id = ?"
    val = (ids_lieux, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'Lieu ajoute'



@app.route('/start/<nom_partie>')
def startPartie(nom_partie):

    id_partie=getIdPartieFromNomPartie(nom_partie)

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

    #Check si les armes sont pretes
    nmb_armes = getNmbArmesInPartieFromIdPartie(id_partie)
    max_joueur = getNmbMaxJoueursFromIdPartie(id_partie)
    if(nmb_armes!=max_joueur):
        return "Toutes les armes n'ont pas ete selectionnees"

    #Check si les lieux sont prets
    nmb_lieux = getNmbLieuxInPartieFromIdPartie(id_partie)
    max_joueur = getNmbMaxJoueursFromIdPartie(id_partie)
    if(nmb_lieux!=max_joueur):
        return "Tous les lieux n'ont pas ete selectionnes"

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

    #Preparation des armes
    commande = "SELECT listeIdArmes FROM parties WHERE id='"+str(id_partie)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    ids_armes = cur.fetchall()
    conn.close

    liste_armes=str(ids_armes[0][0]).split(',')
  
    for i in range(30):
        liste_armes=triIds(liste_armes)


    #Preparation des lieux
    commande = "SELECT listeIdLieux FROM parties WHERE id='"+str(id_partie)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    ids_lieux = cur.fetchall()
    conn.close

    liste_lieux=str(ids_lieux[0][0]).split(',')

    for i in range(30):
        liste_lieux=triIds(liste_lieux)

    #Attribution des contrats
    for i in range(0, max_joueur-1):
        removeContratNul(id_partie,liste_joueurs[i])
        addContrat(id_partie,liste_joueurs[i],liste_joueurs[i+1],liste_armes[i],liste_lieux[i])

    removeContratNul(id_partie, liste_joueurs[max_joueur-1])
    addContrat(id_partie, liste_joueurs[max_joueur-1],liste_joueurs[0],liste_armes[max_joueur-1],liste_lieux[max_joueur-1])

    #Changement de l'etat de la partie
    commande = "UPDATE parties SET etat = ? WHERE id = ?"
    val = (VAL_PARTIE_EN_COURS, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'Partie lancee'

def getEtatPartieFromIdPartie(id_partie):
    commande = "SELECT etat FROM parties WHERE id = '"+str(id_partie)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    return rows[0][0]

@app.route('/afficherResultats/<nom_partie>')    
def getResults(nom_partie):
    id_partie = getIdPartieFromNomPartie(nom_partie)
    etat_partie = getEtatPartieFromIdPartie(id_partie)

   
    if(etat_partie != VAL_PARTIE_FINIE):
        return "La partie n'est pas terminee, vous ne pouvez pas consulter les resultats"

    commande = "SELECT * FROM contrats WHERE id_partie='"+str(id_partie)+"' AND realise='"+str(VAL_CONTRAT_REALISE)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    res = cur.fetchall()
    conn.close

    liste_id_assassins=[]
    liste_noms_assassins=[]
    liste_id_cibles=[]
    liste_noms_cibles=[]
    liste_id_armes=[]
    liste_noms_armes=[]
    liste_id_lieux=[]
    liste_noms_lieux=[]
    liste_dates=[]


    for i in range(0, len(res)):
        liste_id_assassins.append(res[i][1])
        liste_id_cibles.append(res[i][2])
        liste_id_armes.append(res[i][3])
        liste_id_lieux.append(res[i][4])
        liste_dates.append(res[i][7])

    for i in range(0, len(liste_id_assassins)):
        liste_noms_assassins.append(getNomJoueurFromId(liste_id_assassins[i]))

    for i in range(0, len(liste_id_armes)):
        liste_noms_armes.append(getNomArmeFromId(liste_id_armes[i]))

    for i in range(0, len(liste_id_lieux)):
        liste_noms_lieux.append(getNomLieuFromId(liste_id_lieux[i]))

    for i in range(0, len(liste_id_cibles)):
        liste_noms_cibles.append(getNomJoueurFromId(liste_id_cibles[i]))

    liste_resultats = []
    liste_resultats.append(liste_noms_assassins)
    liste_resultats.append(liste_noms_cibles)
    liste_resultats.append(liste_noms_armes)
    liste_resultats.append(liste_noms_lieux)
    liste_resultats.append(liste_dates)
  
    #TODO Tri par heure
    res=""
    for i in range(0,len(liste_resultats[0])):
        res+=str(liste_resultats[0][i]) + " a tue "+ str(liste_resultats[1][i]) + " avec l'arme "+str(liste_resultats[2][i])+ " dans le lieu "+str(liste_resultats[3][i]) + " le "+str(liste_resultats[4][i])+"<br>"
   
    return res

def getAllIdPartieEnCours():
    commande = "SELECT id FROM parties WHERE etat = ?"
    val = (VAL_PARTIE_EN_COURS,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    rows = cur.fetchall()
    conn.close

    liste_id=rows
    return liste_id

@app.route('/modifierMdp/<nom_joueur>/<mdp>/<nouveau_mdp>')
def modifMdp(nom_joueur, mdp, nouveau_mdp):
    id_joueur= getIdJoueurFromNom(nom_joueur)
    if(id_joueur==-1):
        return "Joueur inconnu"

    ids_parties = getAllIdPartieEnCours()

    for i in range(0,len(ids_parties)):
        ids_joueurs = getAllIdJoueursFromIdPartie(ids_parties[i][0])
        for j in range(0, len(ids_joueurs)):
            if(id_joueur==ids_joueurs[j][0]):
                return "Vous etes dans une partie en cours, vous ne pouvez pas changer de mot de passe"

    if(str(mdp)!=str(getMdpFromIdJoueur(id_joueur))):
        return "Mot de passe incorrect"

    commande = "UPDATE joueurs SET mdp = ? WHERE id = ?"
    val = (nouveau_mdp, id_joueur)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return "Mot de passe modifie"


@app.route('/ATTENTION/remove/contrats/ALL')
def RemoveAllContratsDB():
    commande = "DELETE FROM contrats"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Contrats supprimes'

@app.route('/ATTENTION/remove/joueurs/ALL')
def RemoveAllJoueursDB():
    commande = "DELETE FROM joueurs"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Joueurs supprimes'

@app.route('/ATTENTION/remove/armes/ALL')
def RemoveAllArmesDB():
    commande = "DELETE FROM armes"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Armes supprimees'

@app.route('/ATTENTION/remove/lieux/ALL')
def RemoveAllLieuxDB():
    commande = "DELETE FROM lieux"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Lieux supprimes'

@app.route('/ATTENTION/remove/parties/ALL')
def RemoveAllPartiesDB():
    commande = "DELETE FROM parties"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Parties supprimees'

