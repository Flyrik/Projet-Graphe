def lire_fichier(doc):
    matrice = []
    with open(doc, 'r') as file:
        for line in file:
            # Supprimer les espaces inutiles et diviser la ligne en une liste d'entiers
            ligne_entiers = list(map(int, line.strip().split()))
            matrice.append(ligne_entiers)
    return matrice

#2
def afficher_matrice(matrice):
    N = len(matrice)  # Longueur de la première ligne de la matrice
    
    tableau = [[0] * (N+3) for i in range(N+3)]
    tableau[0][0] = ' '
    i =0
    for i in range(1,N + 3):    
        tableau[0][i] = str(i-1) if i> 0 else ''
    
    for i in range(1, N + 3): #remplir la ligne du sommet ficitf alpha avec des *
        tableau[1][i] = "*" 
    tableau[1][-1] = "*"

    for i, ligne in enumerate(matrice, start=2):
        tableau[i][0] = ligne[0]
        for element in matrice: #remplir notre matrice avec les durée en fonction des index donnés (tâche, contrainte), le tout à partir du doc.txt
             for i in range(2,20):
                if  element[i:] != [] :
                    tableau[element[i]+1][element[0]+1] = element[1]

        for i in range (2,N+2) : #remplir notre matrice avec des * à la, place de 0
            for j in range(1,N+3) :
                if tableau[i][j] == 0:
                    tableau[i][j] = "*"
        
        tableau[N+2][0] = N+1 #donner la valeur de N+1 au sommet fictif oméga
        for i in range(1, N + 3): #remplir la ligne du sommet ficitf oméga avec des *
            tableau[N+2][i] = "*"

    #afficher notre matrice
    i=0
    for ligne in tableau: 
        j=0
        for element in ligne:
            if element == "0" and j==0: #décaler la première ligne
                print(" ", end=" ")
            elif j == 1 and i<=10: #décaler les lignes suivantes tant que leur premier chiffre ne comporte pas une dizaine
                print("", end=" ")
            elif j>10 and i !=0: #décaler les chiffres des colonnes dont l'index est supérieu à 10 (cela revient donc à décaler les colonnes lorsque la valeur de la tâche est >= 10)
                print("", end=" ")
            print(element, end=" ") #afficher les éléments de notre matrice
            j=j+1
        i=i+1
        print()
    return tableau
    
    
#3 
def verif_matrice(tableau, matrice2):
    N = len(tableau) #Nous prenons la taille de notre matrice
    a=1
    i=1
    c=0
    
    while i != N: #Nous allons faire N itérations
        for j in range (1,N):
            if tableau[j][i] == "*" and a==1: #vérifie que les cases de la colonne sont = *
                a=1 #si a = 1 cela signifie que jusqu'à présent les cases de la colonne sont = *
        
            else :
                a=0 #si a=0 cela signifie qu'au moins une case de la colonne qui est en train d'être analysée comporte une durée
            

        if a == 1: #se déclenche si notre colonne ne comporte aucune durée (comporte que des *)
            for b in range(i,N-1): 
                for k in range (0,N):
                    tableau[k][b] = tableau[k][b+1] #grâce aux boucles, toutes les colonnes à partir de celle à supprimée, vont être décalée à gauche ce qui va ainsi supprimer la colonne qui ne comporte aucune durée
            for l in range (N):
                tableau[l][N-1] = "" #permet de supprimer la dernière colonne qui est ainsi en doublon
            for b in range(i,N-1):  
                tableau[b]=tableau[b+1]#grâce aux boucles, toutes les lignes à partir de celle à supprimée, vont être décalée vers le haut ce qui va ainsi supprimer la ligne correspondant à la colonne qui ne comporte aucune durée
            tableau[N-1] ="" #permet de supprimer la dernière ligne qui est ainsi en doublon
            i=1
            N=N-1   
        else:
            a=1
            i+=1

    if N == 1 and arc_verif(matrice2) == True: #si N=1 cela signifie que notre matrice à subis N-1 suppression et par conséquent qu'il ne reste plus aucun élément dans cette dernière, ainsi il n'y a pas de circuit et on appelle la fonction arc_verif pour voir si elle nepossède pas d'arc négatifs
        print("\nLa matrice ne comporte aucun circuit, ni arc négatif on peut donc faire un Graphe d'ordonnancement")
        print("Nous pouvons procéder au calcul des rangs :")
        rang = calc_rang(matrice2)
        dict = calc_calendrier__au_plus__tot(matrice2)
        dict2 = calc_calendrier_au__plus_tard(dict, matrice2)
        marge = marges(dict2, dict)
        chemin_critique(matrice2, marge, rang)
        
    else :
        print("\non ne peut pas faire un Graphe d'ordonnancement")   
        print("Nous ne pouvons donc pas procéder au calcul des rangs") 
                       
def arc_verif(matrice2): #fonction pour verifier les arcs négatifs
    
    for i in matrice2: #On regarde dans notre matrice du doc.txt si on a une durée négatif dans la colonne 1 
        if i[1] < 0:
            return False #Si on detecte 1 nombre négatife on retourne faux
                
    return True

def trouver_premiere_cle_vide(dictionnaire):
    for cle, valeur in dictionnaire.items():
        if valeur == None:
            return cle
    return None 
#4
def calc_rang(matrice): #fonction pour calculer le rang
    N = len(matrice)
    
    dico={}
    dico[0] = 0 #On ajoute le rang 0 pour notre tâche fictive alpha
    for i in range(1, N+1): #On parcourt notre graphe afin d'ajouter le rang 1 aux racines
        temp = matrice[i-1][2:] #On ajoute les predecesseurs de notre tâche dans une variable temporaire
        if not temp: #S'il n'y a pas de predecesseurs, le rang est de 1
            dico[i] = 1
        else: #Sinon, le rang sera calculé par la suite, le rang n'est pas encore déclaré
            dico[i] = None

    has_changed = True
    while has_changed:
        has_changed = False
        for i in range(1, N + 1):
            if dico[i] is None:
                temp = matrice[i - 1][2:]
                if all(dico[j] is not None for j in temp):
                    dico[i] = max(dico[j] for j in temp) + 1
                    has_changed = True
    
    dico[N+1] = max(dico.values())+1
   
    for cle, valeur in dico.items():
        print(f"Tache: {cle}, Rang : {valeur}")
    
    return dico

#5
def calc_calendrier__au_plus__tot(matrice): #fonction pour calculer le calandrier au plus tot
    N = len(matrice)
    dico = {}
    dico[0]=0
    # Étape 1: Initialisation des tâches sans prédécesseurs
    for i in range(1, N + 1):
        temp = matrice[i - 1][2:]
        if not temp:
            dico[i] = 0
        else:
            dico[i] = None
    
    # Étape 2: Calcul des dates au plus tôt pour les autres tâches
    has_changed = True
    while has_changed:
        has_changed = False
        for i in range(1, N + 1):
            if i not in dico or dico[i] is None:
                temp = matrice[i - 1][2:]
                if all(dico[j] is not None for j in temp):
                    dico[i] = max(dico[j] + int(matrice[j - 1][1]) for j in temp)
                    has_changed = True
    
    # Trouver la tâche avec la date au plus tot maximale après la tâche oméga
    taches_max = []

    # Parcourir le dictionnaire et ajouter les clés à la liste si la valeur est égale à valeur_cible
    succ = False
    for i in range(1,N+1):
        for j in range(N):
            if i in matrice[j][2:]:
                succ = True
        if succ == False:
            taches_max.append(i)
        else:
            succ = False

    for t in range(len(taches_max)):
        taches_max[t] = dico[taches_max[t]] + matrice[taches_max[t]-1][1]
        
    # Trouver la date de fin maximale
    dico[N+1] = max(taches_max)
    
    # Affichage du calendrier au plus tôt
    print("\nCalendrier plus tôt")
    for cle, valeur in dico.items():
        print(f"Tache: {cle}, Date au plus tôt : {valeur}")

    return dico

def calc_calendrier_au__plus_tard(cal__tot, matrice):
    N = len(matrice)
    dico = {}
    
    for i in range(N+1):
        dico[i] = None
    dico[0] = 0   
    dico[N+1] = cal__tot[N+1]

    # Trouver la tâche avec la date au plus tot maximale après la tâche oméga
    taches_max = []

    # Parcourir le dictionnaire et ajouter les clés à la liste si la valeur est égale à valeur_cible
    succ = False
    for i in range(1,N+1):
        for j in range(N):
            if i in matrice[j][2:]:
                succ = True
        if succ == False:
            taches_max.append(i)
        else:
            succ = False
    
    temp = []
    for element in taches_max:
        temp.append(element)
    
    for l in taches_max:
        dico[l] = dico[N+1] - matrice[l-1][1]
        if len(matrice[l-1]) > 2:
            temp.append(matrice[l-1])
        temp.remove(l)
    
    while temp != []:
        for k in temp:
            preds = []
            for i in k[2:]:  
                preds.append(i)
            
            for element in preds:
                if (dico[element] is None or dico[k[0]] - matrice[element-1][1] < dico[element]):
                    dico[element] = dico[k[0]] - matrice[element-1][1]
                    temp.append(matrice[element-1])
            
             
                    
            temp.remove(k)
                
            
        
    # Affichage du calendrier au plus tôt
    print("\nCalendrier plus tard")
    for cle, valeur in dico.items():
        print(f"Tache: {cle}, Date au plus tard : {valeur}")

    return dico

def marges(cal__tard, cal_tot):
    N = len(cal__tard)
    dico = {}

    for i in range(N):
        dico[i] = cal__tard[i] - cal_tot[i]
    
    # Affichage du calendrier au plus tôt
    print("\nMarges totales")
    for cle, valeur in dico.items():
        print(f"Tache: {cle}, Marge : {valeur}")
    
    return dico
 
def get_successeurs(matrice):
    N = len(matrice)
    dico = {}

    succ = []
    for j in range(1, N + 1):
        if not matrice[j - 1][2:]:
            succ.append(j)
    dico[0] = succ

    for i in range(1, N+1):
        succ = []
        for j in range(1, N+1):
            if i in matrice[j-1][2:]:
                succ.append(j)
        if succ ==  []:
            succ.append(N+1)
        dico[i] = succ
        
    return dico

def chemin_critique(matrice, marges, rang):
    N = len(matrice)
    succ = get_successeurs(matrice)
    marge = []

    rang_max = max(rang.values())

    chemins_critiques = []

    for cle, valeur in marges.items():
        if valeur == 0:
            marge.append(cle)
    
    entrees = []
    for j in range(1, N + 1):
        if not matrice[j - 1][2:] and j in marges:
            entrees.append(j)
    
    for i in entrees:
        tmp = []
        tmp.append(0)
        tmp.append(i)
        chemins_critiques.append(tmp)

    for element in chemins_critiques:
        while rang[element[-1]] + 1 != rang_max:
            if len(succ[element[-1]]) == 1 and marges[succ[element[-1]][0]] == 0:
                element.append(succ[element[-1]][0])
            else:
                chemins_differents = []
                for i in succ[element[-1]]:
                    if marges[i] == 0:
                        chemins_differents = list(element)
                        chemins_differents.append(i)
                        chemins_critiques.append(chemins_differents)
                break

        if rang[element[-1]] + 1 == rang_max:
            element.append(N+1)
    
    index = []
    for items in chemins_critiques:
        if items[-1] != N+1:
            index.append(items)

    for i in index:
        chemins_critiques.remove(i)

    print("\nVoici le(s) chemin(s) critiques de ce graphe :") #affichage chemin critique
    for i in chemins_critiques:
        for j in range(len(i)-1):
            print(i[j],end=" ")
            print("-->", end=" ")
        print(f"{i[j+1]}\n")
    
def main():
        for i in range(1, 15):
            nom_fichier = f"tables/table {i}.txt"
            print(nom_fichier)
            matrice = lire_fichier(nom_fichier)
            matrice2 = lire_fichier(nom_fichier)
            tab = afficher_matrice(matrice)
            verif_matrice(tab,matrice2)    
        
if __name__ == "__main__":
    main()