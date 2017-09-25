from ROOT import *
import os, sys
sys.path.insert(0, '../')
from config_skim import *

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
print "Data tree: "
print fileNameData
print "Sig tree: "
print fileNameSig
print "GJets tree: "
print fileNameGJets
print "QCD tree: "
print fileNameQCD

'''
for i in range(0,len(fileNameData)):
	print "Data file "+str(i)+"  ... "
	fileThis = TFile(fileNameData[i], "READ")
	inputTree = fileThis.Get("DelayedPhoton")
	NEvents = fileThis.Get("NEvents")
	outputFile = TFile(fileNameData[i].replace("private_REMINIAOD","private_REMINIAOD/skim"),"RECREATE")
	outputFile.cd()	
	NEvents_out = NEvents.Clone()
	outputTree = inputTree.CopyTree(cut_skim)
	NEvents_out.Write()
	outputTree.Write()
	
'''
for i in range(0,len(fileNameSig)):
	print "Sig file "+str(i)+"  ... "
	fileThis = TFile(fileNameSig[i], "READ")
	inputTree = fileThis.Get("DelayedPhoton")
	NEvents = fileThis.Get("NEvents")
	outputFile = TFile(fileNameSig[i].replace("private_REMINIAOD","private_REMINIAOD/skim"),"RECREATE")
	outputFile.cd()	
	NEvents_out = NEvents.Clone()
	outputTree = inputTree.CopyTree(cut_skim)
	NEvents_out.Write()
	outputTree.Write()
	
'''
for i in range(0,len(fileNameGJets)):
	print "GJets file "+str(i)+"  ... "
	fileThis = TFile(fileNameGJets[i], "READ")
	inputTree = fileThis.Get("DelayedPhoton")
	NEvents = fileThis.Get("NEvents")
	outputFile = TFile(fileNameGJets[i].replace("private_REMINIAOD","private_REMINIAOD/skim"),"RECREATE")
	outputFile.cd()	
	NEvents_out = NEvents.Clone()
	outputTree = inputTree.CopyTree(cut_skim)
	NEvents_out.Write()
	outputTree.Write()
	
for i in range(0,len(fileNameQCD)):
	print "QCD file "+str(i)+"  ... "
	fileThis = TFile(fileNameQCD[i], "READ")
	inputTree = fileThis.Get("DelayedPhoton")
	NEvents = fileThis.Get("NEvents")
	outputFile = TFile(fileNameQCD[i].replace("private_REMINIAOD","private_REMINIAOD/skim"),"RECREATE")
	outputFile.cd()	
	NEvents_out = NEvents.Clone()
	outputTree = inputTree.CopyTree(cut_skim)
	outputTree.Write()
	NEvents_out.Write()
	
'''
