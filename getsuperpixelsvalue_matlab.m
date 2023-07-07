function img_superpixels_mean = getsuperpixelsvalue_matlab(labels, img)
if ndims(img) == 3
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
else
    img_superpixels_mean = zeros(size(labels));
    label_list = unique(labels);
    for label_i = 1:length(label_list)
        loc = labels == label_list(label_i);
        img_superpixels_mean(loc) = mean(img(loc));
    end
end
end
