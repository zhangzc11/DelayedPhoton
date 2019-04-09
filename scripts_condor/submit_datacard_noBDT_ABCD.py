#!/usr/bin/env python

import subprocess, time, sys, os, shlex

inputData = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root"

inputSigDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"

outputDir = "/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/"

outputDir_mnt = "/mnt/hadoop"+outputDir

os.system("rm -rf "+outputDir_mnt+"/2016ABCD/*noBDT \n")
os.system("mkdir -p "+outputDir_mnt+" \n")
os.system("mkdir -p "+outputDir_mnt+"/2016ABCD \n")
os.system("mkdir -p "+outputDir_mnt+"/2016ABCD/datacards_3J_noBDT/ \n")
os.system("mkdir -p "+outputDir_mnt+"/2016ABCD/datacards_2J_noBDT/ \n")
os.system("mkdir -p "+outputDir_mnt+"/2016ABCD/plots_2J_noBDT/ \n")
os.system("mkdir -p "+outputDir_mnt+"/2016ABCD/plots_3J_noBDT/ \n")
os.system("mkdir -p "+outputDir_mnt+"/2016ABCD/binning_2J_noBDT/ \n")
os.system("mkdir -p "+outputDir_mnt+"/2016ABCD/binning_3J_noBDT/ \n")
os.system("mkdir -p "+outputDir_mnt+"/2016ABCD/datacards_noBDT/ \n")


if __name__ == "__main__":
	sig_list_filename = sys.argv[1]
	pwd = os.getcwd()
	work_directory = pwd.replace("scripts_condor","")
	os.system("mkdir -p "+pwd+"/submit_noBDT_ABCD")
	os.system("rm "+pwd+"/submit_noBDT_ABCD/*")
	os.system("mkdir -p "+pwd+"/log_noBDT_ABCD")
	os.system("rm "+pwd+"/log_noBDT_ABCD/*")
	with open(sig_list_filename,"r") as sig_list_file:
		for this_sig in sig_list_file:
			sig_array = shlex.split(this_sig)
			env_script_n = pwd + "/submit_noBDT_ABCD/" + sig_array[0]+"_datacard.sh"
			env_script_f = open(env_script_n, 'w')
			env_script_f.write("#!/bin/bash\n")
			env_script_f.write("\n")
			env_script_f.write("hostname\n")
			env_script_f.write("date\n")
			env_script_f.write("currentDir=`pwd` \n")
			env_script_f.write("cd " + work_directory + "\n")
			env_script_f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh \n")
			env_script_f.write("export SCRAM_ARCH=slc6_amd64_gcc530 \n")
			env_script_f.write("ulimit -c 0 \n")
			env_script_f.write("eval `scram runtime -sh` \n")
			env_script_f.write('echo "running on category 3J ======= " \n')

			env_script_f.write("cd ${currentDir} \n")
			env_script_f.write("cp "+ work_directory + "/FitABCD ./ \n")
			env_script_f.write("cp -r "+ work_directory + "/data ./ \n")

			env_script_f.write("./FitABCD "+inputData+" "+inputSigDir+"GMSB_"+sig_array[0]+"_13TeV-pythia8.root "+'"'+sig_array[0]+'" '+'"'+sig_array[1]+'" 3J datacard no \n')
			env_script_f.write("cd fit_results/2016ABCD/datacards_3J_noBDT \n")
			env_script_f.write('echo "L100TeV_Ctau1000cm limits below (3J):" \n')
			env_script_f.write("combine DelayedPhotonCard_"+sig_array[0]+".txt -M Asymptotic -n "+sig_array[0]+"\n")

	
			env_script_f.write("cd ${currentDir} \n")
			#env_script_f.write("cp fit_results/2016ABCD/plots_3J_noBDT/* "+outputDir_mnt+"/2016ABCD/plots_3J_noBDT/ \n")
			#env_script_f.write("cp fit_results/2016ABCD/binning_3J_noBDT/* "+outputDir_mnt+"/2016ABCD/binning_3J_noBDT/ \n")
			#env_script_f.write("cp fit_results/2016ABCD/datacards_3J_noBDT/* "+outputDir_mnt+"/2016ABCD/datacards_3J_noBDT/ \n")

			#env_script_f.write('echo "running on category 2J ======= " \n')
			#env_script_f.write("./FitABCD "+inputData+" "+inputSigDir+"GMSB_"+sig_array[0]+"_13TeV-pythia8.root "+'"'+sig_array[0]+'" '+'"'+sig_array[1]+'" 2J datacard no \n')
	
			#env_script_f.write("cd fit_results/2016ABCD/datacards_2J_noBDT \n")
			#env_script_f.write('echo "L100TeV_Ctau1000cm limits below (2J):" \n')
			#env_script_f.write("combine DelayedPhotonCard_"+sig_array[0]+".txt -M Asymptotic -n "+sig_array[0]+"\n")
			
			#env_script_f.write("cd ${currentDir} \n")
			#env_script_f.write("cp fit_results/2016ABCD/datacards_2J_noBDT/* "+outputDir_mnt+"/2016ABCD/datacards_2J_noBDT/ \n")
			#env_script_f.write("cp fit_results/2016ABCD/plots_2J_noBDT/* "+outputDir_mnt+"/2016ABCD/plots_2J_noBDT/ \n")
			#env_script_f.write("cp fit_results/2016ABCD/binning_2J_noBDT/* "+outputDir_mnt+"/2016ABCD/binning_2J_noBDT/ \n")
			#env_script_f.write('echo "combining 2J and 3J datacards:" \n')
			#env_script_f.write("mkdir -p fit_results/2016ABCD/datacards_noBDT \n")
			#env_script_f.write("cd fit_results/2016ABCD/datacards_noBDT \n")
			#env_script_f.write("combineCards.py ch2J=../datacards_2J_noBDT/DelayedPhotonCard_"+sig_array[0]+".txt ch3J=../datacards_3J_noBDT/DelayedPhotonCard_"+sig_array[0]+".txt > DelayedPhotonCard_"+sig_array[0]+".txt \n")	
			#env_script_f.write('echo "L100TeV_Ctau1000cm limits below (2J+3J):" \n')
			#env_script_f.write("combine DelayedPhotonCard_"+sig_array[0]+".txt -M Asymptotic -n "+sig_array[0]+"\n")

			#env_script_f.write("cd ${currentDir} \n")
			#env_script_f.write("cp fit_results/2016ABCD/datacards_noBDT/* "+outputDir_mnt+"/2016ABCD/datacards_noBDT/ \n")
			env_script_f.write("tar -zcvf fitABCD_"+sig_array[0]+".tar fit_results/2016ABCD/\n")
			env_script_f.write("x509loc=${X509_USER_PROXY}")
			env_script_f.write("env -i X509_USER_PROXY=${x509loc} gfal-copy -f --checksum-mode=bothfitABCD_"+sig_array[0]+" gsiftp://transfer.ultralight.org/"+outputDir+sig_array[0]+" \n")


			env_script_f.write("date\n")
			env_script_f.close()
	
			env_jdl_n = pwd + "/submit_noBDT_ABCD/" + sig_array[0]+"_datacard.jdl"
                        env_jdl_f = open(env_jdl_n, 'w')
                        env_jdl_f.write("Universe = vanilla\n")		
                        env_jdl_f.write("Executable = "+env_script_n+"\n")		
                        env_jdl_f.write("Log = log_noBDT_ABCD/"+sig_array[0]+"_PC.log\n")		
                        env_jdl_f.write("Output = log_noBDT_ABCD/"+sig_array[0]+"_$(Cluster).$(Process).out\n")		
                        env_jdl_f.write("Error = log_noBDT_ABCD/"+sig_array[0]+"_$(Cluster).$(Process).err\n")		
                        env_jdl_f.write('Requirements=TARGET.OpSysAndVer=="CentOS7"\n')		
                        env_jdl_f.write("should_transfer_files = YES\n")		
                        env_jdl_f.write("RequestMemory = 2000\n")		
                        env_jdl_f.write("RequestCpus = 1\n")		
                        env_jdl_f.write("x509userproxy = $ENV(X509_USER_PROXY)\n")		
                        env_jdl_f.write("+RunAsOwner = True\n")		
                        env_jdl_f.write("+InteractiveUser = true\n")		
                        env_jdl_f.write('+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/bbockelm/cms:rhel7"\n')		
                        env_jdl_f.write("+SingularityBindCVMFS = True\n")		
                        env_jdl_f.write("run_as_owner = True\n")		
                        env_jdl_f.write("when_to_transfer_output = ON_EXIT\n")		
                        env_jdl_f.write("Queue 1\n")		
			env_jdl_f.close()
			print "condor_submit "+env_jdl_n
	
			os.system("condor_submit "+env_jdl_n)

