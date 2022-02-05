import pandas as pd
import os
import csv
import pickle
from tqdm import tqdm
import numpy as np
from gutenberg_cleaner import super_cleaner
import nltk
import re
import string
import collections


#########################################################################
nltk.download("punkt")
nltk.download("stopwords")


with open("train_books.pickle", "rb") as handle:
    b = pickle.load(handle)

for key in b.keys():
    text = b[key]["text"]
    text = super_cleaner(text)
    text = text.replace("[deleted]", "")
    text = re.sub("\s+", " ", text)
    text = re.sub("\n", " ", text)
    text = re.sub("\\'", "'", text)
    text = re.sub(r'https?:\/\/.\S+', "", text)
    sentences = nltk.sent_tokenize(text)
    flat_dump = []
    for sentence in sentences:
        tokenized = sentence.split(" ")
        tokenized.insert(0, "[BOS]")
        tokenized.insert(len(tokenized), "[EOS]")
        flat_dump.append(tokenized)
    b[key]["raw_text"] = text
    b[key]["text"] = text.lower()
    b[key]["tokenized"] = nltk.tokenize.wordpunct_tokenize(text)
    b[key]["flat_sentences"] = [item.lower() for list in flat_dump for item in list]
    b[key]["ebos_sentences"] = flat_dump


with open("clean_dict.pickle", "wb") as handle:
    pickle.dump(b, handle, protocol=pickle.HIGHEST_PROTOCOL)
