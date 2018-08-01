from ROOT import *
import os, sys
#sys.path.insert(0, '../')
from config_noBDT import *

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
#################plot settings###########################
axisTitleSize = 0.06
axisTitleOffset = .8
axisTitleSizeRatioX   = 0.18
axisLabelSizeRatioX   = 0.12
axisTitleOffsetRatioX = 0.94
axisTitleSizeRatioY   = 0.15
axisLabelSizeRatioY   = 0.108
axisTitleOffsetRatioY = 0.32

leftMargin   = 0.12
rightMargin  = 0.05
topMargin    = 0.07
bottomMargin = 0.12
##############load delayed photon input tree#############

print "\n"
print "input file names: "
#print "Data tree: "
#print fileNameDataSkim
print "Sig tree: "
print fileNameSigSkim_this
#print "GJets tree: "
#print fileNameGJetsSkim
print "QCD tree: "
print fileNameQCDSkim
'''
for i in range(0,len(fileNameDataSkim)):
	print "Data file "+str(i)+"  ... "
	fileThis = TFile(fileNameDataSkim[i], "READ")
	inputTree = fileThis.Get("DelayedPhoton")
	NEvents = fileThis.Get("NEvents")
	outputFile = TFile(fileNameDataSkim[i].replace("private_REMINIAOD/withcut","private_REMINIAOD/skim"),"RECREATE")
	outputFile.cd()	
	NEvents_out = NEvents.Clone()
	outputTree = inputTree.CopyTree(cut_skim)
	NEvents_out.Write()
	outputTree.Write()
'''
for i in range(0,len(fileNameSigSkim_this)):
	print "Sig file "+str(i)+"  ... "
	fileThis = TFile(fileNameSigSkim_this[i].replace("private_REMINIAOD/withcut","private_REMINIAOD/withcut_BDT_train"), "READ")
	inputTree = fileThis.Get("DelayedPhoton")
	NEvents = fileThis.Get("NEvents")
	outputFile = TFile(fileNameSigSkim_this[i].replace("private_REMINIAOD/withcut","private_REMINIAOD/skim_BDT_train"),"RECREATE")
	outputFile.cd()	
	NEvents_out = NEvents.Clone()
	outputTree = inputTree.CopyTree(cut_skim)
	NEvents_out.Write()
	outputTree.Write()
'''
for i in range(0,len(fileNameGJetsSkim)):
	print "GJets file "+str(i)+"  ... "
	fileThis = TFile(fileNameGJetsSkim[i], "READ")
	inputTree = fileThis.Get("DelayedPhoton")
	NEvents = fileThis.Get("NEvents")
	outputFile = TFile(fileNameGJetsSkim[i].replace("private_REMINIAOD/withcut","private_REMINIAOD/skim"),"RECREATE")
	outputFile.cd()	
	NEvents_out = NEvents.Clone()
	outputTree = inputTree.CopyTree(cut_skim_bkg)
	NEvents_out.Write()
	outputTree.Write()
'''
for i in range(0,len(fileNameQCDSkim)):
	print "QCD file "+str(i)+"  ... "
	fileThis = TFile(fileNameQCDSkim[i].replace("private_REMINIAOD/withcut","private_REMINIAOD/withcut_BDT_train"), "READ")
	inputTree = fileThis.Get("DelayedPhoton")
	NEvents = fileThis.Get("NEvents")
	outputFile = TFile(fileNameQCDSkim[i].replace("private_REMINIAOD/withcut","private_REMINIAOD/skim_BDT_train"),"RECREATE")
	outputFile.cd()	
	NEvents_out = NEvents.Clone()
	outputTree = inputTree.CopyTree(cut_skim_bkg)
	outputTree.Write()
	NEvents_out.Write()
