"""Module providing support vector machine and related functions"""

from sklearn.svm import SVC

def svm_model(train_features, train_targets):

    # Initialize the model with default parameters
    model = SVC()

    # Train the model
    model.fit(train_features, train_targets)

    return model
