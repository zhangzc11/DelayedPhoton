#!/usr/bin/env python

import subprocess, time, sys, os, shlex

inputData = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root"

inputSigDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"


if __name__ == "__main__":
	sig_list_filename = sys.argv[1]
	pwd = os.getcwd()
	work_directory = pwd.replace("scripts_condor","")
	env_script_n = pwd + "/run_datacard_noBDT.sh"
	env_script_f = open(env_script_n, 'w')
	env_script_f.write("#!/bin/bash\n")
	env_script_f.write("date\n")

	with open(sig_list_filename,"r") as sig_list_file:
		for this_sig in sig_list_file:
			sig_array = shlex.split(this_sig)
			env_script_f.write("cd " + work_directory + "\n")
			env_script_f.write('echo "running on category 3J ======= for signal model '+sig_array[0]+'" \n')
			env_script_f.write("./Fit2D "+inputData+" "+inputSigDir+"GMSB_"+sig_array[0]+"_13TeV-pythia8.root "+'"'+sig_array[0]+'" '+'"'+sig_array[1]+'" 3J datacard no \n')
			env_script_f.write("cd "+ work_directory +"fit_results/2016/datacards_3J_noBDT \n")
			env_script_f.write('echo "'+sig_array[0]+' limits below (3J):" \n')
			env_script_f.write("combine DelayedPhotonCard_"+sig_array[0]+".txt -M Asymptotic -n "+sig_array[0]+"\n")
	
			env_script_f.write("date\n")
	env_script_f.close()
			
	
