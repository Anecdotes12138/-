function FnUsing()
adjacent_matrix = load('E:\Geolife\Geolife Trajectories 1.3\meet.dat');
[mod,clu] = FastNewman(adjacent_matrix);
ansfilenameCom=['E:\Geolife\Geolife Trajectories 1.3\','FN','Com','meet.csv'];
ansfilenameMod=['E:\Geolife\Geolife Trajectories 1.3\','FN','Mod','meet.csv'];
dlmwrite(ansfilenameCom,clu);
dlmwrite(ansfilenameMod,mod);

