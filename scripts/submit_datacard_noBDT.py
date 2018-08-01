#!/usr/bin/env python

import subprocess, time, sys, os, shlex

inputData = "/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_32p0742ifb.root"

queue = "cmscaf1nh"

inputSigDir = "/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/"

if __name__ == "__main__":
	sig_list_filename = sys.argv[1]
	pwd = os.getcwd()
	work_directory = pwd.replace("scripts","")
	os.system("mkdir -p "+pwd+"/submit_noBDT")
	with open(sig_list_filename,"r") as sig_list_file:
		for this_sig in sig_list_file:
			sig_array = shlex.split(this_sig)
			#print sig_array[0]
			#print sig_array[1]
			env_script_n = pwd + "/submit_noBDT/" + sig_array[0]+"_datacard.sh"
			env_script_f = open(env_script_n, 'w')
			env_script_f.write("#!/bin/bash\n")
			env_script_f.write("\n")
			env_script_f.write("cd " + work_directory + "\n")
			env_script_f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh \n")
			env_script_f.write("export SCRAM_ARCH=slc6_amd64_gcc530 \n")
			env_script_f.write("ulimit -c 0 \n")
			env_script_f.write("eval `scram runtime -sh` \n")
			env_script_f.write('echo "running on category 3J ======= " \n')
			env_script_f.write("./Fit2D "+inputData+" "+inputSigDir+"GMSB_"+sig_array[0]+"_13TeV-pythia8.root "+'"'+sig_array[0]+'" '+'"'+sig_array[1]+'" 3J datacard no \n')
			env_script_f.write("cd "+ work_directory +"fit_results/datacards_3J_noBDT \n")
			env_script_f.write('echo "L100TeV_Ctau1000cm limits below (3J):" \n')
			env_script_f.write("combine DelayedPhotonCard_"+sig_array[0]+".txt -M Asymptotic -n "+sig_array[0]+"\n")
	
			env_script_f.write('echo "running on category 2J ======= " \n')
			env_script_f.write("cd " + work_directory + "\n")
			env_script_f.write("./Fit2D "+inputData+" "+inputSigDir+"GMSB_"+sig_array[0]+"_13TeV-pythia8.root "+'"'+sig_array[0]+'" '+'"'+sig_array[1]+'" 2J datacard no \n')
	
			env_script_f.write("cd "+ work_directory +"fit_results/datacards_2J_noBDT \n")
			env_script_f.write('echo "L100TeV_Ctau1000cm limits below (2J):" \n')
			env_script_f.write("combine DelayedPhotonCard_"+sig_array[0]+".txt -M Asymptotic -n "+sig_array[0]+"\n")
	
			
			env_script_f.write('echo "combining 2J and 3J datacards:" \n')
			env_script_f.write("mkdir -p "+ work_directory +"fit_results/datacards_noBDT \n")
			env_script_f.write("cd "+ work_directory +"fit_results/datacards_noBDT \n")
			env_script_f.write("combineCards.py ch2J=../datacards_2J_noBDT/DelayedPhotonCard_"+sig_array[0]+".txt ch3J=../datacards_3J_noBDT/DelayedPhotonCard_"+sig_array[0]+".txt > DelayedPhotonCard_"+sig_array[0]+".txt \n")	
			env_script_f.write('echo "L100TeV_Ctau1000cm limits below (2J+3J):" \n')
			env_script_f.write("combine DelayedPhotonCard_"+sig_array[0]+".txt -M Asymptotic -n "+sig_array[0]+"\n")
		
			changePermission = subprocess.Popen(['chmod 777 ' + env_script_n], stdout=subprocess.PIPE, shell=True)
			debugout = changePermission.communicate()
			submit_s = 'bsub -q '+queue+' -o ' + pwd + "/submit_noBDT/"+sig_array[0]+"_datacard.log" + ' "source ' + env_script_n + '"'
			print "[submit_datacard]  '-- " + submit_s
			submitJobs = subprocess.Popen([submit_s], stdout=subprocess.PIPE, shell=True)
			output = (submitJobs.communicate()[0]).splitlines()
			print "[submit_datacard]  '-- " + output[0]


		
			
	
