# Killer
Créer une partie : 
/newParty/<nom>/<nmb>

Créer un joueur : 
/newPlayer/<nom_joueur>/<mdp>

Créer une arme :
/newWeapon/<nom_arme>/<descr>

Créer un lieu : 
/newPlace/<nom_lieu>/<descr>

Rejoindre une partie :
/join/<nom_joueur>/<nom_partie>/<mdp>

Ajouter une arme à la partie : 
/addWeapon/<nom_arme>/<nom_partie>

Ajouter un lieu à la partie :
/addPlace/<nom_lieu>/<nom_partie>

Lancer la partie : 
/start/<nom_partie>

Afficher un contrat : 
/myContrat/<nom_joueur>/<nom_partie>/<mdp>

Contrat réalisé :
/contratDone/<nom_assassin>/<nom_partie>/<mdp>/<mdp_victime>

TODO Afficher les résultats :
/afficherResultats/<nom_partie>

TODO Modifier son mdp :
/modifierMdp/<nom_joueur>

Supprimer les bases :
/ATTENTION/remove/contrats/ALL
/ATTENTION/remove/joueurs/ALL
/ATTENTION/remove/parties/ALL
/ATTENTION/remove/armes/ALL
/ATTENTION/remove/lieux/ALL

Supprimer un lieu : 
TODO /ATTENTION/remove/lieux/<nom_lieu>

Supprimer un joueur : 
TODO /ATTENTION/remove/joueurs/<nom_joueur>

Supprimer une arme : 
TODO /ATTENTION/remove/armes/<nom_arme>

Supprimer une partie (et les contrats associés) :
TODO /ATTENTION/remove/parties/<nom_partie>
