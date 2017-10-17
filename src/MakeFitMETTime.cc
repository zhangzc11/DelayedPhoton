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


RooWorkspace* Fit2DMETTimeDataBkg( TTree * treeData, TTree * treeGJets, TTree * treeQCD,  float fracGJets, float fracGJetsErr, float fracQCD, float fracQCDErr)
{
	RooWorkspace* ws = new RooWorkspace( "ws", "" );
	// define variables
	RooRealVar pho1ClusterTime("pho1ClusterTime","#gamma cluster time ",-15.0,15.0,"ns");
	RooRealVar MET("MET","#slash{E}_{T} ",0,1000,"GeV");

	RooRealVar nGJets ("nGJets", "nGJets", fracGJets, fracGJets-3.0*fracGJetsErr, fracGJets+3.0*fracGJetsErr);
	RooRealVar nQCD ("nQCD", "nQCD", fracQCD, fracQCD-3.0*fracQCDErr, fracQCD+3.0*fracQCDErr);
	//RooRealVar nGJets ("nGJets", "nGJets", 0.5,0.0,1.0);
	//RooRealVar nQCD ("nQCD", "nQCD", 0.5,0.0,1.0);

	RooRealVar weightGJets("weightGJets", "weightGJets", (treeData->GetEntries()*1.0)/(treeGJets->GetEntries()*1.0));
	RooRealVar weightQCD("weightQCD", "weightQCD", (treeData->GetEntries()*1.0)/(treeQCD->GetEntries()*1.0));

	//data sets
	RooDataSet data( "data", "data", RooArgSet(pho1ClusterTime, MET), RooFit::Import(*treeData));
	RooDataSet dataGJets( "dataGJets", "dataGJets", RooArgSet(pho1ClusterTime, MET), RooFit::Import(*treeGJets), RooFit::WeightVar("weightGJets"));
	//RooDataSet dataGJets( "dataGJets", "dataGJets", RooArgSet(pho1ClusterTime, MET), RooFit::Import(*treeGJets));
	RooDataSet dataQCD( "dataQCD", "dataQCD", RooArgSet(pho1ClusterTime, MET), RooFit::Import(*treeQCD), RooFit::WeightVar("weightQCD"));
	//RooDataSet dataQCD( "dataQCD", "dataQCD", RooArgSet(pho1ClusterTime, MET), RooFit::Import(*treeQCD));

	//dataGJets.setWeightVar(weightGJets);
	//dataQCD.setWeightVar(weightQCD);

	//RooDataSet -> RooDataHist
	RooDataHist* rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(pho1ClusterTime, MET), dataGJets);	
	RooDataHist* rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(pho1ClusterTime, MET), dataQCD);	
	//RooDataHist -> RooHistPdf
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(pho1ClusterTime, MET), *rhGJets);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(pho1ClusterTime, MET), *rhQCD);
	//RooHistPdf -> RooAbsPdf
	RooAbsPdf * fitModel = new RooAddPdf("fitModel", "fitModel", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));	

	//fit
	RooAbsReal* nll = fitModel->createNLL(data, RooFit::NumCPU(8)) ;
	RooMinimizer m(*nll);

	m.migrad() ;	
	
	//RooFitResult * fres = fitModel->fitTo( data, RooFit::Strategy(2), RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
	//RooFitResult * fres = fitModel->fitTo( data, RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
	RooFitResult * fres1 = m.save();

	int _status = -1;
	_status    = fres1->status();
	
	if(_status!=0)
        {
      		m.minimize("Minuit2", "Hesse");
        }
	RooFitResult * fres = m.save();
	_status    = fres->status();

        nGJets.Print();
        nQCD.Print();

        RooPlot * frame_pho1ClusterTime = pho1ClusterTime.frame(-15.0, 15.0, 100);
        data.plotOn( frame_pho1ClusterTime );
        fitModel->plotOn( frame_pho1ClusterTime, RooFit::Components("rpGJets"), RooFit::LineColor(kViolet + 10) );
        fitModel->plotOn( frame_pho1ClusterTime, RooFit::Components("rpQCD"), RooFit::LineColor(kOrange + 9) );
        fitModel->plotOn( frame_pho1ClusterTime, RooFit::Components("fitModel"), RooFit::LineColor(kGreen) );
        frame_pho1ClusterTime->SetName("pho1ClusterTime_frame");
	
        RooPlot * frame_pho1ClusterTime_LL = pho1ClusterTime.frame(-15.0, 15.0, 100);
	nll->plotOn(frame_pho1ClusterTime_LL, RooFit::ShiftToZero()) ;
	frame_pho1ClusterTime_LL->SetName("pho1ClusterTime_frame_Likelihood");
       
	RooPlot * frame_MET = MET.frame(0, 1000.0, 100);
        data.plotOn( frame_MET );
        fitModel->plotOn( frame_MET, RooFit::Components("rpGJets"), RooFit::LineColor(kViolet + 10) );
        fitModel->plotOn( frame_MET, RooFit::Components("rpQCD"), RooFit::LineColor(kOrange + 9) );
        fitModel->plotOn( frame_MET, RooFit::Components("fitModel"), RooFit::LineColor(kGreen) );
        frame_MET->SetName("MET_frame");
        
	RooPlot * frame_MET_LL = MET.frame(0, 1000.0, 100);
	nll->plotOn(frame_MET_LL, RooFit::ShiftToZero()) ;
        frame_MET_LL->SetName("MET_frame_Likelihood");
	

	ws->import(data);
        ws->import(dataGJets);
        ws->import(dataQCD);
        ws->import(*fitModel);
        ws->import(*frame_pho1ClusterTime);
        ws->import(*frame_pho1ClusterTime_LL);
        ws->import(*frame_MET);
        ws->import(*frame_MET_LL);
        ws->import(*fres);

        return ws;
	
};

RooWorkspace* Fit2DMETTimeDataBkg( TH2F * h2Data, TH2F * h2GJets, TH2F * h2QCD,  float fracGJets, float fracGJetsErr, float fracQCD, float fracQCDErr)
{
	
	RooWorkspace* ws = new RooWorkspace( "ws", "" );
	// define variables
	RooRealVar pho1ClusterTime("pho1ClusterTime","#gamma cluster time ",-15.0,15.0,"ns");
	RooRealVar MET("MET","#slash{E}_{T} ",0,1000,"GeV");

	RooRealVar nGJets ("nGJets", "nGJets", fracGJets, fracGJets-3.0*fracGJetsErr, fracGJets+3.0*fracGJetsErr);
	RooRealVar nQCD ("nQCD", "nQCD", fracQCD, fracQCD-3.0*fracQCDErr, fracQCD+3.0*fracQCDErr);
	//RooRealVar nGJets ("nGJets", "nGJets", 0.5,0.0,1.0);
	//RooRealVar nQCD ("nQCD", "nQCD", 0.5,0.0,1.0);

	//RooDataHist
	RooDataHist* data = new RooDataHist("data", "data", RooArgSet(pho1ClusterTime, MET), h2Data);	
	RooDataHist* rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(pho1ClusterTime, MET), h2GJets);	
	RooDataHist* rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(pho1ClusterTime, MET), h2QCD);	
	//RooDataHist -> RooHistPdf
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(pho1ClusterTime, MET), *rhGJets, 0);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(pho1ClusterTime, MET), *rhQCD, 0);
	//RooHistPdf -> RooAbsPdf
	RooAbsPdf * fitModel = new RooAddPdf("fitModel", "fitModel", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));	

	//fit
	RooAbsReal* nll = fitModel->createNLL(*data, RooFit::NumCPU(8)) ;
	RooMinimizer m(*nll);

	m.migrad() ;	
	
	//RooFitResult * fres = fitModel->fitTo( data, RooFit::Strategy(2), RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
	//RooFitResult * fres = fitModel->fitTo( data, RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
	RooFitResult * fres1 = m.save();

	int _status = -1;
	_status    = fres1->status();
	
	if(_status!=0)
        {
      		m.minimize("Minuit2", "Hesse");
        }
	RooFitResult * fres = m.save();
	_status    = fres->status();

        nGJets.Print();
        nQCD.Print();

        RooPlot * frame_pho1ClusterTime = pho1ClusterTime.frame(-15.0, 15.0, 100);
        data->plotOn( frame_pho1ClusterTime );
        fitModel->plotOn( frame_pho1ClusterTime, RooFit::Components("rpGJets"), RooFit::LineColor(kViolet + 10) );
        fitModel->plotOn( frame_pho1ClusterTime, RooFit::Components("rpQCD"), RooFit::LineColor(kOrange + 9) );
        fitModel->plotOn( frame_pho1ClusterTime, RooFit::Components("fitModel"), RooFit::LineColor(kGreen) );
        frame_pho1ClusterTime->SetName("pho1ClusterTime_frame");
	
        RooPlot * frame_pho1ClusterTime_LL = pho1ClusterTime.frame(-15.0, 15.0, 100);
	nll->plotOn(frame_pho1ClusterTime_LL, RooFit::ShiftToZero()) ;
	frame_pho1ClusterTime_LL->SetName("pho1ClusterTime_frame_Likelihood");
       
	RooPlot * frame_MET = MET.frame(0, 1000.0, 100);
        data->plotOn( frame_MET );
        fitModel->plotOn( frame_MET, RooFit::Components("rpGJets"), RooFit::LineColor(kViolet + 10) );
        fitModel->plotOn( frame_MET, RooFit::Components("rpQCD"), RooFit::LineColor(kOrange + 9) );
        fitModel->plotOn( frame_MET, RooFit::Components("fitModel"), RooFit::LineColor(kGreen) );
        frame_MET->SetName("MET_frame");
        
	RooPlot * frame_MET_LL = MET.frame(0, 1000.0, 100);
	nll->plotOn(frame_MET_LL, RooFit::ShiftToZero()) ;
        frame_MET_LL->SetName("MET_frame_Likelihood");
	
	ws->import(*data);
        ws->import(*rhGJets);
        ws->import(*rhQCD);
        ws->import(*fitModel);
        ws->import(*frame_pho1ClusterTime);
        ws->import(*frame_pho1ClusterTime_LL);
        ws->import(*frame_MET);
        ws->import(*frame_MET_LL);
        ws->import(*fres);
        return ws;
	
};
