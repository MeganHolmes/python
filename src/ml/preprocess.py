"""Module providing preprocessing functions for ML"""

from sklearn.impute import SimpleImputer
import numpy

def fixMissingValuesWithMean(dataset):
    """Fix missing values in dataset using mean strategy"""
    imp = SimpleImputer(missing_values=numpy.nan, strategy='mean')
    imp = imp.fit(dataset)
    return imp.transform(dataset)
