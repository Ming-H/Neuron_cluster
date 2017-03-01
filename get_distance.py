import os
os.chdir("C:/Program Files/Vaa3D-3.20/bin")
namelist = []
for filename in os.listdir(r'E:/neurons'):
    namelist.append(filename)
print len(namelist)
for i in range(len(namelist)-1):
    for j in range(i+1,len(namelist)):
        print namelist[i],namelist[j],namelist[i]+namelist[j]
        os.system("vaa3d.exe /x neuron_distance /f neuron_distance /i E:/neurons/{0} E:/neurons/{1} /o E:/result/{2}.txt".format(namelist[i],namelist[j],namelist[i]+namelist[j]))

        


 
   









'''
C:\Program Files\Vaa3D-3.20\bin>vaa3d.exe /x neuron_distance /f neuron_distance /i C:\Users\zhi\Drop
box\Jefferis_data1.tif_x32_y80_z0_app2.swc C:\Users\zhi\Dropbox\Jefferis_data1.tif_x32_y80_z0_app2.s
wc_assembled.swc
'''

