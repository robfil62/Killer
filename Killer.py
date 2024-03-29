import random, sqlite3
from datetime import datetime
from time import strptime, strftime
from flask import Flask, request, redirect, url_for

VAL_CONTRAT_REALISE = 1
VAL_CONTRAT_EN_COURS = 0
VAL_CONTRAT_ECHOUE = -1
VAL_PARTIE_INIT = 0
VAL_PARTIE_EN_COURS = 1
VAL_PARTIE_FINIE = 2

app = Flask(__name__)

@app.route('/')
def redirectHome():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    html = '<form action="/newPlayer" method="get"> <button type="submit">Creer un joueur</button> </form> <br> <form action="/join" method="get"> <button type="submit">Rejoindre une partie</button> </form> <br>  <form action="/myContrat" method="get"> <button type="submit">Voir mon contrat actuel</button> </form> <br> <form action="/contratDone" method="get"> <button type="submit">Valider mon contrat actuel</button> </form> <br> <form action="/help" method="get"> <button type="submit">Aide</button> </form>'
    return html

@app.route('/admin')
def admin():
    html = '<form action="/newWeapon" method="get"> <button type="submit">Creer une arme</button> </form> <br> <form action="/newPlace" method="get"> <button type="submit">Creer un lieu</button> </form> <br>  <form action="/newParty" method="get"> <button type="submit">Creer une partie</button> </form> <br> <form action="/addWeapon" method="get"> <button type="submit">Ajouter une arme a une partie</button> </form> <br>  <form action="/addPlace" method="get"> <button type="submit">Ajouter un lieu a une partie</button> </form> <br>  <form action="/start" method="get"> <button type="submit">Lancer une partie</button> </form> <br> <form action="/helpAdmin" method="get"> <button type="submit">Aide</button> </form>'
    return html

@app.route("/help")
def help():
    return "# Killer <br> ### Creer un joueur : <br> > /newPlayer/[nom_joueur]/[mdp] <br> ### Rejoindre une partie : <br> > /join/[nom_partie]/[nom_joueur]/[mdp] <br> ### Afficher un contrat : <br> > /myContrat/[nom_partie]/[nom_joueur]/[mdp] <br> ### Contrat realise : <br> > /contratDone/[nom_partie]/[nom_assassin]/[mdp]/[mdp_victime] <br> ### Modifier son mdp : <br> > /modifierMdp/[nom_joueur]/[mdp]/[nouveau_mdp] "


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

@app.route('/contratDone', methods=['GET','POST'])
def setContratRempli():
    if request.method == 'GET':
        return '<form action="/contratDone" method="post"> <label> Nom de la partie <label> <br> <input type="text" name="nom_partie"> <br> <br> <label> Nom du joueur <label> <br> <input type="text" name="nom_assassin"> <br> <br> <label> Mot de passe </label> <br> <input type="password" name="mdp"> <br> <br> <label> Mot de passe de votre victime </label> <br> <input type="password" name="mdp_victime"> <br> <br> <button type="submit">Voir mon contrat</button> </form>'

    else : 
        nom_partie = request.form['nom_partie']
        nom_assassin = request.form['nom_assassin']
        mdp = request.form['mdp']
        mdp_victime = request.form['mdp_victime']
        id_partie=getIdPartieFromNomPartie(nom_partie)
        if id_partie==-1:
            return 'Partie inconnue <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

        etat_partie = getEtatPartieFromIdPartie(id_partie)
        if(etat_partie != VAL_PARTIE_EN_COURS):
            return 'La partie est terminee ou non demarree <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form> '

        id_assassin = getIdJoueurFromNom(nom_assassin)
        if id_assassin ==-1:
            return 'Joueur inconnu <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'
    
        id_contrat_realise = getIdContratFromIdAssassin(id_partie, id_assassin)
        if id_contrat_realise != -1:
            if (str(getMdpFromIdJoueur(id_assassin))!=str(mdp)):
                return 'Mot de passe assassin incorrect <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

            id_cible = getIdCibleFromIdContrat(id_contrat_realise)
            if (str(getMdpFromIdJoueur(id_cible))!=str(mdp_victime)):
                return 'Mot de passe de la victime incorrect <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

            id_contrat_cible = getIdContratFromIdAssassin(id_partie, id_cible)
            id_cible_cible = getIdCibleFromIdContrat(id_contrat_cible)

            if (id_cible_cible == id_assassin):
                setUpdateEtatContrat(VAL_CONTRAT_REALISE, id_contrat_realise)
                setUpdateEtatContrat(VAL_CONTRAT_ECHOUE, id_contrat_cible)
                setUpdateEtatPartie(VAL_PARTIE_FINIE, id_partie)
                return('FIN DE PARTIE ------------------ Gagnant : '+ nom_assassin+'<br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>') 

            else:
                id_arme_cible = getIdArmeFromIdContrat(id_contrat_cible)
                id_lieu_cible = getIdLieuFromIdContrat(id_contrat_cible)
                setUpdateEtatContrat(VAL_CONTRAT_REALISE, id_contrat_realise)
                setUpdateEtatContrat(VAL_CONTRAT_ECHOUE, id_contrat_cible)
                addContrat(id_partie, id_assassin, id_cible_cible, id_arme_cible, id_lieu_cible)
                return(nom_assassin + ", votre nouveau contrat : "+getContrat(getIdContratFromIdAssassin(id_partie,id_assassin)) +'<br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>')
        else:
            return 'Joueur pas dans la partie <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

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

@app.route('/newParty', methods=['GET','POST'])
def addPartie():
    if request.method == 'GET':
        return '<form action="/newParty" method="post"> <label> Nom de la partie <label> <br> <input type="text" name="nom_partie"> <br> <br> <label> Nombre de joueurs <label> <br> <input type="int" name="nmb_joueurs"> <br> <br> <button type="submit">Creer</button> </form>'

    else :
        nom_partie = request.form['nom_partie']
        nmb_joueurs = request.form['nmb_joueurs']

        commande = "SELECT nom FROM parties WHERE nom = ?"
        val = (nom_partie,)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        partie = cur.fetchall()
        conn.close

        if(len(partie)!=0):
            return 'La partie existe deja  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

        commande = "INSERT INTO parties (nom, nmbJoueurs) VALUES (?,?)"
        val = (nom_partie, nmb_joueurs)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        conn.commit()
        conn.close

        return 'Partie creee <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

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
    print(ids)
    for i in range(nmbJoueurs):
        place=random.randint(0,nmbJoueurs-i-1)
        idsTries.append(ids[place])
        ids.remove(ids[place])

        print(idsTries)
    return idsTries

@app.route('/join', methods=['GET','POST'])
def joinPartie():
    if(request.method == 'GET'):
        html = '<form action="/join" method="post"> <label> Nom de la partie <label> <br> <input type="text" name="nom_partie"> <br> <br> <label> Nom du joueur <label> <br> <input type="text" name="nom_joueur"> <br> <br> <label> Mot de passe </label> <br> <input type="password" name="mdp"> <br> <br> <button type="submit">Creer</button> </form>'
        return html

    else :
        nom_partie = request.form['nom_partie']
        nom_joueur = request.form['nom_joueur']
        mdp = request.form['mdp']
    commande = "SELECT id,mdp FROM joueurs WHERE nom = ?"
    val = (nom_joueur,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    joueur = cur.fetchall()
    conn.close

    if(len(joueur)!=1):
        return 'Joueur inconnu <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

    if(str(joueur[0][1])!=str(mdp)):
        return 'Mot de passe incorrect <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

    commande = "SELECT id FROM parties WHERE nom = ?"
    val = (nom_partie,)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    partie = cur.fetchall()
    conn.close

    if(len(partie)!=1):
        return 'Partie inconnue <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

    id_partie = partie[0][0]
    id_joueur = joueur[0][0]

    nmb_max = getNmbMaxJoueursFromIdPartie(id_partie)
    nmb_joueurs = getNmbJoueursInPartieFromIdPartie(id_partie)

    if(nmb_max == nmb_joueurs):
        return 'Le nombre maximal de joueurs a ete atteint <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

    commande = "SELECT id_assassin FROM contrats WHERE id_assassin = ? AND id_partie = ?"
    val = (id_joueur, id_partie)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    id = cur.fetchall()
    conn.close

    if(len(id)!=0):
        return 'joueur deja dans la partie <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

    commande = "INSERT INTO contrats (id_partie, id_assassin) VALUES (?,?)"
    val = (id_partie, id_joueur)
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande,val)
    conn.commit()
    conn.close

    return 'joueur ajoute a la partie <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'


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

@app.route('/triche/<id_partie>')
def printAllContrats(id_partie):
    liste_id_joueurs = getAllIdJoueursFromIdPartie(id_partie)
    nmb_joueurs=len(liste_id_joueurs)
    res=""
    for i in range(0,nmb_joueurs):
        res = res +'<br>'+getNomJoueurFromId(liste_id_joueurs[i][0])+ " "+(getContrat(getIdContratFromIdAssassin(id_partie, liste_id_joueurs[i][0])))

    return res

@app.route('/myContrat', methods=['GET','POST'])
def printContratFromJoueur():
    if (request.method=='GET'):
        return '<form action="/myContrat" method="post"> <label> Nom de la partie <label> <br> <input type="text" name="nom_partie"> <br> <br> <label> Nom du joueur <label> <br> <input type="text" name="nom_joueur"> <br> <br> <label> Mot de passe </label> <br> <input type="password" name="mdp"> <br> <br> <button type="submit">Voir mon contrat</button> </form>'
    else:
        nom_partie = request.form['nom_partie']
        nom_joueur = request.form['nom_joueur']
        mdp = request.form['mdp']
        id_partie = getIdPartieFromNomPartie(nom_partie)

        etat_partie = getEtatPartieFromIdPartie(id_partie)
        if(etat_partie != VAL_PARTIE_EN_COURS):
            return 'La partie est terminee ou non demarree <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form> '

        id_joueur = getIdJoueurFromNom(nom_joueur)
        if(str(getMdpFromIdJoueur(id_joueur))!=str(mdp)):
            return 'Mot de passe incorrect <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form> <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form> '

        return nom_joueur + ", votre contrat : " + getContrat(getIdContratFromIdAssassin(id_partie,id_joueur)) + '<br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form> '

@app.route('/newWeapon',methods=['GET','POST'])
def addArme():
    if request.method=='GET':
        return '<form action="/newWeapon" method="post"> <label> Nom de l arme <label> <br> <input type="text" name="nom_arme"> <br> <br> <label> Description <label> <br> <input type="text" name="descr"> <br> <br> <button type="submit">Creer</button> </form>'

    else : 
        nom_arme = request.form['nom_arme']
        descr = request.form['descr']
        commande = "SELECT id FROM armes WHERE nom = ?"
        val = (nom_arme,)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        arme = cur.fetchall()
        conn.close

        if(len(arme)!=0):
            return 'L arme existe deja <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'


        commande = "INSERT INTO armes (nom, description) VALUES (?, ?)"
        val = (nom_arme,descr)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        conn.commit()
        conn.close

        return 'Arme creee <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

@app.route('/newPlace', methods = ['GET','POST'])
def addLieu():
    if request.method =='GET':
        return '<form action="/newPlace" method="post"> <label> Nom du lieu <label> <br> <input type="text" name="nom_lieu"> <br> <br> <label> Description <label> <br> <input type="text" name="descr"> <br> <br> <button type="submit">Creer</button> </form>'

    else :
        nom_lieu = request.form['nom_lieu']
        descr = request.form['descr']
        commande = "SELECT id FROM lieux WHERE nom = ?"
        val = (nom_lieu,)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        lieu = cur.fetchall()
        conn.close

        if(len(lieu)!=0):
            return 'Le lieu existe deja <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

        commande = "INSERT INTO lieux (nom, description) VALUES (?, ?)"
        val = (nom_lieu,descr)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        conn.commit()
        conn.close

        return 'Lieu cree <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'


@app.route('/newPlayer',methods = ['POST', 'GET'])
def addJoueur():
    if(request.method == 'GET'):
        html = '<form action="/newPlayer" method="post"> <label> Nom du joueur <label> <br> <input type="text" name="nom_joueur"> <br> <br> <label> Mot de passe </label> <br> <input type="password" name="mdp"> <br> <br> <button type="submit">Creer</button> </form>'
        return html

    else :
        nom_joueur = request.form['nom_joueur']
        mdp = request.form['mdp']
        commande = "SELECT id FROM joueurs WHERE nom = ?"
        val = (nom_joueur,)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        joueur = cur.fetchall()
        conn.close

        if(len(joueur)!=0):
            return 'Le joueur existe deja  <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form> '


        commande = "INSERT INTO joueurs (nom, mdp) VALUES (?, ?)"
        val = (nom_joueur,mdp)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        conn.commit()
        conn.close

        return 'Joueur cree <br> <br> <form action="/home" method="get"> <button type="submit">Menu</button> </form>'

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

def getIdLieuFromNomLieu(nom_lieu):
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


@app.route('/addWeapon',methods=['GET','POST'])
def addWeapon():
    if request.method=='GET':
        return '<form action="/addWeapon" method="post"> <label> Nom de l arme <label> <br> <input type="text" name="nom_arme"> <br> <br> <label> Nom de la partie </label> <br> <input type="text" name="nom_partie"> <br> <br> <button type="submit">Ajouter</button> </form>'

    else : 
        nom_arme = request.form['nom_arme']
        nom_partie = request.form['nom_partie']
        id_arme = getIdArmeFromNomArme(nom_arme)
        if (id_arme==-1):
            return 'Arme inconnue <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

        id_partie = getIdPartieFromNomPartie(nom_partie)
        if (id_partie == -1):
            return 'Partie inconnue <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

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
                return 'Le nombre maximal d arme a ete selectionne <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

            for i in range(0,len(liste_id)):
                if (str(liste_id[i])==str(id_arme)):
                    return 'Arme deja ajoutee <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

            ids_armes=ids_armes+","+str(id_arme)

        commande = "UPDATE parties SET listeIdArmes = ? WHERE id = ?"
        val = (ids_armes, id_partie)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        conn.commit()
        conn.close

        return 'Arme ajoutee <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'


@app.route('/addPlace', methods=['GET','POST'])
def addPlace():
    if request.method=='GET':
        return '<form action="/addPlace" method="post"> <label> Nom du lieu <label> <br> <input type="text" name="nom_lieu"> <br> <br> <label> Nom de la partie </label> <br> <input type="text" name="nom_partie"> <br> <br> <button type="submit">Ajouter</button> </form>'
    
    else : 
        nom_lieu = request.form['nom_lieu']
        nom_partie = request.form['nom_partie']
        id_lieu = getIdLieuFromNomLieu(nom_lieu)
        if (id_lieu==-1):
            return 'Lieu inconnu  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

        id_partie = getIdPartieFromNomPartie(nom_partie)
        if (id_partie == -1):
            return 'Partie inconnue  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

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
                return 'Le nombre maximal de lieu a ete selectionne  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

            for i in range(0,len(liste_id)):
                if (str(liste_id[i])==str(id_lieu)):
                    return 'Lieu deja ajoute  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

            ids_lieux=ids_lieux+","+str(id_lieu)

        commande = "UPDATE parties SET listeIdLieux = ? WHERE id = ?"
        val = (ids_lieux, id_partie)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        conn.commit()
        conn.close

        return 'Lieu ajoute  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'



@app.route('/start', methods=['GET','POST'])
def startPartie():
    if request.method =='GET':
        return '<form action="/start" method="post"> <label> Nom de la partie <label> <br> <input type="text" name="nom_partie"> <br> <br> <button type="submit">Lancer</button> </form>'

    else : 
        nom_partie = request.form['nom_partie']
        id_partie=getIdPartieFromNomPartie(nom_partie)

        if id_partie ==-1:
            return 'Partie inconnue  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

        #Check si la partie n'est pas deja commencee
        commande = "SELECT etat FROM parties WHERE id = ?"
        val = (id_partie,)
        conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
        cur=conn.cursor()
        cur.execute(commande,val)
        etat = cur.fetchall()
        conn.close

        if(etat[0][0]!= VAL_PARTIE_INIT):
            return 'La partie est deja en cours  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'
            
        #Check si tous les joueurs sont la
        nmb_joueur = getNmbJoueursInPartieFromIdPartie(id_partie)
        max_joueur = getNmbMaxJoueursFromIdPartie(id_partie)
        if(nmb_joueur!=max_joueur):
            return 'Tous les joueurs ne sont pas prets  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

        #Check si les armes sont pretes
        nmb_armes = getNmbArmesInPartieFromIdPartie(id_partie)
        max_joueur = getNmbMaxJoueursFromIdPartie(id_partie)
        if(nmb_armes!=max_joueur):
            return 'Toutes les armes n ont pas ete selectionnees <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

        #Check si les lieux sont prets
        nmb_lieux = getNmbLieuxInPartieFromIdPartie(id_partie)
        max_joueur = getNmbMaxJoueursFromIdPartie(id_partie)
        if(nmb_lieux!=max_joueur):
            return 'Tous les lieux n ont pas ete selectionnes  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

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

        return 'Partie lancee  <br> <br> <form action="/admin" method="get"> <button type="submit">Menu</button> </form>'

def getEtatPartieFromIdPartie(id_partie):
    commande = "SELECT etat FROM parties WHERE id = '"+str(id_partie)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    rows = cur.fetchall()
    conn.close

    return rows[0][0]

def triListes(listes):
    liste_ass = listes[0]
    liste_cib = listes[1]
    liste_arm = listes[2]
    liste_li = listes[3]
    liste_dates_str = listes[4]

    liste_dates = []
    liste_ass_tri = []
    liste_cib_tri = []
    liste_arm_tri = []
    liste_li_tri = []

    for i in range(0,len(liste_dates_str)):
        date = datetime.strptime(liste_dates_str[i],"%d/%m/%Y %H:%M:%S")
        liste_dates.append(date)

    for i in range(0,len(liste_dates)):
        mi = liste_dates[i]
        id_min = i
        
        for j in range(i+1,len(liste_dates)):
            if(liste_dates[j]<mi):
                mi = liste_dates[j]
                id_min = j

        save_i = liste_dates[i]
        liste_dates[i]=liste_dates[id_min]
        liste_dates[id_min] = save_i

        save_i = liste_ass[i]
        liste_ass[i]=liste_ass[id_min]
        liste_ass[id_min] = save_i

        save_i = liste_cib[i]
        liste_cib[i]=liste_cib[id_min]
        liste_cib[id_min] = save_i

        save_i = liste_arm[i]
        liste_arm[i]=liste_arm[id_min]
        liste_arm[id_min] = save_i

        save_i = liste_li[i]
        liste_li[i]=liste_li[id_min]
        liste_li[id_min] = save_i
        

    for i in range(0,len(liste_dates)):
        liste_dates_str[i]=liste_dates[i].strftime("%d/%m/%Y %H:%M:%S")

    liste_res=[]
    liste_res.append(liste_ass)
    liste_res.append(liste_cib)
    liste_res.append(liste_arm)
    liste_res.append(liste_li)
    liste_res.append(liste_dates_str)

    return liste_res

@app.route('/afficherResultats/<nom_partie>')    
def getResults(nom_partie):
    id_partie = getIdPartieFromNomPartie(nom_partie)

    if(id_partie == -1):
        return "Partie inconnue"

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

    liste_resultats = triListes(liste_resultats)
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

    commande = "DELETE FROM contrats"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Parties supprimees'


@app.route('/ATTENTION/remove/joueur/<nom_joueur>')
def RemoveJoueur(nom_joueur):
    id_joueur = getIdJoueurFromNom(nom_joueur)
    if (id_joueur==-1):
        return "Joueur inconnu"

    commande = "DELETE FROM joueurs WHERE id = '"+str(id_joueur)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Joueur supprime'

@app.route('/ATTENTION/remove/arme/<nom_arme>')
def RemoveArme(nom_arme):
    id_arme=getIdArmeFromNomArme(nom_arme)
    if (id_arme==-1):
        return "Arme inconnue"

    commande = "DELETE FROM armes WHERE id = '"+str(id_arme)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Arme supprimee'

@app.route('/ATTENTION/remove/lieu/<nom_lieu>')
def RemoveLieu(nom_lieu):
    id_lieu=getIdLieuFromNomLieu(nom_lieu)
    if (id_lieu==-1):
        return "Lieu inconnu"

    commande = "DELETE FROM lieux WHERE id = '"+str(id_lieu)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Lieu supprime'

@app.route('/ATTENTION/remove/partie/<nom_partie>')
def RemovePartie(nom_partie):
    id_partie = getIdPartieFromNomPartie(nom_partie)

    if(id_partie==-1):
        return "Partie inconnue"

    commande = "DELETE FROM parties WHERE nom = '"+nom_partie+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close

    commande = "DELETE FROM contrats WHERE id_partie = '"+str(id_partie)+"'"
    conn=sqlite3.connect("C:/Users/robin/Projets VSC/Killer/killer.db")
    cur=conn.cursor()
    cur.execute(commande)
    conn.commit()
    conn.close
    return 'Partie supprimee'
