#begin programme basé sur le livre nltk
import nltk
import nltk, re, pprint
import os
import string
import spacy
import xml.etree.ElementTree as ET

from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

from nltk import ne_chunk, pos_tag
from nltk.tree import *

from collections import defaultdict

from spacy import displacy





def deb():
    #import de mon texte
    txt=open("List_of_serial_killers_by_country.xml","r").read()

    #tokenization
    tokens=nltk.word_tokenize(txt)
    text=nltk.Text(tokens)

#recherche du radical (stemmer)
def radical():
    #Porter est le plus utilisé
    #The Porter Stemmer is a good choice if you are indexing some texts and want to support search using alternative forms of words
    porter = nltk.PorterStemmer()
    #Lancaster est le plus dur mais il fait des erreurs
    lancaster = nltk.LancasterStemmer()

    tokenPorter = [porter.stem(t) for t in tokens]
    tokenLancaster = [lancaster.stem(t) for t in tokens]

#lemmatisation
#The WordNet lemmatizer only removes affixes if the resulting word is in its dictionary.
#This additional checking process makes the lemmatizer slower than the above stemmers.
#Notice that it doesn't handle lying, but it converts women to woman.

#The WordNet lemmatizer is a good choice if you want to compile the vocabulary of some texts and want a list of valid lemmas (or lexicon headwords).
def lemma():
    wnl = nltk.WordNetLemmatizer()
    print([wnl.lemmatize(t) for t in tokens])

#regular expression tokenizer regex
def regularExp():
    pattern = r'''(?x)     # set flag to allow verbose regexps
    (?:[A-Z]\.)+       # abbreviations, e.g. U.S.A.
    | \w+(?:-\w+)*       # words with optional internal hyphens
    | \$?\d+(?:\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
    | \.\.\.             # ellipsis
    | [][.,;"'?():-_`]   # these are separate tokens; includes ], [
    '''
    print(nltk.regexp_tokenize(txt, pattern))

#on va pouvoir tag, enfin ptain
def tag():
    tagged=nltk.pos_tag(text)
    print(tagged)


def truc():
    txt=open("List_of_serial_killers_by_country.xml","r").read()
    print(len(txt),txt)
    print(word_tokenize(txt))
    stem = PorterStemmer()
    lem = WordNetLemmatizer()
    pos_tag(word_tokenize(txt))
    print(lemmatize_sentence(txt))
    stop_words = stopwords.words('english')
    len(stop_words)
    # token = lemmatizer.lemmatize(token, pos)

def lemmatize_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(word_tokenize(sentence)):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence


def toy():
    nlp = spacy.load('en')
    stop_words = stopwords.words('english')

    sent = "In this article, we see how Emmet Brown, a young man living near State Street, killed a man in San Franciso, the great city, yersteday."
    sent1 = sent.translate(str.maketrans('', '', string.punctuation))
    sentModif = lemmatize_sentence(sent1)

    filtered_sentence = [w for w in sentModif if not w in stop_words]

    sent2=' '.join(filtered_sentence)
    #on va sortir le nom principal






            # print(token.text)
    # for np in doc.noun_chunks:
    #     print(np.text)
    #     if(token.head.lemma_=="kill"):
    #         print("t")


    #
    # # print(filtered_sentence)
    #
    # chunked = ne_chunk(pos_tag(filtered_sentence))
    # # chunked.draw()
    #
    # named_entities = defaultdict(list)
    #
    # for node in chunked:
    #     # Check if node is a Tree
    #     # If not a tree, ignore
    #     if type(node) is nltk.tree.Tree:
    #         # Get the type of entity
    #         label = node.label()
    #         entity = node[0][0]
    #         named_entities[label].append(entity)
    #
    # print(named_entities)
    print()

def list():
    listAss=[]
    for ss in wn.synsets('kill'):
        killer = wn.synset(ss.name())
        # print(killer)
        if killer.hyponyms()!=[]:
            for a in killer.hyponyms():
                # print("-",a)
                listAss.append(a.name())
                for synset in wn.synsets(a.name().split('.')[0]):
                    for lemma in synset.lemmas():
                        # print("-:-",lemma)
                        listAss.append(lemma.name())
    return listAss


#lemmatisation
#The WordNet lemmatizer only removes affixes if the resulting word is in its dictionary.
#This additional checking process makes the lemmatizer slower than the above stemmers.
#Notice that it doesn't handle lying, but it converts women to woman.

#The WordNet lemmatizer is a good choice if you want to compile the vocabulary of some texts and want a list of valid lemmas (or lexicon headwords).
def lemma():

    #chercher le verbe
    #verifier qu'il est du champ lexical de tuer
    #trouver son nominal (nsubj) qui est le syntactic subjet et le proto-agent de la clause
    #Un sujet nominal (nsubj) est un nominal qui est le sujet syntaxique et le proto-agent d'une clause.
    #trouver son prénom ou son pseudo
    wnl = nltk.WordNetLemmatizer()
    print([wnl.lemmatize(t) for t in tokens])


def top():
    nlp = spacy.load('en')

    # find()

    sent = "In this article, we see how Emmet Brown, a young man living near State Street, killed a man in San Franciso, the great city, yersteday."
    doc=nlp(sent)

    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # Find named entities, phrases and concepts
    for entity in doc.ents:
        print(entity.text, entity.label_)

    # for ent in doc.ents:
    #     print(ent, ent.label_)
    # for ent in doc:
    #     print(ent)

    #trouver le root
    # rootKill=wn.synsets('kill',"v")[0].root_hypernyms()
    print(rootKill)

def find(sentT):

    # sent = "In this article, we see how Emmet Brown, a young man living near State Street, killed a man in San Franciso, the great city, yersteday."
    # for sent in nltk.sent_tokenize(sentT):

    #on parse la phrase
    # doc = nlp(sentT)
    # displacy.serve(doc, style="dep")
    # displacy.serve(doc, style="ent")

    s=nlp(sentT).sents
    listRes=[]
    for sent in s:
        # displacy.serve(sent, style="dep")
        for token in sent:
            if(token.dep_=="relcl" or token.dep_=="compound" or token.dep_=="compound" or token.dep_=="dobj"):
                # print("------------")
                a=0
            if(token.dep_=="relcl"):
                listRes.append(token.orth_)
                # print(token.dep_," : ",token.orth_)
            if(token.dep_=="compound"):
                listRes.append(token.orth_)
                listRes.append(token.head.lemma_)
                # print(token.dep_," : ",token.orth_," : ",token.head)
            if token.pos_ == "VERB":
                if len(wn.synsets(token.lemma_,"v"))>0 :
                    if rootMoveV == wn.synsets(token.lemma_,"v")[0].root_hypernyms() or rootKillV == wn.synsets(token.lemma_,"v")[0].root_hypernyms():
                        listRes.append(token.lemma_)
                        # print(token)


            # if(token.dep_=="appos"):
            #     print(token.dep_," : ",token.orth_," : ",token.head," : ",token)
            if(token.dep_=="pobj"):
                listRes.append(token.orth_)
                # print(token.dep_," : ",token.orth_)
            if(token.dep_=="amod"):
                listRes.append(token.orth_)
                listRes.append(token.head.lemma_)
                # print(token.dep_," : ",token.orth_," : ",token.head)
            if(token.dep_=="dobj"):
                listRes.append(token.orth_)
                # print(token.dep_," : ",token.orth_)
            if(token.dep_=="nummod"):
                listRes.append(token.orth_)
                # print(token.dep_," : ",token.orth_)

        for entity in sent.ents:
            # if len(wn.synsets(entity.lemma_,"n"))>0 :

            if(entity.label_ == "PERSON"):
                print("+++",entity.text, entity.label_)
            # if(entity.label_ == "GPE"):
                # print(entity.text, entity.label_)

    #tant qu'il reste des chose a trouver

    #on analyse les différente phrase de sentT
    # chaque phrase est nlpisé
    # on cherche d'abord le verbe de tuerie
    # on recupère les verbes de la phrase
    #on prend leur relation
    # puis on analyse tout les mots et chercher à recrer le texte utile

    listDejaAp=[]
    for s in listRes:
        if s not in listDejaAp:
            listDejaAp.append(s)
        elif len(wn.synsets(s,"v"))>0 and rootKillV == wn.synsets(s,"v")[0].root_hypernyms() and s in listDejaAp:
            listDejaAp.append("and")
    #analyse du texte pour supprimer les doublons
    #remplace les autres killed par and
    #supprime les doublons de nom

    listRes = listDejaAp


    #il reste a analyser les nom propre avec les verbe pour ne ressortir que le necessaire
    #qui à tué, quand et ou + 50 assasin

    #constitué un corpus
    #segmenté les données
    # appliqué un pos tagger
    # reconnu les entités nommés
    # identifié les indices temporels
    #

    print(' '.join(str(e) for e in listRes))

    #trouver qqun qui aurait tué
    # for X in doc:
    #     if X.pos_=="VERB":
    #         print(stemmer.stem(X.text)))
            # if stemmer.stem(X.text) in listVocab:
            #     print(stemmer.stem(X.text),X.pos_)






def tycoon(sentT):

    #on recupere le text et on la nlpise en phrase
    s=nlp(sentT).sents
    # displacy.serve(nlp(sentT).sents, style="dep")
    listRes=[]
    #pour chaque phrase, on cherche les personne et leur qualificatif (role,pseudo,...) et si un verbe leur fait reference
    listPers=[]
    listNoun=[]
    listVerb=[]

    for sent in s:
        # displacy.serve(sent, style="dep")
        # displacy.serve(sent, style="ent")
        #on recherche toute les entités person de la phrase
        for entity in sent.ents:
            if(entity.label_ == "PERSON"):
                #on les ajoute à note map improvisé
                listPers.append(entity.text.split())
                listVerb.insert(len(listPers)-1,[])
                listNoun.insert(len(listPers)-1,[])

        #recuperation des token lié au nom
        for token in sent:
            for
            if token.lemma_==
        #pour tout les nom, on cherche s'il sont des qualificatif relié aux person
        #on va aussi trouver les verbes directement ou indirectement relier au nom/person
        passe=False
        #tant qu'on fait pas un passage a vide on boucle sur les nom de la phrase #passe/compteTrouver
        while not passe:
            compteTrouver=0
            for token in sent:
                if token.pos_=="NOUN":
                    #pour chaque assemblage de la map improvisé person, nom, verbe
                    for i,list in enumerate(listPers):
                        #si on trouve un nouveau (qui n'a jamais été trouvé) token relié, directement ou par un nom qualificateur, a la personne courante
                        if(token.head in list or token.head in listNoun[i]) and token not in listNoun[i]:
                            compteTrouver+=1 #alors on incremente le compte de passage pour préciser qu'il n'est pas a vide
                            listNoun[i].append(token) #on ajoute le token a la map improvisé
                        #si on trouve un nouveau (qui n'a jamais été trouvé) token relié, directement ou non, a un verbe trouvé
                        if(token.head in listVerb[i]) and token not in listNoun[i]:
                            listNoun[i].append(token)


            for token in sent:
                if token.pos_ == "VERB":
                    #pour la taille de la map
                    for i in range(0,len(listPers)):
                        #on cherche l'hypernyms du nom (kill,move,think) afin de ne pas prendre des verbe inutile
                        hyp=wn.synsets(token,"v")[0].root_hypernyms()
                        if rootMoveV == hyp or rootKillV == hyp or rootSuspectV== hyp:
                            print("Verb :",token,token.pos_,token.dep_,token.head.head,token.orth_)
                            #si le verbe correspond a une personne ou nom relié a une personne alors on l'ajoute dans la map a l'index de la personne
                            if (token.head in listPers[i] or token.head in listNoun[i] or token.head.head in listVerb[i] or token.dep_=="ROOT" ) and token not in listVerb[i] :
                                hyp=wn.synsets(token,"v")[0].root_hypernyms()
                                listVerb[i].append(token)
                                compteTrouver+=1
                            # advcl Adverb Clause Modifier group of words that functions as an adverb.
                            # xcomp open clausal complément

            if compteTrouver==0:
                passe=True #si on a fait un passage a vide alors on arrete la boucle

        [print(listPers[i],listNoun[i],listVerb[i]) for i in range(0,len(listPers))]








nlp = spacy.load('en')
stemmer = PorterStemmer()
rootKillV=wn.synsets('kill',"v")[0].root_hypernyms()
rootMoveV=wn.synsets('push',"v")[0].root_hypernyms()
rootSuspectV=wn.synsets('suspect',"v")[0].root_hypernyms()

tree = ET.parse("List_of_serial_killers_by_country.xml")
root=tree.getroot()

strRoot=ET.tostring(root,encoding='unicode',method='text')

# lCharRoot=list(strRoot)
# liststrRoot=strRoot.split("|-")

strRoot=strRoot.replace("[[", "").replace("]]","")
liststrRoot=strRoot.split("*")

# liststrRoot=['*Abdullah Shah: killed at least twenty travelers on the road from Kabul to Jalalabad serving under Zardad Khan; also killed his wife; executed on 20 April 2004.&lt;ref name="BBC"&gt;{{cite web |url=http://news.bbc.co.uk/2/hi/south_asia/3662935.stm |title=Former Afghan commander executed |date=27 April 2004 |website=[[BBC News Online|BBC News]] |accessdate=20 August 2009}}&lt;/ref&gt;']
liststrRoot=["*John Baughman: former American police officer who pushed his second wife from the roof of the Royal Antiguan Hotel in 1995; suspected of killing a close friend and first wife back in the USA; committed suicide in 2000.&lt;ref&gt;{{cite news |url=https://www.chicagotribune.com/news/ct-xpm-2000-06-02-0006020165-story.html |title=Family's Built-Up Pain Eased By Hanging In Antigua |first1=Marla |last1=Donato |first2=David |last2=Heinzmann |date=June 2, 2000 |newspaper=[[Chicago Tribune |access-date=24 November 2019}}&lt;/ref&gt;"]
# liststrRoot=['*Marcelo Antelo: also known as "The San La Muerte Killer"; drug addict who killed at least four people between February and August 2010, allegedly in the name of a pagan saint; sentenced to life imprisonment.&lt;ref&gt;{{cite news |url=https://www.clarin.com/crimenes/largo-prontuario-Marcelo-Antelo_0_SyXXJx2DXg.html |title=El largo prontuario de Marcelo Antelo |trans-title=The long record of Marcelo Antelo |first1=Horacio |last1=Ezcurra |first2=Rodrigo |last2=Ezcurra |first3=Marcelo |last3=Antelo |lastauthoramp=yes |date=September 9, 2012 |newspaper=[[Clarín (Argentine newspaper)|Clarín]] |language=es |access-date=24 November 2019 |url-status=live |archive-url=https://archive.today/20190910080104/https://www.clarin.com/crimenes/largo-prontuario-Marcelo-Antelo_0_SyXXJx2DXg.html |archivedate=September 10, 2019}}&lt;/ref&gt;']
# liststrRoot=['*[[Cayetano Domingo Grossi]]: the first serial killer in Argentine history; Italian immigrant who murdered five of his newborn children between 1896 and 1898; executed 1900.&lt;ref&gt;{{cite web |url=http://www.acciontv.com.ar/soca/polis/enero13/grosi.htm |title=El fusilamiento de Cayetano Grossi (1900) |trans-title=The execution of Cayetano Grossi (1900) |website=AcciónTV |language=es |access-date=12 November 2015}}&lt;/ref&gt;']

for sent in liststrRoot:
    continueF=True
    wordToken=nltk.word_tokenize(sent)
    sort=[]
    for i,w in enumerate(wordToken):



        if w=="ref":
            debut=i-1
            continueF=False

        if continueF == True:
            sort.append(w)

        if w=="/ref":
            fin=i+1
            continueF=True


    # stop_words = stopwords.words('english')

    # print(wordToken[debut])
    #suppression des ref du sent

    # sort = [w for w in sort if not w in stop_words]
    sent=' '.join(str(e) for e in sort)

    # print(nltk.sent_tokenize(sent))
    print("------------------------------------------------------------")
    # find(sent)
    tycoon(sent)
