"""Module providing naive bayes and related functions"""

from sklearn.naive_bayes import GaussianNB

def naive_bayes_model(train_features, train_targets):

    # Initialize the model with default parameters
    model = GaussianNB()

    # Train the model
    model.fit(train_features, train_targets)

    return model
