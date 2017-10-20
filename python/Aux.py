#! /usr/bin/env python
from ROOT import *

def drawCMS(myC, energy, lumi):

	myC.cd()

        tlatex = TLatex()
        baseSize = 25
        tlatex.SetNDC()
        tlatex.SetTextAngle(0)
        tlatex.SetTextColor(kBlack)
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

