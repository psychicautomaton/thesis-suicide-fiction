import pandas as pd
import os
import csv
import pickle
from tqdm import tqdm
import numpy as np
import nltk
import re
import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English
nlp = English()
nlp.max_length = 2500000
################################################################################

#suicide terms lists
s_terms = []
s_terms_flat = []
with open("suicideterms.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        s_terms.append(row[0].split(" "))
        s_terms_flat.append(row[0])
    s_terms.append('suicide')
    s_terms_flat.append('suicide\ posts')
s_terms = s_terms[1:]
s_terms_flat = s_terms_flat[1:]

#open training texts dict
with open("clean_dict.pickle", "rb") as handle:
    b = pickle.load(handle)

#define patternmaker for spacy pattern searches
def patternmaker(t):
    l = []
    for word in t:
        l.append({'TEXT': word})
    return l

#set up matcher
matcher = Matcher(nlp.vocab)
passages = pd.DataFrame(columns=["title", "text"])

#hyperparameters
n = 500

for book in b.keys():
    txt = b[book]["text"]
    doc = nlp(txt)

    for i, term in enumerate(s_terms):
        pattern = patternmaker(term)
        matcher.add(s_terms_flat[i], [pattern])
        matches = matcher(doc)
        match_inds = [ind[1:] for ind in matches]

        for j, item in enumerate(match_inds):
            ind1 = item[0]-n
            ind2 = item[1]+n
            passages.loc[j, "title"] = book
            passages.loc[j, "text"] = doc[ind1:ind2]


passages.to_csv('passages.csv')


cols = ["book", "term", "passage"]

df = pd.DataFrame(columns=cols)

df

passages = []
titles = []
for book in tqdm(b.keys()):
    txt = b[book]["text"]
    doc = nlp(txt)

    for i,term in enumerate(s_terms):
        pattern = patternmaker(term)
        matcher.add(s_terms_flat[i], [pattern])
        matches = matcher(doc)
        match_inds = [ind[1:] for ind in matches]

        for j, item in enumerate(match_inds):
            ind1 = item[0]-n
            ind2 = item[1]+n
            passages.append(doc[ind1:ind2])
            titles.append(book)
df["passage"] = passages
df["book"] = titles
df



#create matcher
for i,term in enumerate(s_terms):
    pattern = patternmaker(term)
    matcher.add(s_terms_flat[i], [pattern])
    matches = matcher(doc)
    match_inds = [ind[1:] for ind in matches]

    for j, item in enumerate(match_inds):
        df.loc[(i*length) + j,"passage"] = "a"
        length = len(match_inds)
df
