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

def charger_tab_vote():

    f = open("tab_vote.csv","r")

    tab_vote = []

    i = 0
    while 1:

        l = f.readline()

        if not l:
            break

        j = -1
        tab_vote.append(["", []])
        for data in l.split(";"):
            if j < 0:
                tab_vote[i][0] = data
            else:
                tab_vote[i][1] += [j] * int(data)

            j += 1

        i += 1

    return tab_vote

def estEntier(nb):

    return int(nb) == nb

def median_vote(tab_vote):
    "Retourne la note médiane pour chaque candidat"

    nb_elec = len(tab_vote[0][1])

    rang_median = (nb_elec + 1) / 2

    list_mediane = []

    if estEntier(rang_median):
        rang_median = int(rang_median) # convertion de float -> int

        for data in tab_vote:
            votes = data[1]
            mediane = votes[rang_median - 1]
            proportion = votes.count(mediane)/nb_elec
            list_mediane.append([mediane, proportion])

    else:
        rang_median = int(rang_median) # convertion de float -> int

        for data in tab_vote:
            votes = data[1]
            mediane = (votes[rang_median - 1] + votes[rang_median - 1 + 1])/2
            proportion = votes.count(mediane)/nb_elec
            list_mediane.append([mediane, proportion])

    return list_mediane


# liste candidat
liste_candidats = ["Balou",
                   "Hermione",
                   "Chuck Norris",
                   "Elsa",
                   "Gandalf",
                   "Beyoncé"]


# Nombre d'électeurs
nb_electeurs = 5

# vote
tab_vote = charger_tab_vote()

print(tab_vote)

# médianes
list_medianes = median_vote(tab_vote)

print(list_medianes)