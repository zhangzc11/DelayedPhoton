//C++ INCLUDES
#include <vector>
#include <fstream>
#include <iostream>
#include <math.h>   
//ROOT INCLUDES
//#include <TSYSTEM.h>
#include <TSystem.h>
#include <TTree.h>
#include <TLatex.h>
#include <TString.h>
#include <TFile.h>
#include <TH1D.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TF1.h>
#include <TBox.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <TColor.h>
#include <TGraphErrors.h>
#include <TRandom3.h>
#include <TLegend.h>
#include <TMath.h>
#include <TROOT.h>
#include <Math/GaussIntegrator.h>
#include <Math/IntegratorOptions.h>
#include <TFractionFitter.h>
#include <TRandom3.h>
//LOCAL INCLUDES
#include "Aux.hh"
//Axis
const float axisTitleSize = 0.06;
const float axisTitleOffset = .8;

const float axisTitleSizeRatioX   = 0.18;
const float axisLabelSizeRatioX   = 0.12;
const float axisTitleOffsetRatioX = 0.84;

const float axisTitleSizeRatioY   = 0.15;
const float axisLabelSizeRatioY   = 0.108;
const float axisTitleOffsetRatioY = 0.52;

//Margins
const float leftMargin   = 0.13;
const float rightMargin  = 0.05;
const float topMargin    = 0.07;
const float bottomMargin = 0.12;

using namespace std;


float getXsecBR(std::string sigModelName)
{
	float fxsecBR = 1.0;
	ifstream is("data/XsecBR.dat");
	while(!is.eof())
	{
		std::string name;
		std::string xsec;
		std::string BR;
		std::string xsecBR;
		is>>name;
		is>>xsec;
		is>>BR;
		is>>xsecBR;
		if(name.compare(sigModelName)==0)
		{
			fxsecBR = strtof(xsecBR.c_str(), 0);
			return fxsecBR;
		}
	}
	return fxsecBR;
}
;
