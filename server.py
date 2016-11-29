from flask import Flask, Response, request
import pandas as pd
import numpy as np
from transliterate import translit, get_available_language_codes
import json
import os
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import re, collections
import jellyfish
from itertools import product


newcorpus = PlaintextCorpusReader('/home/ilia/Documents/IE/03.NLP/assignment/final/corpus/', '.*')

app = Flask(__name__)
 
@app.route("/spell")
def hello():
    return "NLP GROUP B!"


@app.route('/toutf', methods=['GET', 'POST'])
def toUtf():
    utf_ = request.get_json(force=True)
    #utf_ = utf_['some']
    if('utf' in utf_):
        utf = translit(utf_['utf'], 'ka', reversed=True)
        print(utf)
        response_ = pd.Series(utf, index=['resp'])
        response = Response(response_.to_json())
        
    elif('sdx' in utf_):
        utf = call_soundex(tkn_utf(utf_['sdx']))
        print(utf)
        response_ = pd.Series(utf)
        print(response_)
        response = Response(response_.to_json())
    elif('malformed' in utf_):
        utf = identify_malformed(utf_['malformed'])
        print('utf:',utf)
        response_ = pd.Series(utf)
        print('respone:',response_)
        response = Response(response_.to_json())
    elif('features' in utf_):
        ftrs = {}
        utf = identify_malformed(utf_['features'])
        print(utf)
        for w in utf:
            ftrs[w] = lv_dist(call_soundex(tkn_utf(w)).values())
        #print(ftrs)
        response_ = pd.Series(ftrs)
        print('respone:',response_)
        response = Response(response_.to_json())
    elif('self' in utf_):
        utf_m = identify_malformed(utf_['self'])
        utf = []
        for w in utf_m:
            utf.append(tkn_utf(w)[0])
        utf_f = final(utf)
        print(utf_f)
        # for w in utf:
        #     ftrs[w] = lv_dist(call_soundex(tkn_utf(w)).values())
        # #print(ftrs)
        response_ = pd.Series(utf_f)
        print('respone:',response_)
        response = Response(response_.to_json())
    elif('togeo' in utf_):
        utf_m = utf_['togeo']
        utf = []
        for w in utf_m:
            utf.append(translit(w, 'ka'))
        print(utf)
        # for w in utf:
        #     ftrs[w] = lv_dist(call_soundex(tkn_utf(w)).values())
        # #print(ftrs)
        response_ = pd.Series(utf)
        print('respone:',response_)
        response = Response(response_.to_json())
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

def utf_corpus():
    utf_corp = []
    for w in newcorpus.words():
        utf_corp.append(translit(w.lower(), 'ka', reversed=True))
    return utf_corp

def tkn_utf(txt):
    return list(translit(w.lower(), 'ka', reversed=True) for w in txt.split(' ') if w.isalpha())

def tkn(txt):
    return set(w.lower() for w in txt.split(' ') if w.isalpha())


def identify_malformed(txt):
    malformed_ = set(tkn(txt))
    malformed = list(malformed_.difference(newcorpus.words()))
    print('malformed:',malformed)
    return malformed


def get_soundex(name):
    name = name.upper()
    soundex = ''
    soundex += name[0]
    dictionary = {"BFPV": "1", "CGJKQSXZ":"2", "DT":"3", "L":"4", "MN":"5", "R":"6", "AEIOUHWY":"."}
    for char in name[1:]:
        for key in dictionary.keys():
            if char in key:
                code = dictionary[key]
                if code != soundex[-1]:
                    soundex += code
    soundex = soundex.replace('.', '')
    soundex = soundex[:4].ljust(4, '0')
    return soundex

def call_soundex(lst):
    sdx = {}
    for i in range(0, len(lst)):
        sdx[str(lst[i])+'-'+str(i)] = get_soundex(lst[i])
    #print(sdx)
    return sdx

def lv_dist(mlf):
    mlf = list(mlf)[0]
    dst = []
    for wrd in newcorpus.words():
        dst.append(jellyfish.levenshtein_distance(mlf, wrd))
    return dst

def final(mlf):
    print(mlf)
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    sdx_input = call_soundex(mlf)
    sdx_raw = call_soundex(utf_corpus())
    for (i, j), (k, v) in product(sdx_input.items(), sdx_raw.items()):
        l1.append(i.split('-')[0])
        l2.append(j)
        l3.append(k.split('-')[0])
        l4.append(v)
        l5.append(jellyfish.levenshtein_distance(j, v))
        l6.append(jellyfish.levenshtein_distance(i.split('-')[0], k.split('-')[0]))
    df = pd.DataFrame(np.nan, index=range(0, len(l1)), columns=['wrd', 'sx_wrd', 'cpr', 'sx_cpr', 'sx_dist', 'lv_dist',])
    df['wrd'] = l1
    df['sx_wrd'] = l2
    df['cpr'] = l3
    df['sx_cpr'] = l4
    df['sx_dist'] = l5
    df['lv_dist'] = l6
    print(df.head(5))
    
    min_df_lv = df[df['lv_dist']<=2]
    
    selected = []
    for i in range(0, len(mlf)):
        if len(mlf[i]) > 0:
            x = min_df_lv[min_df_lv['wrd'] == list(mlf)[i]].sort_values(by='sx_dist', ascending=False).head(10)
            #print(x)
            s = x.groupby(['cpr'])['wrd'].transform('count')
            selected.append(x['cpr'].ix[s.idxmax()])
            print(x['cpr'].ix[s.idxmax()])
    return selected


if __name__=="__main__":
    app.run()