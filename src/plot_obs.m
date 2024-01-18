% This program plots the observation in the grid world test cases
clear; clc; close all;
%% 1D grid
load('../output/1D_grid.mat')
OBS = [OBS;0];
figure;
for i=1:size(OBS,1)
    plot(OBS(i),0,'o','MarkerFaceColor','b','MarkerSize',20)
    hold on
%     yline(0.5)
%     yline(-0.5)
    hold off
    xlim([-0.5 9.5])
%     grid on
    n = 0.5;
    pbaspect([10 1 1])
    for j=1:9
        xline(n)
        n = n+1;
    end
%     xticks([-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5])
    filename = [sprintf('%03d',i) '.jpg'];
    fullname = fullfile('1D_grid',filename);
    saveas(gcf,fullname)  
end

%% 2D grid

load('../output/2D_grid_obstacle_continuous.mat')
N = 9;
OBS(end,:) = [N N];
nx = linspace(3,6,50);
ny = nx;
P = [];
for i = 1:50
    for j = 1:50
        P= [P;nx(i) ny(j)];
    end
end
% Nz = zeros(size(Nx));
figure;
for i=1:size(OBS,1)
    plot(OBS(i,1),OBS(i,2),'o','MarkerFaceColor','b','MarkerSize',10)
    hold on
    plot(P(:,1),P(:,2),'s','MarkerFaceColor','r','MarkerSize',6)
%     yline(0.5)
%     yline(-0.5)
    hold off
    xlim([-0.5 N+0.5])
    ylim([-0.5 N+0.5])
%     grid on
    n = 0.5;
    for j=1:N
        xline(n)
        yline(n)
        n = n+1;
    end
%     xlim([-0.5 3.5])
%     ylim([-0.5 3.5])
%     axis equal
%     xticks([-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5])
    filename = [sprintf('%03d',i) '.jpg'];
    fullname = fullfile('2D_grid_continuous',filename);
    saveas(gcf,fullname)  
end

%% 3D grid
load('../output/3D_grid_obstacle.mat')
N = 9;
OBS(end,:) = [N N N];
nx = linspace(3,6,50);
ny = nx;
nz = nx;
P = [];
for i = 1:50
    for j = 1:50
        for k = 1:50
            P = [P;nx(i) ny(j) nz(k)];
        end
    end
end
% Nz = zeros(size(Nx));
%%
figure;
for i=1:size(OBS,1)
    scatter3(OBS(i,1),OBS(i,2),OBS(i,3),60,'MarkerFaceColor','b')
    hold on
    scatter3(P(:,1),P(:,2),P(:,3),10,'MarkerFaceColor','r')
%     yline(0.5)
%     yline(-0.5)
    hold off
    xlim([-0.5 N+0.5])
    ylim([-0.5 N+0.5])
    zlim([-0.5 N+0.5])
%     grid on
%     n = 0.5;
%     for j=1:N
%         xline(n)
%         yline(n)
%         n = n+1;
%     end
%     xlim([-0.5 3.5])
%     ylim([-0.5 3.5])
%     axis equal
%     xticks([-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5])
    filename = [sprintf('%03d',i) '.jpg'];
    fullname = fullfile('3D_grid',filename);
    saveas(gcf,fullname)  
end


%% Create a video from image sequence
clc
outputVideo = VideoWriter(fullfile('1D_grid','1D_grid.mp4'));
outputVideo.FrameRate = 1;
open(outputVideo)
for i = 1:10
   filename = [sprintf('%03d',i) '.jpg'];
   img = imread(fullfile('1D_grid',filename));
   writeVideo(outputVideo,img)
end
close(outputVideo)