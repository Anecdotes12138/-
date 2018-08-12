function [mod clu] = FastNewman(adjacent_matrix)
% FastNewman算法实现社团发现
% 该算法参见文献《Fast algorithm for detecting community structure in networks》(2003)
% 输入
% adjacent_matrix - 邻接矩阵
% 输出
% Z - n-1*3矩阵，第i行表示第i次合并，第1列和第2列表示合并的社团标号，第3列是合并后的模块度
% H - 聚类树图的句柄
tic
%代码块
n = size(adjacent_matrix,1); % 节点数目
max_id = n;
Z = [];
mod = [];
clu = [];
clusters = [1:n; zeros(1,n); 1:n]; % 初始划分，第1行是节点标号，第2行是社团标号的变换，第3行是社团标号
step = 1;
while numel(unique(clusters(3,:))) ~= 1 
% while step < n
    [Q e a clusters] = GetModularity(adjacent_matrix, clusters);
    mod = [mod;Q];
    clu = [clu;clusters];
    k = size(e,1); % 社团数目
    DeltaQs = [];
    for i = 1:size(e,1)
        for j = 1:size(e,1)
            if i ~= j
                DeltaQ = 2*(e(i,j)-a(i)*a(j));
                DeltaQs = [DeltaQs [i;j;DeltaQ]];
            end            
        end
    end
    [maxDeltaQ,id] = max(DeltaQs(3,:)); id = id(1);
    i = DeltaQs(1,id); j = DeltaQs(2,id); % 找出DeltaQ最大的社团对的序号
    max_id = max_id + 1;
    c_id1 = find(clusters(2,:) == i);   %得到i社团所含的节点标号
    c_id2 = find(clusters(2,:) == j);    %得到j社团所含的节点标号
    id1 = unique(clusters(3,c_id1));    %i社团所含节点所在的社团
    id2 = unique(clusters(3,c_id2));    %j社团所含节点……
    clusters(3,c_id1) = max_id;      %合并社团i和j
    clusters(3,c_id2) = max_id;  
    Z = [Z; [id1 id2 length([c_id1 c_id2])]];
    step = step + 1;
end
toc
disp(['运行时间: ',num2str(toc)]);
if nargout == 2
    H = dendrogram(Z,0);
    saveas(1,['E:\Geolife\Geolife Trajectories 1.3\FNtrees.png']);
end

end

