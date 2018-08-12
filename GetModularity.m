function [Q e a out_clusters] = GetModularity(adjacent_matrix, clusters)
%% 获取无向无权网络的某种划分的模块度
%% 模块度的提出和计算方法见如下文献:
% 《Finding and evaluating community structure in network》(2004)
% 输入
% adjacent_matrix - 网络的邻接矩阵
% clusters - 网络的社团划分，第1行是节点标号，第2行是社团标号的变换，第3行是社团标号
% 输出
% Q - 划分的模块度
% e - k*k矩阵，k是社团数目，其中元素的定义见上述文献
% a - 意义见上述定义
% out_clusters - 与输入含义相同

uni = unique(clusters(3,:));
for i = 1:length(uni)
    idices = find(clusters(3,:) == uni(i));
    clusters(2,idices) = i;
end

m = sum(sum(adjacent_matrix))/2; % 网络的边的数目
Q = 0 ;
k = numel(unique(clusters(2,:))); % 社团数目
e = zeros(k);
for i=1:k
    idx = find(clusters(2,:)==i);
    labelsi = clusters(1,idx);   %找到在i社团中的所有节点
    for j=1:k
        idx = find(clusters(2,:)==j);
        labelsj = clusters(1,idx);  %找到在j社团中的所有节点
        for ii=1:length(labelsi)
            vi = labelsi(ii);   %对于i社团中的节点ii
            for jj=1:length(labelsj)
                vj = labelsj(jj);  %对于j社团中的节点jj
                e(i,j) = e(i,j)+adjacent_matrix(vi,vj);
            end
        end        
    end
end

e = e/2;
% for i=1:k
%     e(i,i) = e(i,i)*2;
% end

e = e/m;
a = [];
for i=1:k
    ai = sum(e(i,:));
    a = [a; ai];
    Q = Q + e(i,i)-ai^2;
end

out_clusters = clusters;

end