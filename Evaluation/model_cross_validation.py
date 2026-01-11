import random
import math
import numpy as np
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets


def get_model(method):
    model = None
    if method == "DecisionTreeClassifier":
        model = DecisionTreeClassifier(
        max_depth = 10,
        random_state = 42
    )
        
    elif method == "GaussianNB":
        model = GaussianNB()

    elif method == "LogisticRegression":
        model = LogisticRegression(
            penalty = 'l2',
            solver = 'lbfgs',
            random_state = 42,
            multi_class = 'multinomial'
        )

    elif method == "RandomForestClassifier":
        model = RandomForestClassifier(
            max_depth = 15,
            n_estimators = 250,
            random_state = 42
        )

    elif method == "XGBClassifier":
        model = XGBClassifier(
            max_depth = 7,
            random_state = 42
        )
    return model

def get_splits(n, k, seed):
    splits = None
    splits = []
    random.seed(seed)
    idx = list(range(n))
    random.shuffle(idx)

    cur = 0
    for i in range(k):
        size = n // k
        foldNumExtra = n % k
        if i < foldNumExtra:
            size += 1
        foldIdx = idx[cur:cur + size]
        splits.append(foldIdx)
        cur += size

    return splits

def my_cross_val(method, X, y, splits):
    errors = []
    for testIdx in splits:
        trainIdx = []
        for idx in range(len(X)):
            if idx not in testIdx:
                trainIdx.append(idx)
        trainIdx = np.array(trainIdx, dtype=int)
        testIdx = np.array(testIdx, dtype=int)
        if len(trainIdx) == 0:
            continue

        X_train = X[trainIdx]
        Y_train = y[trainIdx]
        X_test = X[testIdx]
        Y_test = y[testIdx]
        model = get_model(method)
        model.fit(X_train, Y_train)

        pred = model.predict(X_test)
        wrong = 0
        for i in range(len(Y_test)):
            if pred[i] != Y_test[i]:
                wrong += 1
        errRate = wrong / len(Y_test)
        errors.append(errRate)

    return np.array(errors)
