#!/usr/bin/env python

import subprocess, time, sys, os, shlex


outputDir = "/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/"


if __name__ == "__main__":
	sig_list_filename = sys.argv[1]
	version = sys.argv[2]
	year = sys.argv[3]
	pwd = os.getcwd()
	work_directory = pwd.replace("scripts_condor","")
	os.system("mkdir -p "+pwd+"/submit_HybridNew_"+year)
	os.system("rm "+pwd+"/submit_HybridNew_"+year+"/*")
	os.system("mkdir -p "+pwd+"/log_HybridNew_"+year)
	os.system("rm "+pwd+"/log_HybridNew_"+year+"/*")
	os.system("hadoop fs -mkdir "+outputDir+"HybridNew_"+version+"_"+year)
	with open(sig_list_filename,"r") as sig_list_file:
		for this_sig in sig_list_file:
			sig_array = shlex.split(this_sig)
			env_script_n = pwd + "/submit_HybridNew_"+year+"/" + sig_array[0]+"_datacard.sh"
			sig_model = sig_array[0].replace("Ctau", "CTau")

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

			env_script_f.write("cd ${currentDir} \n")
			env_script_f.write("mkdir "+sig_model+" \n")
			env_script_f.write("echo "+sig_model+" >> list.list \n")
			env_script_f.write("cp "+ work_directory + "/combine/HybridNew/run_HybridNew_condor_"+year+".py ./ \n")
			env_script_f.write("cp -r "+ work_directory + "/combine/datacards/2016_"+version+" 2016 \n")
			env_script_f.write("cp -r "+ work_directory + "/combine/datacards/2017_"+version+" 2017 \n")
			env_script_f.write("cp -r "+ work_directory + "/combine/datacards/combine_"+version+" combine \n")
			env_script_f.write("cp -r "+ work_directory + "/combine/limitTrees_"+version+" limitTrees \n")

			env_script_f.write("python run_HybridNew_condor_"+year+".py list.list \n")
			env_script_f.write("mv *.root "+sig_model+" \n")
			env_script_f.write("mv plots "+sig_model+" \n")
	
			env_script_f.write("cd ${currentDir} \n")
			env_script_f.write("tar -zcvf "+sig_model+".tar "+sig_model+"\n")
			env_script_f.write("x509loc=${X509_USER_PROXY} \n")
			env_script_f.write("env -i X509_USER_PROXY=${x509loc} gfal-copy -f --checksum-mode=both "+sig_model+".tar gsiftp://transfer.ultralight.org/"+outputDir+"HybridNew_"+version+"_"+year+"/"+sig_model+".tar \n")

			env_script_f.write("date\n")
			env_script_f.write("rm -rf * \n")
			env_script_f.close()
			env_jdl_n = pwd + "/submit_HybridNew_"+year+"/" + sig_model+"_datacard.jdl"
                        env_jdl_f = open(env_jdl_n, 'w')
                        env_jdl_f.write("Universe = vanilla\n")		
                        env_jdl_f.write("Executable = "+env_script_n+"\n")		
                        env_jdl_f.write("Log = log_HybridNew_"+year+"/"+sig_model+"_PC.log\n")		
                        env_jdl_f.write("Output = log_HybridNew_"+year+"/"+sig_model+"_$(Cluster).$(Process).out\n")		
                        env_jdl_f.write("Error = log_HybridNew_"+year+"/"+sig_model+"_$(Cluster).$(Process).err\n")		
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

