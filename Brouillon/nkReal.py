#begin programme basé sur le livre nltk
import nltk
import nltk, re, pprint
import os
import string
import xml.etree.ElementTree as ET


from nltk.tree import *
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.chunk import conlltags2tree, tree2conlltags

from nltk import ne_chunk, pos_tag
from nltk.tree import *

from collections import defaultdict
from pprint import pprint


from nltk.tree import Tree
from nltk.grammar import Nonterminal

def extract_entity_names(t):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == 'NN':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names


ROOT = 'ROOT'
def getNodes(tree):
    for node in tree:
        if type(node) is nltk.Tree:
            if node.label() == ROOT:
                print( "======== Sentence =========")
                print ("Sentence:", " ".join(node.leaves()))
            else:
                print( "Label:", node.label())
                print ("Leaves:", node.leaves())

            getNodes(node)
        else:
            print( "Word:", node)
def find_noun_phrases(tree):
    return [subtree for subtree in tree.subtrees(lambda t: t.label()=='NP')]
def find_head_of_np(np):
    noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    top_level_trees = [np[i] for i in range(len(np)) if type(np[i]) is Tree]
    ## search for a top-level noun
    top_level_nouns = [t for t in top_level_trees if t.label() in noun_tags]
    if len(top_level_nouns) > 0:
        ## if you find some, pick the rightmost one, just 'cause
        return top_level_nouns[-1][0]
    else:
        ## search for a top-level np
        top_level_nps = [t for t in top_level_trees if t.label()=='NP']
        if len(top_level_nps) > 0:
            ## if you find some, pick the head of the rightmost one, just 'cause
            return find_head_of_np(top_level_nps[-1])
        else:
            ## search for any noun
            nouns = [p[0] for p in np.pos() if p[1] in noun_tags]
            if len(nouns) > 0:
                ## if you find some, pick the rightmost one, just 'cause
                return nouns[-1]
            else:
                ## return the rightmost word, just 'cause
                return np.leaves()[-1]
def operation(sent):
    print("+:----------------------------:+")
    #preprocess
    tokenned=[token for token in nltk.word_tokenize(sent)]
    tagged = nltk.pos_tag(tokenned)

    #trouver des depandence pour faire des groupes et analyser les sentence = permet de passer au sens
    pattern='''
    NP: {<DT>? <JJ>* <NN>} # NP
    V: {<V.*>} # Verb
    '''

    cp = nltk.RegexpParser(pattern)
    cs = cp.parse(tagged)
    iob_tagged = nltk.tree2conlltags(cs)
    ne_tree = nltk.chunk.ne_chunk(iob_tagged)

    # for subtree in cs.subtrees():
    #     print(subtree)

    #pour trouver les person,org,gpe
    # print(cs)
    # getNodes(ne_tree)


    #
    # for example in tagged:
    #     tree = Tree.fromstring(example)
    #     for np in find_noun_phrases(tree):
    #         print ("noun phrase:")
    #         print (" ".join(np.leaves()))
    #         head = find_head_of_np(np)
    #         print ("head:")
    #         print (head)



    ne = conlltags2tree(iob_tagged)
    # pprint(iob_tagged)
    original_text = []
    for subtree in ne:
        # skipping 'O' tags

        #si il y a un arbre dans l'arbe, alors on recupere la contenu pour montrer ces mots qui sont associé
        if type(subtree) == Tree:
            original_label = subtree.label()
            original_string = " ".join([token for token, pos in subtree.leaves()])
            original_text.append((original_string, original_label))
            # print((original_string, original_label))
    # pprint(original_text)
        # else:
        #     print(subtree)
    #
    # print("++++[[]]")
    # entites=[]
    # for ent in ne_tree:
    #     if hasattr(ent, 'label'):
    #         entites.append(ent)

        # if type(ent) == Tree:
        #     original_label = ent.label()
        #     original_string = " ".join([token for token, pos in ent.leaves()])
        #     entites.append((original_string, original_label))
        #     #
        #     # print((original_string, original_label))


    #
    # tot=[]
    # while len(entites)>0 and len(original_text)>0:
    #     for ent in entites:
    #         tot.append(ent)
    #         entites.remove(ent)
    #     for txt in original_text:
    #         if txt[1] == "V":
    #             tot.append(txt)
    #             original_text.remove(txt)
    #             break
    #         else:
    #             tot.append(txt)
    #             original_text.remove(txt)
    #
    #
    # print(tot)
    # # print(original_text)

    print("+:----------------------------:+")



def test(sent):

    tokenned=[token for token in nltk.word_tokenize(sent)]
    tagged = nltk.pos_tag(tokenned)

    treebank = nltk.corpus.treebank



    dataset_size = len(treebank.parsed_sents())

    ## here, we define the split percentage for the training set and the
    ## learning set, in our case ~3% and ~97%

    split_size = int(dataset_size * 0.97)
    learning_set = treebank.parsed_sents()[:split_size]
    test_set = treebank.parsed_sents()[split_size:]




    sents = treebank.sents()
    raw_test_set = [ [ w for w in sents[i] ] for i in range(split_size, dataset_size) ]

    # This is where we will store all of the productions necessary to
    # construct the PCFG.
    tbank_productions = []

    # For all of the (parsed) sentences in the learning set, extract the
    # productions (i.e. extract the rules).
    for sent in learning_set:
    	for production in sent.productions():
    		tbank_productions.append(production)

    # Now, we will add the lexical rules for the ENTIRE lexicon.
    for word, tag in treebank.tagged_words():

    	# for each tagged word, we create a tree containing that
    	# lexical rule, in order to be able to add it to our
    	# production set tbank_productions.

    	t = Tree.fromstring("("+ tag + " " + word  +")")
    	for production in t.productions():
    		tbank_productions.append(production)

    # At this point, we have the syntactic rules extracted from the
    # learning set and all of the lexical rules. We are ready to extract
    # the PCFG.
    tbank_grammar = nltk.grammar.induce_pcfg(Nonterminal('S'), tbank_productions)



    parser = nltk.ChartParser(tbank_grammar)
    for tree in parser.parse(tokenned):
        print(tree)
def prepaList(para,file):
    stemmer = PorterStemmer()
    rootKillV=wn.synsets('kill',"v")[0].root_hypernyms()
    rootMoveV=wn.synsets('push',"v")[0].root_hypernyms()
    rootSuspectV=wn.synsets('suspect',"v")[0].root_hypernyms()

    tree = ET.parse(file)
    root=tree.getroot()

    strRoot=ET.tostring(root,encoding='unicode',method='text')

    # lCharRoot=list(strRoot)
    # liststrRoot=strRoot.split("|-")

    strRoot=strRoot.replace("[[", "").replace("]]","")
    liststrRoot=""


    if(para == 1):
        liststrRoot=['*Abdullah Shah: killed at least twenty travelers on the road from Kabul to Jalalabad serving under Zardad Khan; also killed his wife; executed on 20 April 2004.&lt;ref name="BBC"&gt;{{cite web |url=http://news.bbc.co.uk/2/hi/south_asia/3662935.stm |title=Former Afghan commander executed |date=27 April 2004 |website=[[BBC News Online|BBC News]] |accessdate=20 August 2009}}&lt;/ref&gt;']
    elif(para==2):
        liststrRoot=["*John Baughman: former American police officer who pushed his second wife from the roof of the Royal Antiguan Hotel in 1995; suspected of killing a close friend and first wife back in the USA; committed suicide in 2000.&lt;ref&gt;{{cite news |url=https://www.chicagotribune.com/news/ct-xpm-2000-06-02-0006020165-story.html |title=Family's Built-Up Pain Eased By Hanging In Antigua |first1=Marla |last1=Donato |first2=David |last2=Heinzmann |date=June 2, 2000 |newspaper=[[Chicago Tribune |access-date=24 November 2019}}&lt;/ref&gt;"]
    elif(para==3):
        liststrRoot=['*Marcelo Antelo: also known as "The San La Muerte Killer"; drug addict who killed at least four people between February and August 2010, allegedly in the name of a pagan saint; sentenced to life imprisonment.&lt;ref&gt;{{cite news |url=https://www.clarin.com/crimenes/largo-prontuario-Marcelo-Antelo_0_SyXXJx2DXg.html |title=El largo prontuario de Marcelo Antelo |trans-title=The long record of Marcelo Antelo |first1=Horacio |last1=Ezcurra |first2=Rodrigo |last2=Ezcurra |first3=Marcelo |last3=Antelo |lastauthoramp=yes |date=September 9, 2012 |newspaper=[[Clarín (Argentine newspaper)|Clarín]] |language=es |access-date=24 November 2019 |url-status=live |archive-url=https://archive.today/20190910080104/https://www.clarin.com/crimenes/largo-prontuario-Marcelo-Antelo_0_SyXXJx2DXg.html |archivedate=September 10, 2019}}&lt;/ref&gt;']
    elif(para==4):
        liststrRoot=['*[[Cayetano Domingo Grossi]]: the first serial killer in Argentine history; Italian immigrant who murdered five of his newborn children between 1896 and 1898; executed 1900.&lt;ref&gt;{{cite web |url=http://www.acciontv.com.ar/soca/polis/enero13/grosi.htm |title=El fusilamiento de Cayetano Grossi (1900) |trans-title=The execution of Cayetano Grossi (1900) |website=AcciónTV |language=es |access-date=12 November 2015}}&lt;/ref&gt;']
    else:
        liststrRoot=strRoot.split('*')
        sent=' '.join(str(e) for e in liststrRoot)
        liststrRoot=sent.split('===')


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
        sent=' '.join(str(e) for e in sort)
        sent=sent.replace("*", "")
        print("------------------------------------------------------------")
        return sent


ROOT = 'ROOT'
def getNodesString(parent):
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == ROOT:
                print(ROOT)
                # print ("======== Sentence =========")
                # print ("Sentence:", " ".join(node.leaves()))
            else:
                print("--",node)
                # print ("Label:", node.label())
                # print ("Leaves:", node.leaves())

            getNodes(node)
        else:
            print ("Word:", node)



def getLabel():
    for i in tree.subtrees(filter=lambda x: x.label() == 'NP'):
        print(i)

def cfg_parse(sentence):
    s_NP=""
    s_V=""
    s_N=""
    sent_tk = nltk.pos_tag(word_tokenize(sentence))
    for one in sent_tk:
        if one[1] == 'NNP':
            s_NP += "\'"+one[0] + "\'"
        elif one[1] == 'VBD' or one[1]=='VBN':
            s_V += "\'" + one[0] + "\'"
        elif one[1] == 'NN':
            s_N += "\'" + one[0] + "\'"
        # else:
        #     print("")#"one")
    cfg_grammar2 = nltk.CFG.fromstring("""
    S -> NP VP
    VP -> V N
    NP -> {}
    V -> {}
    N -> {}
    """.format(s_NP,s_V,s_N))

    return cfg_grammar2
# print(cfg_parse(new))
#
#
#
#
# #
# # new = prepaList(2,"List_of_serial_killers_by_country.xml")
# # cfg_parse(new)
# #
# # sent = "Mary saw Bob".split()
# # rd_parser = nltk.RecursiveDescentParser(grammar1)
# # for tree in rd_parser.parse(sent):
# #     print(tree)
#
# # for n in nltk.sent_tokenize(new):
# #     print(n)
# #     print("cfg : ",cfg_parse(n))
#
# token=nltk.pos_tag(nltk.word_tokenize(new))
# grammar_np=r"NP: {<DT>?<JJ>*<NN>}"
# chunk_parser = nltk.RegexpParser(grammar_np)
#
#
#
# parser = nltk.ChartParser(cfg_parse(new))
# # for tree in parser.parse(nltk.word_tokenize(new)):
#     # print(tree)
#
#

#
#
# treebank = chunk_parser.parse(token)
#
#
#
# dataset_size = len(token)
#
# ## here, we define the split percentage for the training set and the
# ## learning set, in our case ~3% and ~97%
#
# split_size = int(dataset_size * 0.97)
# learning_set = treebank[:split_size]
# test_set = treebank[split_size:]
#
#
#
#
# sents = token
# raw_test_set = [ [ w for w in sents[i] ] for i in range(split_size, dataset_size) ]
#
# # This is where we will store all of the productions necessary to
# # construct the PCFG.
# tbank_productions = []

# For all of the (parsed) sentences in the learning set, extract the
# productions (i.e. extract the rules).
# for sent in learning_set:
#     for production in sent.productions():
#         tbank_productions.append(production)


# Now, we will add the lexical rules for the ENTIRE lexicon.
# for word, tag in token:
#
#     # for each tagged word, we create a tree containing that
#     # lexical rule, in order to be able to add it to our
#     # production set tbank_productions.
#
#     t = Tree.fromstring("("+ tag + " " + word  +")")
#     for production in t.productions():
#         tbank_productions.append(production)

# At this point, we have the syntactic rules extracted from the
# learning set and all of the lexical rules. We are ready to extract
# the PCFG.
# tbank_grammar = nltk.grammar.induce_pcfg(Nonterminal('S'), tbank_productions)










# [operation(s) for s in nltk.sent_tokenize(prepaList(2,"List_of_serial_killers_by_country.xml"))]
# [test(s) for s in nltk.sent_tokenize(prepaList(2,"List_of_serial_killers_by_country.xml"))]
#
# grammar = '''
#     NP:
#        {<DT>*(<NN.*>|<JJ.*>)*<NN.*>}
#      NVN:
#        {<NP><VB.*><NP>}
#     '''
# chunker = nltk.chunk.RegexpParser(grammar)
# tokenned=[token for token in nltk.word_tokenize(prepaList(2,"List_of_serial_killers_by_country.xml"))]
# tagged = nltk.pos_tag(tokenned)
#
# tree = chunker.parse(tagged)
#
# # getNodesString(tree)
#


# getNodes(tree)

# from nltk.tree import ParentedTree
# ptree = ParentedTree.fromstring('(ROOT (S (NP (PRP It)) \
#         (VP (VBZ is) (ADJP (RB so) (JJ nice))) (. .)))')
#
# leaf_values = ptree.leaves()
#
# if 'nice' in leaf_values:
#     leaf_index = leaf_values.index('nice')
#     tree_location = ptree.leaf_treeposition(leaf_index)
#     print(tree_location)
#     print(ptree[tree_location])
#
#
# from nltk.tree import ParentedTree
# ptree = ParentedTree.fromstring('(ROOT (S (NP (JJ Congressional) \
#     (NNS representatives)) (VP (VBP are) (VP (VBN motivated) \
#     (PP (IN by) (NP (NP (ADJ shiny) (NNS money))))))) (. .))')
#
# def traverse(t):
#     try:
#         t.label()
#     except AttributeError:
#         return
#     else:
#
#         if t.height() == 2:   #child nodes
#             print(t.parent())
#             return
#
#         for child in t:
#             traverse(child)
#
# traverse(ptree)
#













from nltk.grammar import DependencyGrammar
from nltk.parse import (DependencyGraph,ProjectiveDependencyParser,NonprojectiveDependencyParser,)
from nltk.sem import relextract

treebank_data = """
 Pierre  NNP     2       NMOD
 Vinken  NNP     8       SUB
 ,       ,       2       P
 61      CD      5       NMOD
 years   NNS     6       AMOD
 old     JJ      2       NMOD
 ,       ,       2       P
 will    MD      0       ROOT
 join    VB      8       VC
 the     DT      11      NMOD
 board   NN      9       OBJ
 as      IN      9       VMOD
 a       DT      15      NMOD
 nonexecutive    JJ      15      NMOD
 director        NN      12      PMOD
 Nov.    NNP     9       VMOD
 29      CD      16      NMOD
 .       .       9       VMOD
 """


dg = DependencyGraph(treebank_data)
# dg.tree().pprint()


# for head, rel, dep in dg.triples():
#      print('({h[0]}, {h[1]}), {r}, ({d[0]}, {d[1]})'.format(h=head, r=rel, d=dep))

#recuperation sent
# sent = prepaList(2,"List_of_serial_killers_by_country.xml")

#trouver des depandence pour faire des groupes et analyser les sentence = permet de passer au sens
pattern='''
NP: {<DT>? <JJ>* <NN>*} # NP
'''
#V: {<V.*>} # Verb
# '''

# pattern='''  NP: {<DT>? <JJ>* <NN>*} # NP
#     P: {<IN>}           # Preposition
#     V: {<V.*>}          # Verb
#     PP: {<P> <NP>}      # PP -> P NP
#     VP: {<V> <NP|PP>*}  # VP -> V (NP|PP)*
# '''

# new=sent
# #tokenise et tagged
# tokens =nltk.word_tokenize(new)
# tagged_sentences = nltk.pos_tag(tokens)# [ nltk.pos_tag(token) for token in tokens]
#
# for token in sentt:
#     token=nltk.word_tokenize(token)
#     tagged_sentences=nltk.pos_tag(token)
#     #utilisation de la grammaire pour parse
#     cp = nltk.RegexpParser(pattern)
#     cs = cp.parse(tagged_sentences)
#     #reccuperation conlltags
#     iob_tagged = nltk.tree2conlltags(cs)
#     #chunk
#     ne_tree = nltk.chunk.ne_chunk(iob_tagged)
#     #extraction de l'arbe en relation semi
#     pairs = relextract.tree2semi_rel(cs)
#     #The function semi_rel2reldict() processes triples of these pairs, i.e., pairs of the form ((string1, Tree1), (string2, Tree2), (string3, Tree3)) and outputs a dictionary (a reldict) in which Tree1 is the subject of the relation, string2 is the filler and Tree3 is the object of the relation. string1 and string3 are stored as left and right context respectively.
#     reldicts = relextract.semi_rel2reldict(pairs)

class doc():
    pass
# IN = re.compile(r'.*\bin\b(?!\b.+ing)')
# doc.headline=["test headline for sentence"]
#
# doc.text = nltk.chunk.ne_chunk(tagged_sentences)
# # pprint(doc.__dict__)
# print(doc.text)
# for rel in nltk.sem.relextract.extract_rels('ORG', 'LOC', doc, corpus='ieer', pattern=IN):
#     print(rel)
#     print(nltk.sem.rtuple(rel) )# you can change it according
#
# IN = re.compile(r'.*\bin\b(?!\b.+ing)')
# # for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
# #     print("-"*20)
# #     print(doc.__dict__)
#
#
# new=sent
# #tokenise et tagged
# tokens =nltk.word_tokenize(new)
# tagged_sentences = nltk.pos_tag(tokens)# [ nltk.pos_tag(token) for token in tokens]
# cp = nltk.RegexpParser(pattern)
# cs = cp.parse(tagged_sentences)
# doc.headline=["test headline for sentence"]
# # ne_tree = nltk.chunk.ne_chunk(tagged_sentences)
# pairs = relextract.tree2semi_rel(cs)
# reldicts = relextract.semi_rel2reldict(pairs)
# for txt in reldicts:
#     doc.text=txt
#     print("-"*20)
#     print(txt)
#     for rel in nltk.sem.relextract.extract_rels('ORG', 'LOC', doc, corpus='ieer', pattern=IN):
#         print(rel,nltk.sem.relextract.rtuple(rel))

# sent = prepaList(2,"List_of_serial_killers_by_country.xml")



text=("John Baughman: former American police officer who pushed his second wife from the roof of the Royal Antiguan Hotel in 1995. suspected of killing a close friend and first wife back in the USA; committed suicide in 2000.")



#
# for new in nltk.sent_tokenize(sent):
#
#     #tokenise et tagged
#     token =nltk.word_tokenize(new)
#     tagged=nltk.pos_tag(token)
#
#     #utilisation de la grammaire pour parse
#     cp = nltk.RegexpParser(pattern)
#     cs = cp.parse(tagged)
#
#     #reccuperation conlltags
#     iob_tagged = nltk.tree2conlltags(cs)
#     #chunk
#     ne_tree = nltk.chunk.ne_chunk(iob_tagged)
#
#
#
#     #extraction de l'arbe en relation semi
#     pairs = relextract.tree2semi_rel(cs)
#     # getNodesString(ne_tree)
#     # for s, tree in pairs:#[18:22]:
#         # print('("%s", %s)' % (" ".join(s[-5:]),tree))
#         # print(tree)
#         # print(s)
#         # print('("%s", %s)' % (" ".join(s[-5:]),tree))
#
#
#
#     #The function semi_rel2reldict() processes triples of these pairs, i.e., pairs of the form ((string1, Tree1), (string2, Tree2), (string3, Tree3)) and outputs a dictionary (a reldict) in which Tree1 is the subject of the relation, string2 is the filler and Tree3 is the object of the relation. string1 and string3 are stored as left and right context respectively.
#
#     reldicts = relextract.semi_rel2reldict(pairs)
#     if(len(reldicts)>0):
#         for k, v in sorted(reldicts[0].items()):
#             print(k, '=>', v) # doctest: +ELLIPSIS
#
#
#     for r in reldicts:
#         print('=' * 20)
#         print(r['subjtext'])
#         print(r['filler'])
#         print(r['objtext'])
#



from nltk.corpus import conll2002



de = """
.*
(
de/SP|
del/SP
)
"""
DE = re.compile(de, re.VERBOSE)
rels = [rel for doc in conll2002.chunked_sents('esp.train')for rel in relextract.extract_rels('ORG', 'LOC', doc, corpus='conll2002', pattern = DE)]
for r in rels[:10]:
    # print(relextract.clause(r, relsym='DE'))    # doctest: +NORMALIZE_WHITESPACE
    a=1
vnv = """
(
is/V|
was/V|
werd/V|
wordt/V
)
.*
van/Prep
"""
VAN = re.compile(vnv, re.VERBOSE)
for doc in conll2002.chunked_sents('ned.train'):
    for r in relextract.extract_rels('PER', 'ORG', doc, corpus='conll2002', pattern=VAN):
        # print(relextract.clause(r, relsym="VAN"))
        a=1





























a=1
