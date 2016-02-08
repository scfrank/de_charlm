#!/usr/bin/python3

import argparse
import kenlm


KLM='char_de_wb_o6_low.lm.klm'

ex1 = 'Dies ist ein deutscher Satz'
ex2 = 'Ein Mann auf einem Fahrrad'
ex3 = 'Sie essen bald zu Abend'
ex4 = 'kind mit "beyonce" und "hello kitty" hemd'
ex5 = 'Kind mit "Rezeptbuch" und auch ein "Unterirdische Gespenster" Hemd'
ex6 = "kind mit 'rezeptbuch' und auch ein 'unterirdische gespenster' hemd"

exa = 'asdf kjwe iru xc'
exb = 'fewticlkjvi'
exc = 'this is an english sentence'
exd = 'please dont rate this as high as a german sentence'
exe = ''
exf = ' '
exg = '.'


"""LM corpus has 'french quotes' (« »). We want to replace quotes in input
("") with these (or just strip them? Makes output less intelligible.) """
def replace_quotes(chars):
    while '"' in chars: # quotes (should!) come in pairs.
        chars = chars.replace('"', '«', 1)
        chars = chars.replace('"', '»', 1)
    return chars


class LMQuerier:

    def __init__(self, model_name, lowercase=True):
        self.model = kenlm.LanguageModel(model_name)
        self.lower = lowercase

    def query_lm(self, example, deal_with_quotes=True):
        ex = self.char_string(example, deal_with_quotes)
        return self.norm_score(ex)

    # Return length-normalised score
    def norm_score(self, example):
        s = self.model.score(example)
        # an empty string has a (low) 'unnormalised' score
        if len(example) > 0:
            chrs = len(example)/2 # bc spaces
            s = s/chrs
        return s

    def char_string(self, example, deal_with_quotes=True):
        if self.lower:
            ex = example.lower()
        ex = example.replace(' ', '@')
        if deal_with_quotes:
            ex = replace_quotes(ex)
        chars = ' '.join(list(ex))
        return chars

    def test(self):
        good = [ex1, ex2, ex3, ex4, ex5, ex6]
        print("Good examples")
        for ex in good:
            print('%s : %f' % (ex, self.query_lm(ex)))

        bad = [exa, exb, exc, exd, exe, exf, exg]
        print("Bad examples")
        for ex in bad:
            print('%s : %f' % (ex, self.query_lm(ex)))


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--notlower', action='store_true')
    parser.add_argument('--model', type=str)
    args = parser.parse_args()

    if not args.model:
        print('no model argument, using %s' % KLM)
        args.model = KLM

    lmq = LMQuerier(args.model, not args.notlower)
    lmq.test()
