#!/usr/bin/env python

import subprocess, time, sys, os, shlex


if __name__ == "__main__":
	sig_list_filename = sys.argv[1]
	pwd = os.getcwd()
	work_directory = pwd.replace("scripts_condor","")
	with open(sig_list_filename,"r") as sig_list_file:
		for this_sig in sig_list_file:
			sig_array = shlex.split(this_sig)
			env_script_n = pwd + "/submit_noBDT_ABCD_binAndDatacard/" + sig_array[0]+"_datacard.sh"
			env_jdl_n = pwd + "/submit_noBDT_ABCD_binAndDatacard/" + sig_array[0]+"_datacard.jdl"
			minsize = 1000
			actualsize = 0
			if os.path.isfile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/fitABCD_"+sig_array[0]+".tar"):
				actualsize =os.path.getsize("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/fitABCD_"+sig_array[0]+".tar")
			if actualsize < minsize:
				print "job "+ sig_array[0]+"  failed, resubmitting now"
				os.system("rm "+ pwd + "/log_noBDT_ABCD_binAndDatacard/"+sig_array[0]+"*")
				print "condor_submit "+env_jdl_n
				os.system("condor_submit "+env_jdl_n)

		
			
	
