function labels=ERS(img, nC)

    addpath(genpath(cd(cd)));
    img=double(img);
    labels=zeros(size(img));
    if length(size(img))==3
%        poolobj = gcp('nocreate'); % Check if a parallel pool already exists
%        if isempty(poolobj) % If no parallel pool exists, create one
%            poolobj = parpool(12); % Create a new parallel pool
%        end
        parfor band_i =1:size(img,3)
            grey_img=img(:,:,band_i);
            grey_img=(grey_img-min(min(grey_img)))/(max(max(grey_img))-min(min(grey_img)));
            grey_img=double(round(grey_img*250));
            [labels_]=mex_ers(grey_img,double(ceil(nC)));
            labels(:,:,band_i)=labels_;
        end
    else
            grey_img=img;
            grey_img=(grey_img-min(min(grey_img)))/(max(max(grey_img))-min(min(grey_img)));
            grey_img=double(round(grey_img*250));
            labels=mex_ers(grey_img,double(ceil(nC)));
    end
end