import unittest
from nose.tools import eq_, assert_almost_equals, assert_greater_equal
from hw2_utils import preproc, clf_base, constants, hand_weights, evaluation, naive_bayes
import numpy as np
from collections import Counter

LYRICS_DEV_CSV = 'lyrics-dev.csv'
LYRICS_TRAIN_CSV = 'lyrics-train.csv'

# LYRICS_DEV_CSV = 'lyrics-mini.csv'
# LYRICS_TRAIN_CSV = 'lyrics-dev.csv'

class TestClfBase(unittest.TestCase):

    def setUp(self):
        global x_tr, y_tr, x_dv, y_dv, counts_tr, x_dv_pruned, x_tr_pruned, x_bl_pruned
        global labels
        global vocab

        y_tr,x_tr = preproc.read_data(LYRICS_TRAIN_CSV,preprocessor=preproc.bag_of_words)
        labels = set(y_tr)

        counts_tr = preproc.aggregate_counts(x_tr)

        y_dv,x_dv = preproc.read_data(LYRICS_DEV_CSV,preprocessor=preproc.bag_of_words)

        x_tr_pruned, vocab = preproc.prune_vocabulary(counts_tr, x_tr, 10)
        x_dv_pruned, _ = preproc.prune_vocabulary(counts_tr, x_dv, 10)

    def test_d2_1_featvec(self):
        label = '1980s'
        fv = clf_base.make_feature_vector({'test':1,'case':2},label)
        eq_(len(fv),3)
        eq_(fv[(label,'test')],1)
        eq_(fv[(label,'case')],2)
        eq_(fv[(label,constants.OFFSET)],1)

    def test_d2_2_predict(self):
        global x_tr_pruned, x_dv_pruned, y_dv

        print(x_tr_pruned[0])
        y_hat,scores = clf_base.predict(x_tr_pruned[0],hand_weights.theta_hand,labels)
        eq_(scores['pre-1980'],0.1)
        assert_almost_equals(scores['2000s'],1.3,places=5)
        eq_(y_hat,'2000s')
        eq_(scores['1980s'],0.0)

        y_hat = clf_base.predict_all(x_dv_pruned,hand_weights.theta_hand,labels)
        assert_almost_equals(evaluation.acc(y_hat,y_dv),.3422222, places=5)

    @unittest.skip("does't use setup")
    def test_d2_2_predict_steve(self):
        _labels = set(['1980s', '1990s', 'pre-1980', '2000s'])
        bf = Counter({'come': 28, 'on': 28, 'you': 18, 'show': 17, 'the': 16, 'let': 15, 'me': 15, 'where': 15, 'its': 15, 'at': 15, 'like': 12, 'i': 11, 'of': 7, 'place': 7, 'name': 6, 'is': 6, 'it': 6, 'that': 6, 'ah': 5, 'they': 4, 'and': 4, 'oh': 3, 'said': 2, 'wanna': 2, 'take': 2, 'all': 2, 'blues': 2, 'was': 2, 'shoutin': 2, 'go': 2, 'wow': 1, 'whoa': 1, 'got': 1, 'a': 1, 'little': 1, 'track': 1, 'sally': 1, 'ill': 1, 'sue': 1, 'were': 1, 'gonna': 1, 'rock': 1, 'away': 1, 'our': 1, 'last': 1, 'time': 1, 'down': 1, 'lost': 1, 'my': 1, 'shoes': 1, 'had': 1, 'some': 1, 'cat': 1, 'people': 1, 'yellin': 1, 'for': 1, 'more': 1, 'kept': 1, 'sayin': 1, 'man': 1})

        # print(x_tr_pruned[0])

        y_hat, scores = clf_base.predict(bf,hand_weights.theta_hand,_labels)
        assert_almost_equals(scores['2000s'], 1.3, places=5)
        eq_(y_hat, '2000s')
        eq_(scores['pre-1980'],0.1)
        eq_(scores['1980s'],0.0)

        # y_hat = clf_base.predict_all(x_dv_pruned,hand_weights.theta_hand,labels)
        # assert_almost_equals(evaluation.acc(y_hat,y_dv),.3422222, places=5)

    def test_d3_1_corpus_counts(self):
        # public
        iama_counts = naive_bayes.get_corpus_counts(x_tr_pruned,y_tr,"1980s");
        eq_(iama_counts['today'],50)
        eq_(iama_counts['yesterday'],14)
        eq_(iama_counts['internets'],0)

    def test_d3_2_pxy(self):
        global vocab, x_tr_pruned, y_tr

        # check that distribution normalizes to one
        #log_pxy = naive_bayes.estimate_pxy(x_tr_pruned, y_tr, "1980s", 0.1, vocab)
        log_pxy = naive_bayes.estimate_pxy(x_tr_pruned,y_tr,"1980s",0.1,vocab)
        assert_almost_equals(np.exp(list(log_pxy.values())).sum(),1)

        # check that values are correct
        assert_almost_equals(log_pxy['money'],-7.6896,places=3)
        assert_almost_equals(log_pxy['fly'],-8.6369,places=3)

        log_pxy_more_smooth = naive_bayes.estimate_pxy(x_tr_pruned,y_tr,"1980s",10,vocab)
        assert_almost_equals(log_pxy_more_smooth['money'],-7.8013635125541789,places=3)
        assert_almost_equals(log_pxy_more_smooth['tonight'], -6.4054072405225515,places=3)

    def test_d3_3a_nb(self):
        global x_tr_pruned, y_tr

        theta_nb = naive_bayes.estimate_nb(x_tr_pruned,y_tr,0.1)

        y_hat,scores = clf_base.predict(x_tr_pruned[55],theta_nb,labels)
        assert_almost_equals(scores['2000s'],-1840.5064690929203,places=3)
        eq_(y_hat,'1980s')

        y_hat,scores = clf_base.predict(x_tr_pruned[155],theta_nb,labels)
        assert_almost_equals(scores['1980s'], -2153.0199277981355, places=3)
        eq_(y_hat,'2000s')

    def test_d3_3b_nb(self):
        global y_dv
        y_hat_dv = evaluation.read_predictions('nb-dev.preds')
        assert_greater_equal(evaluation.acc(y_hat_dv,y_dv),.46)

    def test_d3_4a_nb_best(self):
        global x_tr_pruned, y_tr, x_dv_pruned, y_dv
        vals = np.logspace(-3,2,11)
        best_smoother, scores = naive_bayes.find_best_smoother(x_tr_pruned,y_tr,x_dv_pruned,y_dv,[1e-3,1e-2,1e-1,1])
        assert_greater_equal(scores[.1],.46)
        assert_greater_equal(scores[.01],.45)



