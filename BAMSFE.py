# -*- coding: UTF-8 -*-
import numpy as np
from sklearn.decomposition import PCA
import matlab.engine
import gc
eng=matlab.engine.start_matlab()
# from memory_profiler import profile


def performPCA(img, n_components):
    X = np.reshape(img, (img.shape[0] * img.shape[1], img.shape[-1]))
    X_centered = X - np.mean(X, axis=0)
    pca = PCA(n_components=n_components)
    pca.fit(X_centered)
    X_transformed = pca.transform(X_centered)
    img_reconstructed = np.reshape(X_transformed, (img.shape[0], img.shape[1], -1))
    X=None
    X_centered=None
    pca=None
    X_transformed=None
    gc.collect()
    return np.squeeze(img_reconstructed)

# @profile()
def BAMSFE(img, supersize_step=5, pca_per_v=0.99, threshold_a=0.01, pca_flag=True):
    if pca_flag:
        img_PCA = performPCA(img, n_components=pca_per_v)
    else:
        img_PCA = img
    superpixels_value_dstack = None
    if len(img_PCA.shape) == 3:
        # print('PCA保留波段数目：{}'.format(img_PCA.shape[-1]))
        superpixelsImgValue_list = []
        supersize_list_all = []
        flag = 0
        supersize_i = 0
        supersize = 0
        EV_list = []
        while flag < 2:
            supersize = supersize + supersize_step
            supernum = int(img_PCA.shape[0] * img_PCA.shape[1] / supersize / supersize)
            superpixelsLabel = eng.ERS(img_PCA, supernum)
            superpixelsImgValue = eng.getsuperpixelsvalue_matlab(superpixelsLabel, img_PCA)
            EV_v = eng.optimization_matlab(img_PCA, superpixelsImgValue)
            EV_list.append(EV_v)
            if supersize_i > 0:
                if (EV_list[supersize_i] / np.sum(EV_list) < threshold_a) or (EV_list[supersize_i] / EV_list[supersize_i - 1] > (1 - threshold_a)):
                    flag = 2
            if flag < 2:
                supersize_list_all.append(supersize)
                superpixelsImgValue_list.append(superpixelsImgValue)
                del superpixelsImgValue
                supersize_i = supersize_i + 1
                del superpixelsLabel
                del EV_v
                superpixelsImgValue = None
                gc.collect()
        superpixelsImgValue_list_array = np.array(superpixelsImgValue_list)
        for supersize_ii, supersize_ in enumerate(supersize_list_all):
            if supersize_ii == 0:
                superpixels_value_dstack = np.squeeze(superpixelsImgValue_list_array[supersize_ii, :, :, :])
            else:
                superpixels_value_dstack = np.dstack((superpixels_value_dstack, np.squeeze(superpixelsImgValue_list_array[supersize_ii, :, :, :])))

        del superpixelsImgValue_list
        del supersize_list_all
        del EV_list
        del superpixelsImgValue_list_array
        gc.collect()
        img_PCA = None

    else:
        # print('PCA保留波段数目：1')
        img_PCA = np.squeeze(img_PCA)
        superpixelsImgValue_list = []
        supersize_list_all = []
        flag = 0
        supersize_i = 0
        supersize = 0
        EV_list = []
        while flag < 2:
            supersize = supersize + supersize_step
            supernum = int(img.shape[0] * img.shape[1] / supersize / supersize)
            superpixelsLabel = eng.ERS(img_PCA, supernum)
            superpixelsImgValue = eng.getsuperpixelsvalue_matlab(superpixelsLabel, img_PCA)
            superpixelsImgValue_array = np.array(superpixelsImgValue).reshape(img_PCA.shape)
            EV_v = eng.optimization_matlab(img_PCA, superpixelsImgValue_array)
            EV_list.append(EV_v)
            if supersize_i > 0:
                if (EV_list[supersize_i] / np.sum(EV_list) < threshold_a) or (EV_list[supersize_i] / EV_list[supersize_i - 1] > (1 - threshold_a)):
                    flag = 2
            if flag < 2:
                supersize_list_all.append(supersize)
                superpixelsImgValue_list.append(superpixelsImgValue_array)
            supersize_i = supersize_i + 1
            del superpixelsLabel, superpixelsImgValue_array, EV_v
            gc.collect()
        superpixelsImgValue_list_array = np.array(superpixelsImgValue_list)
        for supersize_ii, supersize_ in enumerate(supersize_list_all):
            if supersize_ii == 0:
                superpixels_value_dstack = np.squeeze(superpixelsImgValue_list_array[supersize_ii, :, :])
            else:
                superpixels_value_dstack = np.dstack((superpixels_value_dstack, np.squeeze(superpixelsImgValue_list_array[supersize_ii, :, :])))
        gc.collect()
        del superpixelsImgValue_list, supersize_list_all, EV_list, superpixelsImgValue_list_array
        gc.collect()
        img_PCA = None

    eng.clear(nargout=0)
    eng.close()
    img_PCA = None
    return superpixels_value_dstack
