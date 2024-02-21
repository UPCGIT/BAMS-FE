function EV = optimization_matlab_BAMS(img, imgers, returnSum)

if (ndims(img) == 3) && (ndims(imgers) == 3)
    ndims_band=size(img,3);
    EV=zeros(1, ndims_band);
    parfor band_i=1:ndims_band
        band_image=reshape(img(:,:,band_i), 1, size(img,1)*size(img,2))';
        band_imageers=reshape(imgers(:,:,band_i),1,size(img,1)*size(img,2))'+1;
        
        meanValues=accumarray(band_imageers, band_image,[], @mean);
        sampleCounts=accumarray(band_imageers, 1);
        uI=mean(band_image(:));
        ev_img=(meanValues-mean(uI)).^2.*sampleCounts;
        EV(band_i)=sum(ev_img(:))/sum(sum((band_image - uI).^2));
    end

elseif (ismatrix(img)) && (ismatrix(imgers))
    ev_img = 0;
    uI = mean(reshape(img, 1, size(img, 1)*size(img, 2)));
    ers_uniquedata = unique(imgers);
    parfor super_i = 1:length(ers_uniquedata)
        loc = find(imgers == ers_uniquedata(super_i));
        uS = mean(img(loc));
        ev_img = ev_img + (uS - uI)^2 * length(loc);
    end
    ev_img = ev_img / sum(sum((img - uI).^2));
    EV = ev_img;
else
    disp('the dimension for optimization is wrong')
end

if nargin==2
    EV=sum(EV(:));
end
