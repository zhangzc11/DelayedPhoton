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
const float axisTitleOffset = 0.9;

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

void DrawDataBkgSig(TH1F *h1Data, TH1F *h1Bkg, TH1F *h1Sig, TH1F *h1all, float lumi, std::string sigModelTitle, std::string sigModelName, std::string suffix, TString outPlotsDir)
{
	
	
	TCanvas *myC = new TCanvas( "myC", "myC", 200, 10, 800, 800 );
        myC->SetHighLightColor(2);
        myC->SetFillColor(0);
        myC->SetBorderMode(0);
        myC->SetBorderSize(2);
        myC->SetLeftMargin( leftMargin );
        myC->SetRightMargin( rightMargin );
        myC->SetTopMargin( topMargin );
        myC->SetBottomMargin( bottomMargin );
        myC->SetFrameBorderMode(0);
        myC->SetFrameBorderMode(0);
	myC->SetLogy(1);	
	
	h1Data->SetLineWidth(2);
	h1Data->SetLineColor(kBlack);
	h1Data->SetMarkerStyle(8);
	h1Data->GetYaxis()->SetTitleSize(axisTitleSize);
	h1Data->GetXaxis()->SetTitleSize(axisTitleSize);
	h1Data->GetYaxis()->SetTitleOffset(axisTitleOffset);
	h1Data->GetXaxis()->SetTitleOffset(axisTitleOffset);

	h1Data->Draw("E");
	//h1Data->GetYaxis()->SetRangeUser(1e-3, 1000.0*std::max(h1Data->GetMaximum(), h1Bkg->GetMaximum(), h1Sig->GetMaximum()));
	h1Data->GetYaxis()->SetRangeUser(1e-3, 1000.0*h1Data->GetMaximum());
	
	h1Bkg->SetLineColor(kBlue);
	h1Bkg->SetLineWidth(2);
	h1Sig->SetLineColor(kGreen);
	h1Sig->SetLineWidth(2);
	h1all->SetLineColor(kRed);
	h1all->SetLineWidth(2);

	h1Bkg->Draw("samehisto");
	h1Sig->Draw("samehisto");
	h1all->Draw("samehisto");
	
	TLegend * leg = new TLegend(0.18, 0.7, 0.93, 0.89);
        leg->SetNColumns(2);
        leg->SetBorderSize(0);
        leg->SetTextSize(0.03);
        leg->SetLineColor(1);
        leg->SetLineStyle(1);
        leg->SetLineWidth(1);
        leg->SetFillColor(0);
        leg->SetFillStyle(1001);
        leg->AddEntry(h1Data,"data","lep");
        leg->AddEntry(h1Bkg,"#gamma + jets/QCD bkg","l");
        leg->AddEntry(h1Sig, sigModelTitle.c_str(),"l");
        leg->AddEntry(h1all,"combined fit","l");
        leg->Draw();

	DrawCMS(myC, 13, lumi);
        myC->SetTitle("");
        myC->SaveAs("fit_results/"+outPlotsDir+("/"+sigModelName+"_fit_bkgsig_"+suffix+".pdf").c_str());
        myC->SaveAs("fit_results/"+outPlotsDir+("/"+sigModelName+"_fit_bkgsig_"+suffix+".png").c_str());
        myC->SaveAs("fit_results/"+outPlotsDir+("/"+sigModelName+"_fit_bkgsig_"+suffix+".C").c_str());
	
}
;


void DrawCMS(TCanvas *myC, int energy, float lumi)
{
	myC->cd();
	TLatex *tlatex =  new TLatex();
	
	tlatex->SetNDC();
        tlatex->SetTextAngle(0);
        tlatex->SetTextColor(kBlack);
        tlatex->SetTextFont(63);
        tlatex->SetTextAlign(11);
        tlatex->SetTextSize(25);
        tlatex->DrawLatex(0.16, 0.95, "CMS");
        tlatex->SetTextFont(53);
        tlatex->DrawLatex(0.23, 0.95, "Preliminary");
        tlatex->SetTextFont(43);
        tlatex->SetTextSize(23);

	TString lumiString = Form("%.2f pb^{-1} (%d TeV)", lumi, energy);

	if (lumi > 1000.0)
	{
		lumiString = Form("%.2f fb^{-1} (%d TeV)", lumi/1000.0, energy);
	}
        
	std::string Lumi ((const char*) lumiString);
	tlatex->SetTextAlign(31);
        tlatex->DrawLatex(0.9, 0.95, Lumi.c_str());
        tlatex->SetTextAlign(11);
};
