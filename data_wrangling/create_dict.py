import pandas as pd
import os
import csv
import pickle
from tqdm import tqdm
import numpy as np
import nltk
import re
################################################################################

rootdir = "/Users/umadwivedi/Documents/Projects/YALE/THESIS/working files/training_texts/"

books = {}
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        file_parsed = re.sub(".txt", "", file)
        books[file_parsed] = {}
        filename = os.path.join(subdir,file)
        with open(filename) as f:
            try:
                book = f.read()
                books[file_parsed]["length"] = len(book)
                books[file_parsed]["text"] = book
                print(file_parsed, books[file_parsed].keys(), books[file_parsed]["text"][0:20])
            except:
                continue

with open("train_books.pickle", "wb") as handle:
    pickle.dump(books, handle, protocol=pickle.HIGHEST_PROTOCOL)
