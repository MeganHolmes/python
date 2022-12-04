"""Module providing KNN and related functions"""

from sklearn.neighbors import KNeighborsClassifier

def trainKNN(features_train, targets_train, k):

    # Instantiating the model (using the default parameters)
    knn = KNeighborsClassifier(n_neighbors=k)

    # Fitting the model with data
    knn.fit(features_train, targets_train)

    return knn,
