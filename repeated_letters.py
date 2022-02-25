#! /usr/bin/env python
'''
Determine how many Wordle solution words have
repeated letters
'''

import re
import argparse
import collections
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt

if __name__ == "__main__":
   parser = argparse.ArgumentParser()

   parser.add_argument("-w", "--wordlefile", type=str, default="./wordle-words.csv", help="Previous Wordle solutions csv file.")

   args = parser.parse_args()

   # get list of n-letter words
   wordleFile = args.wordlefile

   # Read in csv file of previous Wordle solutions into a pandas data frame
   # First line is the header: date,puzzle number,word
   df = pd.read_csv(wordleFile)
   # Convert the "date" column to a datetime object
   df['date'] = pd.to_datetime(df['date'])
   # Convert "puzzle" column to string type
   df['puzzle number'] = df['puzzle number'].apply(str)
   df['puzzle number'] = df['puzzle number'].str.strip()
   # Convert "word" column to strings
   df['word'] = df['word'].apply(str)
   df['word'] = df['word'].str.strip()
   # Create a new column of dictionary containing letter frequencies
   df['freqs'] = [ collections.Counter(x) for x in df['word'] ]

   # Extract words with multiple letters (len(dict) < 5
   freqDF = df[ df['freqs'].apply(len) < 5 ]
   doubleFreqDF = df[ df['freqs'].apply(len) < 4 ]

   # Gather some statistics
   # number of puzzles so far
   nWordles = len( df.index )
   # number of words that had repeated letters
   nRep = len( freqDF.index )
   # number of words that had 2 differentletters repeated
   nDoubleRep = len( doubleFreqDF.index )
   # stat string 
   statStr = str(nWordles) + " puzzles to date with " + str(nRep) + " containing repeated letters and " + \
         str(nDoubleRep) + " of those containing two repeated letters."
   print( statStr )
   # Plat the frequency as a date plot
   dates = df['date'].to_list()
   freqs = df['freqs'].to_list()
   freqs = [ 5 - len(x) for x in freqs ]

   ax = plt.subplot(111)
   ax.set_title("Frequency of Wordle answers containing 1 or more repeated letters.\n" + statStr)
   ax.bar(dates, freqs, width=1.5)
   ax.xaxis_date()
   plt.show()
