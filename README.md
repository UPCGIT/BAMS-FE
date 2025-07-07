# BAMS-FE
If you use the code, please cite the paper:

J. Li, H. Sheng, M. Xu, S. Liu, and Z. Zeng, “BAMS-FE: Band-by-Band Adaptive Multiscale Superpixel Feature Extraction for Hyperspectral Image Classification,” IEEE Transactions on Geoscience and Remote Sensing, vol. 61, pp. 1–15, 2023, doi: 10.1109/TGRS.2023.3294227.

The feature extraction code of "BAMS-FE: Band-by-Band Adaptive Multiscale Superpixel Feature Extraction for Hyperspectral Image Classification". Here we provide two versions of the BAMS algorithm: one in Python and the other in MATLAB. The Python version requires calling MATLAB functions. The algorithm used in our paper is based on the Python version. The file ERS.m needs to call the entropy superpixels segmentation algorithm, which is available as an open-source algorithm on GitHub (https://github.com/mingyuliutw/EntropyRateSuperpixel). Please make sure to prepare this algorithm before running the code. 
## 2024.02.21更新
本次更新提交了一个demo，提交了由ERS编译而来的mex文件，本demo可以直接运行（前提是配置好python和matlab的环境）
