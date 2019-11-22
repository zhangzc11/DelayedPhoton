#!/usr/bin/env python

import subprocess, time, sys, os, shlex

outputDir = "/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/"


if __name__ == "__main__":
	sig_list_filename = sys.argv[1]
	version = sys.argv[2]
        year = sys.argv[3]
	pwd = os.getcwd()
	work_directory = pwd.replace("scripts_condor","")

	with open(sig_list_filename,"r") as sig_list_file:
		for this_sig in sig_list_file:
			sig_array = shlex.split(this_sig)
			sig_model = sig_array[0].replace("Ctau", "CTau")

			env_script_n = pwd + "/submit_HybridNew_"+year+"/" + sig_array[0]+"_datacard.sh"
			env_jdl_n = pwd + "/submit_HybridNew_"+year+"/" + sig_model+"_datacard.jdl"


			minsize = 200
			actualsize = 0
			if os.path.isfile("/mnt/hadoop"+outputDir+"HybridNew_"+version+"_"+year+"/"+sig_model+".tar"):
				actualsize =os.path.getsize("/mnt/hadoop"+outputDir+"HybridNew_"+version+"_"+year+"/"+sig_model+".tar")
			if actualsize < minsize:
				print "job "+ sig_array[0]+"  failed, resubmitting now"
				os.system("rm "+ pwd + "/log_HybridNew_"+year+"/"+sig_model+"*")
				print "condor_submit "+env_jdl_n
				os.system("condor_submit "+env_jdl_n)

		
			
	
