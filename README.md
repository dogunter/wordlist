# wordlist ("wordle-list")
wordlist.py is a basic text parser written in Python that operates on a dictionary file (think /usr/share/dict/words) that contains a single word entry per line.

It can be used to find all n-letter words matching a given set of criteria. The default is 5-letter words, those featured in the game Wordle.

## usage: wordlist.py [-h] [-n NLETTERS] [-d DICT] [-i IGNORE] [-c CONTAINS] [-m MATCH] [-e EXCLUDE]

options:
  -h, --help            show this help message and exit
  -n NLETTERS, --nletters NLETTERS
                        Parse only words of length NLETTERS.
  -d DICT, --dict DICT  Word dictionary to use
  -i IGNORE, --ignore IGNORE
                        Ignore these letters.
  -c CONTAINS, --contains CONTAINS
                        Must contain these letters.
  -m MATCH, --match MATCH
                        Match these letters in givin positions.
  -e EXCLUDE, --exclude EXCLUDE
                        Exclude words with these letters in specified positions.

## Examples.
### 1) List all 6-letter words that do not contain 'c', 'k', or 'w'.
`wordlist.py -n 6 -i ckw

### 2) List all 5-letter words (default) that do not contain 'u' or 'a', but do contain the letter 'c'.
`wordlist.py -i ua -c c

### 3) List all 5-letter words that do not contain 'a', 'e', or 'f', but do contain the letter 'g' and the letter 'h' in the first position.
`wordlist.py -i aef -c g -m h1

### 4) List all 5-letter words that do not contain the letters 'abef', do contain the letters 'ght', but do not contain the letter 'c' in the second position.
~wordlist.py -i abef -c ght -e c2

### 5) List all 5-letter words that contain an 'i' in the 2nd position, 'g' in the 3rd, 'h' in the 4th, and a 't' in the 5th.
`wordlist.py -m i2g3h4t5

