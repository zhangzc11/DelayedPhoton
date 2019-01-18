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
print "Data tree: "
print fileNameDataSkim
print "Sig tree: "
print fileNameSigSkim
print "GJets tree: "
print fileNameGJetsSkim
print "QCD tree: "
print fileNameQCDSkim

def GetKeyNames( self, dir = "" ):
        self.cd(dir)
        return [key.GetName() for key in gDirectory.GetListOfKeys()]
def GetClassNames( self, dir = "" ):
        self.cd(dir)
        return [key.GetClassName() for key in gDirectory.GetListOfKeys()]

TFile.GetKeyNames = GetKeyNames
TFile.GetClassNames = GetClassNames


#fileName_all = fileNameSigSkim + fileNameQCDSkim + fileNameGJetsSkim + fileNameDataSkim
#fileName_all = fileNameSigSkim + fileNameQCDSkim + fileNameGJetsSkim + fileNameEWKSkim
#fileName_all = fileNameEWKGSkim
fileName_all = fileNameSigNewSkim + fileNameEWKSkim + fileNameGJetsSkim + fileNameQCDSkim

for i in range(0,len(fileName_all)):
	print "skim file "+fileName_all[i]

	fileThis = TFile(fileName_all[i], "READ")
	keyList = fileThis.GetKeyNames()
	classList = fileThis.GetClassNames()
	outputFile = TFile(fileName_all[i].replace("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut","/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT"),"RECREATE")

	outputFile.cd()

	for j in range(0, len(keyList)):
		print classList[j] + "   ===   " + keyList[j]
		if classList[j] == "TTree":
			fileThis.cd()
			inputTree = fileThis.Get(keyList[j])
			outputFile.cd()
			outputTree = inputTree.CopyTree(cut_skim)
			outputTree.Write()
		if classList[j] == "TH1F":
			fileThis.cd()
			histThis = fileThis.Get(keyList[j])
			outputFile.cd()
			histThis_out = histThis.Clone()
			histThis_out.Write()

