import nltk
import os
import re
import sys
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from distutils.dir_util import mkpath
from nltk.tag import pos_tag
from nltk import word_tokenize
from collections import Counter



pac = sys.argv[1]

mkpath( os.getcwd() + "/file/metriche/" )



path = os.getcwd() + "/file/Totale_" + pac + ".txt"

train_text = state_union.raw(path)
sample_text = state_union.raw(path)

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
tokenized = custom_sent_tokenizer.tokenize(sample_text)

out_file = open(os.getcwd () + "/file/metriche/POS" + pac + ".txt","w")
outfile = open(os.getcwd () + "/file/metriche/Metriche_" + pac + ".txt", "a")


def n_token(path, n_ids):
    f = open(path,'rU')
    text = f.read ()
    token_text = word_tokenize (text)
    N_token = len (token_text) 
    outfile.write("\nTokens: " + str(N_token / float(n_ids)) )


def process_content(n_ids):
    N_nouns = 0
    N_verbs = 0
    N_vbz = 0
    
    try:
        for i in tokenized:  #tokenized[:5]
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            out_file.write(str(tagged))
            
            counts = Counter(tag for word, tag in tagged)
            if counts.get("NN") != None:
                 N_nouns = N_nouns + counts.get("NN")
            if counts.get("NNS") != None:
                 N_nouns = N_nouns + counts.get("NNS")
            if counts.get("NNP") != None:
                 N_nouns = N_nouns + counts.get("NNP")
            if counts.get("NNPS") != None:
                 N_nouns = N_nouns + counts.get("NNPS")
            if counts.get("VB") != None:
                 N_verbs = N_verbs + counts.get("VB")
            if counts.get("VBD") != None:
                 N_verbs = N_verbs + counts.get("VBD")
            if counts.get("VBG") != None:
                 N_verbs = N_verbs + counts.get("VBG")
            if counts.get("VBN") != None:
                 N_verbs = N_verbs + counts.get("VBN")
            if counts.get("VBP") != None:
                 N_verbs = N_verbs + counts.get("VBP")
            if counts.get("VBZ") != None:
                 N_verbs = N_verbs + counts.get("VBZ")
                 N_vbz = N_vbz + counts.get("VBZ")

    except Exception as e:
        print(str(e))
    
    outfile.write("\nNouns: " + str(N_nouns / float(n_ids)) )
    outfile.write("\nVerbs: " + str(N_verbs / float(n_ids)) )
    outfile.write("\nSPW: " + str(N_vbz / float(n_ids)) )


def n_identifiers():
    f = open(os.getcwd () + "/file/metriche/Metriche_" + pac + ".txt", "r")
    text = f.readlines()
    num = 0

    for line in text:
        if re.search("Number_of_Classes: ", line) or re.search("Number_of_Methods: ", line) or re.search("Number_of_Variables: ", line):
            word = line.split()
            num = num + int(word[1])
    
    return num



n_ids = n_identifiers()
n_token(path, n_ids)
process_content(n_ids)
