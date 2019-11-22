import os, math
import numpy as np
from Aux import *
from config_noBDT import cut, fileNameData, cut_GJets, weight_cut, lumi
from ROOT import TFile, TH1F, gROOT

gROOT.SetBatch(True)

fileDir="/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"

ctau_data = ['10', '50', '100', '200', '400', '600', '800', '1000', '1200', '10000']
lambda_data = ['100', '150', '200', '250', '300', '350', '400']


datacardDir = '../combine/datacards/2016_v15/'
datacardDir_obs = '../combine/datacards/2016_v16/'

splits=['0, 250','0, 250', '1.5, 100', '1.5, 150']

idx_split = 0

cut_this =  cut+" && pho1ClusterTime_SmearToData > -2.0 && pho1ClusterTime_SmearToData < 25.0"


time_split_by_CAT = [0.0, 0.0, 1.5, 1.5]
met_split_by_CAT = [250.0, 250.0, 100.0, 150.0]


def getABCD(Ctau, Lambda):	
	fileThis = TFile(fileDir+"GMSB_L"+Lambda+"TeV_Ctau"+Ctau+"cm_13TeV-pythia8.root")
	treeThis = fileThis.Get("DelayedPhoton")
	hNEventsThis = fileThis.Get("NEvents")
	N_total = hNEventsThis.GetBinContent(1)

	splitCAT = 0
	frLambda = float(Lambda)
	frCtau = float(Ctau)

	if frLambda < 301:
		if frCtau < 20:
			splitCAT = 0
		else:
			splitCAT = 2
	else:
		if frCtau < 20:
			splitCAT = 1
		else:
			splitCAT = 3
	time_split = time_split_by_CAT[splitCAT]
	met_split = met_split_by_CAT[splitCAT]

	histA = TH1F("histA","",100,0,100)
	histB = TH1F("histB","",100,0,100)
	histC = TH1F("histC","",100,0,100)
	histD = TH1F("histD","",100,0,100)
	
	myC = TCanvas( "myC", "myC", 200, 10, 800, 800 )

	treeThis.Draw("NPU>>histA",weight_cut+"("+cut_this + " && pho1ClusterTime_SmearToData < "+str(time_split) + " && t1MET < "+ str(met_split) + ")")
	treeThis.Draw("NPU>>histB",weight_cut+"("+cut_this + " && pho1ClusterTime_SmearToData < "+str(time_split) + " && t1MET > "+ str(met_split) + ")")
	treeThis.Draw("NPU>>histC",weight_cut+"("+cut_this + " && pho1ClusterTime_SmearToData > "+str(time_split) + " && t1MET > "+ str(met_split) + ")")
	treeThis.Draw("NPU>>histD",weight_cut+"("+cut_this + " && pho1ClusterTime_SmearToData > "+str(time_split) + " && t1MET < "+ str(met_split) + ")")
	
	xsec, exsec = getXsecBR(Lambda, Ctau)
	
	NA = histA.Integral()
	NB = histB.Integral()
	NC = histC.Integral()
	ND = histD.Integral()
	
	A = NA*lumi*xsec/N_total
	B = NB*lumi*xsec/N_total
	C = NC*lumi*xsec/N_total
	D = ND*lumi*xsec/N_total
	
	eA = A*np.sqrt(1./NA + 1.0/N_total)
	eB = B*np.sqrt(1./NB + 1.0/N_total)
	eC = C*np.sqrt(1./NC + 1.0/N_total)
	eD = D*np.sqrt(1./ND + 1.0/N_total)
	
	eAint = int(pow(10,-1*int(math.log10(eA))+1)*eA)
	eAP = eAint *1.0/pow(10,-1*int(math.log10(eA))+1)
	AP = int(A*pow(10,-1*int(math.log10(eA))+1))*1.0/pow(10,-1*int(math.log10(eA))+1)
	if eAint < 5:
		eAP = int(pow(10,-1*int(math.log10(eA))+2)*eA)*1.0/pow(10,-1*int(math.log10(eA))+2)
		AP = int(A*pow(10,-1*int(math.log10(eA))+2))*1.0/pow(10,-1*int(math.log10(eA))+2)

	eBint = int(pow(10,-1*int(math.log10(eB))+1)*eB)
	eBP = eBint *1.0/pow(10,-1*int(math.log10(eB))+1)
	BP = int(B*pow(10,-1*int(math.log10(eB))+1))*1.0/pow(10,-1*int(math.log10(eB))+1)
	if eBint < 5:
		eBP = int(pow(10,-1*int(math.log10(eB))+2)*eB)*1.0/pow(10,-1*int(math.log10(eB))+2)
		BP = int(B*pow(10,-1*int(math.log10(eB))+2))*1.0/pow(10,-1*int(math.log10(eB))+2)
	
	eCint = int(pow(10,-1*int(math.log10(eC))+1)*eC)
	eCP = eCint *1.0/pow(10,-1*int(math.log10(eC))+1)
	CP = int(C*pow(10,-1*int(math.log10(eC))+1))*1.0/pow(10,-1*int(math.log10(eC))+1)
	if eCint < 5:
		eCP = int(pow(10,-1*int(math.log10(eC))+2)*eC)*1.0/pow(10,-1*int(math.log10(eC))+2)
		CP = int(C*pow(10,-1*int(math.log10(eC))+2))*1.0/pow(10,-1*int(math.log10(eC))+2)

	eDint = int(pow(10,-1*int(math.log10(eD))+1)*eD)
	eDP = eDint *1.0/pow(10,-1*int(math.log10(eD))+1)
	DP = int(D*pow(10,-1*int(math.log10(eD))+1))*1.0/pow(10,-1*int(math.log10(eD))+1)
	if eDint < 5:
		eDP = int(pow(10,-1*int(math.log10(eD))+2)*eD)*1.0/pow(10,-1*int(math.log10(eD))+2)
		DP = int(D*pow(10,-1*int(math.log10(eD))+2))*1.0/pow(10,-1*int(math.log10(eD))+2)

	print Ctau+" & "+str(AP)+" $\\pm$ "+str(eAP)+" & "+str(BP)+" $\\pm$ "+str(eBP)+" & "+str(CP)+" $\\pm$ "+str(eCP)+" & "+str(DP)+" $\\pm$ "+str(eDP)+"\\\\"
	

for idx1 in range(len(lambda_data)):
	print "\\begin{table}[!htb]"
	print "\\footnotesize"
	print "\\begin{center}"
	print "\\caption{(2016) Event yields in bins A,B,C,D using the 2016 event selection for GMSB SPS8 $\\Lambda = "+lambda_data[idx1]+"\\TeV$ and varying \\ctau. Please see the article for corresponding definitions of the \\tpho-\\ptmiss splits for each signal point.}"
	print "\\label{tab:abcd_sig_yield_L"+lambda_data[idx1]+"_2016}"	
	print "\\begin{tabular}{c|cccc}"
	print "\\hline"
	print "$\\ctau~(\\cm)$ & Yield in Bin A & Yield in Bin B & Yield in Bin C & Yield in Bin D \\\\"
	for idx2 in range(len(ctau_data)):
		getABCD(ctau_data[idx2], lambda_data[idx1])
	print "\\hline"
	print "\\end{tabular}"
	print "\\end{center}"
	print "\\end{table}"
			

'''
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
