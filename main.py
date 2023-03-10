############################
## Jeu du Serpent | Snake ##
############################

from tkinter import *
from random import randrange
from math import *

# Variables

# Tailles du canvas du jeu.
W = 600
H = 600

assert W == 600 and H == 600

global taille_serpent
global etat
global taille_bloc
global stop
global game_over


etat = "droite"         # Variable de la direction du serpent
taille_serpent = 4      # Variable de la taille du serpent.
taille_bloc= int(H/20)  # Variable de la taille d'un carré faisant partie du serpent en fonction de la résolution.
stop = False            # Variable de si le jeu est arrêté.
game_over = False       # Variable de si la partie est finie ou non.

coord_pomme = [0, 0]

serpent_base = (
    (W/2-int(taille_bloc/2),W/2-int(taille_bloc/2),W/2-int(taille_bloc/2),W/2-int(taille_bloc/2)),
    (W/2-int(taille_bloc/2),W/2-int(taille_bloc/2),W/2-int(taille_bloc/2),W/2-int(taille_bloc/2)),
    (W/2-int(taille_bloc/2),W/2-int(taille_bloc/2),W/2-int(taille_bloc/2),W/2-int(taille_bloc/2)),
    (W/2-int(taille_bloc/2),W/2-int(taille_bloc/2),W/2-int(taille_bloc/2),W/2-int(taille_bloc/2))
)

# Liste des couleurs utilisés dans le programme:
couleur = (
    '#000000',  # Noir
    '#FFFFFF',  # Blanc
    '#6CBB3C',  # Vert du serpent
    '#FF0000',  # Rouge
)

couleur_pomme = (
    '#FF0000',  # Rouge
    '#8db600',  # Vert
    '#FFA500',  # Orange
)
# Fonctions

# Fonctions pour faire changer la direction du serpent avec le clavier.

def haut(event):
    '''Fonction qui change la direction du serpent vers le haut.'''
    global etat
    if etat == "gauche" or etat == "droite":      # S'assure que le serpent ne puisse pas faire demi-tour.
        etat = "haut"

def bas(event):
    '''Fonction qui change la direction du serpent vers le bas.'''
    global etat
    if etat == "gauche" or etat == "droite":      # Idem
        etat = "bas"

def droite(event):
    '''Fonction qui change la direction du serpent vers la droite.'''
    global etat
    if etat == "haut" or etat == "bas":      # Idem
        etat = "droite"

def gauche(event):
    '''Fonction qui change la direction du serpent vers la gauche.'''
    global etat
    if etat == "haut" or etat == "bas":      # Idem
        etat = "gauche"

# Fonctions pour la fin de partie et la gestion des bords de la cartes.

def activer_game_over():
    '''Fonction qui active la fin de partie.'''
    global stop, game_over, score
    stop = True ; game_over = True      # Arrête le serpent et marque la partie comme finie.
    
def ecran_game_over():
    '''Fonction qui dessine l'écran de fin de partie'''
    game.delete(ALL)
    game.create_text(W/2, H/2, text='Game \n over', font=('Impact', 30), fill=couleur[3])

def hors_limite(x:int, y:int):
    '''Fonction qui arrête la partie si le serpent sort de la carte dans une partie classique.'''
    if x >= W or y >= H or x <= 0 or y <= 0:
        activer_game_over()
        
def suicide():
    '''Fonction qui arrête la partie si le serpent se mord la queue.'''
    for i in range(4, taille_serpent):
        if serpent[i][0] == serpent[0][0]  and serpent[i][1] == serpent[0][1] :
            activer_game_over()

# Fonctions pour le mouvement du serpent.

def tete():
    '''Fonction qui change la position de la tête en fonction de la direction.'''
    global origine
    origine = list(serpent)
    if etat == "droite":
        serpent[0] = [serpent[0][0]+taille_bloc, serpent[0][1], serpent[0][2]+taille_bloc, serpent[0][3]]
    elif etat == "gauche":
        serpent[0] = [serpent[0][0]-taille_bloc, serpent[0][1], serpent[0][2]-taille_bloc, serpent[0][3]]
    elif etat == "haut":
        serpent[0] = [serpent[0][0], serpent[0][1]-taille_bloc, serpent[0][2], serpent[0][3]-taille_bloc]
    elif etat == "bas":
        serpent[0] = [serpent[0][0], serpent[0][1]+taille_bloc, serpent[0][2], serpent[0][3]+taille_bloc]

def bordure():
    '''Fonction qui gère les actions du serpent en fonction de son environement et du mode de jeu.'''
    hors_limite(int(serpent[0][0]), int(serpent[0][1]))
    if taille_serpent > 4:          # Afin d'éviter que la partie s'arrête sans que le serpent ne se soit mordu le corps.
        suicide()

def deplacement():
    '''Fonction qui deplace le reste du corps du serpent.'''
    tete()
    for i in range(1,taille_serpent):
        serpent[i] = origine[i-1]
    for i in range(0,taille_serpent):   
        game.create_rectangle(serpent[i], width=taille_bloc , outline=couleur[2], fill=couleur[2])
    effacement()
    tete_qui_mange()
    bordure()
    if stop == False:                   # Arrête le serpent quand la partie est finie ou que le jeu est en pause.
        game.after(100, deplacement)
    elif game_over == True:
        ecran_game_over()

def effacement():
    '''Fonction qui efface la queue du serpent.'''
    global nombre_iteration
    if nombre_iteration > 2:
        game.create_rectangle(origine[taille_serpent-1][0], origine[taille_serpent-1][1], origine[taille_serpent-1][2]+2, origine[taille_serpent-1][3]+2, width=taille_bloc, outline=couleur[1], fill=couleur[1])    # Efface l'ancien dernier bloc du serpent.
    nombre_iteration += 1
    
# Fonctions pour lancer une partie et la mettre en pause.

def pause(event):
    '''Fonction qui met en pause la partie.'''
    global stop, ecran_pause
    if game_over == True:
        return
    elif stop == False:     # Vérifie si le jeu n'est pas déjà arrêté.
        stop = True
        ecran_pause = game.create_text(W/2, H/2, text='Pause', font=('Impact', 30))
    elif stop == True:      #  Relance le jeu si il est arrêté.
        stop = False
        game.delete(ecran_pause)
        deplacement()

def nouvelle_partie_classique():
    '''Fonction qui commence une nouvelle partie.'''
    global stop, serpent, etat, game_over, infinie, nombre_iteration, score, taille_serpent
    game.delete(ALL)
    serpent = list(serpent_base)    # Initialisation des coordonnées du serpent.
    stop = False ; etat = "droite" ; game_over = False ; infinie = False ; nombre_iteration = 0 ; score = 0 ; taille_serpent = 4
    pomme()
    deplacement()
    tex.configure(text = 'Score = ' + str(score))

# Fonctions pour permettre l'utilisation du jeu sans la souris.

def fin_partie(event):
    '''Fonction qui arrête la partie lorsqu'une touche est actionner.'''
    activer_game_over()
    
def quitter(event):
    '''Fonction pour quitter le jeu lorsqu'une touche est actionner.'''
    win.quit()

def lancer_classique(event):
    '''Fonction qui lance une partie classique lorsqu'une touche est actionner.'''
    nouvelle_partie_classique()

# Fonctions pour le score et manger les pommes

def position_aleatoire(x:int, y:int)->tuple:
    '''Fonction qui génère des positions aléatoires aux points x et y, qui ne peuvent pas être en dehors du canvas.'''
    x = 0 ; y = 0
    x = randrange(0, L)
    y = randrange(0, H)
    return x,y

def pomme():
    '''Fonction qui dessine une pomme avec une position aleatoire qui ne peut pas être en dehors du canvas.
    La Couleur de la pomme est determinée par une liste de couleur : "couleur".'''
    nb = 0
    coord_pomme[1] = randrange(0, W-taille_bloc, taille_bloc)
    coord_pomme[0] = randrange(0, H-taille_bloc, taille_bloc)
    for i in range(0, taille_serpent):          # Pour éviter que la pomme soit positionné dans le serpent.
        if serpent[i][0] == coord_pomme[0]  and serpent[i][1] == coord_pomme[1]:
            coord_pomme[1] = randrange(0, W-taille_bloc, taille_bloc)
    coord_pomme[0] = randrange(0, H-taille_bloc, taille_bloc)
    coul = couleur_pomme[randrange(0,len(couleur_pomme))]
    game.create_rectangle(coord_pomme[0], coord_pomme[1], coord_pomme[0]+taille_bloc, coord_pomme[1]+taille_bloc, outline = 'white', fill = coul, width=5)

def alonger_serpent():
    '''Fonction qui rajoute un bloc à la fin du serpent quand il mange une pomme.'''
    indice_dernier = len(serpent)-1
    serpent.append(origine[indice_dernier])

def manger():
    '''Fonction qui augmmente le score de 1 point lorsqu'une pomme est mangée'.'''
    global score, taille_serpent
    alonger_serpent()
    taille_serpent += 1
    score += 1
    tex.configure(text = 'Score = ' + str(score))   # Rafraichis le label pour le score.
 
def tete_qui_mange():
    '''Fonction qui permet d'augmenter le score et redessiner une nouvelle pomme orsque le serpent mange une pomme.'''
    if int(serpent[0][0])-15 == coord_pomme[0] and int(serpent[0][1])-15 == coord_pomme[1]:
        manger()
        pomme()

# Widgets

win = Tk()
win.title('Snake')

game = Canvas(win, width=W, height=H, bg=couleur[1])
game.grid(rowspan=14, column=0)

# Assignation des touches directionnelles pour choisir la direction du serpent
win.bind('<Up>', haut)
win.bind('<Down>', bas)
win.bind('<Left>', gauche)
win.bind('<Right>', droite)

# Assignation de la touche 'p' pour mettre le jeu en pause.
win.bind('<p>', pause)

# Assignation de la touche 'f' pour arrêter la partie.
win.bind('<f>', fin_partie)

# Assignation de la touche 'q' pour quitter le jeu.
win.bind('<q>', quitter)

# Assignation de la touche 'c' pour lancer une partie classique.
win.bind('<n>', lancer_classique)

but1 = Button(win, text='Nouvelle partie [n]', fg=couleur[0], bg=couleur[1], command=nouvelle_partie_classique)
but1.grid(row=1, column=1)

but2 = Button(win, text='Fin de partie [f]', fg=couleur[0], bg=couleur[1], command=activer_game_over)
but2.grid(row=3, column=1)

but3 = Button(win, text='Quitter [q]', fg=couleur[0], bg=couleur[1], command=win.quit)
but3.grid(row=13, column=1)

tex = Label(win, text = 'score = 0', fg = 'grey', bg = 'white', font = "TkFont")
tex.grid(column = 1, row = 4, sticky ='s')

win.mainloop()
