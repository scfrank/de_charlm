
This is a quick character language model (by default trained on German fiction
text). It uses SRILM, KenLM and leans heavily on:
http://victor.chahuneau.fr/notes/2012/07/03/kenlm.html

# Installation/setup

Uses Python3. KenLM requires the python3-dev packages (available on apt-get).

Virtualenv setup, in your project directory:
```
virtualenv -p python3 venv
source venv/bin/activate
```
Install dependencies (cython and kenlm). Note that kenlm needs to
support at least order 12. (I am not sure what the `-a` flag does.)
```
pip install cython
git clone https://github.com/vchahun/kenlm.git
cd kenlm
./bjam --max-kenlm-order=12
# compile LM estimation code
python setup.py install # install Python module
cd -
```
(There should be a way to compile kenlm with `--max-kenlm-order=12' to
enable better character language models but I couldn't get it to work
with the python interface.

# Usage

You probably want to use the LMQuerier in `query_lm.py':
```
from query_lm import LMQuerier

lmq = LMQuerier(lm_model)
lm_pplx = lmq.norm_score(example_string)
```

On the command line (where it will just do some basic testing),
`query_lm.py` takes a model name:

```
$python query_lm.py -h
usage: query_lm.py [-h] [--notlower] [--model MODEL]
```

Lowercasing the data is default. If the model is estimated on
non-lowercased data, you probably want to use the `notlower` flag.

The model can be an arpa-formatted LM from SRILM or one that's been binarised using kenlm (see below).

# Corpus

I'm using the later German novels in the [txtLAB450 corpus]
(http://txtlab.org/?p=601). These are included in the DE_19_novels.tar

The `tokchars.py` script needs to be pointed at the correct directory
(i.e.  where you've unpacked the corpus).

Any other corpus can be used but should be relatively clean since no
tokenisation (apart from possibly lowercasing) is performed.
The novels corpus is _not_ one sentence/line, which will add some
noise but hopefully nothing serious.

## Building a LM.
If you want to build a LM, you need srilm (you're on your own here).
The lm provided here was created using the following command:
```
ngram-count -order 12 -text de_chars -write-vocab de_char_vocab
-no-sos -no-eos -tolower -wbdiscount -lm char_de_wb_o12_low.lm
```
Note that Witten-Bell smoothing works with character distributions,
whereas Kneser-Ney fails (and is the reason why we can't use KenLM to
estimate the LM).

After building the LM, use KenLM to binarise it:
```
./kenlm/bin/build_binary char_de_wb_o12_low.lm char_de_wb_o12_low.lm.klm
```






