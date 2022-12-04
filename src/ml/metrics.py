"""Module providing ML metrics functions"""

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import recall_score, f1_score,plot_confusion_matrix

def printStandardMetrics(targets_test, test_predictions):

    cnfMatrix = confusion_matrix(targets_test, test_predictions,
         normalize='true')
    print('Confusion Matrix\n', cnfMatrix)

    # TN / (TP + FP)
    specificity = cnfMatrix[1, 1] / (cnfMatrix[0, 0] + cnfMatrix[1, 0])
    accuracy = accuracy_score(targets_test, test_predictions)
    recall = recall_score(targets_test, test_predictions)

    # Print Evaluation Metrics
    print("Accuracy:",accuracy)

    # (true positive rate)
    print("Sensitivity / Recall:", recall)

    # (true negative rate)
    print("Specificity:",specificity)

    # print("F1 Score:",f1_score(targets_test, test_predictions))

    return accuracy, recall, specificity
