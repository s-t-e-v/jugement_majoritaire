from random import randint

def vote(liste_candidats, nb_electeurs):
    "Collecte les votes"

    nb_candid = len(liste_candidats)

    # tableau candidat
    tab_vote = [ [0]*7 for _ in range(nb_candid) ]

    print(tab_vote)

    # Vote

    for e in range(nb_electeurs):
        print(f"\n==== Electeur #{e+1} ====")
        for c in range(nb_candid):
            print("** Vote pour le candidat " + liste_candidats[c] + " **")
            print("[0] Excellent    [1] Très bien    [2] Bien    [3] Assez bien    [4] Passable    [5] Insuffisant    [6] A rejeter")
            vote = int(input("> "))

            tab_vote[c][vote] += 1

    return tab_vote

def generation_vote(liste_candidats, nb_electeurs, save=False):

    nb_candid = len(liste_candidats)

    # tableau candidat
    tab_vote = [ [0]*7 for _ in range(nb_candid) ]
 
    for c in range(nb_candid):
        max_electeur = randint(0, nb_electeurs)
        for m in range(0, 5):
            nb_vote = randint(0, max_electeur)
            tab_vote[c][m] = nb_vote
            max_electeur -= nb_vote

        tab_vote[c][6] = nb_electeurs - sum(tab_vote[c])
        tab_vote[c][0:0] = [liste_candidats[c]]

    # save
    if save:
        f = open("tab_vote.csv", "w")

        for data in tab_vote:
            for d in data:
                f.write(d)
                f.write(";")
            f.write("\n")
        
        f.close()

    return tab_vote

def charger_tab_vote():

    f = open("tab_vote.csv","r")

    tab_vote = []

    i = 0
    while 1:

        l = f.readline()

        if not l:
            break

        j = -1
        tab_vote.append([])
        for data in l.split(";"):
            if j < 0:
                tab_vote[i].append(data)
            else:
                tab_vote[i].append(int(data))

            j += 1

        i += 1

    return tab_vote

def estEntier(nb):

    return int(nb) == nb

def median_vote(tab_vote):
    "Retourne la note médiane pour chaque candidat"

    nb_elec = sum(tab_vote[0][1:])
    rang_median = (nb_elec + 1) / 2

    list_mediane = []

    for data in tab_vote:

        vote = data[1:]

        i = 0
        r = vote[i]

        while  1:

            if r + vote[i+1] > rang_median:
                break

            i += 1
            r += vote[i]

        if estEntier(rang_median):
            if r >= rang_median:
                list_mediane.append(i)
            else:
                list_mediane.append(i+1)
        else:
            if r + 1 > rang_median:
                list_mediane.append((i+(i+1))/2)
            else:
                list_mediane.append(i+1)

    return list_mediane

def indices(list, elt):

    i = 0

    list_idx = []
    for l in list:
        if l == elt:
            list_idx.append(i)
        i +=1

    return list_idx

def departage(tab_vote, list_mediane):


    idx_gagnant = 0
    tab_vote_gagnants = []
    

    # selection des gagnants
    i = 0
    min_mediane = min(list_mediane)
    for t, m in zip(tab_vote, list_mediane):

        if m == min_mediane:
            tab_vote_gagnants.append([t[1:], i])

        i += 1

    # Algo departage
    if len(tab_vote_gagnants) == 1: # si un unique candidat avec mention majoritaire la plus haute
        idx_gagnant = tab_vote_gagnants[0][1]
    else:
        # departage ex aeqo
        sp = 1
        so = 1
        while 1:


            # Calcul de la propor de partisans et d'opposants pour chaque candidats pour la mention sup et inferieur respectivement
            list_propr_oppos = []
            list_propr_partis = []
            for t in tab_vote_gagnants:
                propr_oppos = 0
                propr_partis = 0
                for o in range(min_mediane+so, 7):
                    
                    propr_oppos += t[0][o]
                list_propr_oppos.append(propr_oppos)

                for p in range(min_mediane-sp, -1, - 1):
                    
                    propr_partis += t[0][p]
                list_propr_partis.append(propr_partis)


            # departage avec max partisans / max opposants

            max_partis = max(list_propr_partis)
            max_oppos = max(list_propr_oppos)
            

            idx_g = indices(list_propr_partis, max_partis)
            idx_l = indices(list_propr_oppos, max_oppos)

            print(f"proportion partisans +{sp} :", list_propr_partis)
            print(f"proportion opposants +{so} :", list_propr_oppos)
            print("")
            print("idx partisans max", idx_g)
            print("idx opposants max", idx_l)
            print("")

            if max_partis > max_oppos:
                if len(idx_g) == 1:
                    i = idx_g[0]
                    idx_gagnant = tab_vote_gagnants[i][1]
                    break
                else:
                    sp += 1
                    suppr = False
            else:
                suppr = False
                for l in idx_l:
                    if l not in idx_g:
                        del tab_vote_gagnants[l]
                        suppr = True

            if not suppr:
                so += 1

            # if min_mediane + so >= len(tab_vote[0][1:]):
            #     break
            # elif len(idx_g) == 1:

            #     i = idx_g[0]

            #     if i not in idx_l or len(tab_vote_gagnants) == 1:
            #         idx_gagnant = tab_vote_gagnants[i][1]
            #         break
                
            #     so += 1
            # else: # suppression des perdants: ceux avec la même proportion max d'opposants et ne faisant pas partie des gagnants avec la proportion supérieur de partisant la plus haute
            #     suppr = False
            #     for l in idx_l:
            #         if len(idx_l) != len(tab_vote_gagnants):
            #             if l not in idx_g or (len(idx_g) == len(tab_vote_gagnants) and l in idx_g):
            #                 del tab_vote_gagnants[l]
            #                 suppr = True

                # if min_mediane - sp < 1:
                #     if not suppr:
                #         so += 1
                # else:
                #     sp += 1


    return idx_gagnant


# liste candidat
liste_candidats = ["Balou",
                   "Hermione",
                   "Chuck Norris",
                   "Elsa",
                   "Gandalf",
                   "Beyoncé"]


# Nombre d'électeurs
nb_electeurs = 25

# vote
# tab_vote = charger_tab_vote()
tab_vote = generation_vote(liste_candidats, nb_electeurs)

print(tab_vote)

# médianes
list_medianes = median_vote(tab_vote)

print(list_medianes)

# départage

idx_gagnant = departage(tab_vote, list_medianes)

# Affichage gagnant

print("Le vainqueur par jugement majoritaire est:", tab_vote[idx_gagnant][0])