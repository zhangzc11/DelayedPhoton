import ROOT as root
import os, sys
import numpy as np
import array
import random
from config_noBDT import fileNameSigSkim
from config_noBDT import fileNameGJetsSkim
from config_noBDT import fileNameQCDSkim
from config_noBDT import fileNameData
from config_noBDT import fileNameDataSkim

root.gROOT.ProcessLine("struct MyStruct{float pho1ClusterTime_SmearToData221;};")
from ROOT import MyStruct

random.seed(920728)

def smear_and_fill(oldTree, newTree, s, smearTime):
	num_entries = oldTree.GetEntries()
    	for i in range(num_entries):
        	oldTree.GetEntry(i)
        	if i % 10000 == 0:
            		print "Processing event {} of {}".format(i, num_entries)
        	if smearTime > 0.00001:
			s.pho1ClusterTime_SmearToData221 = random.gauss(oldTree.pho1ClusterTime, smearTime)
		else:
			s.pho1ClusterTime_SmearToData221 = oldTree.pho1ClusterTime

        	newTree.Fill()

def smear_file(inFileName, smearTime):
	#inFileName = "/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016B_ver1.root"
	inFile = root.TFile(inFileName, "READ")
	inTree = inFile.Get("DelayedPhoton")
	inNevents = inFile.Get("NEvents")

	outFile = root.TFile(inFileName.replace('skim','skim_smear'), 'RECREATE')
	outTree = inTree.CloneTree(0)

	s = MyStruct()
	new_time_branch = outTree.Branch('pho1ClusterTime_SmearToData221',root.AddressOf(s, 'pho1ClusterTime_SmearToData221'), 'pho1ClusterTime_SmearToData221/F')

	print "Writing new ROOT background file with smeared time"

	smear_and_fill(inTree, outTree, s, smearTime)
	outFile.cd()
	outTree.GetCurrentFile().Write()
	inNevents.Write()
	outTree.GetCurrentFile().Close()

'''
for i in range(0, len(fileNameSigSkim)):
	print "smearing Sig file "+str(i)+"  ... "
	smear_file(fileNameSigSkim[i].replace("private_REMINIAOD/withcut","private_REMINIAOD/skim"), 0.221)

for i in range(0, len(fileNameGJetsSkim)):
	print "smearing GJets file "+str(i)+"  ... "
	smear_file(fileNameGJetsSkim[i].replace("private_REMINIAOD/withcut","private_REMINIAOD/skim"), 0.221)

for i in range(0, len(fileNameQCDSkim)):
	print "smearing QCD file "+str(i)+"  ... "
	smear_file(fileNameQCDSkim[i].replace("private_REMINIAOD/withcut","private_REMINIAOD/skim"), 0.221)
'''

print "smearing Data file"
for i in range(0, len(fileNameDataSkim)):
        newFileNameThis = fileNameDataSkim[i].replace("private_REMINIAOD/withcut", "private_REMINIAOD/skim")
        newFileNameThis_GoodLumi = newFileNameThis.replace(".root","_GoodLumi.root")
        print "reweighting Data file: "+newFileNameThis_GoodLumi
	smear_file(newFileNameThis_GoodLumi, 0.0)


