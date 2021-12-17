from calculate_affinity import main
import statistics

PVAL = 0.1
ID = "elevebf12"

def normalize(vect):
    for k,v in vect.items():
        vect[k] = v/abs(max(vect.values()))


def algo(ID, p):
    hexads, motivations = main(ID,p)
    if [*hexads.keys()][0] == [*motivations.keys()][0]:
        return [*hexads.keys()][0]

    normalize(hexads)
    normalize(motivations)

    maxV = -30000000000
    recommande = None
    for k,v in hexads.items():
        tmp = statistics.mean([v,motivations[k]])
        if tmp >= maxV:
            maxV = tmp
            recommande = k
    return recommande

if __name__ == "__main__":
    reco = algo(ID,PVAL)
    print(f"Recommendation d'élément de jeu pour {ID} : {reco}")



