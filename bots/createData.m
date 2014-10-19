function createData

%Init
clc;


%Define Patters
p1 = sin(linspace(0,2*pi,6*24));
p2 = cos(linspace(0,2*pi*2,6*24));
p1 = (p1 - min(p1)) ./ 2;
p2 = (p2 - min(p2)) ./ 2;



%Domain - IP field
DP = zeros(50,10);
DP(1:25,1:5) = 1;
DP(26:end,6:end) = 1;



%Pattern field
P1 = repmat(p1,25,1);
P2 = repmat(p2,25,1);
P = [P1 ; P2];



%Create Tensor
for i=1:144
  p = P(:,i);
  p = repmat(p,1,10);
  N = rand(size(p)) * 5.00;
  T(:,:,i) = N + (DP.*p);
end  
T = T - min(T(:));
T = T ./ max(T(:));



%Flatten and store
[s1,s2,s3] = size(T)

fid = fopen('tensor','w');
fprintf(fid,'%d,%d,%d\n',s1,s2,s3);
for i=1:s1
  for j=1:s2
    for l=1:s3
      fprintf(fid,'%d,%d,%d,%f\n',i,j,l,T(i,j,l));
    end
  end
end
fclose(fid);
