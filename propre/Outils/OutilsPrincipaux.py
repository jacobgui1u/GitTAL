import nltk
import nltk, re, pprint
import os
import string
import xml.etree.ElementTree as ET

from nltk.grammar import DependencyGrammar
from nltk.parse import (DependencyGraph,ProjectiveDependencyParser,NonprojectiveDependencyParser,)
from nltk.sem import relextract

from nltk.tree import *
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.corpus import conll2002

from nltk import ne_chunk, pos_tag
from nltk.tree import *

from collections import defaultdict
from pprint import pprint


from nltk.tree import Tree
from nltk.grammar import Nonterminal
from nltk.sem.relextract import _join, list2sym
from collections import defaultdict
from nltk.sem.relextract import rtuple

import numpy as np

# import de la classe document
from Outils import document



# récuperation d'un fichier
def recuperationText(url):
    file = open(url, 'rb')
    lsortie = np.load(file)
    close(file)
    return lsortie

# récuperation du text d'un fichier en arbreXML
def recuperationArbreText(url):
    # récuperation de l'arbe xml
    tree = ET.parse(url)
    root=tree.getroot()
    # récuperation du texte
    strRoot=ET.tostring(root,encoding='unicode',method='text')
    return strRoot


# formatage du texte pour le rendre utilisable
def formatage(text):
    # mise en forme du texte
    liststrRoot = ""

    # mise en forme des noms des meurtriers pour les listes
    # voir si on peut recuperer le meurtirer comme ca
    strRoot = text.replace("[[", "").replace("]]","")

    # pour les listes
    liststrRoot = strRoot.split('*')
    sent = ' '.join(str(e) for e in liststrRoot)


    # suppresion des references pour ne garder que les texte
    liststrRoot = sent.split('===')
    listRes = []
    for sent in liststrRoot:
        continueF = True
        wordToken = nltk.word_tokenize(sent)
        sort = []
        for i, w in enumerate(wordToken):
            # on ignore la ponctuation
            if w.isalpha():
                if w == "ref":
                    debut = i-1
                    continueF = False

                if continueF is True:
                    sort.append(w)

                if w == "/ref":
                    fin = i+1
                    continueF = True
        sent = ' '.join(str(e) for e in sort)
        sent = sent.replace("*", "")
        listRes.append(sent)
    return listRes


# utilisation des phrases de test
def sentTest(para):
    strRootList = []
    if(para == 1):
        strRoot = '*Abdullah Shah: killed at least twenty travelers on the road from Kabul to Jalalabad serving under Zardad Khan; also killed his wife; executed on 20 April 2004.&lt;ref name="BBC"&gt;{{cite web |url=http://news.bbc.co.uk/2/hi/south_asia/3662935.stm |title=Former Afghan commander executed |date=27 April 2004 |website=[[BBC News Online|BBC News]] |accessdate=20 August 2009}}&lt;/ref&gt;'
        strRootList.append(strRoot)
    elif(para == 2):
        strRoot = "*John Baughman: former American police officer who pushed his second wife from the roof of the Royal Antiguan Hotel in 1995; suspected of killing a close friend and first wife back in the USA; committed suicide in 2000.&lt;ref&gt;{{cite news |url=https://www.chicagotribune.com/news/ct-xpm-2000-06-02-0006020165-story.html |title=Family's Built-Up Pain Eased By Hanging In Antigua |first1=Marla |last1=Donato |first2=David |last2=Heinzmann |date=June 2, 2000 |newspaper=[[Chicago Tribune |access-date=24 November 2019}}&lt;/ref&gt;"
        strRootList.append(strRoot)
    elif(para == 3):
        strRoot = '*Marcelo Antelo: also known as "The San La Muerte Killer"; drug addict who killed at least four people between February and August 2010, allegedly in the name of a pagan saint; sentenced to life imprisonment.&lt;ref&gt;{{cite news |url=https://www.clarin.com/crimenes/largo-prontuario-Marcelo-Antelo_0_SyXXJx2DXg.html |title=El largo prontuario de Marcelo Antelo |trans-title=The long record of Marcelo Antelo |first1=Horacio |last1=Ezcurra |first2=Rodrigo |last2=Ezcurra |first3=Marcelo |last3=Antelo |lastauthoramp=yes |date=September 9, 2012 |newspaper=[[Clarín (Argentine newspaper)|Clarín]] |language=es |access-date=24 November 2019 |url-status=live |archive-url=https://archive.today/20190910080104/https://www.clarin.com/crimenes/largo-prontuario-Marcelo-Antelo_0_SyXXJx2DXg.html |archivedate=September 10, 2019}}&lt;/ref&gt;'
        strRootList.append(strRoot)
    elif(para == 4):
        strRoot = '*[[Cayetano Domingo Grossi]]: the first serial killer in Argentine history; Italian immigrant who murdered five of his newborn children between 1896 and 1898; executed 1900.&lt;ref&gt;{{cite web |url=http://www.acciontv.com.ar/soca/polis/enero13/grosi.htm |title=El fusilamiento de Cayetano Grossi (1900) |trans-title=The execution of Cayetano Grossi (1900) |website=AcciónTV |language=es |access-date=12 November 2015}}&lt;/ref&gt;'
        strRootList.append(strRoot)
    elif(para == 5):
        strRoot = '[[John Balaban (serial killer)|John Balaban]]: also known as the "Romanian Maniac"; Romanian emigrant who murdered at least five people in France and Australia from 1948 to 1953, including his wife and her family; executed 1953.'
        strRootList.append(strRoot)

    return strRootList

# tokenisation et tagging, prend un string en parametre
def preProcess(text):
    tagged = []
    sentencesTokenized = nltk.sent_tokenize(text)
    wordTokenized = [nltk.word_tokenize(sent) for sent in sentencesTokenized]
    tagged = [nltk.pos_tag(sent) for sent in wordTokenized]
    if len(tagged) > 0:
        return tagged[0]


# création d'un arbre à partir du texte taggé
# utilisation d'un pattern pour trouver ce qu'on veut
def chunker2Tree(tagged):
    if type(tagged) != type(None):
        # reccuperation conlltags
        ne_tree = nltk.ne_chunk(tagged)
        # ne_tree = nltk.ne_chunk(tagged, binary=False)
        return ne_tree


def chunker2TreePattern(tagged):
    if type(tagged)!= type(None):
        pattern='''
        NP: {<DT>? <JJ>* <NN*>* <NNP>*} # NP
        NNS: {<NNS>* <NN>*}
        V: {<V.*>}    # Verb
        CD: {<CD>*}   #date
        '''

        cp = nltk.RegexpParser(pattern)
        cs = cp.parse(tagged)
        return res


# retourne un Inside-outside-beginning qui permet de connaitre le bloc dans le string
# prend un arbre en parametre
def iobTaggSent(block):
    if type(block)!=type(None):
        iob_tagged = nltk.tree2conlltags(block)
        return iob_tagged


# recuperateur des phrases iob taggé
def recuperateurBlockSent():
    phrase=[[]]
    i = 0
    for iob in iob_tagged:
        # print(iob)
        if len(iob) > 0:
            if iob[2] != "O":
                phrase[i].append(iob)
            else:
                if phrase[i] != []:
                    i += 1
                    phrase.append([])


# réécriture de la fonction semi_rel2redict
def semi_rel2reldict(pairs, window=5, trace=False):
    """
        Converts the pairs generated by ``tree2semi_rel`` into a 'reldict': a dictionary which
        stores information about the subject and object NEs plus the filler between them.
        Additionally, a left and right context of length =< window are captured (within
        a given input sentence).
        :param pairs: a pair of list(str) and ``Tree``, as generated by
        :param window: a threshold for the number of items to include in the left and right context
        :type window: int
        :return: 'relation' dictionaries whose keys are 'lcon', 'subjclass', 'subjtext', 'subjsym', 'filler', objclass', objtext', 'objsym' and 'rcon'
        :rtype: list(defaultdict)
    """
    result = []
    while len(pairs) >= 2:
        reldict = defaultdict(str)
        reldict['lcon'] = _join(pairs[0][0][-window:])
        reldict['subjclass'] = pairs[0][1].label()
        reldict['subjtext'] = _join(pairs[0][1].leaves())
        reldict['subjsym'] = list2sym(pairs[0][1].leaves())
        reldict['filler'] = _join(pairs[1][0])
        reldict['untagged_filler'] = _join(pairs[1][0], untag=True)
        reldict['objclass'] = pairs[1][1].label()
        reldict['objtext'] = _join(pairs[1][1].leaves())
        reldict['objsym'] = list2sym(pairs[1][1].leaves())
        reldict['rcon'] = []
        if trace:
            print("(%s(%s, %s)" % (reldict['untagged_filler'], reldict['subjclass'], reldict['objclass']))
        result.append(reldict)
        pairs = pairs[1:]
    return result


def toSemi():
    # print(relextract.tree2semi_rel(chunked))
    return 1


# createur des relations d'un text a partir d'un filtre relfilter
def creatRelation(tree):

    if type(tree) != type(None):
        pattern = re.compile(r'.*\bin\b(?!\b.+ing)')# (r'(ab)*')#(r'.*\bof\b.*')

        # sujet recherché
        subjclass = 'PERSON'
        objclass = 'ORGANIZATION'
        window = 5

        # print(semi_rel2reldict(relextract.tree2semi_rel(chunked)))
        reldicts = semi_rel2reldict(relextract.tree2semi_rel(tree))


        relfilter = lambda x: (x['subjclass'] == 'PERSON' or x['subjclass'] == "ORGANIZATION" or x['objclass'] == objclass)
        rels = list(filter(relfilter, reldicts))

        return rels


# recuperation des relation a afficher et usage d'un filtre
def recuperateurAfficheurRelation(reldicts, tree):
    for rel in reldicts:
        for k, v in sorted(rel.items()):
            print(k, '=>', v)  # doctest: +ELLIPSIS
            a = 1
        print('=' * 40)

        print("sujet text : ", rel['subjtext'])
        print("filler : ", rel['filler'])
        print("objet texte : ", rel['objtext'])
        print('=' * 40)




def filtreRelDependance(tree):
    if type(tree) != type(None):

        IN = re.compile('.*(kill(er|ed|ing)?|murder(er|ed)?|assassin(ated)?|convict(ed)?|push(ed|ing)?).*',re.DOTALL)
        IN = re.compile('.*.', re.DOTALL)

        lRes = []
        lRes.append([])
        for rel in nltk.sem.relextract.extract_rels('PERSON', 'GPE', tree, corpus='ace', pattern = IN):
            lRes[len(lRes)-1].append(rel)
        for rel in nltk.sem.relextract.extract_rels('PERSON', 'PERSON', tree,corpus='ace', pattern = IN):
            lRes[len(lRes)-1].append(rel)
        for rel in nltk.sem.relextract.extract_rels('PERSON', 'ORGANIZATION', tree,corpus='ace', pattern = IN):
            lRes[len(lRes)-1].append(rel)


        for relation in lRes:
            if relation != []:
                print("="*50)
                for rel in relation:
                    if rel != []:
                        # on test pour que le noom commence par la bonne lettre
                        if re.match(".*\[PER: '[a-zA-Z\s\S]*(E|B|J|D|B|L|O)[a-z]+.*",repr(nltk.sem.rtuple(rel))):
                            print("rel : ",nltk.sem.rtuple(rel))
                            print()
                            # print("Sentence : ",re.sub(r'/[^\s]+','',str(tree))) # On enlève les tags pour les entités non nommées
                print("="*50)

        # doc=document.doc()
        #
        # doc.headline=['foo']
        # doc.text=tree


def TesteurMot():
    rootKillV = wn.synsets('kill', "v")[0].root_hypernyms()
    rootMoveV = wn.synsets('push', "v")[0].root_hypernyms()
    rootSuspectV = wn.synsets('suspect', "v")[0].root_hypernyms()

def stemmPorter():
    # outils
    stemmer = PorterStemmer()
