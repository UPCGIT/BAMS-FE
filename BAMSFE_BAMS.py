# -*- coding: UTF-8 -*-
import numpy as np
from sklearn.decomposition import PCA
import matlab.engine
import gc
import matplotlib.pyplot as plt
eng=matlab.engine.start_matlab()
matlab_add_path="addpath(genpath(cd(cd(cd(cd)))))"
eng.eval(matlab_add_path)


def performPCA(img, n_components, eigValuesFlag=False):
    if img.ndim == 3:
        X = np.reshape(img, (img.shape[0] * img.shape[1], img.shape[-1]))
    else:
        X = np.reshape(img, (-1, 1))

    X_centered = X - np.mean(X, axis=0)
    
    pca = PCA(n_components=n_components)
    pca.fit(X_centered)
    
    # Extract eigenvalues
    eigenvalues = pca.explained_variance_
    
    X_transformed = pca.transform(X_centered)
    img_reconstructed = np.squeeze(np.reshape(X_transformed, (img.shape[0], img.shape[1], -1)))
    
    X = None
    X_centered = None
    pca = None
    X_transformed = None
    gc.collect()
    if eigValuesFlag:
        return np.squeeze(img_reconstructed), eigenvalues[:img_reconstructed.shape[-1]]
    else:
        return np.squeeze(img_reconstructed)


# @profile()
def BAMSFE(img, supersize_step=5, pca_per_v=0.99, threshold_a=0.01,lambda_v=0.5, sigma=5,pca_flag=True, supersizeReturn=False, args=None, segLabel=False):
    if pca_flag:
        img_PCA = performPCA(img, n_components=pca_per_v)
    else:
        img_PCA = img
    superpixels_value_dstack = None
    if len(img_PCA.shape) == 3:
        # print('PCA保留波段数目：{}'.format(img_PCA.shape[-1]))
        superpixelsImgValue_list = []
        superpixelsLabel_list=[]
        supersize_list_all = []
        flag = 0
        supersize_i = 0
        supersize = 0
        EV_list = []
        while flag < 2:
            supersize = supersize + supersize_step
            supernum = int(img_PCA.shape[0] * img_PCA.shape[1] / supersize / supersize)
            superpixelsLabel = eng.ERS_BAMS(eng.double(img_PCA), eng.double(supernum), eng.double(lambda_v), eng.double(sigma))
            superpixelsImgValue = eng.getsuperpixelsvalue_matlab_BAMS(eng.double(superpixelsLabel), eng.double(img_PCA))
            EV_v = eng.optimization_matlab_BAMS(eng.double(img_PCA), eng.double(superpixelsLabel))
            EV_list.append(EV_v)
            if supersize_i > 0:
                if (EV_list[supersize_i] / np.sum(EV_list) < threshold_a) or (EV_list[supersize_i] / EV_list[supersize_i - 1] > (1 - threshold_a)):
                    flag = 2
            if flag < 2:
                supersize_list_all.append(supersize)
                superpixelsImgValue_list.append(superpixelsImgValue)
                superpixelsLabel_list.append(superpixelsLabel)
                del superpixelsImgValue
                supersize_i = supersize_i + 1
                del superpixelsLabel
                del EV_v
                gc.collect()
        superpixelsImgValue_list_array = np.array(superpixelsImgValue_list)
        superpixelsLabel_list_array=np.array(superpixelsLabel_list)
        for supersize_ii, supersize_ in enumerate(supersize_list_all):
            if supersize_ii == 0:
                superpixels_value_dstack = np.squeeze(superpixelsImgValue_list_array[supersize_ii, :, :, :])
                superpixels_label_dstack=np.squeeze(superpixelsLabel_list_array[supersize_ii, :,:,:])
            else:
                superpixels_value_dstack = np.dstack((superpixels_value_dstack, np.squeeze(superpixelsImgValue_list_array[supersize_ii, :, :, :])))
                superpixels_label_dstack=np.dstack((superpixels_label_dstack, np.squeeze(superpixelsLabel_list_array[supersize_ii, :,:,:])))

        if args:
            plt.plot(np.arange(len(EV_list)), EV_list)
            plt.savefig(args.figuresavepath+'EV_list'+args.figure_name+'.svg')
            plt.close()
        del superpixelsImgValue_list
        del EV_list
        del superpixelsImgValue_list_array
        gc.collect()
        img_PCA = None

    else:
        # print('PCA保留波段数目：1')
        img_PCA = np.squeeze(img_PCA)
        superpixelsImgValue_list = []
        superpixelsLabel_list=[]
        supersize_list_all = []
        flag = 0
        supersize_i = 0
        supersize = 0
        EV_list = []
        while flag < 2:
            supersize = supersize + supersize_step
            supernum = int(img.shape[0] * img.shape[1] / supersize / supersize)
            superpixelsLabel = eng.ERS_BAMS(eng.double(img_PCA), eng.double(supernum), eng.double(lambda_v), eng.double(sigma))
            superpixelsImgValue = eng.getsuperpixelsvalue_matlab_BAMS_pro(eng.double(superpixelsLabel), eng.double(img_PCA))
            superpixelsImgValue_array = np.array(superpixelsImgValue).reshape(img_PCA.shape)
            EV_v = eng.optimization_matlab_BAMS(eng.double(img_PCA), eng.double(superpixelsLabel))
            EV_list.append(EV_v)
            if supersize_i > 0:
                if (EV_list[supersize_i] / np.sum(EV_list) < threshold_a) or (EV_list[supersize_i] / EV_list[supersize_i - 1] > (1 - threshold_a)):
                    flag = 2
            if flag < 2:
                supersize_list_all.append(supersize)
                superpixelsImgValue_list.append(superpixelsImgValue_array)
                superpixelsLabel_list.append(superpixelsLabel)
            supersize_i = supersize_i + 1
            del superpixelsLabel, superpixelsImgValue_array, EV_v
            gc.collect()
        superpixelsImgValue_list_array = np.array(superpixelsImgValue_list)
        superpixelsLabel_list_array=np.array(superpixelsLabel_list)
        for supersize_ii, supersize_ in enumerate(supersize_list_all):
            if supersize_ii == 0:
                superpixels_value_dstack = np.squeeze(superpixelsImgValue_list_array[supersize_ii, :, :])
                superpixels_label_dstack=np.squeeze(superpixelsLabel_list_array[supersize_ii, :,:])
            else:
                superpixels_value_dstack = np.dstack((superpixels_value_dstack, np.squeeze(superpixelsImgValue_list_array[supersize_ii, :, :])))
                superpixels_label_dstack=np.dstack((superpixels_label_dstack, np.squeeze(superpixelsLabel_list_array[supersize_ii, :,:])))
        gc.collect()
        del superpixelsImgValue_list,  EV_list, superpixelsImgValue_list_array
        gc.collect()
        img_PCA = None

    eng.clear(nargout=0)
    eng.close()
    img_PCA = None
    if supersizeReturn:
        return superpixels_value_dstack, supersize_list_all
    elif segLabel:
        return superpixels_label_dstack
    else:
        return superpixels_value_dstack


