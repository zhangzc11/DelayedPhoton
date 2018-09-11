#!/usr/bin/env python

import subprocess, time, sys, os, shlex


if __name__ == "__main__":
	sig_list_filename = sys.argv[1]
	pwd = os.getcwd()
	work_directory = pwd.replace("scripts_condor","")
	with open(sig_list_filename,"r") as sig_list_file:
		for this_sig in sig_list_file:
			sig_array = shlex.split(this_sig)
			env_script_n = pwd + "/submit_noBDT/" + sig_array[0]+"_datacard.sh"
			env_jdl_n = pwd + "/submit_noBDT/" + sig_array[0]+"_datacard.jdl"
			minsize = 2000
			actualsize = 0
			if os.path.isfile("../fit_results/datacards_3J_noBDT/higgsCombine"+sig_array[0]+".Asymptotic.mH120.root"):
				actualsize =os.path.getsize("../fit_results/datacards_3J_noBDT/higgsCombine"+sig_array[0]+".Asymptotic.mH120.root")
			if actualsize < minsize:
				print "job "+ sig_array[0]+"  failed, resubmitting now"
				os.system("rm "+ pwd + "/log_noBDT/"+sig_array[0]+"*")
				print "condor_submit "+env_jdl_n
				os.system("condor_submit "+env_jdl_n)

		
			
	
