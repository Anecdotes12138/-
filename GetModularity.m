function [Q e a out_clusters] = GetModularity(adjacent_matrix, clusters)
%% ��ȡ������Ȩ�����ĳ�ֻ��ֵ�ģ���
%% ģ��ȵ�����ͼ��㷽������������:
% ��Finding and evaluating community structure in network��(2004)
% ����
% adjacent_matrix - ������ڽӾ���
% clusters - ��������Ż��֣���1���ǽڵ��ţ���2�������ű�ŵı任����3�������ű��
% ���
% Q - ���ֵ�ģ���
% e - k*k����k��������Ŀ������Ԫ�صĶ������������
% a - �������������
% out_clusters - �����뺬����ͬ

uni = unique(clusters(3,:));
for i = 1:length(uni)
    idices = find(clusters(3,:) == uni(i));
    clusters(2,idices) = i;
end

m = sum(sum(adjacent_matrix))/2; % ����ıߵ���Ŀ
Q = 0 ;
k = numel(unique(clusters(2,:))); % ������Ŀ
e = zeros(k);
for i=1:k
    idx = find(clusters(2,:)==i);
    labelsi = clusters(1,idx);   %�ҵ���i�����е����нڵ�
    for j=1:k
        idx = find(clusters(2,:)==j);
        labelsj = clusters(1,idx);  %�ҵ���j�����е����нڵ�
        for ii=1:length(labelsi)
            vi = labelsi(ii);   %����i�����еĽڵ�ii
            for jj=1:length(labelsj)
                vj = labelsj(jj);  %����j�����еĽڵ�jj
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