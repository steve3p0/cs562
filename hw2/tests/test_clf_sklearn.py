from nose.tools import eq_, ok_, assert_almost_equals
from hw2_utils import preproc, clf_sklearn, evaluation
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


def setup_module():
    global vocab, label_set, x_tr_pruned, df_train, df_dev, df_test, count_vec

    y_tr,x_tr = preproc.read_data('lyrics-train.csv',preprocessor=preproc.bag_of_words)
    labels = set(y_tr)

    counts_tr = preproc.aggregate_counts(x_tr)

    x_tr_pruned, vocab = preproc.prune_vocabulary(counts_tr, x_tr, 10)

    label_set = sorted(list(set(y_tr)))

    df_train = pd.read_csv('lyrics-train.csv')
    df_dev = pd.read_csv('lyrics-dev.csv')
    df_test = pd.read_csv('lyrics-test-hidden.csv')
    
    count_vec = CountVectorizer(vocabulary=vocab)

def test_d5_1_train_logistic():
    global count_vec, df_train, df_dev
    
    count_vec = CountVectorizer(vocabulary=vocab)
    
    X_train = count_vec.transform(df_train.Lyrics)
    
    mod = clf_sklearn.train_logistic_regression(X_train, df_train.Era)
    
    # try predicting
    X_dev = count_vec.transform(df_dev.Lyrics)
    y_hat_dev = mod.predict(X_dev)
    
    acc = evaluation.acc(y_hat_dev, df_dev.Era)
    assert_almost_equals(acc, 0.47, places=1)
    
def test_d5_2_tf_idf():
    global count_vec, vocab, df_train, df_dev, df_test
    
    count_vec = CountVectorizer(vocabulary=vocab)
    
    train_counts = count_vec.transform(df_train.Lyrics)
    dev_counts = count_vec.transform(df_dev.Lyrics)
    test_counts = count_vec.transform(df_test.Lyrics)
    
    (train_tfidf, dev_tfidf, test_dfidf), tf_transformer = clf_sklearn.transform_tf_idf(train_counts, dev_counts, test_counts)
    
    # test whether tf/idf was trained properly:
    short_song = count_vec.transform(["you and me and you"])
    shorter_song = count_vec.transform(["you and me and"])
    
    short_song_tfidf = tf_transformer.transform(short_song)
    shorter_song_tfidf = tf_transformer.transform(shorter_song)
    
    assert_almost_equals(short_song_tfidf.toarray()[0,0], 0.66, places=2)
    assert_almost_equals(shorter_song_tfidf.toarray()[0,0], 0.40, places=2)
    
    
    mod = clf_sklearn.train_logistic_regression(train_tfidf, df_train.Era)
    y_hat_dev = mod.predict(dev_tfidf)
    
    acc = evaluation.acc(y_hat_dev, df_dev.Era)
    assert_almost_equals(acc, 0.5, places=1)
    