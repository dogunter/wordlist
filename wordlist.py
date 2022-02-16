#! /usr/bin/env python

import re
import argparse

# Open the dictionary and return a list of nLetter words
def getWords(dictFile, nLetters):
   with open(dictFile, 'r') as infile:
      words = [word for word in infile.read().split() if len(word) == nLetters]
   return(words)
 
def removeIgnored(words, ignored):
   badWords = []
   # Convert ignored to a list separated by '|' symbol
   ignoredStr = []
   ignoredStr[:0] = ignored # Creates a list of individual characters from a string
   sep = '|'
   # Set the ignored list regular expression (?i) is for case ignore
   ignoredStr = '(?i)'+sep.join(ignoredStr)

   for word in words:
      x = re.findall(ignoredStr, word)
      if x:
         badWords.append(word)
   for word in badWords:
      words.remove(word)

   return words

def mustContain(words, contains):
   goodWords = []
   nContains = len(contains) #words should contain this many letters
   # Convert string of letters "contains" to a suitable regex
   containsStr = []
   containsStr[:0] = contains
   # Ex) if contains == 'ak', regexStr = '[a, k]' as a string
   #regexStr = '[%s]' % ', '.join([str(i) for i in containsStr])

   for word in words:
      containsAll = True
      for letter in containsStr:
         #x = re.findall(regexStr, word)
         x = re.search(letter, word)
         if not x:
            containsAll = False
      #if len(x) == nContains: # This is a good word
      if containsAll:
         goodWords.append(word)

   return goodWords

def mustMatch(words, match):
   # Ex) There's a 'c' in the 3rd position and an 'n' in the 5th: -m c3n5
   # The regex string would be '^\w{2}c' followed by '^\w{4}n'
   
   matchWords = []
   # parse the match string
   r = re.compile("([a-z]+)([0-9]+)")
   matchList = r.findall(match) # Ex) matchList = [('c', '3'), ('n', '5')]
   
   regs = []
   for pair in matchList:
      letter = pair[0]
      index = str(int(pair[1]) - 1)
      regs.append("^\w{"+index+"}"+letter ) 
   

   for word in words:
      goodWord = True
      # Search through all the regex patterns, if one fails, set
      # goodWord to false
      for regEx in regs:
         x = re.match(regEx, word)
         if not x:
            goodWord = False
      # If goodWord is still True, we have a good word
      if goodWord:
         matchWords.append(word)

   return matchWords

def excludeSpecified(words, exlude):
   # Ex) There cannot be a 'c' in the 3rd position nor an 'n' in the 5th: -e c3n5
   # The regex string would be '^\w{2}c' followed by '^\w{4}n'
   
   goodWords = []
   # parse the match string
   r = re.compile("([a-z]+)([0-9]+)")
   excludeList = r.findall(exlude) # Ex) excludeList = [('c', '3'), ('n', '5')]
   regs = []
   for pair in excludeList:
      letter = pair[0]
      index = str(int(pair[1]) - 1)
      regs.append("^\w{"+index+"}"+letter ) 

   for word in words:
      goodWord = True
      # Search through all the regex patterns, if one matches, set
      # goodWord to false
      for regEx in regs:
         x = re.match(regEx, word)
         if x:
            goodWord = False
      # If goodWord is still True, we have a good word
      if goodWord:
         goodWords.append(word)

   return goodWords


if __name__ == "__main__":
   parser = argparse.ArgumentParser()

   parser.add_argument("-n", "--nletters", type=int, default=5, help="Parse only words of length NLETTERS.")
   parser.add_argument("-d", "--dict", type=str, default="./words.english", help="Word dictionary to use.")
   parser.add_argument("-i", "--ignore", type=str, default="", help="Ignore these letters.")
   parser.add_argument("-c", "--contains", type=str, default="", help="Must contain these letters.")
   parser.add_argument("-m", "--match", type=str, help="Match these letters in given positions.")
   parser.add_argument("-e", "--exclude", type=str, help="Exclude words with these letters in specified positions.")

   args = parser.parse_args()

   # get list of n-letter words
   dictFile = args.dict
   nLetters = args.nletters
   ignored = args.ignore
   contains = args.contains
   match = args.match
   exclude = args.exclude

   # Get the list of nLetter-words
   words = getWords(dictFile, nLetters)
   # Pare the list down based on other options given

   # Ignore words with these letters
   if ignored:
      words = removeIgnored(words,ignored)

   # Words must have these letters
   if contains:
      words = mustContain(words, contains)

   # Words must have these letters in defined positions
   if match:
      words = mustMatch(words, match)

   # Exclude words that have these letters in the specified positions
   if exclude:
      words = excludeSpecified(words, exclude)

   print(words)

