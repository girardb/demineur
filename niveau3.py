from MinesweeperApp import MinesweeperApp

# TODO:
# PAS OUBLIER DE FIX LES DEUX TESTS QUI FAIL POUR LE NIVEAU 2
# Clean le code -> jviens de le copy paste dans une class donc c'est messy un peu beaucoup
# ^ il y a genre un million d'attributs rattachés à un object MinesweeperApp. Jdevrais tu le breakdown encore plus? (breakdown en plus de classes)
# SHOULD I CHANGE THE DESIGN SO THAT THE FIRST TILE SELECTED IS AN EMPTY TILE # HOW
# MAYBE ADD THE MIDDLE BUTTON MECHANIC/COMMAND FROM THE REAL MINESWEEPER GAME
# capoter si le user fait spawner plus de 999 mines et que le timer dépasse 999 secondes
# ADD BORDERS --- jpas capable d'ajouter de border sur la grid. ca a l'air un peu off
# Make menu friendlier
# Fix game won/lost window
# Clicking on help -> lol you don't need help -> should spawn a window with something funny
# niveau2 ->est-ce que je devrais print la grille avec les index quand la personne a gagner/perdu?
# le smiley et le surprised smiley sont centrés un peu différemment. eyesore
# Rajouter beginner, medium, hard level ? -> rajouter un bouton beginner, medium, hard que quand on pèse dessus ca change les valeurs dans les entrées de height pour le truc pre-set genre 16x30 avec 99 mines.
# ^ ou encore mieux mais plus tough -> radio buttons pour ceux là pis un pour activer custom input. Pas nécessaire je pense though.
# le smiley est supposé reset le jeu quand tu cliques dessus ou juste changer de smiley à surprised ?? lol
# Centrer le smiley # use button.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # ou quelque chose du genre
# NEGATIVE FLAG COUNT GOES TO FF9

if __name__ == '__main__':
    # Startup time est un peu long. Faudrait que je check ca prend combien de RAM aussi, d'un coup que j'exagère.
    app = MinesweeperApp()
