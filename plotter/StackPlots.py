from ROOT import *
import os, sys
sys.path.insert(0, '../')
from config import *

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)

##############load delayed photon input tree#############

print "\n"
print "input file names: "
print "Data tree: "+fileNameData
print "GJets tree: "+fileNameGJets
print "QCD tree: "+fileNameQCD
print "Sig tree: "+fileNameSig

fileData = TFile(fileNameData)
fileGJets = TFile(fileNameGJets)
fileQCD = TFile(fileNameQCD)
fileSig = TFile(fileNameSig)

treeData = fileData.Get("DelayedPhoton")
treeGJets = fileGJets.Get("DelayedPhoton")
treeQCD = fileQCD.Get("DelayedPhoton")
treeSig = fileSig.Get("DelayedPhoton")

nEntriesData = treeData.GetEntries()
nEntriesGJets = treeGJets.GetEntries()
nEntriesQCD = treeQCD.GetEntries()
nEntriesSig = treeSig.GetEntries()

print "\n"
print "number of events in tree: "
print "Data: " + str(treeData.GetEntries())
print "GJets: " + str(treeGJets.GetEntries())
print "QCD: " + str(treeQCD.GetEntries())
print "Sig: " + str(treeSig.GetEntries())

print "\n cut = " + cut



