#! /Users/nicolasvinurel/anaconda/envs/icutestenv
# -*- coding: utf-8 -*-

import polyglot
from polyglot.text import Text, Word

fichier = open('/Users/nicolasvinurel/Desktop/depot/revendication/static/vocabulaire/ennonce', 'r') 
text = fichier.read()
text = Text(text)
for word, tag in text.pos_tags:
	print(u"{:<16}{:>2}".format(word, tag))
fichier.close()
