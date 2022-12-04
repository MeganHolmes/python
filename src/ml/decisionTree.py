"""Module providing decision tree and related functions"""

from sklearn.tree import DecisionTreeClassifier

def trainDecisionTree(train_features, train_targets):

    # Initialize the model with default parameters
    model = DecisionTreeClassifier()

    # Train the model
    model.fit(train_features, train_targets)

    return model
