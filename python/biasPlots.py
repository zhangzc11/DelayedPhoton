from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array

from config import lumi
from config import outputDir

gROOT.SetBatch(True)

#gStyle.SetOptStat(0)
#gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
os.system("cp biasPlots.py "+outputDir)
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

biasFiles = [
		'bias_M1000GeV_Ctau500mm_0.00000',
		'bias_M1000GeV_Ctau500mm_0.00010',
		'bias_M1000GeV_Ctau500mm_0.00100',
		'bias_M1000GeV_Ctau500mm_0.01000',
		'bias_M1000GeV_Ctau500mm_0.02000',
		'bias_M1000GeV_Ctau500mm_0.10000',
		'bias_M1000GeV_Ctau500mm_0.50000'
	 	]



for fbias in biasFiles:
	
	file_bias = TFile("../fit_results/bias/"+fbias+".root")
	tree_bias = file_bias.Get("biasTree")
	
	histBias = TH1F("hbias","hbias",100,-15,10)
	
	tree_bias.Draw("-1.0*biasNorm>>hbias","status==0 && covStatus==3")

		
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

	histBias.SetTitle("")
	histBias.SetLineWidth(2)
        histBias.Draw()
        histBias.GetXaxis().SetTitleSize( axisTitleSize )
        histBias.GetXaxis().SetTitleOffset( axisTitleOffset )
        histBias.GetYaxis().SetTitleSize( axisTitleSize )
        histBias.GetYaxis().SetTitleOffset( axisTitleOffset )
        histBias.GetXaxis().SetTitle("(Ns_{fit} - Ns_{true})/#sigma_{Ns_{fit}}")
        histBias.GetYaxis().SetTitle("events")

	drawCMS2(myC, 13, lumi)	

	myC.SaveAs(outputDir+"/"+fbias+".pdf")
	myC.SaveAs(outputDir+"/"+fbias+".png")
	myC.SaveAs(outputDir+"/"+fbias+".C")



