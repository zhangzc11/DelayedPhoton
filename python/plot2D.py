from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array

from config import lumi
from config import cut
from config import fileNameData
from config import outputDir

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)
gStyle.SetPalette(1)

os.system("mkdir -p "+outputDir)
#os.system("mkdir -p ../data")
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

	
file_data = TFile(fileNameData)
tree_data = file_data.Get("DelayedPhoton")

histBias = TH2F("hdata","hdata",100,-10,15, 100, 0, 600)

tree_data.Draw("MET:pho1ClusterTime>>hdata",cut)
	
myC = TCanvas( "myC", "myC", 200, 10, 800, 800 )
myC.SetHighLightColor(2)
myC.SetFillColor(0)
myC.SetBorderMode(0)
myC.SetBorderSize(2)
myC.SetLeftMargin( leftMargin )
myC.SetRightMargin( rightMargin )
myC.SetTopMargin( topMargin )
myC.SetBottomMargin( bottomMargin )
myC.SetFrameBorderMode(0)
myC.SetFrameBorderMode(0)

N_blind = 5
x_blind = [1.0,15.0,15.0,1.0,1.0]
y_blind = [100.0,100.0,600.0,600.0,100.0]
graph_blind = TGraph(N_blind, np.array(x_blind), np.array(y_blind))
graph_blind.SetFillColor(kOrange+3)


histBias.SetTitle("")
histBias.Draw("COLZ")
graph_blind.Draw("Fsame")

histBias.GetXaxis().SetTitleSize( axisTitleSize )
histBias.GetXaxis().SetTitleOffset( axisTitleOffset )
histBias.GetYaxis().SetTitleSize( axisTitleSize )
histBias.GetYaxis().SetTitleOffset( axisTitleOffset )
histBias.GetXaxis().SetTitle("#gamma cluster time [ns]")
histBias.GetYaxis().SetTitle("#slash{E}_{T} [GeV]")


drawCMS2(myC, 13, lumi)	

myC.Modified()
myC.Update()

myC.SaveAs(outputDir+"/MET_Time_2D_blinded.pdf")
myC.SaveAs(outputDir+"/MET_Time_2D_blinded.png")
myC.SaveAs(outputDir+"/MET_Time_2D_blinded.C")



