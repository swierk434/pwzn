#python pwzn1.py ComunismManifesto.txt 10 5
#python pwzn1.py ComunismManifesto.txt 10 5
#python pwzn1.py ComunismManifesto.txt 10 0 --list the of and to in a The by is that
#python pwzn1.py ComunismManifesto.txt 10 0 --list the of and to in a The by is that --frases a i o --frases2 b c

import re
import collections
import rich
import argparse
from collections import defaultdict
from rich.progress import track
from ascii_graph import Pyasciigraph
from _collections_abc import Iterable 
collections.Iterable = Iterable

rich.get_console().clear()

def frases_in_token(token, frases):
    for frase in frases:
        if frase in token:
            return True
    return False

def frases_in_token2(token, frases):
    for frase in frases:
        if not frase in token:
            return False
    return True

parser = argparse.ArgumentParser()
parser.add_argument('file_name')
parser.add_argument('max_mords', type=int, default=10)
parser.add_argument('min_length', type=int ,default=0)
parser.add_argument('--list', nargs='+')
parser.add_argument('--frases', nargs='+')
parser.add_argument('--frases2', nargs='+')

args = parser.parse_args()

file_path = args.file_name

with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

tokens = re.findall(r'\b\w+\b', text)
Histogram = defaultdict(int)

for token in track(tokens):
    if len(token) >= args.min_length:
        if not token in args.list:
            if not frases_in_token(token, args.frases):
                if frases_in_token2(token, args.frases2):
                    Histogram[token] += 1

Histogram = sorted(Histogram.items(), key = lambda kv: kv[1], reverse=True)

graph = Pyasciigraph()

for line in graph.graph('Wyniki', Histogram[0:(args.max_mords-1)]):
    print(line)