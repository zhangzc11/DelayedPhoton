from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import weight_cut, fileNameData, fileNameSig

gROOT.SetBatch(True)

cut_blind = "(pho1ClusterTime_SmearToData < 3 || t1MET < 200)"
cut_trigger = "(HLTDecision[81] == 1)"
cut_photonID = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && pho1SigmaIetaIeta < 0.00994"
cut_nJets = "n_Jets > 2"
cut_nPhotons = "n_Photons == 2"
cut_MET_filter = "Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"


inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"

tableFileName = "./cut_flow_Table.txt"
#Data
fileData = TFile(fileNameData)
treeData = fileData.Get("DelayedPhoton")
n_blindData = treeData.GetEntries(cut_blind)
print n_blindData
n_triggerData = treeData.GetEntries(cut_blind+"&&"+cut_trigger)
print n_triggerData
n_photonIDData = treeData.GetEntries(cut_blind+"&&"+cut_trigger+"&&"+cut_photonID)
print n_photonIDData
n_nJetsData = treeData.GetEntries(cut_blind+"&&"+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets)
print n_nJetsData
n_nPhotonsData = treeData.GetEntries(cut_blind+"&&"+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+"&&"+cut_nPhotons)
print n_nPhotonsData
n_MET_filterData = treeData.GetEntries(cut_blind+"&&"+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+"&&"+cut_nPhotons+"&&"+cut_MET_filter)
print n_MET_filterData

#Sig
fileSig = TFile(fileNameSig)
hNEventsThis = fileSig.Get("NEvents")
N_total = hNEventsThis.GetBinContent(1)
lumi_xs = 0.00174708*35922.0/N_total
treeSig = fileSig.Get("DelayedPhoton")
n_blindSig = lumi_xs*treeSig.GetEntries(weight_cut+"1.0")
print n_blindSig
n_triggerSig = lumi_xs*treeSig.GetEntries(weight_cut+"("+cut_trigger+")")
print n_triggerSig
n_photonIDSig = lumi_xs*treeSig.GetEntries(weight_cut+"("+cut_trigger+"&&"+cut_photonID+")")
print n_photonIDSig
n_nJetsSig = lumi_xs*treeSig.GetEntries(weight_cut+"("+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+")")
print n_nJetsSig
n_nPhotonsSig = lumi_xs*treeSig.GetEntries(weight_cut+"("+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+"&&"+cut_nPhotons+")")
print n_nPhotonsSig
n_MET_filterSig = lumi_xs*treeSig.GetEntries(weight_cut+"("+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+"&&"+cut_nPhotons+"&&"+cut_MET_filter+")")
print n_MET_filterSig

print n_blindSig/np.sqrt(n_blindSig)
print int(100.0*n_triggerSig/n_blindSig)

f1=open(tableFileName, 'a')

#print  "without cut (data blinded) & "+ "%.0f " % n_blindSig + "(100\\%)& "+"%.0f " % n_blindSig + "(100\\%) & "+ "%.5f" % float(n_blindSig/np.sqrt(float(n_blindSig))) + "\\\\"
print  "without cut (data blinded) & "+ "%.0f " % n_blindData + "(100\\%)& "+"%.2f " % n_blindSig + "(100\\%) & "+ "%.5f" % float(n_blindSig/np.sqrt(float(n_blindData))) + "\\\\"
print  "+ trigger path& "+"%.0f" % n_triggerData+"("+"%.0f"%float(100.0*n_triggerData/n_blindData)+"\\%)  & "+"%.2f"%n_triggerSig + "("+"%.0f"%float(100.0*n_triggerSig/n_blindSig)+"\\%) & "+"%.5f"%float(n_triggerSig/np.sqrt(n_triggerData))+"\\\\"
print  "+ photon ID cut& "+"%.0f" % n_photonIDData+"("+"%.0f"%float(100.0*n_photonIDData/n_blindData)+"\\%)  & "+"%.2f"%n_photonIDSig + "("+"%.0f"%float(100.0*n_photonIDSig/n_blindSig)+"\\%) & "+"%.5f"%float(n_photonIDSig/np.sqrt(n_photonIDData))+"\\\\"
print  "+ nJets cut& "+"%.0f" % n_nJetsData+"("+"%.0f"%float(100.0*n_nJetsData/n_blindData)+"\\%)  & "+"%.2f"%n_nJetsSig + "("+"%.0f"%float(100.0*n_nJetsSig/n_blindSig)+"\\%) & "+"%.5f"%float(n_nJetsSig/np.sqrt(n_nJetsData))+"\\\\"
print  "+ nPhotons cut& "+"%.0f" % n_nPhotonsData+"("+"%.0f"%float(100.0*n_nPhotonsData/n_blindData)+"\\%)  & "+"%.2f"%n_nPhotonsSig + "("+"%.0f"%float(100.0*n_nPhotonsSig/n_blindSig)+"\\%) & "+"%.5f"%float(n_nPhotonsSig/np.sqrt(n_nPhotonsData))+"\\\\"
print  "+ MET filters & "+"%.0f" % n_MET_filterData+"("+"%.0f"%float(100.0*n_MET_filterData/n_blindData)+"\\%)  & "+"%.2f"%n_MET_filterSig + "("+"%.0f"%float(100.0*n_MET_filterSig/n_blindSig)+"\\%) & "+"%.5f"%float(n_MET_filterSig/np.sqrt(n_MET_filterData))+"\\\\"

