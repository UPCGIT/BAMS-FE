function EV = optimization_matlab(img, imgers)

if ndims(img) == 3
%    poolobj = gcp('nocreate'); % Check if a parallel pool already exists
%    if isempty(poolobj) % If no parallel pool exists, create one
%        poolobj = parpool(12); % Create a new parallel pool
%    end
    bandnum = size(img, 3);
    EV_img = 0;
    for data_i = 1:floor(size(imgers, 3)/bandnum)
        x = imgers(:, :, (data_i - 1)*bandnum+1:data_i*bandnum);
        ev_img = 0;
        parfor band_i = 1:size(x, 3)
            img_row = img(:, :, band_i);
            uI = mean(reshape(img_row, 1, size(img_row, 1)*size(img_row, 2)));
            x_img = x(:, :, band_i);
            x_img_uniquedata = unique(x_img);
            ev_band = 0;
            for super_i = 1:length(x_img_uniquedata)
                loc = find(x_img == x_img_uniquedata(super_i));
                uS = mean(img_row(loc));
                ev_band = ev_band + (uS - uI)^2 * length(loc);
            end
            ev_img = ev_img + ev_band / sum(sum((img_row - uI).^2));
        end
        if data_i == 1
            EV_img = ev_img;
        else
            EV_img = [EV_img, ev_img];
        end
    end
    EV = EV_img;
else
    ev_img=0;
    uI=mean(reshape(img, 1, size(img,1)*size(img,2)));
    ers_uniquedata=unique(imgers);
    for super_i=1:length(ers_uniquedata)
        loc=find(imgers==ers_uniquedata(super_i));
        uS=mean(img(loc));
        ev_img=ev_img+(uS-uI)^2*length(loc);
    end
    ev_img=ev_img/sum(sum((img-uI).^2));
    EV=ev_img;
end
