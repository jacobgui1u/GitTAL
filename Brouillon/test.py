import nltk
import re

from nltk.sem import extract_rels,rtuple
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer #unsupervised machine learning sentence tokenizer
from nltk.corpus import treebank

from nltk.corpus import wordnet as wn

from nltk.corpus import ieer
from nltk.sem import relextract

import xml.etree.ElementTree as ET
import numpy as np

def testMotSyn():

    #nltk.download('wordnet')
    from nltk.corpus import wordnet

    synonyms=[]
    antonyms=[]

    for syn in wordnet.synsets("killer"):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    print(set(syn.lemmas()))
    print(set(antonyms))


    # print(wordnet.synsets("killer"))
    # for syn in wordnet.synsets('killer'):

        # for l in syn.lemmas():
        #     print("l:",l)
        #     synonyms.append(l.name())
        #     if l.antonyms():
        #         antonyms.append(l.antonyms()[0].name())

    #similaire? w1.wup_similarity(w2) (w1 et w2 deux synset de mot)

    # print(set(synonyms))
    # print(set(antonyms))

#testMotSyn()


def test():

#     # open the file in read binary mode
#     f = open('save/interet.txt', "rb")
#     #read the file to numpy array
#     lsortie = np.load(f)
#
#     chunkgram=r"""Chunk : {<RB.?>*<VB.?>*<NNP><NN>?}
# """
#
#     objetInteret=[]
#     lTag=[]
#     tagged=[]
#
#     for l in lsortie:
#         #fin block decoupage
#         lTag=[]
#         tagged=[]
#
#         token = nltk.sent_tokenize(l)
#         tagged = nltk.pos_tag(token)
#         entities = nltk.chunk.ne_chunk(tagged,binary=True)
#
#         chunkParser = nltk.RegexpParser(chunkgram)
#         chunked = chunkParser.parse(tagged)
#
#         # tree = chunked[1].text
#         # print(tree)
#         pairs = relextract.tree2semi_rel(chunked)
#         for s, tree in pairs:
#             print('("...%s", %s)' % (" ".join(s[-5:]),chunked))



    #billgatesbio from http://www.reuters.com/finance/stocks/officerProfile?symbol=MSFT.O&officerId=28066
    f = open('save/interet.txt', 'rb')
    lsortie = np.load(f)

    for sample in lsortie:


        # Tokenize and POS tag the sentence
        tokens = nltk.word_tokenize(sample)
        tagged_sent = nltk.pos_tag(tokens)

        # Chunk the pattern determiner <DT>,
        # followed by noun <NN*>
        # then a prepositional phrase made up of
        # a preposition and proper noun <IN><NNP>+
        grammar = "NP: {<DT><NN*>+<IN><NNP>+}"

        cp = nltk.RegexpParser(grammar)
        # print(cp.parse(tagged_sent))

        IN = re.compile(r'.\bin\b(?!\b.+ing)')
        headline=["test headline for sentence"]
        for i,sent in enumerate(tagged_sent):
            text = nltk.ne_chunk(sent)
            for rel in nltk.sem.relextract.extract_rels('ORG', 'LOC', sent, corpus='ace', pattern=IN):
                print(nltk.sem.rtuple(rel) )

        #
        # sentences = nltk.sent_tokenize(sample)
        # tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        # tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        #
        #
        #
        # # here i changed reg ex and below i exchanged subj and obj classes' places
        # #OF = re.compile(r'.*\bof\b.*')
        #
        # for i, sent in enumerate(tagged_sentences):
        #     sent = nltk.ne_chunk(sent) # ne_chunk method expects one tagged sentence
        #     print(sent)

    # docs = ieer.parsed_docs('NYT_19980315')
    # tree = docs[1].text
    # print(tree) # doctest: +ELLIPSIS





    # for l in lsortie:
    #     #fin block decoupage
    #     lTag=[]
    #     tagged=[]
    #
    #     token = nltk.sent_tokenize(l)
    #     tagged = nltk.pos_tag(token)
    #     entities = nltk.chunk.ne_chunk(tagged,binary=True)
    #
    #     chunkParser = nltk.RegexpParser(chunkgram)
    #     chunked = chunkParser.parse(tagged)
    #
    #     for chunk in entities:
    #         words2 = nltk.word_tokenize(''.join(chunk))
    #         tagged2 = nltk.pos_tag(words2)
    #         namedEnt2 = nltk.ne_chunk(tagged2, binary=False)
    #
    #         chunkParser2 = nltk.RegexpParser(chunkgram)
    #         chunked2 = chunkParser.parse(namedEnt2)
    #
    #         for chunk2 in namedEnt2:
    #             #print(chunk2)
    #             if hasattr(chunk2, 'label') and chunk2[0][0]=="Killer":
    #                 #print(namedEnt2)
    #                 objetInteret.append(namedEnt2)
    #                 print(namedEnt2)
    #
    # print(objetInteret)
        #             #print(chunk.label(), ' '.join(c[0] for c in chunk))
        # for i in token:
        #
        #     words = nltk.sent_tokenize(i)
        #
        #     tagged2 = nltk.pos_tag(words)
        #     namedEnt2 = nltk.ne_chunk(tagged2, binary=False)
        #
        #     chunkParser = nltk.RegexpParser(chunkGram)
        #     chunked = chunkParser.parse(namedEnt2)
        #     print(tagged2)
        #
        #     print(chunked)
        #     print(namedEnt)
        #     print("-------------")



def utilisationListeIntert():
    try:
        # open the file in read binary mode
        f = open('save/interet.txt', "rb")
        #read the file to numpy array
        objetInteret = np.load(f)
        #close the file
        #print(objetInteret)

        #
        for objet in objetInteret:
            print(objet)
            # for chunk in objet:
            #
            #
            #     stop_words=set(stopwords.words("english"))
            #     print(stop_words)
            #
            #     sent = nltk.sent_tokenize(''.join(chunk))
            #     tagged = nltk.pos_tag(sent)
            #     namedEnt = nltk.ne_chunk(tagged, binary=False)
            #
            #     if hasattr(namedEnt, 'label'):
            #         print(namedEnt.label())
#
#                 words = nltk.word_tokenize(''.join(chunk))
#                 tagged = nltk.pos_tag(words)
#
#                 namedEnt = nltk.ne_chunk(tagged, binary=False)
#
#
#                 chunkGram=r"""Chunk: {<RB.?>*<NN.?>*<NNP.?>*}"""
#
#                 chunkParser = nltk.RegexpParser(chunkGram)
#                 chunked = chunkParser.parse(namedEnt)
#
# # namedEnt.draw()
#
#                 for chunkWord in namedEnt:
#                     if hasattr(chunkWord, 'label') and chunkWord.label()=="PERSON":
#                         print(chunkWord)

                    # if hasattr(chunk, 'label') and chunk.label()=="PERSON" and chunk[0][0][0]=="O":
                    #    print(chunk.label(), ' '.join(c[0] for c in chunk))
                    # if hasattr(chunk, 'label') and chunk.label()=="PERSON" :
                    #    print(chunk.label(), ' '.join(c[0] for c in chunk))
        f.close()
        print("closing file")
    except Exception as e:
        print(str(e))

#creationListInteret()
# utilisationListeIntert()
#test()




def ie_preprocess():

    tree = ET.parse("List_of_serial_killers_by_country.xml")
    root=tree.getroot()

    strRoot=ET.tostring(root,encoding='unicode',method='text')

    # lCharRoot=list(strRoot)
    # liststrRoot=strRoot.split("|-")

    strRoot=strRoot.replace("[[", "").replace("]]","")
    liststrRoot=strRoot.split("*")

    print(liststrRoot)
    for sample in liststrRoot:
        sentences = nltk.sent_tokenize(sample)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        for sentence in sentences:


            # grammar = "NP: {<DT><NN*>+<IN><NNP>+}"
            grammar = """r: {<NNP>}
            {<NN>}
            }<VBD|IN>+{
"""
            cp = nltk.RegexpParser(grammar)
            # print(cp.parse(sentence))

            # res=cp.parse(sentence)
            # res.draw()
            nltk.chunk.conllstr2tree(sentence, chunk_types=['NP']).draw()


        # IN = re.compile(r'.\bin\b(?!\b.+ing)')
        # headline=["test headline for sentence"]
        # for i,sent in enumerate(tagged_sent):
        #     text = nltk.ne_chunk(sent)
        #     for rel in nltk.sem.relextract.extract_rels('ORG', 'LOC', sent, corpus='ace', pattern=IN):
        #         print(nltk.sem.rtuple(rel) )

        # grammar = "NP: {<DT>?<JJ>*<NN>}"
        # cp = nltk.RegexpParser(grammar)
        # result = cp.parse(sentence)
        # # result.draw()
        # print(result)

# ie_preprocess()

def testeurNLTK():
    tree = ET.parse("List_of_serial_killers_by_country.xml")
    root=tree.getroot()

    strRoot=ET.tostring(root,encoding='unicode',method='text')

    # lCharRoot=list(strRoot)
    # liststrRoot=strRoot.split("|-")

    strRoot=strRoot.replace("[[", "").replace("]]","")
    # liststrRoot=strRoot.split("*")

    # # make object text of nltk from tokenized object
    # text = nltk.Text(nltk.word_tokenize(strRoot))
    # # renvoie les occurence du mot
    # match = text.concordance('killer')

    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(strRoot)

    new_sentence = []

    for word in words:
        if word not in stop_words:
            new_sentence.append(word)
    print(new_sentence)

def list():
    listAss=[]
    for ss in wn.synsets('kill'):
        killer = wn.synset(ss.name())
        # print(killer)
        if killer.hyponyms()!=[]:
            for a in killer.hyponyms():
                # print("-",a)
                listAss.append(a)
                for synset in wn.synsets(a.name().split('.')[0]):
                    for lemma in synset.lemmas():
                        # print("-:-",lemma)
                        listAss.append(lemma)


    tree = ET.parse("List_of_serial_killers_by_country.xml")
    root=tree.getroot()

    strRoot=ET.tostring(root,encoding='unicode',method='text')

    # lCharRoot=list(strRoot)
    # liststrRoot=strRoot.split("|-")

    strRoot=strRoot.replace("[[", "").replace("]]","")
    liststrRoot=strRoot.split("*")


    listLocalisation=[]
    for i,sample in enumerate(liststrRoot[0:100]):
        for j, chaine in enumerate(nltk.word_tokenize(sample)):

            if wn.synsets(chaine)!=[]:
                for ass in listAss:
                    # print(chaine,ass.name())
                    if chaine == ass.name():
                        # ici on stock le sample, le word tokenizé du sample et le sample de la chaine qui correspond a killer. on stock aussi le sample et si la chaine peut etre un verbe
                        if wn.synsets(chaine,'v') ==[]:
                            listLocalisation.append([i,j,chaine,sample,False])
                        elif wn.synsets(chaine,'v') !=[]:
                            listLocalisation.append([i,j,chaine,sample,True])

                        break

    # # localisateur print(liststrRoot[631],nltk.word_tokenize(liststrRoot[631])[1])
    for i in listLocalisation:
        print(i)



from nltk.wsd import lesk

def pos_tag_convert_penn_to_wn(tag):
    """
    Convert POS tag from Penn tagset to WordNet tagset.

    :param tag: a tag from Penn tagset
    :return: a tag from WordNet tagset or None if no corresponding tag could be found
    """
    from nltk.corpus import wordnet as wn

    if tag in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ
    elif tag in ['RB', 'RBR', 'RBS']:
        return wn.ADV
    elif tag in ['NN', 'NNS', 'NNP', 'NNPS']:
        return wn.NOUN
    elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return wn.VERB
    return None


def sensAmbigue():

    sent = ["Emmet Brown killed a man in San Franciso yersteday.","Emmet Brown eat an ice in new york today."]

    for sample in sent:
        # Tokenize and POS tag the sentence
        tokens = nltk.word_tokenize(sample)
        tagged_sent = nltk.pos_tag(tokens)
        print(tagged_sent)

        # for word in tagged_sent:
        #     if(pos_tag_convert_penn_to_wn(word[1])=='v'):
        #         print("ok")

        namedEnt = nltk.ne_chunk(tagged_sent)
        print(namedEnt)
    # print(lesk(sent, 'killed', 'n'))
    # print(lesk(sent, 'killed'))

from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint

sent = "In this article, we see how Emmet Brown, a young man living near State Street, killed a man in San Franciso, the great city, yersteday."
#
# tokens = nltk.word_tokenize(sent)
# tagged_sent = nltk.pos_tag(tokens)
#
#
# pattern = 'NP: {<DT>?<JJ>*<NN>}'
# cp = nltk.RegexpParser(pattern)
# cs = cp.parse(tagged_sent)
# print(cs)
# iob_tagged = tree2conlltags(cs)
# pprint(iob_tagged)
import spacy
nlp = spacy.load('en')
sent = nlp(sent)
# for s in sent.sents:
#     tmp = nlp(str(s))
#
#     for ent in tmp.ents:
#         print(ent,ent.text, ent.label_)
# for token in sent:
#     print(token.text, token.pos_, token.dep_)
# for token in sent:
#     print(token.text)
# for token in sent:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop)
#
# for ent in sent.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)
#
# for token in sent:
#     print(token.text, token.has_vector, token.vector_norm, token.is_oov)

spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
len(spacy_stopwords)

for token in sent:
    if not token.is_stop:
        print (token)

for token in sent:
    print (token, token.lemma_)
# from nltk.chunk import conlltags2tree, tree2conlltags
# #
# # sentence = "Mark and John are working at Google."
# ne_tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)))
# #
# # iob_tagged = tree2conlltags(ne_tree)
# # print(iob_tagged)
# #
# #
# # ne_tree = conlltags2tree(iob_tagged)
# # print(ne_tree)
#
# grammar = "NP: {<DT>?<JJ>*<NN>}"
#
# cp = nltk.RegexpParser(grammar)
#
# result = cp.parse(ne_tree)
#
# print(result)
# # result.draw()
#
# t=tree2conlltags(result)
# print(type(t))
# nltk.chunk.conllstr2tree(t, chunk_types=['NP']).draw()


# sensAmbigue()
#
# listAss=[]
# for ss in wn.synsets('kill'):
#     killer = wn.synset(ss.name())
#     print(killer)
#     if killer.hyponyms()!=[]:
#         for a in killer.hyponyms():
#             print("-",a)
#             listAss.append(a.name())
#             for synset in wn.synsets(a.name().split('.')[0]):
#                 for lemma in synset.lemmas():
#                     print("-:-",lemma)
#                     listAss.append(lemma)















def extractionArbreStr(TabRoot,semiRel):
    ROOT = 'ROOT'
    for node in semiRel:
        if type(node) is nltk.Tree:
            if node.label() == ROOT:
                print(ROOT)
                print ("======== Sentence =========")
                print ("Sentence:", " ".join(node.leaves()))
                extractionArbreStr(TabRoot,node)
            else:
                lves=[]
                for leave in node.leaves():
                    lves.append("'"+leave[0]+"'")
                res="nltk.Tree('"+node.label()+"', ["+''.join(lves)+"]), "
                TabRoot.append(res)

        else:
            res="'"+node[0]+"',"
            TabRoot.append(res)
    return TabRoot


doc.headline=['foo']
texte=conlltags2tree(tree2conlltags(nltk.ne_chunk(tagged)))
TabRoot=[]
TabRoot=extractionArbreStr(TabRoot,nltk.ne_chunk(tagged))


# print("["+''.join(TabRoot)+"]")

doc.text=''.join(TabRoot)

doc.text=[nltk.Tree('PERSON', ['John']), nltk.Tree('PERSON', ['Baughman']), ':','former',nltk.Tree('GPE', ['American']), 'police','officer','who','pushed','his','second','wife','from','the','roof','of','the',nltk.Tree('ORGANIZATION', ['Royal''Antiguan''Hotel']), 'in','1995',';','suspected','of','killing','a','close','friend','and','first','wife','back','in','the',nltk.Tree('ORGANIZATION', ['USA']), ';','committed','suicide','in','2000','.']
