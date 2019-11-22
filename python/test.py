from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TH2F
import os, sys
from Aux import *
from config_noBDT import cut, cut_GJets, cut_QCD_CR, cut_EWKCR, cut_noDisc, cut_noSigmaIetaIeta, cut_GJets_noSigmaIetaIeta, splots, lumi, outputDir, cut_noSminor, cut_GJets_noSminor, cut_blindMET, cut_blindTime, cut_MET_filter
from config_noBDT import fractionGJets, fractionQCD, useFraction, kFactor, cut_GJets, xbins_MET, xbins_time, sigLegend, weight_cut
import numpy as np
import array

print "Gjets CR cut ==="
print cut_GJets
print "QCD CR cut ==="
print cut_QCD_CR

print "SR cut ==="
print cut
