import os
import numpy as np
from config_noBDT import cut, fileNameData, cut_GJets
from ROOT import TFile


ctaus = ['10', '200', '400', '600', '800', '1000', '1200', '10000']
lambdas = ['100', '150', '200', '250', '300', '350', '400']
lambdas1 = ['100', '150', '200', '250']
lambdas2 = ['300', '350', '400']


ctaus_data = ['10','200']
lambdas_data = ['200', '350']

datacardDir = '../combine/datacards/2016/'

splits=['0, 250','0, 250', '1.5, 100', '1.5, 150']

idx_split = 0
#extract observed A and predicted B, C, D

print cut
print fileNameData

fileData = TFile(fileNameData)
treeData = fileData.Get("DelayedPhoton")

for idx1 in range(len(ctaus_data)):
	for idx2 in range(len(lambdas_data)):
		print splits[idx_split]+" &",
		lines_obs = os.popen("grep observation "+datacardDir+"DelayedPhotonCard_L"+lambdas_data[idx2]+"TeV_Ctau"+ctaus_data[idx1]+"cm.txt").read().split()
		
		time_split = splits[idx_split].split(", ")[0]
		met_split = splits[idx_split].split(", ")[1]
		
		#A = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData < "+str(time_split) + " && t1MET < "+ str(met_split) + " && pho1ClusterTime_SmearToData > -2.0 ")
		Cneg2 = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData < "+str(-1.0*float(time_split)) + " && t1MET > "+ str(met_split) + " && pho1ClusterTime_SmearToData < -2.0 ")
		Dneg2 = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData < "+str(-1.0*float(time_split)) + " && t1MET < "+ str(met_split) + " && pho1ClusterTime_SmearToData < -2.0 ")

		N_gt2ns = treeData.GetEntries(cut_GJets+" && pho1ClusterTime_SmearToData < -2.0 &&  t1MET < 100 && t1MET > 50")
		N_st2ns = treeData.GetEntries(cut_GJets+" && pho1ClusterTime_SmearToData > -2.0 &&  t1MET < 100 && t1MET > 50 && pho1ClusterTime_SmearToData < "+str(-1.0*float(time_split)))
		transfer_factor = (N_gt2ns+N_st2ns)*1.0/N_gt2ns

		Cneg = Cneg2*transfer_factor
		Dneg = Dneg2*transfer_factor

		print str(int(float(lines_obs[1])))+" &"+lines_obs[3]+" & "+lines_obs[4]+" & "+str(Cneg/100.0)+" & "+lines_obs[2]+" &"+str(Dneg/100.0)+" && " +str(transfer_factor)+" \\\\"

		idx_split += 1



#extract signal yields in ABCD bins
'''
for idx1 in range(len(ctaus)):
	print ctaus[idx1],
	for idx2 in range(len(lambdas1)):
		SF = 1.0
		if lambdas1[idx2] == '100':
			SF = 100.0
		if lambdas1[idx2] == '150' and ctaus[idx1] == '10':
			SF = 100.0

		lines_obs = os.popen("grep 'rate  ' "+datacardDir+"DelayedPhotonCard_L"+lambdas1[idx2]+"TeV_Ctau"+ctaus[idx1]+"cm.txt").read().split()
		print '& %.4s, %.4s, %.4s, %.4s' % ('%.3f' % (SF*float(lines_obs[1])), '%.3f' % (SF*float(lines_obs[5])),'%.3f' % (SF*float(lines_obs[7])),'%.3f' % (SF*float(lines_obs[3]))),

	print "\\\\"


for idx1 in range(len(ctaus)):
	print ctaus[idx1],
	for idx2 in range(len(lambdas2)):
		lines_obs = os.popen("grep 'rate  ' "+datacardDir+"DelayedPhotonCard_L"+lambdas2[idx2]+"TeV_Ctau"+ctaus[idx1]+"cm.txt").read().split()
		print '& %.4s, %.4s, %.4s, %.4s' % ('%.3f' % (SF*float(lines_obs[1])), '%.3f' % (SF*float(lines_obs[5])),'%.3f' % (SF*float(lines_obs[7])),'%.3f' % (SF*float(lines_obs[3]))),
		#print "& %6.2f, %6.2f, %6.2f, %6.2f "%(float(lines_obs[1]), float(lines_obs[5]), float(lines_obs[7]), float(lines_obs[3])),
	print " & \\\\"

'''
