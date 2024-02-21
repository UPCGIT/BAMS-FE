function labels=ERS_BAMS(img, nC, lambda, sigma, conn)


    if nargin==2
        lambda=0.5;
        sigma=5;
        conn=1;
    elseif nargin==3
        sigma=5;
        conn=1;
    elseif nargin==4
        conn=1;
    end

    addpath(genpath(cd(cd)));
    img=double(img);
    lambda=double(lambda);
    sigma=double(sigma);
    labels=zeros(size(img));
    if length(size(img))==3
        parfor band_i =1:size(img,3)
            grey_img=img(:,:,band_i);
            grey_img=(grey_img-min(min(grey_img)))/(max(max(grey_img))-min(min(grey_img)));
            grey_img=double(round(grey_img*250));
            [labels_]=mex_ers(grey_img,double(ceil(nC)),lambda,sigma, conn);
            labels(:,:,band_i)=labels_;
        end
    else
            grey_img=img;
            grey_img=(grey_img-min(min(grey_img)))/(max(max(grey_img))-min(min(grey_img)));
            grey_img=double(round(grey_img*250));
            labels=mex_ers(grey_img,double(ceil(nC)),lambda,sigma, conn);
    end
end