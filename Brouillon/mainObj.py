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



rootKillV=wn.synsets('kill',"v")[0].root_hypernyms()
rootMoveV=wn.synsets('push',"v")[0].root_hypernyms()
rootSuspectV=wn.synsets('suspect',"v")[0].root_hypernyms()



def text_to_sents(text):
    return nltk.sent_tokenize(text)



def process_text_ner(text):
    """ Fonction qui permet d'identifier le type des mots et les entités nommées dans la phrase passée en paramètre. Cette fonction est à appeler une fois que du texte est extrait sous forme brute depuis le xml"""
    tokenized_text = nltk.word_tokenize(text)
    tokenized_text = [t for t in tokenized_text if t.isalpha()] #on se débarasse de la ponctuation
    wn = nltk.WordNetLemmatizer()
    lemms = [ wn.lemmatize(w) for w in tokenized_text]#res = [ nltk.pos_tag(t) for t in lemms  ]
    return nltk.ne_chunk(nltk.pos_tag(tokenized_text))

def relations(text):
    """Fonction qui sert à afficher les relations entre des personnes qui sont séparées dans la phrase par des mots du champ lexical du meurtre """

    # IN = re.compile('.*(kill(er|ed|ing)?|murder(er|ed)?|assassin(ated)?|convict(ed)?).*',re.DOTALL)
    IN = re.compile('.*.',re.DOTALL)
    print(text)



    for rel in nltk.sem.relextract.extract_rels('PERSON','PERSON',text,corpus='ace',pattern = IN):

        #Si le nom commence bien par la lettre E ou B (pour les tests)
        if re.match(".*\[PER: '[a-zA-Z\s\S]*(E|B|J|D|B|L)[a-z]+.*",repr(nltk.sem.rtuple(rel))):
            print("="*30)
            print("Detected relation : ",nltk.sem.rtuple(rel))
            print()
            print("Sentence : ",re.sub(r'/[^\s]+','',str(text))) #On enlève les tags pour les entités non nommées
            print("="*30)



T="John Baughman: former American police officer who pushed his second wife from the roof of the Royal Antiguan Hotel in 1995; suspected of killing a close friend and first wife back in the USA; committed suicide in 2000."
sents = text_to_sents(T)

# for s in sents:
#     # traitement des phrases
#     # print(process_text_ner(s))
#     relations(process_text_ner(s))
#


from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
            else:
                continue
    return continuous_chunk

my_sent = "WASHINGTON -- In the wake of a string of abuses by New York police officers in the 1990s, Loretta E. Lynch, the top federal prosecutor in Brooklyn, spoke forcefully about the pain of a broken trust that African-Americans felt and said the responsibility for repairing generations of miscommunication and mistrust fell to law enforcement."
print(get_continuous_chunks(T))
