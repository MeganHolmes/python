"""Module providing logistic regression and related functions"""

from sklearn.linear_model import LogisticRegression

def trainLogisticRegression(features_train, targets_train):
    # Instantiating the model (using the default parameters)
    logreg = LogisticRegression()

    # Fitting the model with data
    logreg.fit(features_train, targets_train)

    return logreg
