import Outils.OutilsPrincipaux as outils
from pprint import pprint




text=outils.recuperationArbreText("./../XMLSources/List_of_serial_killers_by_country.xml")
for sent in outils.formatage(text):
# for sent in outils.sentTest(5):
    #formatage de la phrase sent
    format=outils.formatage(sent)

    #pour les phrases formaté
    for sentFormat in format:
        #preProcess (tokened,tagged)
        preProc = outils.preProcess(sentFormat)
        #creation d'un arbre de la phrase tagged
        tree = outils.chunker2Tree(preProc)
        # pprint(tree)
        # tree = outils.chunker2TreePattern(preProc)
        # pprint(tree)
        # pprint(tree)

        #creation d'un arbre taggé avec IOB
        iob = outils.iobTaggSent(tree)
        # pprint(tree)


        Relation=outils.creatRelation(tree)

        # print(Relation)

        # outils.recuperateurAfficheurRelation(Relation,tree)
        outils.filtreRelDependance(tree)