from lireLaby import labyFromFile
import copy
from turtle import*


def afficheTextuel(laby, dico):
    labystr = ""
    for i in range(len(laby)):
        for j in range(0, len(laby[i])):
            if i == dico["entrée"][0] and j == dico["entrée"][1]:
                labystr += "x"
            elif i == dico["sortie"][0] and j == dico["sortie"][1]:
                labystr += "o"
            elif laby[i][j] == 1:
                labystr += "#"

            else:
                labystr += "."

        labystr += "\n"
    print(labystr)


def carre(cl, dis):  # murs
    fillcolor(cl)  # pas marché avec fillcolor
    begin_fill()
    for i in range(4):
        speed('fastest')
        forward(dis)
        left(90)
    end_fill()


def carre_esp(dis):  # crée les espace
    for i in range(4):
        speed('fastest')
        penup()
        forward(dis)
        pendown()
        left(90)


def try_p(x):  # crée ligne par ligne
    penup()
    right(180)
    forward(30*x)
    left(90)
    forward(30)
    left(90)
    pendown()


def afficheGraphique(laby, dico):
    x = len(laby[0])
    speed(1000)
    penup()
    goto(-300, 200)
    pendown()
    for i in range(len(laby)):
        for j in range(0, len(laby[i])):
            if i == dico["entrée"][0] and j == dico["entrée"][1]:
                carre("green", 30)
            elif i == dico["sortie"][0] and j == dico["sortie"][1]:
                carre("cyan", 30)
            elif laby[i][j] == 1:
                carre('red', 30)
            else:
                carre_esp(30)
            penup()
            forward(30)
            pendown()
        try_p(x)
    up()
    xs, ys = cell2pixel(dicoJeu["entrée"][0], dicoJeu["entrée"][1])
    goto(xs-30, ys)
    color('black')


def pixel2cell(xp, yp):
    x_or = -300
    y_or = 230
    taille_pixel = 30
    dx = xp-x_or
    dy = -(yp-y_or)
    indice_colonne = dx//taille_pixel
    indice_ligne = dy//taille_pixel
    return indice_colonne, indice_ligne


def testClic(x, y):
    ind_colonne, ind_ligne = pixel2cell(x, y)
    ind_ligne_max = len(labymodifié)-1
    ind_colonne_max = len(labymodifié[0])-1
    print(ind_ligne, ' ', ind_colonne)
    if 0 <= ind_ligne <= ind_ligne_max and 0 <= ind_colonne <= ind_colonne_max:
        print('Ca marche')
    else:
        print("ERROR, nous sommes en dehors du laby")


def cell2pixel(i, j):
    px_a = -300 + 30 * j + 15
    py_a = 230 - 30 * i - 15
    return px_a, py_a


def typeCellule(indice_col, indice_lin, dico):
    if 0 <= indice_lin < len(laby) and 0 <= indice_col < len(laby[0]):
        if dico["entrée"][1] == indice_col and dico["entrée"][0] == indice_lin:
            return("entrée")
        elif dico["sortie"][1] == indice_col and dico["sortie"][0] == indice_lin:
            # color("green")
            # print("bien joué!")
            return("sortie")
        elif laby[int(indice_lin)][int(indice_col)] == 1:
            return("mur")
        elif laby[int(indice_lin)][int(indice_col)] == 0:
            return("passage")
    else:
        print("ICI")
        return("mur")


def type_passage(i, j, dico):  # pour identigier les impasses et les carrefours
    nbre_m = 0  # nbre de murs entourant la tortue
    if typeCellule(i, j, dico) == 'passage':
        if typeCellule(i-1, j, dico) == "mur" and i > 0:
            nbre_m += 1
        if typeCellule(i+1, j, dico) == "mur" and i > 0:
            nbre_m += 1
        if typeCellule(i, j-1, dico) == "mur" and i > 0:
            nbre_m += 1
        if typeCellule(i, j+1, dico) == "mur" and i > 0:
            nbre_m += 1
    if nbre_m == 0 or nbre_m == 1:
        return 'carrefour'
    if nbre_m == 2:
        return 'standard'
    if nbre_m == 3:
        return 'impasse'


def tt_color(i, j):

    if type_passage(i, j, dicoJeu) == 'carrefour':
        color('blue')
    if type_passage(i, j, dicoJeu) == 'impasse':
        color('purple')
    if type_passage(i, j, dicoJeu) == 'standard':
        color('black')
    if typeCellule(i, j, dicoJeu) == 'sortie':
        color('green')
        write("victoire !!!")


dist = 30
listcmd = []


def gauche():
    x, y = pixel2cell(xcor(), ycor())
    r = typeCellule(int(x)-1, int(y), dicoJeu)
    print(xcor(), ycor())
    print(x, y)
    print(r)
    i, j = int(x-1), int(y)
    if r == "passage" or r == "entrée" or r == "sortie":
        setheading(180)
        penup()
        forward(dist)
        print("gauche ; left")
        tt_color(i, j)
        listcmd.append('g')
        # print(listcmd)
    if r == 'mur':
        write('erreur : déplacement impossible')
        color('red')


def droite():
    x, y = pixel2cell(xcor(), ycor())
    r = typeCellule(int(x)+1, int(y), dicoJeu)
    print(x, y)
    print(r)
    i, j = int(x+1), int(y)
    if r == "passage" or r == "entrée" or r == "sortie":
        setheading(0)
        penup()
        forward(dist)
        tt_color(i, j)
        print("droite ; right")
        listcmd.append('d')
        # print(listcmd)
    if r == 'mur':
        write('erreur : déplacement impossible')
        color('red')


def haut():
    x, y = pixel2cell(xcor(), ycor())
    r = typeCellule(int(x), int(y)-1, dicoJeu)
    print(x, y)
    print(r)
    i, j = int(x), int(y-1)
    if r == "passage" or r == "entrée" or r == "sortie":
        setheading(90)
        penup()
        forward(dist)
        print("haut ; up")
        tt_color(i, j)
        listcmd.append('h')
        # print(listcmd)
    if r == 'mur':
        write('erreur : déplacement impossible')
        color('red')


def bas():
    x, y = pixel2cell(xcor(), ycor())
    r = typeCellule(int(x), int(y)+1, dicoJeu)
    print(x, y)
    print(r)
    i, j = int(x), int(y+1)
    if r == "passage" or r == "entrée" or r == "sortie":
        setheading(270)
        penup()
        forward(dist)
        tt_color(i, j)
        print("bas ; down")
        listcmd.append('b')
        print(listcmd)
    if r == 'mur':
        write('erreur : déplacement impossible')
        color('red')


###################################### AUTOMATIC #############################################

#  li = list
def suivrechemin(li):  # qui trouve la sortie à l'aide de la liste de commandes(cmd)
    speed('fastest')
    for cmd in li:
        if cmd == 'g':
            x, y = pixel2cell(xcor(), ycor())
            r = typeCellule(int(x)-1, int(y), dicoJeu)
            # print(xcor(), ycor())
            # print(x, y)
            # print(r)
            i, j = int(x-1), int(y)
            if r == "passage" or r == "entrée" or r == "sortie":
                setheading(180)
                penup()
                forward(dist)
                print("gauche ; left")
                tt_color(i, j)
            if r == 'mur':
                print('erreur : déplacement impossible ')
                return None
        if cmd == 'd':
            x, y = pixel2cell(xcor(), ycor())
            r = typeCellule(int(x)+1, int(y), dicoJeu)
            # print(x, y)
            # print(r)
            i, j = int(x+1), int(y)
            if r == "passage" or r == "entrée" or r == "sortie":
                setheading(0)
                penup()
                forward(dist)
                tt_color(i, j)
                print("droite ; right")
            if r == 'mur':
                print('erreur : déplacement impossible ')
                return None
        if cmd == 'h':
            x, y = pixel2cell(xcor(), ycor())
            r = typeCellule(int(x), int(y)-1, dicoJeu)
            # print(x, y)
            # print(r)
            i, j = int(x), int(y-1)
            if r == "passage" or r == "entrée" or r == "sortie":
                setheading(90)
                penup()
                forward(dist)
                print("haut ; up")
                tt_color(i, j)
                listcmd.append('h')
                print(listcmd)
            if r == 'mur':
                print('erreur : déplacement impossible ')
                return None
        if cmd == 'b':
            x, y = pixel2cell(xcor(), ycor())
            r = typeCellule(int(x), int(y)+1, dicoJeu)
            # print(x, y)
            # print(r)
            i, j = int(x), int(y+1)
            if r == "passage" or r == "entrée" or r == "sortie":
                setheading(270)
                penup()
                forward(dist)
                tt_color(i, j)
                print("bas ; down")
                listcmd.append('b')
                print(listcmd)
            if r == 'mur':
                print('erreur : déplacement impossible ')
                return None


def chemininverse(li):
    li2 = []
    listinverse = []
    for i in range(len(li)-1, -1, -1):
        listinverse.append(li[i])
    for elem in listinverse:
        if elem == 'd':
            li2.append('g')
        if elem == 'g':
            li2.append('d')
        if elem == 'h':
            li2.append('b')
        if elem == 'b':
            li2.append('h')
    suivrechemin(li2)


# def explorer():
#     x, y = pixel2cell(xcor(), ycor())
#     r = typeCellule(int(x), int(y)+1, dicoJeu)
#     i, j = int(x), int(y+1)
#     liste_branche = []
#     liste_exp = [dicoJeu["entrée"]]
#     while len(liste_exp) != 0:
#         branche = []
#         curr = liste_exp[0]
#         liste_exp.pop(0)
#         branche.append(curr)
#         while curr != [dicoJeu["sortie"]]:
#             if type_passage(curr) == "passage":
#                 curr =
#                 branche.append(curr)
#             if type_passage(curr) == "impasse":
#                 break
#             if type_passage(curr) == "carrefour":
#                 possibilité1 =
#                 possibilité2 =
#                 liste_exp.append(possibilité1, possibilité2)
#                 break
#             liste_branche.append(branche)


################################################PROGRAMME PRINCIPALE###############################################################
lance = textinput("lance", "on commence XD ?  ")
if lance not in ["oui", "OUI", "Oui", "yes", "YES", "Yes", "non", "NON", "Non", "no", "NO", "No"]:
    lance = textinput("lance", "invalide input, esseye encore")
while lance in ["oui", "OUI", "Oui", "yes", "YES", "Yes"]:
    typejeu = textinput("type", "manuelement ou automatiquement? ")
    if typejeu not in ["manuelement", "m", "manuel", "automatiquement", "a", "auto"]:
        typejeu = textinput("type", "invalide input, esseye encore")
    if typejeu in ["manuelement", "m", "manuel", "automatiquement", "a", "auto"]:
        level = textinput("difficulté?", "facile ou moyenne ou difficile?")
        if level in ["facile", "easy", "f"]:
            nom_fichier = 'laby0.laby'
        elif level in ["moyenne", "m", "medium"]:
            nom_fichier = 'laby1.laby'
        elif level in ["dificile", "d", "advanced"]:
            nom_fichier = 'laby2.laby'
        else:
            level = textinput("difficulté?", "invalide input, esseye encore")

        laby, mazein, mazeout = labyFromFile(nom_fichier)

        dicoJeu = {}

        dicoJeu["entrée"] = mazein
        dicoJeu["sortie"] = mazeout
        print(dicoJeu["entrée"])

        print("Le laby est :", laby)
        print("\n")
        print("Le dico est ", dicoJeu)

        labymodifié = copy.deepcopy(laby)
        afficheTextuel(laby, dicoJeu)
        afficheGraphique(laby, dicoJeu)
        # position_entrée(dicoJeu)
        print(typeCellule(0, 10, dicoJeu))
        print(typeCellule(10, 0, dicoJeu))

        # l2 = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'g', 'd', 'd',
        #       'd', 'd', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h', ]

        # key bindings
        if typejeu in ["manuelement", "m", "manuel"]:
            onkeypress(gauche, "Left")
            onkeypress(droite, "Right")
            onkeypress(haut, "Up")
            onkeypress(bas, "Down")
            print(pixel2cell(xcor(), ycor()))
            listen()
        if typejeu in ["automatiquement", "a", "auto"]:
            if level in ["facile", "easy", "f"]:
                listcmd = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd',
                           'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'd']
            elif level in ["moyenne", "m", "medium"]:
                listcmd = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h', 'h',
                           'h', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'h', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd']
            elif level in ["dificile", "d", "advanced"]:
                listcmd = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'h', 'h', 'd', 'h', 'd', 'd', 'd', 'd',
                           'h', 'h', 'h', 'g', 'g', 'g', 'g', 'g', 'h', 'h', 'g', 'g', 'g', 'g', 'h', 'h', 'd', 'd', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'b', 'b', 'd', 'd', 'b', 'd', 'd', 'h', 'd', 'd', 'd', 'd', 'd']
            suivrechemin(listcmd)
            chemininverse(listcmd)
        done()
        # lance = textinput("lance", "tu veux jouer encore? ")
        # typejeu = textinput("type", "manuelement ou automatiquement? ")

if lance in ["non", "NON", "Non", "no", "NO", "No"]:
    write("OK, aurevoir!")
    done()
# print(cell2pixel(1, 0))
# print(compteur_voisinage(1, 5, dicoJeu))
# print(typeCellule2(14, 0, dicoJeu))
# impasser(dicoJeu)
# print(typeCellule(0, 10, dicoJeu))
# print(typeCellule(10, 0, dicoJeu))
