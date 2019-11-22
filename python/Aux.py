#! /usr/bin/env python
from ROOT import TLatex, TCanvas
import shlex

def getXsecBR(Lambda, Ctau):
        fxsecBR = 0.0
        efxsecBR = 0.0
        Ctau_this=str(Ctau)
        if Ctau_this == "0.1":
                Ctau_this = "0_1"
        if Ctau_this == "0.01":
                Ctau_this = "0_01"

        model_to_find="L"+str(Lambda)+"TeV_Ctau"+Ctau_this+"cm"

        with open("../data/XsecBR.dat","r") as xsec_file:
                for this_model in xsec_file:
                        this_model_array = shlex.split(this_model)
                        if this_model_array[0] == model_to_find:
                                #print this_model
                                fxsecBR = float(this_model_array[4])
                                efxsecBR = float(this_model_array[5])
        #print model_to_find
        return fxsecBR,efxsecBR

def drawCMS(myC, energy, lumi):

	myC.cd()

        tlatex = TLatex()
        baseSize = 25
        tlatex.SetNDC()
        tlatex.SetTextAngle(0)
        tlatex.SetTextColor(1)
        tlatex.SetTextFont(63)
        tlatex.SetTextAlign(11)
        tlatex.SetTextSize(25)
        tlatex.DrawLatex(0.16, 0.92, "CMS")
        tlatex.SetTextFont(53)
        tlatex.DrawLatex(0.23, 0.92, "Preliminary")
        tlatex.SetTextFont(43)
        tlatex.SetTextSize(23)
	lumiString = "%.2f" % lumi
        Lumi = "" + lumiString + " pb^{-1} ("+str(energy)+" TeV)"
        if lumi > 1000:
		lumiString = "%.2f" % (lumi/1000.0)
                Lumi = "" + lumiString + " fb^{-1} ("+str(energy)+" TeV)"
        tlatex.SetTextAlign(31)
        tlatex.DrawLatex(0.9, 0.92, Lumi)
        tlatex.SetTextAlign(11)

def drawCMS2(myC, energy, lumi):

	myC.cd()

        tlatex = TLatex()
        baseSize = 25
        tlatex.SetNDC()
        tlatex.SetTextAngle(0)
        tlatex.SetTextColor(1)
        tlatex.SetTextFont(63)
        tlatex.SetTextAlign(11)
        tlatex.SetTextSize(25)
        tlatex.DrawLatex(0.16, 0.95, "CMS")
        tlatex.SetTextFont(53)
        tlatex.DrawLatex(0.23, 0.95, "Preliminary")
        tlatex.SetTextFont(43)
        tlatex.SetTextSize(23)
	lumiString = "%.1f" % lumi
        Lumi = "" + lumiString + " pb^{-1} ("+str(energy)+" TeV)"
        if lumi > 1000:
		lumiString = "%.1f" % (lumi/1000.0)
                Lumi = "" + lumiString + " fb^{-1} ("+str(energy)+" TeV)"
        tlatex.SetTextAlign(31)
        tlatex.DrawLatex(0.9, 0.95, Lumi)
        tlatex.SetTextAlign(11)


def drawCMS3(myC, energy, lumi):
        myC.cd()

        tlatex = TLatex()
        baseSize = 25
        tlatex.SetNDC()
        tlatex.SetTextAngle(0)
        tlatex.SetTextColor(1)
        tlatex.SetTextFont(63)
        tlatex.SetTextAlign(11)
        tlatex.SetTextSize(25)
        tlatex.DrawLatex(0.18, 0.96, "CMS")
        tlatex.SetTextFont(53)
        tlatex.DrawLatex(0.26, 0.96, "Preliminary")
        tlatex.SetTextFont(43)
        tlatex.SetTextSize(23)
        lumiString = "%.1f" % lumi
        Lumi = "" + lumiString + " pb^{-1} ("+str(energy)+" TeV)"
        if lumi > 1000:
                lumiString = "%.1f" % (lumi/1000.0)
                Lumi = "" + lumiString + " fb^{-1} ("+str(energy)+" TeV)"
        tlatex.SetTextAlign(31)
        tlatex.DrawLatex(0.85, 0.96, Lumi)
        tlatex.SetTextAlign(11)

