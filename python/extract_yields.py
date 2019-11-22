import os, math
import numpy as np
from config_noBDT import cut, fileNameData, cut_GJets
from ROOT import TFile


ctaus = ['10', '50', '100', '200', '400', '600', '800', '1000', '1200', '10000']
lambdas = ['100', '150', '200', '250', '300', '350', '400']
lambdas1 = ['100', '150', '200', '250']
lambdas2 = ['300', '350', '400']


ctaus_data = ['10','200']
lambdas_data = ['200', '350']

datacardDir = '../combine/datacards/2016_v15/'
datacardDir_obs = '../combine/datacards/2016_v16/'

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
		lines_pre = os.popen("grep observation "+datacardDir+"DelayedPhotonCard_L"+lambdas_data[idx2]+"TeV_Ctau"+ctaus_data[idx1]+"cm.txt").read().split()
		lines_obs = os.popen("grep observation "+datacardDir_obs+"DelayedPhotonCard_L"+lambdas_data[idx2]+"TeV_Ctau"+ctaus_data[idx1]+"cm.txt").read().split()
		print " %9.0f & %9.0f & %9.2f & %9.0f & %9.2f & %9.0f & %9.2f" % (float(lines_obs[1]),float(lines_obs[3]),float(lines_pre[3]),float(lines_obs[4]),float(lines_pre[4]),float(lines_obs[2]),float(lines_pre[2]))
		
		time_split = splits[idx_split].split(", ")[0]
		met_split = splits[idx_split].split(", ")[1]
		
		A = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData < "+str(time_split) + " && t1MET < "+ str(met_split) + " && pho1ClusterTime_SmearToData > -2.0 ")
		B = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData < "+str(time_split) + " && t1MET > "+ str(met_split) + " && pho1ClusterTime_SmearToData > -2.0 ")
		C = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData > "+str(time_split) + " && t1MET > "+ str(met_split) + " && pho1ClusterTime_SmearToData > -2.0 ")
		D = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData > "+str(time_split) + " && t1MET < "+ str(met_split) + " && pho1ClusterTime_SmearToData > -2.0 ")

		N1 = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData < "+str(time_split) + " && t1MET < 100.0")
		N2 = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData > "+str(time_split) + " && t1MET < 100.0")
		M1 = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData < 1.0 && t1MET < "+ str(met_split))
		M2 = treeData.GetEntries(cut+" && pho1ClusterTime_SmearToData < 1.0 && t1MET > "+ str(met_split))
	
		err_M21 = M2*1.0/M1*math.sqrt(1.0/M1 + 1.0/M2)	
		err_N21 = N2*1.0/N1*math.sqrt(1.0/N1 + 1.0/N2)	
		B_pred = A*M2*1.0/M1
		errB_pred = math.sqrt(math.pow(A*err_M21,2.0) + A*1.0*M2*M2/(M1*M1))
		D_pred = A*N2*1.0/N1
		errD_pred = math.sqrt(math.pow(A*err_N21,2.0) + A*1.0*N2*N2/(N1*N1))
		C_pred = B_pred*D_pred*1.0/A
		errC_pred = C_pred*math.sqrt(1.0/A + (B_pred*B_pred*errD_pred*errD_pred + D_pred*D_pred*errB_pred*errB_pred)/(B_pred*B_pred*D_pred*D_pred))

		print splits[idx_split]+" &",
		print " %9.0f & %9.0f & %9.2f $\\pm$%8.2f & %9.0f & %9.2f $\\pm$%8.2f & %9.0f & %9.2f $\\pm$%8.2f" % (A, B, B_pred, errB_pred, C, C_pred, errC_pred, D, D_pred, errD_pred)

		idx_split += 1

'''
#extract signal yields in ABCD bins
for idx1 in range(len(ctaus)):
        print ctaus[idx1],
        for idx2 in range(len(lambdas1)):
                SF = 1.0
                if lambdas1[idx2] == '100':
                        SF = 100.0
                if lambdas1[idx2] == '150' and ctaus[idx1] == '10':
                        SF = 100.0

                lines_obs = os.popen("grep 'rate  ' "+datacardDir_obs+"DelayedPhotonCard_L"+lambdas1[idx2]+"TeV_Ctau"+ctaus[idx1]+"cm.txt").read().split()
                print '& %.4s, %.4s, %.4s, %.4s' % ('%.3f' % (SF*float(lines_obs[1])), '%.3f' % (SF*float(lines_obs[5])),'%.3f' % (SF*float(lines_obs[7])),'%.3f' % (SF*float(lines_obs[3]))),

        print "\\\\"


for idx1 in range(len(ctaus)):
        print ctaus[idx1],
        for idx2 in range(len(lambdas2)):
                lines_obs = os.popen("grep 'rate  ' "+datacardDir_obs+"DelayedPhotonCard_L"+lambdas2[idx2]+"TeV_Ctau"+ctaus[idx1]+"cm.txt").read().split()
                print '& %.4s, %.4s, %.4s, %.4s' % ('%.3f' % (SF*float(lines_obs[1])), '%.3f' % (SF*float(lines_obs[5])),'%.3f' % (SF*float(lines_obs[7])),'%.3f' % (SF*float(lines_obs[3]))),
                #print "& %6.2f, %6.2f, %6.2f, %6.2f "%(float(lines_obs[1]), float(lines_obs[5]), float(lines_obs[7]), float(lines_obs[3])),
        print " & \\\\"

'''
