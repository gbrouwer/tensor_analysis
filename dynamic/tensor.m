function tensor

%Init
clc;
%nSteps = 25;












% 
% %Create Starting Similarities
% x0 = mvnrnd([0 0],[0.125 0; 0 0.1],20);
% x1 = mvnrnd([0 0],[0.125 0; 0 0.1],20);
% x2 = mvnrnd([0 0],[0.125 0; 0 0.1],20);
% x3 = mvnrnd([0 0],[0.125 0; 0 0.1],20);
% X = [x0 ; x1; x2 ; x3];
% 
% 
% 
% %Displace
% newX = X;
% newX(1:1:20,1) = newX(1:1:20,1) - 2;
% newX(21:1:40,1) = newX(21:1:40,1) + 2;
% %newX(41:1:60,2) = newX(41:1:60,2) - 2;
% %newX(61:1:80,2) = newX(61:1:80,2) + 2;
% labels = [zeros(20,1) ; ones(20,1)];% ; ones(20,1)+1; ones(20,1)+2] + 1;
% 
% 
% %Create Colors
% colors(1,:) = [1 1 0];
% colors(2,:) = [1 0 0];
% colors(3,:) = [0 0.5 0];
% colors(4,:) = [0 0.25 1];
% 
% 
% 
% %Create Dynamic
% for i=1:nSteps
%   r = (i-1)/(nSteps-1);
%   XD(:,:,i) = newX.*r + X.*(1-r);
% end
% 
% 
% 
% 
% % for j=1:nSteps
% %   clf;
% %   for i=1:size(XD,1)
% %     hold on;
% %     h = scatter(XD(i,1,j),XD(i,2,j),'filled');
% %     set(h,'MarkerFaceColor',colors(labels(i),:),'MarkerEdgeColor',colors(labels(i),:));
% %     hold off;
% %     axis([-5 5 -5 5]);
% %     grid on; box on;
% %   end
% %   pause(0.1);
% % end
% % return
% 
% 
% 
% %Create Tensor
% for i=1:nSteps
%   D = squareform(pdist(XD(:,:,i)));
%   D = D ./ max(D(:));
%   D = 1 - D;
%   T(:,:,i) = D;
% end
% 
% 
% 
% %Store
% [s1,s2,s3] = size(T);
% fid = fopen('tensor','w');
% fprintf(fid,'%d,%d,%d\n',s1,s2,s3);
% for i=1:s1
%   for j=1:s2
%     for l=1:s3
%       fprintf(fid,'%d,%d,%d,%f\n',i,j,l,T(i,j,l));
%     end
%   end
% end
% fclose(fid);
% 
% 
% 
% %Run Python Script
% system('python python/runDTA.py 2 2 2');
% 
% 
% 
% %Read Back Decomposition
% core = readMatrix3D('core');
% U0 = readMatrix2D('U0');
% U1 = readMatrix2D('U1');
% U2 = readMatrix2D('U2');
% b0 = readMatrixNN('b0');
% b1 = readMatrixNN('b1');
% b2 = readMatrixNN('b2');
% 
% 
% 
% % V = U0 * squeeze(core(:,:,2)) * U2'
% % 
% % plot(V');
% % 
% 
% 
% % 
% % 
% % subplot(2,2,1);
% % for i=1:size(U0,1)
% %   h = scatter(U0(i,1),U0(i,2),'filled');
% %   set(h,'MarkerFaceColor',colors(labels(i),:),'MarkerEdgeColor',colors(labels(i),:));
% %   hold on;
% % end
% % box on; grid on;
% % 
% % U2
% % subplot(2,2,2);
% % for i=1:size(U2,1)
% %   h = scatter(U2(i,1),U2(i,2),'filled');
% %   set(h,'MarkerFaceColor',colors(labels(i),:),'MarkerEdgeColor',colors(labels(i),:));
% %   hold on;
% % end
% % box on; grid on;
% 
% % 
% % subplot(2,2,3);
% % for i=1:2:size(U2,1)
% %   h = scatter(U2(i,1),U2(i,2),'filled');
% %   set(h,'MarkerFaceColor',[i/nSteps 0 1],'MarkerEdgeColor',[i/nSteps 0 1]);
% %   hold on;
% % end
% % box on; grid on;
% % 
% % subplot(2,2,4);
% % for i=2:2:size(U2,1)
% %   h = scatter(U2(i,1),U2(i,2),'filled');
% %   set(h,'MarkerFaceColor',[i/nSteps 0 1],'MarkerEdgeColor',[i/nSteps 0 1]);
% %   hold on;
% % end
% % box on; grid on;
% % 
% % % 
% 
% 
% 
% 
% 
% % 
% % subplot(2,2,3);
% % for i=1:size(U2,1)
% %   h = scatter(U2(i,1),U2(i,2),'filled');
% %   set(h,'MarkerFaceColor',[labels2(i) 0 1-labels2(i)],'MarkerEdgeColor',[labels2(i) 0 1-labels2(i)]);
% %   hold on;
% % end
% % box on; grid on;
% % %subplot(2,2,2);
% % %scatter(U1(:,1),U1(:,2),'filled');
% % %subplot(2,2,3);
% % %scatter(U2(:,1),U2(:,2),'filled');
% % 




%--------------------------------------------------------------------------
function X = readMatrixNN(filename);

  X = csvread(filename);
  X = X(:,end);
  n = sqrt(size(X,1));
  X = reshape(X,n,n);

%--------------------------------------------------------------------------
function X = readMatrix3D(filename);

  X = csvread(filename);
  xdim = X(end,1)+1;
  ydim = X(end,2)+1;
  zdim = X(end,3)+1;
  X = reshape(X(:,end),zdim,ydim,xdim);
  X = permute(X,[3 2 1])
  
%--------------------------------------------------------------------------
function X = readMatrix2D(filename);

  X = csvread(filename);
  xdim = X(end,1)+1;
  ydim = X(end,2)+1;
  X = reshape(X(:,end),ydim,xdim)';  