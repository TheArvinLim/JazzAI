# This sample code uses a standard scikit-learn algorithm, the Adaboost classifier.

# Your code must create a 'clf' variable. This clf must be a scikit-learn compatible
# classifier, ie, it should:
#  1. have at least fit(X,y) and predict(X) methods
#  2. inherit sklearn.base.BaseEstimator
#  3. handle the attributes in the __init__ function
#  4. have a classes_ attribute
#  5. have a predict_proba method (optional)
#     See: https://doc.dataiku.com/dss/latest/machine-learning/custom-models.html

from sklearn.base import BaseEstimator
import numpy as np
import pandas as pd

class NaiveModel(BaseEstimator):
    """This shows how you can create a custom model that implements BaseEstimator 
    """
    def fit(self, X, y):
        self.classes_ = pd.unique(y)

        return self
        
    def predict(self, X):
        D = self.predict_proba(X)
        return self.classes_[np.argmax(D, axis=1)]
    
    def predict_proba(self, X):
        # prob_matrix = np.random.random((X.shape[0], len(self.classes_))) 
        # row_sums = prob_matrix.sum(axis=1)
        # normalised_prob_matrix = prob_matrix / row_sums[:, np.newaxis]

        normalised_prob_matrix = np.zeros((X.shape[0], len(self.classes_))) + 1. / len(self.classes_)

        return normalised_prob_matrix