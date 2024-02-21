function img_superpixels_mean = getsuperpixelsvalue_matlab_BAMS(labels, img, mask)
if nargin == 2
    if (ndims(img) == 3) && (ndims(labels) == 3)
        img_superpixels_mean = zeros(size(img));
        parfor band_i = 1:size(img, 3)
            img_band = img(:, :, band_i);
            img_superpixels_mean_band = zeros(size(img_band));
            labels_band = labels(:, :, band_i);
            label_list = unique(labels_band);
            for label_i = 1:length(label_list)
                loc = labels_band == label_list(label_i);
                img_superpixels_mean_band(loc) = mean(img_band(loc));
            end
            img_superpixels_mean(:, :, band_i) = img_superpixels_mean_band;
        end
    elseif (ismatrix(img)) && (ismatrix(labels))
        img_superpixels_mean = zeros(size(labels));
        label_list = unique(labels);
        for label_i = 1:length(label_list)
            loc = labels == label_list(label_i);
            img_superpixels_mean(loc) = mean(img(loc));
        end
    elseif (ndims(img) == 3) && (ismatrix(labels))
        label_list = unique(labels);
        labels_rc_c = reshape(labels, size(labels, 1)*size(labels, 2), 1);
        img_rc_c = reshape(img, size(img, 1)*size(img, 2), size(img, 3));
        img_superpixels_mean_rc_c = zeros(size(img_rc_c));
        for label_i = 1:length(label_list)
            loc = find(labels_rc_c == label_list(label_i));
            img_superpixels_mean_rc_c(loc, :) = repmat(mean(img_rc_c(loc, :)), length(loc), 1);
        end
        img_superpixels_mean = reshape(img_superpixels_mean_rc_c, size(img));
    else
        disp('dimension wrong in getsuperpixelsvalue_matlab');
    end
elseif nargin == 3
    if (ismatrix(img)) && (ismatrix(labels))
        img_superpixels_mean = zeros(size(labels));
        label_list = unique(labels(mask==1));
        for label_i = 1:length(label_list)
            loc = labels == label_list(label_i);
            img_superpixels_mean(loc) = mean(img(loc));
        end
    end
end

end
