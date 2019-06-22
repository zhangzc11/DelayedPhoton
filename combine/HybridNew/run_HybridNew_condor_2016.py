#!/usr/bin/env python

import subprocess, time, sys, os, shlex
from ROOT import TFile
import numpy as np


if __name__ == "__main__":
	sig_list_filename = sys.argv[1]
	os.system("mkdir -p plots")
	f1=open("results.tex","a")
	with open(sig_list_filename,"r") as sig_list_file:
		for this_sig_line in sig_list_file:
			this_sig = shlex.split(this_sig_line)[0]
			this_sig_2016 = this_sig.replace("CTau","Ctau")
			this_sig_2017 = this_sig.replace("cm","")
			this_sig_2017 = this_sig_2017.replace("TeV","")
			lambda_this = int(this_sig[1:4])
			ctau_this = int(this_sig[12:-2])
		
			#2016Only
			file_limit_Asymptotic_2016 = TFile("limitTrees/higgsCombine"+this_sig+"_2016.Asymptotic.mH120.root")
			limits_Asymptotic_2016 = []
			limitTree_Asymtotic_2016 = file_limit_Asymptotic_2016.Get("limit")
			for entry in limitTree_Asymtotic_2016:
				limits_Asymptotic_2016.append(entry.limit)

			mean_r_2016 = int(limits_Asymptotic_2016[5]*100.0)/100.0
			print "2016: generating toys for "+this_sig+" with r from "+str(mean_r_2016*0.5)+" to "+str(mean_r_2016*1.7) +" wiht step of "+str(mean_r_2016*0.07)
                        for r in np.arange(mean_r_2016*0.3, mean_r_2016*1.7, mean_r_2016*0.07):
				print "generating toy for r = "+str(r)
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
                        for r in np.arange(mean_r_2016*1.7, mean_r_2016*4.0, mean_r_2016*0.2):
				print "generating toy for r = "+str(r)
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
				os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --singlePoint "+str(r)+" --saveToys --saveHybridResult -T 2000 --clsAcc 0 -s -1 -n "+this_sig+"_2016")
				
			os.system("hadd higgsCombine"+this_sig+"_2016.HybridNew.mH120.merged.root higgsCombine"+this_sig+"_2016.HybridNew.mH120.*.root")				
			os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+"_2016.HybridNew.mH120.merged.root -n "+this_sig+"_2016_Observed --plot=plots/limit_obs_scan_"+this_sig+"_2016.png ")	
			os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+"_2016.HybridNew.mH120.merged.root --expectedFromGrid 0.5 -n "+this_sig+"_2016_Exp0p5 --plot=plots/limit_exp0p5_scan_"+this_sig+"_2016.png")
			os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+"_2016.HybridNew.mH120.merged.root --expectedFromGrid 0.84 -n "+this_sig+"_2016_Exp0p84 --plot=plots/limit_exp0p84_scan_"+this_sig+"_2016.png")
			os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+"_2016.HybridNew.mH120.merged.root --expectedFromGrid 0.16 -n "+this_sig+"_2016_Exp0p16 --plot=plots/limit_exp0p16_scan_"+this_sig+"_2016.png")
			os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+"_2016.HybridNew.mH120.merged.root --expectedFromGrid 0.975 -n "+this_sig+"_2016_Exp0p975 --plot=plots/limit_exp0p975_scan_"+this_sig+"_2016.png")
			os.system("combine 2016/DelayedPhotonCard_"+this_sig_2016+".txt -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine"+this_sig+"_2016.HybridNew.mH120.merged.root --expectedFromGrid 0.025 -n "+this_sig+"_2016_Exp0p025 --plot=plots/limit_exp0p025_scan_"+this_sig+"_2016.png")

