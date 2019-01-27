from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfTransformer

# deliverable 5.1
def train_logistic_regression(X, y):
    """
    Train a Logistic Regression classifier
    
    Pay attention to the mult_class parameter to control how the classifier handles multinomial situations!
    
    :params X: a sparse matrix of features
    :params y: a list of instance labels
    :returns: a trained logistic regression classifier
    :rtype sklearn.linear_model.LogisticRegression
    """
    raise NotImplementedError

def transform_tf_idf(X_train_counts, X_dev_counts, X_test_counts):
    """
    :params X_train_counts: the bag-of-words matrix producd by CountVectorizer for the training split
    :params X_dev_counts: the same, but for the dev split
    :params X_test_counts: ditto, for the test split
    :returns: a tuple of tf-idf transformed count matrices for train/dev/test (in that order), as well as the resulting transformer
    :rtype ((sparse, sparse, sparse), TfidfTransformer)
    """
    raise NotImplementedError
