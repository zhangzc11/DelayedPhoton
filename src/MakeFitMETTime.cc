//C++ INCLUDES
#include <vector>
#include <fstream>
//ROOT INCLUDES
//#include <TSYSTEM.h>
#include <TSystem.h>
#include <TTree.h>
#include <TLatex.h>
#include <TString.h>
#include <TFile.h>
#include <TH1D.h>
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
//ROOFIT INCLUDES
#include <RooWorkspace.h>
#include <RooDataSet.h>
#include <RooRealVar.h>
#include <RooExponential.h>
#include <RooAddPdf.h>
#include <RooGaussian.h>
#include <RooMinimizer.h>
#include <RooFitResult.h>
#include <RooPlot.h>
#include <RooExtendPdf.h>
#include <RooStats/SPlot.h>
#include <RooStats/ModelConfig.h>
#include <RooGenericPdf.h>
#include <RooFormulaVar.h>
#include <RooBernstein.h>
#include <RooMinuit.h>
#include <RooNLLVar.h>
#include <RooRandom.h>
#include <RooDataHist.h>
#include <RooHistPdf.h>
//#include <RealVar.h>
//LOCAL INCLUDES
#include "MakeFitMETTime.hh"
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
const float leftMargin   = 0.12;
const float rightMargin  = 0.05;
const float topMargin    = 0.07;
const float bottomMargin = 0.12;

using namespace std;

RooWorkspace* FitDataBkgFraction( TTree * tree, TString varName, TString varTitle, TString varUnit, float varLow, float varHigh, TH1F * h1_GJets, TH1F * h1_QCD)
{
	RooWorkspace* ws = new RooWorkspace( "ws", "" );

	// define variables
	RooRealVar fitVar ( varName, varTitle, varLow, varHigh, varUnit);	
	//RooRealVar nGJets ("nGJets", "nGJets", 5835.0, 0.5*5835.0, 1.5*5835.0);
	//RooRealVar nGJets ("nGJets", "nGJets", 5800.0, 0.0, tree->GetEntries());	
	RooRealVar nGJets ("nGJets", "nGJets", 0.5, 0.0, 1.5);	
	//RooRealVar nQCD ("nQCD", "nQCD", 3500.0, 0.5*3500, 1.5*3500.0);
	//RooRealVar nQCD ("nQCD", "nQCD", 3500.0, 0.0, tree->GetEntries());	
	RooRealVar nQCD ("nQCD", "nQCD", 0.5, 0.0, 1.5);	

	// import dataset
	RooDataSet data( "data", "", RooArgSet(fitVar), RooFit::Import(*tree));

	// Import Background shapes
	RooDataHist * rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(fitVar), h1_GJets);
	RooDataHist * rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(fitVar), h1_QCD);
	
	// Define PDFs from Background shapes
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(fitVar), *rhGJets, 2);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(fitVar), *rhQCD, 2);

	// Add all PDFs to form fit model
	RooAbsPdf * fitModel = new RooAddPdf("fitModel", "fitModel", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));

	// do fit and save to workspace
	RooFitResult * fres = fitModel->fitTo( data, RooFit::Strategy(2), RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
	
	nGJets.Print();
	nQCD.Print();

	RooPlot * frame = fitVar.frame(varLow, varHigh, 100);
	data.plotOn( frame );
	fitModel->plotOn( frame, RooFit::Components("rpGJets"), RooFit::LineColor(kViolet + 10) );
	fitModel->plotOn( frame, RooFit::Components("rpQCD"), RooFit::LineColor(kOrange + 9) );
	fitModel->plotOn( frame, RooFit::Components("fitModel"), RooFit::LineColor(kGreen) );

	frame->SetName(varName+"_frame");
	
	ws->import(data);
	ws->import(*fitModel);
	ws->import(*frame);
	ws->import(*fres);

	return ws;
};


TFractionFitter* FitDataBkgFractionFilter(TH1F * h1_data, TH1F * h1_GJets, TH1F * h1_QCD)
{
	TObjArray *temp = new TObjArray(2);
	temp->Add(h1_GJets);
	temp->Add(h1_QCD);

	TFractionFitter* fit = new TFractionFitter(h1_data, temp);
	fit->Constrain(0,0.0,1.0);
	fit->Constrain(1,0.0,1.0);
	Int_t status = fit->Fit();
	cout << "fit status: " << status << endl;
	Double_t par0, par0err, par1, par1err;
	fit->GetResult(0, par0, par0err);
	fit->GetResult(1, par1, par1err);
	cout << "fraction GJets: " << par0 << " +/- " << par0err <<endl;
	cout << "fraction QCD: " << par1 << " +/- " << par1err <<endl;
	
	return fit;
};

