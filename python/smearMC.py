import ROOT as root
import os, sys
import numpy as np
import array
import random
from config_noBDT import fileNameSigSkim
from config_noBDT import fileNameGJetsSkim
from config_noBDT import fileNameQCDSkim
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
        	s.pho1ClusterTime_SmearToData221 = random.gauss(oldTree.pho1ClusterTime, smearTime)
        	newTree.Fill()


inFileName = "/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016B_ver1.root"
inFile = root.TFile(inFileName, "READ")
inTree = inFile.Get("DelayedPhoton")
inNevents = inFile.Get("NEvents")

outFile = root.TFile(inFileName.replace('skim','skim_smear'), 'RECREATE')
outTree = inTree.CloneTree(0)

s = MyStruct()
new_time_branch = outTree.Branch('pho1ClusterTime_SmearToData221',root.AddressOf(s, 'pho1ClusterTime_SmearToData221'), 'pho1ClusterTime_SmearToData221/F')

print "Writing new ROOT background file with smeared time"

smear_and_fill(inTree, outTree, s, 0.221)
outFile.cd()
outTree.GetCurrentFile().Write()
inNevents.Write()
outTree.GetCurrentFile().Close()


