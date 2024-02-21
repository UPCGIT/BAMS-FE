import numpy as np
import time
import math
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

def scale_image_for_bands(image, per=0):
    if image.ndim == 3:
        min_values = np.percentile(image, per, axis=(0, 1))
        max_values = np.percentile(image, 100 - per, axis=(0, 1))
        scaled_image = (image - min_values) / (max_values - min_values)
    elif image.ndim == 2:
        min_values = np.percentile(image, per)
        max_values = np.percentile(image, 100 - per)
        scaled_image = (image - min_values) / (max_values - min_values)
    return scaled_image

def svm_classifier(img, train_gt, test_gt):

    x_train = img[train_gt > 0].reshape(-1, img.shape[-1])
    x_test = img[test_gt > 0].reshape(-1, img.shape[-1])
    y_train = train_gt[train_gt > 0].reshape(-1, 1).ravel()
    svm_model_final = svm.SVC(kernel='rbf', probability=False,random_state=0,C=1024, gamma=0.125)
    svm_model_final.fit(x_train, y_train)
    svm_predict = svm_model_final.predict(x_test)
    x_test = None
    x_train = None
    y_train=None
    return svm_predict, svm_model_final


def randomForest(img, train_gt, test_gt=[]):
    x_train = img[train_gt > 0].reshape(-1, img.shape[-1])
    if len(test_gt)>0:
        x_test = img[test_gt > 0].reshape(-1, img.shape[-1])
    y_train = train_gt[train_gt > 0].reshape(-1, 1).ravel()
    random_forest_model_test_random=RandomForestClassifier(random_state=0)
    random_forest_model_test_random.fit(x_train, y_train)
    if len(test_gt)>0:
        random_forest_predict=random_forest_model_test_random.predict(x_test)
    importances=random_forest_model_test_random.feature_importances_
    indices=np.argsort(importances)[::-1]
    importances=None
    x_test = None
    x_train = None
    y_train=None
    if len(test_gt)>0:
        return random_forest_predict, random_forest_model_test_random, indices
    else:
        return  random_forest_model_test_random, indices


def sample_gt(gt, train_size, mode="random", less_choice_per=0.5):
    """
    Extract a fixed precentage of samples from an array of labels
    :param gt: a 2D array of int labels
    :param train_size: [0,1] float
    :param mode:
    :return: train_gt, test_gt (2D array of int labels)
    """
    indices = np.nonzero(gt)
    X = list(zip(*indices))
    y = gt[indices].ravel()
    train_gt = np.zeros_like(gt)
    test_gt = np.zeros_like(gt)
    if gt.ndim == 2:
        if mode == "random":
            if train_size >= 1:
                data_label = gt.reshape(gt.shape[0] * gt.shape[1])
                train_gt = np.zeros_like(data_label)
                test_gt = data_label.copy()
                data_location = np.arange(data_label.shape[0])
                train_size = int(train_size)
                for i in np.unique(y):
                    if train_size >= np.sum(data_label == i):
                        train_size_class = math.ceil(np.sum(data_label == i)*less_choice_per)
                        replaceOptions = False
                    else:
                        train_size_class = train_size
                        replaceOptions = False
                    np.random.seed(int(time.time()))
                    choice_train_location = np.random.choice(data_location[data_label == i], min(train_size_class, np.sum(data_label == i)), replace=replaceOptions)
                    train_gt[choice_train_location] = i
                    test_gt[choice_train_location] = 0
                    choice_train_location = None
                train_gt = train_gt.reshape(gt.shape[0], gt.shape[1])
                test_gt = test_gt.reshape(gt.shape[0], gt.shape[1])
                train_size = None
                data_location = None
                data_label = None
            else:
                data_label = gt.reshape(gt.shape[0] * gt.shape[1])
                train_gt = np.zeros_like(data_label)
                test_gt = data_label.copy()
                data_location = np.arange(data_label.shape[0])
                for i in np.unique(y):
                    replaceOptions = False
                    np.random.seed(int(time.time()))
                    choice_train_location = np.random.choice(data_location[data_label == i], math.ceil(train_size * np.sum(data_label == i)), replace=replaceOptions)
                    train_gt[choice_train_location] = i
                    test_gt[choice_train_location] = 0
                train_gt = train_gt.reshape(gt.shape[0], gt.shape[1])
                test_gt = test_gt.reshape(gt.shape[0], gt.shape[1])
                data_location = None
                data_label = None
        elif mode == "disjoint":
            test_gt = np.copy(gt)
            for c in np.unique(gt):
                mask = gt == c
                for x in range(gt.shape[0]):
                    first_half_count = np.count_nonzero(mask[:x, :])
                    second_half_count = np.count_nonzero(mask[x:, :])
                    try:
                        ratio = first_half_count / (second_half_count + first_half_count)
                        if ratio > train_size - 0.05 and ratio < train_size + 0.05:
                            break
                    except ZeroDivisionError:
                        continue
                        ratio = None
                    second_half_count = None
                    first_half_count = None
                mask[:x, :] = 0
                train_gt[mask] = 0
                mask = None
            test_gt[train_gt > 0] = 0
        else:
            raise ValueError("{} sampling is not implemented yet.".format(mode))
        y = None
        X = None
        indices = None
    elif gt.ndim == 1:
        if mode == "random":
            if train_size >= 1:
                data_label = gt
                train_gt = np.zeros_like(data_label)
                test_gt = data_label.copy()
                data_location = np.arange(data_label.shape[0])
                train_size = int(train_size)
                for i in np.unique(y):
                    if train_size >= np.sum(data_label == i):
                        train_size_class = math.ceil(np.sum(data_label == i) / 2)
                        replaceOptions = False
                    else:
                        train_size_class = train_size
                        replaceOptions = False
                    np.random.seed(int(time.time()))
                    choice_train_location = np.random.choice(data_location[data_label == i], min(train_size_class, np.sum(data_label == i)), replace=replaceOptions)
                    train_gt[choice_train_location] = i
                    test_gt[choice_train_location] = 0
                    choice_train_location = None
            else:
                data_label = gt
                train_gt = np.zeros_like(data_label)
                test_gt = data_label.copy()
                data_location = np.arange(data_label.shape[0])
                for i in np.unique(y):
                    replaceOptions = False
                    np.random.seed(int(time.time()))
                    choice_train_location = np.random.choice(data_location[data_label == i], math.ceil(train_size * np.sum(data_label == i)), replace=replaceOptions)
                    train_gt[choice_train_location] = i
                    test_gt[choice_train_location] = 0
                data_location = None
                data_label = None
    return train_gt, test_gt