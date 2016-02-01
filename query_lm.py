#!/usr/bin/python3

import argparse
import kenlm


KLM='char_de_wb_o6_low.lm.klm'

ex1 = 'Dies ist ein deutscher Satz'
ex2 = 'Ein Mann auf einem Fahrrad'
ex3 = 'Sie essen bald zu Abend'

exa = 'asdf kjwe iru xc'
exb = 'fewticlkjvi'
exc = 'this is an english sentence'
exd = 'please dont rate this as high as a german sentence'
exe = ''

class LMQuerier:

    def __init__(self, model_name, lowercase=True):
        self.model = kenlm.LanguageModel(model_name)
        self.lower = lowercase

    # Return length-normalised score
    def norm_score(self, example):
        s = self.model.score(example)
        if len(example) == 0:
          # return the LM score for zero-length inputs
          return s / 1
        else:
          chrs = len(example)/2 # bc spaces
          return s/chrs

    def char_string(self, example):
        if self.lower:
            ex = example.lower()
        ex = example.replace(' ', '@')
        chars = ' '.join(list(ex))
        return chars

    def test(self):
        good = [ex1, ex2, ex3]
        print("Good examples")
        for ex in good:
            l = self.char_string(ex)
            print('%s %s: %f' % (ex, '', self.norm_score(l)))

        bad = [exa, exb, exc, exd, exe]
        print("Bad examples")
        for ex in bad:
            l = self.char_string(ex)
            print('%s %s: %f' % (ex, '', self.norm_score(l)))


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
