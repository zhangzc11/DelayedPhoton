#!/usr/bin/env python

import subprocess, time, sys, os, shlex
from ROOT import TFile
import numpy as np

tree_dir = "../limitTrees_v18"
datacard_dir = "../datacards/combine_v18"

runToy = True

if __name__ == "__main__":
	sig_list_filename = sys.argv[1]
	os.system("mkdir -p logs")
	f1=open("results.tex","a")
	with open(sig_list_filename,"r") as sig_list_file:
		for this_sig_line in sig_list_file:
			this_sig = shlex.split(this_sig_line)[0]
			lambda_this = int(this_sig[1:4])
			ctau_this = int(this_sig[12:-2])
			#print lambda_this
			#print ctau_this
			limits_SF = 1.0
			if lambda_this == 100:
				limits_SF = 0.01
			if lambda_this == 150 and ctau_this == 10:
				limits_SF = 0.01
			if lambda_this == 150 and ctau_this == 50:
				limits_SF = 0.01
			if lambda_this == 150 and ctau_this == 100:
				limits_SF = 0.01
			if lambda_this == 150 and ctau_this == 200:
				limits_SF = 0.01

			file_limit_Asymptotic = TFile(tree_dir+"/higgsCombine"+this_sig+"_2016And2017.Asymptotic.mH120.root")
			limits_Asymptotic = []
			limitTree_Asymtotic = file_limit_Asymptotic.Get("limit")
			for entry in limitTree_Asymtotic:
				limits_Asymptotic.append(entry.limit)

			mean_r = int(limits_Asymptotic[5]*100.0)/100.0
			if runToy:
				print "generating toys for "+this_sig+" with r from "+str(mean_r-0.5)+" to "+str(mean_r+0.5) +" wiht step of 0.05"
				for r in np.arange(mean_r-0.5, mean_r+0.5, 0.05):
					print "generating toy for r = "+str(r)
					os.system("echo combine "+datacard_dir+"/datacard_GMSB_"+this_sig+"_2016And2017.txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 500 --clsAcc 0 -s -1 -n "+this_sig+" >> logs/"+this_sig+".log")
					os.system("combine "+datacard_dir+"/datacard_GMSB_"+this_sig+"_2016And2017.txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 500 --clsAcc 0 -s -1 -n "+this_sig+" >> logs/"+this_sig+".log")
					
				os.system("echo hadd higgsCombine"+this_sig+".HybridNew.mH120.merged.root higgsCombine"+this_sig+".HybridNew.mH120.*.root >> logs/"+this_sig+".log")		
				os.system("hadd higgsCombine"+this_sig+".HybridNew.mH120.merged.root higgsCombine"+this_sig+".HybridNew.mH120.*.root")				
				os.system("echo combine "+datacard_dir+"/datacard_GMSB_"+this_sig+"_2016And2017.txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+".HybridNew.mH120.merged.root -n "+this_sig+"_Observed --plot=plots/limit_obs_scan_"+this_sig+".png >> logs/"+this_sig+".log")	
				os.system("combine "+datacard_dir+"/datacard_GMSB_"+this_sig+"_2016And2017.txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+".HybridNew.mH120.merged.root -n "+this_sig+"_Observed --plot=plots/limit_obs_scan_"+this_sig+".png >> logs/"+this_sig+".log")	
				os.system("echo combine "+datacard_dir+"/datacard_GMSB_"+this_sig+"_2016And2017.txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+".HybridNew.mH120.merged.root --expectedFromGrid 0.5 -n "+this_sig+"_Exp0p5 --plot=plots/limit_exp0p5_scan_"+this_sig+".png >> logs/"+this_sig+".log")
				os.system("combine "+datacard_dir+"/datacard_GMSB_"+this_sig+"_2016And2017.txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+".HybridNew.mH120.merged.root --expectedFromGrid 0.5 -n "+this_sig+"_Exp0p5 --plot=plots/limit_exp0p5_scan_"+this_sig+".png >> logs/"+this_sig+".log")


			limitFile_obs = TFile("higgsCombine"+this_sig+"_Observed.HybridNew.mH120.root")
			limitTree_obs = limitFile_obs.Get("limit")
			limits_obs = []
			for entry in limitTree_obs:
				limits_obs.append(entry.limit)

			limitFile_exp = TFile("higgsCombine"+this_sig+"_Exp0p5.HybridNew.mH120.quant0.500.root")
			limitTree_exp = limitFile_exp.Get("limit")
			limits_exp = []
			for entry in limitTree_exp:
				limits_exp.append(entry.limit)
			diff_percent_exp = 100.0*(limits_exp[0]-limits_Asymptotic[2])/limits_Asymptotic[2]
			diff_percent_obs = 100.0*(limits_obs[0]-limits_Asymptotic[5])/limits_Asymptotic[5]
			print >> f1, this_sig+" & %.2f"%limits_Asymptotic[2]+" & %.2f"%limits_exp[0]+" (%.2f"%diff_percent_exp+"\\%%) & %.2f"%limits_Asymptotic[5]+" & %.2f"%limits_obs[0]+" (%.2f"%diff_percent_obs+"\\%) \\\\"
			
