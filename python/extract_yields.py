import os
import numpy as np


ctaus = ['10', '200', '400', '600', '800', '1000', '1200', '10000']
lambdas = ['100', '150', '200', '250', '300', '350', '400']
lambdas1 = ['100', '150', '200', '250']
lambdas2 = ['300', '350', '400']


ctaus_data = ['10','200']
lambdas_data = ['200', '300']

datacardDir = '../combine/datacards/2016/'

splits=['0, 200','0, 300','1.5, 100', '1.5, 150']

idx_split = 0
#extract observed A and predicted B, C, D
for idx1 in range(len(ctaus_data)):
	for idx2 in range(len(lambdas_data)):
		#print ctaus_data[idx1]+" "+lambdas_data[idx2]
		print splits[idx_split]+" &",
		lines_obs = os.popen("grep observation "+datacardDir+"DelayedPhotonCard_L"+lambdas_data[idx2]+"TeV_Ctau"+ctaus_data[idx1]+"cm.txt").read().split()
		print str(int(float(lines_obs[1])))+" &"+lines_obs[2]+" & "+lines_obs[4]+" & "+lines_obs[3]+" \\\\"
		idx_split += 1

#extract signal yields in ABCD bins

for idx1 in range(len(ctaus)):
	print ctaus[idx1],
	for idx2 in range(len(lambdas1)):
		lines_obs = os.popen("grep 'rate  ' "+datacardDir+"DelayedPhotonCard_L"+lambdas1[idx2]+"TeV_Ctau"+ctaus[idx1]+"cm.txt").read().split()
		if ctaus[idx1] == '10' or ctaus[idx1] =='200' or ctaus[idx1] == '400':
			print "& %6.1f, %6.1f, %6.1f, %6.1f "%(float(lines_obs[1]), float(lines_obs[3]), float(lines_obs[7]), float(lines_obs[5])),
		else:
			print "& %6.2f, %6.2f, %6.2f, %6.2f "%(float(lines_obs[1]), float(lines_obs[3]), float(lines_obs[7]), float(lines_obs[5])),
	print "\\\\"


for idx1 in range(len(ctaus)):
	print ctaus[idx1],
	for idx2 in range(len(lambdas2)):
		lines_obs = os.popen("grep 'rate  ' "+datacardDir+"DelayedPhotonCard_L"+lambdas2[idx2]+"TeV_Ctau"+ctaus[idx1]+"cm.txt").read().split()
		print "& %6.2f, %6.2f, %6.2f, %6.2f "%(float(lines_obs[1]), float(lines_obs[3]), float(lines_obs[7]), float(lines_obs[5])),
	print " & \\\\"


