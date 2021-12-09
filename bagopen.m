clc,clear all
camera='Camera_2_V76_0.08U_1125_009';
type=1;%depth=0 / rgb=1;

filepath=fullfile('H:\deeplabcut\76\ICH12d',[camera,'.bag']);
bag=rosbag(filepath);
% startTime=bag.StartTime;
% EndTime=bag.EndTime;
% Time=EndTime-startTime;
if type==1
    message='/device_0/sensor_1/Color_0/image/data';
elseif type==0
    message='/device_0/sensor_0/Depth_0/image/data';
else
    fprintf("type error");
    return
end
geometry_message=select(bag,'Time', ...
    [bag.StartTime bag.EndTime],'Topic',message);
N=geometry_message.NumMessages;
data=readMessages(geometry_message,'DataFormat','struct');

for i=1:N
    filename=sprintf('0%04d.jpg',i);
    data1=data{i};
    [M,N]=size(data1.Data);
    img_H=data1.Height;
    img_W=data1.Width;
    img_data=data1.Data;
    % image=reshape(img_data,480,848,3);
    g=[];
    r=[];
    image=[]; 
    if type==1
        b=[];
        r=img_data(1:3:end);
        g=img_data(2:3:end);
        b=img_data(3:3:end);
        r=reshape(r,848,480);
        g=reshape(g,848,480);
        b=reshape(b,848,480);
        image(:,:,1)=r;
        image(:,:,2)=g;
        image(:,:,3)=b;
        image=uint8(image);
    %     imshow(image)
        imwrite(image,filename)
    else
        r=img_data(1:2:end);
        g=img_data(2:2:end);
        r=reshape(r,848,480);
        g=reshape(g,848,480);
        image(:,:,2)=g;
        image=uint8(g);
        filename=sprintf('0%04d.jpg',i);
        imwrite( ind2rgb(im2uint8(mat2gray(g)), parula(100)), filename)
end
