function k_cliUsing()
adjacent_matrix = load('E:\Geolife\Geolife Trajectories 1.3\meet.dat');
[components,cliques,CC]= k_cli(4,adjacent_matrix)
components=cell2table(components);
cliques=cell2table(cliques);
ansfilenameCom=['E:\Geolife\Geolife Trajectories 1.3\','CPM','Com','meet.csv'];
ansfilenameCli=['E:\Geolife\Geolife Trajectories 1.3\','CPM','Cli','meet.csv'];
ansfilenameC=['E:\Geolife\Geolife Trajectories 1.3\','CPM','C','meet.csv'];
writetable(components,ansfilenameCom);
writetable(cliques,ansfilenameCli);
dlmwrite(ansfilenameC, CC);

