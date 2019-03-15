from MinesweeperApp import MinesweeperApp

# TODO:
# Clean le code
# ^ il y a genre un million d'attributs rattachés à un object MinesweeperApp. Jdevrais tu le breakdown encore plus? (breakdown en plus de classes)
# ADD BORDERS --- jpas capable d'ajouter de border sur la grid. ca a l'air un peu off
# Clicking on help -> lol you don't need help -> should spawn a window with something funny
# niveau2 ->est-ce que je devrais print la grille avec les index quand la personne a gagner/perdu?
# le smiley et le surprised smiley sont centrés un peu différemment. eyesore
# Quand t'es à 0 flag et t'en place 1 tu vas à 999 flags
# Rendre plus beau le win/lose screen?
# Make menu friendlier ?
# Le settings menu est laid un peu
# Rajouter le question mark? Flag -> question mark -> vide

# Centrer le smiley # use button.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # ou quelque chose du genre
# ^ Faire sticker le timer et flag counter sur leur coté respectif



if __name__ == '__main__':
    app = MinesweeperApp()
