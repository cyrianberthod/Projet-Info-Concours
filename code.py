##Importations
import numpy as np
import matplotlib.pyplot as plt
import random as rd
#on pose l=ligne et c=colonne
#Joueur 1 = croix , Joueur 2 = rond
coord_bordure=[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4)]

#------------------------------------------------Matrice-------------------------------------------------------------------------------

#initialiation
def play():
    global Plateau
    Plateau=np.zeros((5,5))
    global joueur
    joueur = rd.randint(1,2)

play()


def capture_cube(case): #capture le cube en position case si cela est possible
    P=Plateau
    l,c=case
    positions_possibles=[]# récupère les coordonnées (i,j) de tout les endroits ou le joueur peut jouer un nouveau coup , en bordure!
    for position in coord_bordure:#lp=ligne du doublet dans position cp=colonne du doublet dans position
        lp,cp=position
        if P[lp,cp]==0 or P[lp,cp]==joueur:
             positions_possibles.append((l,c))
    if case in positions_possibles: #verifie que  la position est valide
        P[l,c]=-1 #on enlève le cube, -1=case vide
        print(P)
        return True
    return False

##Peut-on pousser ici ?
def poussepossible(case): #renvoie liste des coorconnées des posi° où on peut pousser
    l,c = case
    A=[(0,0),(0,4),(4,0),(4,4)] #listes des coord des angles
    if case in A: #si le pion a été pris dans un angle
      return [(abs(l-4),c),(l,abs(4-c))]#on fixe l ou c , on determine les endroits ou on peut pousser par la relation avec abs() (faire dessin)
    L=[(l,0),(l,4),(0,c),(4,c)] #si le pion n'a pas été pris dans un angle 4 posibilités
    for k in range(4):
        if L[k]==case:
            del L[k]     #on ne peut pas laisser le pion où on l'a pris
        return L

def pousseok(vide,case): #case = coordonnées de là où on veut pousser
    Lpos=poussepossible(vide) #liste des positions de pousse possibles
    for k in Lpos:
        if case==k:  #l'endroit où le joueur veut poser est dans Lposs => c ok
            return True
    return False

## Pousse de la ligne ou de la colonne
def pousse(vide,case):
    P = Plateau
    l,c = case #position de la case de pose
    lv,cv = vide #position de la case vide

    #décalage de la ligne ou de la colonne de pousse
    if l == lv:
        if c<cv:
            for k in range (cv,0,-1):
                P[l,k]=P[l,k-1]
        elif c > cv: #peut etre remplacer par else si impossible de poser au même endroit
            for k in range (cv,4):
                P[l,k]=P[l,k+1]
    elif c == cv: #peut etre remplacer par else 
        if l < lv:
            for k in range (lv,0,-1):
                P[k,c]=P[k-1,c]
        elif l > lv: #peut etre remplacer par else si impossible de poser au même endroit
            for k in range (lv,4):
                P[k,c]=P[k+1,c]
            
    #pose du cube à la position de pousse           
    P[l,c] = joueur 
    print(P)


    


#------------------------------------------------------Interface Graphique-----------------------------------------------------------

#figure
fig = plt.figure()
ax = plt.axes(aspect=1) #repère orthonormé
plt.xlim(-1,6) 
plt.ylim(-1,6)
plt.axis('off')
plt.title('QUIXO')
contour = plt.Rectangle((-1,-1),7,7,fc=(0.8,0.8,0.8))
ax.add_patch(contour)
fond = plt.Rectangle((0,0),5,5, fc=(0.4,0.25,0.2))
ax.add_patch(fond)
bouton=plt.Rectangle((1,5.2),3,0.6,fc='black') #bouton new game
ax.add_patch(bouton)
newgame=plt.text(2.5,5.5,'New Game',fontsize=10,horizontalalignment='center',verticalalignment='center',color='w')
for k in range (-1,5): #grille
    h=k+0.975
    lignev = plt.Rectangle((h,0),0.05,5,fc=(0.8,0.8,0.8))
    ligneh = plt.Rectangle((0,h),5,0.05,fc=(0.8,0.8,0.8))
    ax.add_patch(lignev)
    ax.add_patch(ligneh)



def refresh(): #mise à jour de la figure en fonction de la matrice
    P=Plateau
    neutre=[]
    croix=[]
    rond=[]
    global vide #nécessaire pour pour l'appeler dans clic
    for l in range(5):
        for c in range(5):
            case=(l,c)
            if P[l,c]==0:
                neutre.append(case)
    
            elif P[l,c]==1:
                croix.append(case)
            
            elif P[l,c]==2:
              rond.append(case)
    
            elif P[l,c]==-1:
                vide = case #pas besoin de liste, maximum une case vide
                yc, xc = vide 
                yc = 4-yc #passage de la matrice a la figure
                dessinvide = plt.Rectangle((xc,yc), width=1, height=1, facecolor=(0.8,0.8,0.8)) 
                ax.add_patch(dessinvide)
    
    for cube in croix:
        yc, xc = cube
        yc = 4-yc #passage de la matrice a la figure
        dessinneutre = plt.Rectangle((xc+0.025,yc+0.025), width=0.95, height=0.95, facecolor=(0.4,0.25,0.2))
        ax.add_patch(dessinneutre)
        branche1 = plt.Rectangle((xc+0.25,yc+0.35), width=0.1, height=0.6, angle=-45, facecolor='black')
        branche2 = plt.Rectangle((xc+0.65,yc+0.3), width=0.1, height=0.6, angle=45, facecolor='black')
        ax.add_patch(branche1)
        ax.add_patch(branche2)
    for cube in rond:
        yc, xc = cube
        yc = 4-yc #passage de la matrice a la figure
        dessinneutre = plt.Rectangle((xc+0.025,yc+0.025), width=0.95, height=0.95, facecolor=(0.4,0.25,0.2))
        ax.add_patch(dessinneutre)
        dessinrond = plt.Circle((xc+0.5,yc+0.5), radius=0.3, facecolor='black')
        ax.add_patch(dessinrond)
    for cube in neutre:
        yc, xc = cube
        yc = 4-yc #passage de la matrice a la figure
        dessinneutre = plt.Rectangle((xc+0.025,yc+0.025), width=0.95, height=0.95, facecolor=(0.4,0.25,0.2))
        ax.add_patch(dessinneutre)

#actions declenchées par le clique de souris 
def clic(event):
    x,y = event.xdata,event.ydata #récupère les coord du clique
    c = int(x-x%1) #passage de la figure à la matrice
    l = int(4-(y-y%1))
    #global case 
    case = (l,c)
    testvide = np.where(Plateau == -1)[0]
    if testvide.size == 0: #vérifie que aucun cube n'a deja été sélectioné
        print('capture')
        capture_cube(case)
        refresh()
    else: #le cube à été capturé, phase de pousse.
        print('test pose')
        if pousseok(vide, case):
            pousse(vide,case)
            print('pose')
            refresh()

            #changement de tour
            global joueur
            if joueur==1:
                joueur=2
            else:
                joueur=1
             


fig.canvas.mpl_connect('button_press_event', clic)
plt.interactive(True) 
plt.pause(10000) #evite que la figure se ferme 
plt.show(block=False) #evite les bugs 

    


