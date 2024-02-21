import numpy as np
from scipy import io as scio
from BAMSFE_BAMS import BAMSFE
from utils import svm_classifier, randomForest, sample_gt, scale_image_for_bands

img=scio.loadmat('Indian_pines_corrected.mat')['indian_pines_corrected']
gt=scio.loadmat('Indian_pines_gt.mat')['indian_pines_gt']

img_bamsfe=BAMSFE(img=img, supersize_step=5, pca_per_v=0.99, threshold_a=0.01, pca_flag=True)

train_gt, test_gt=sample_gt(gt=gt, train_size=5, mode='random')

pred_gt, classifier_model = svm_classifier(scale_image_for_bands(img_bamsfe), train_gt, test_gt)
preded_img = classifier_model.predict(scale_image_for_bands(img_bamsfe).reshape([-1, img_bamsfe.shape[-1]]))
preded_img = preded_img.reshape(gt.shape[0], gt.shape[1])
pred_gt = preded_img[gt > 0]
y_test = gt[gt > 0]
print('SVM分类器的OA值: {}'.format(np.sum(y_test==pred_gt)/len(y_test))) 
       
pred_gt, classifier_model, random_forest_feature_improtance = randomForest(img_bamsfe, train_gt, test_gt)
preded_img = classifier_model.predict(img_bamsfe.reshape([-1, img_bamsfe.shape[-1]]))
preded_img = preded_img.reshape(gt.shape[0], gt.shape[1])
pred_gt = preded_img[gt > 0]
y_test = gt[gt > 0]
print('RF分类器的OA值: {}'.format(np.sum(y_test==pred_gt)/len(y_test)))




