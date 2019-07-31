SBD train/dev/test splits after:

    Gillick, D. 2009. Sentence boundary detection and the problem with the U.S.
    In _NAACL-HLT_, pages 241-244.

Gillick states that sections 03-06 of the WSJ portion of the Penn Treebank is a
standard dataset for this task. I use sections 00-02 for development and the 
remaining sections for training.

The WSJ data has never (as far as I know) been distributed in an untokenized
form. To create this data, I take the leaves of the parse trees and then 
"detokenize" using the Stanford NLP tokenizer in detokenization mode.
