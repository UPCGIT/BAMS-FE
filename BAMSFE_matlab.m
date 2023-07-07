function superpixels_value_dstack=BAMSFE_matlab(img, supersize_step, pca_per_v, threshold_a, pca_flag)
% img: input data, rows*cols or rows*cols*channels
% supersize_step: the start scale and the scale step for superpixels segmentation
% pca_per_v: the number or cumulative percentage for pca projection; if pca_per_v>=1 and isint(pca_per_v) it means the pca transform will save pca_per_v compents; else if pca_per_v<1, it means the cumulative percentage will be used
% threshold_a: the threshold of EV, the smaller of this value it will lead to more scale segmentation
% pca_flag: true or false, true means apply pca transform while false means no pca transform will be applyed.
% out:superpixels_value_dstack with shape of rows*cols*featureNumbers
if pca_flag
    imgPCA=performPCA_matlab(img, pca_per_v);
else
    imgPCA=img;
end
superpixels_value_dstack=[];
if numel(size(imgPCA))==3
    superpixelsImgValue_list={};
    supersize_list_all={};
    flag=0;
    supersize_i=1;
    supersize=0;
    EV_list={};
    while flag<2
        supersize=supersize+supersize_step;
        supernum=floor(size(imgPCA,1)*size(imgPCA,2)/supersize/supersize);
        superpixelsLabel=ERS(imgPCA, supernum);
        superpixelsImgValue=getsuperpixelsvalue_matlab(superpixelsLabel, imgPCA);
        EV_v=optimization_matlab(imgPCA, superpixelsImgValue);
        EV_list{end+1}=EV_v;
        if supersize_i>1
            if EV_list{supersize_i}/sum(cell2mat(EV_list))<threshold_a || EV_list{supersize_i}/EV_list{supersize_i-1}>1-threshold_a
                flag=2;
            end
        end
        if flag<2
            supersize_list_all{end+1}=supersize;
            superpixelsImgValue_list{end+1}=superpixelsImgValue;
        end
        supersize_i=supersize_i+1;
        clear superpixelsImgValue superpixelsLabel EV_v
    end
    superpixelsImgValue_list_array=cat(3, superpixelsImgValue_list{:});
    superpixels_value_dstack=superpixelsImgValue_list_array;
else
    imgPCA=squeeze(imgPCA);
    superpixelsImgValue_list={};
    supersize_list_all={};
    flag=0;
    supersize_i=1;
    supersize=0;
    EV_list={};
    while flag<2
        supersize=supersize+supersize_step;
        supernum=floor(size(img,1)*size(img,2)/supersize/supersize);
        superpixelsLabel=ERS(imgPCA, supernum);
        superpixelsImgValue=getsuperpixelsvalue_matlab(superpixelsLabel, imgPCA);
        superpixelsImgValue_array=reshape(superpixelsImgValue, size(imgPCA));
        EV_v=optimization_matlab(imgPCA, superpixelsImgValue_array);
        EV_list{end+1}=EV_v;
        if supersize_i>1
            if EV_list{supersize_i}/sum(cell2mat(EV_list))<threshold_a || EV_list{supersize_i}/EV_list{supersize_i-1}>1-threshold_a
                flag=2;
            end
        end
        if flag<2
            supersize_list_all{end+1}=supersize;
            superpixelsImgValue_list{end+1}=superpixelsImgValue_array;
        end
        supersize_i=supersize_i+1;
        clear superpixelsLabel superpixelsImgValue EV_v
    end
    superpixelsImgValue_list_array=cat(3, superpixelsImgValue_list{:});
    superpixels_value_dstack=superpixelsImgValue_list_array;
end
