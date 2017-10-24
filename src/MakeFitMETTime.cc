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
#include <RooParamHistFunc.h>
#include <RooRealSumPdf.h>
#include <RooHistFunc.h>
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
const float leftMargin   = 0.13;
const float rightMargin  = 0.05;
const float topMargin    = 0.07;
const float bottomMargin = 0.12;

using namespace std;

RooWorkspace* FitDataBkgFraction( TH1F * h1_Data, TString varName, TString varTitle, TString varUnit, float varLow, float varHigh, TH1F * h1_GJets, TH1F * h1_QCD)
{
	RooWorkspace* ws = new RooWorkspace( "ws", "" );

	// define variables
	RooRealVar fitVar ( varName, varTitle, varLow, varHigh, varUnit);	
	//RooRealVar nGJets ("nGJets", "nGJets", 5835.0, 0.5*5835.0, 1.5*5835.0);
	//RooRealVar nGJets ("nGJets", "nGJets", 5800.0, 0.0, tree->GetEntries());	
	RooRealVar nGJets ("nGJets", "nGJets", 0.5, 0.0001, 10000.0);	
	//RooRealVar nQCD ("nQCD", "nQCD", 3500.0, 0.5*3500, 1.5*3500.0);
	//RooRealVar nQCD ("nQCD", "nQCD", 3500.0, 0.0, tree->GetEntries());	
	RooRealVar nQCD ("nQCD", "nQCD", 0.5, 0.0001, 10000.0);	


	// Import data
	RooDataHist * data = new RooDataHist("data", "data", RooArgSet(fitVar), h1_Data);
	// Import Background shapes
	RooDataHist * rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(fitVar), h1_GJets);
	RooDataHist * rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(fitVar), h1_QCD);

	//to avoid zero likelihood, fill empty template bins with tiny values
	for(int i=0;i<data->numEntries() ; i++)
	{
		data->get(i);
		rhGJets->get(i);
		rhQCD->get(i);
		float weight_data = data->weight();
		float weight_rhGJets = rhGJets->weight();
		float weight_rhQCD = rhQCD->weight();
		if((weight_rhGJets + weight_rhQCD < 1e-5) && (weight_data > 0))
		{
			rhGJets->set(1e-5);
			rhQCD->set(1e-5);
		}
	}
	
	// Define PDFs from Background shapes
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(fitVar), *rhGJets);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(fitVar), *rhQCD);

	// Add all PDFs to form fit model
	RooAbsPdf * fitModel = new RooAddPdf("fitModel", "fitModel", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));

	// do fit and save to workspace
	RooFitResult * fres = fitModel->fitTo( *data, RooFit::Strategy(2), RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
	
	nGJets.Print();
	nQCD.Print();

	RooPlot * frame = fitVar.frame(varLow, varHigh, 100);
	data->plotOn( frame, RooFit::Name("plot_data"));
	fitModel->plotOn( frame, RooFit::Components("rpGJets"), RooFit::LineColor(kViolet + 10), RooFit::Name("plot_GJets") );
	fitModel->plotOn( frame, RooFit::Components("rpQCD"), RooFit::LineColor(kOrange + 9), RooFit::Name("plot_QCD") );
	fitModel->plotOn( frame, RooFit::Components("fitModel"), RooFit::LineColor(kGreen) , RooFit::Name("plot_all"));

	frame->SetName(varName+"_frame");


	//save the plot	
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

	frame->SetMaximum(150.0*frame->GetMaximum());
	frame->SetMinimum(0.1);
	frame->Draw();
	TLegend * leg = new TLegend(0.18, 0.7, 0.93, 0.89);
	leg->SetNColumns(2);
        leg->SetBorderSize(0);
        leg->SetTextSize(0.03);
        leg->SetLineColor(1);
        leg->SetLineStyle(1);
        leg->SetLineWidth(1);
        leg->SetFillColor(0);
        leg->SetFillStyle(1001);
	leg->AddEntry("plot_data","data","lep");
	leg->AddEntry("plot_GJets","#gamma + jets","l");
	leg->AddEntry("plot_QCD","QCD","l");
	leg->AddEntry("plot_all","combined fit","l");
	leg->Draw();

     	myC->SetTitle("");
        myC->SaveAs("fit_results/plots/bkg_yield_fit_"+varName+".pdf");
        myC->SaveAs("fit_results/plots/bkg_yield_fit_"+varName+".png");
        myC->SaveAs("fit_results/plots/bkg_yield_fit_"+varName+".C");

	
	ws->import(*data);
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
	RooDataSet dataQCD( "dataQCD", "dataQCD", RooArgSet(pho1ClusterTime, MET), RooFit::Import(*treeQCD), RooFit::WeightVar("weightQCD"));


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
	//RooRealVar nGJets ("nGJets", "nGJets", 0.5,0.001,10000.0);
	//RooRealVar nQCD ("nQCD", "nQCD", 0.5,0.001,10000.0);

	//RooDataHist
	RooDataHist* data = new RooDataHist("data", "data", RooArgSet(pho1ClusterTime, MET), h2Data);	
	RooDataHist* rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(pho1ClusterTime, MET), h2GJets);	
	RooDataHist* rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(pho1ClusterTime, MET), h2QCD);	

	//to avoid zero likelihood, fill empty template bins with tiny values
	for(int i=0;i<data->numEntries() ; i++)
	{
		data->get(i);
		rhGJets->get(i);
		rhQCD->get(i);
		float weight_data = data->weight();
		float weight_rhGJets = rhGJets->weight();
		float weight_rhQCD = rhQCD->weight();
		if((weight_rhGJets + weight_rhQCD < 1e-5) && (weight_data > 0))
		{
			rhGJets->set(1e-5);
			rhQCD->set(1e-5);
		}
	}
	
	//RooDataHist -> RooHistPdf
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(pho1ClusterTime, MET), *rhGJets, 0);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(pho1ClusterTime, MET), *rhQCD, 0);
	//RooHistPdf -> RooAbsPdf
	RooAbsPdf * fitModel = new RooAddPdf("fitModel", "fitModel", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));	

	//fit
	RooAbsReal* nll = fitModel->createNLL(*data, RooFit::NumCPU(8)) ;
	//RooFitResult * fres = fitModel->fitTo( *data, RooFit::Strategy(2), RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
	RooFitResult * fres = fitModel->fitTo( *data, RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
        
	nGJets.Print();
        nQCD.Print();

	//draw some fit_results/plots
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

        RooPlot * frame_pho1ClusterTime = pho1ClusterTime.frame(-15.0, 15.0, 100);
        data->plotOn( frame_pho1ClusterTime, RooFit::Name("pho1ClusterTime_data") );
        fitModel->plotOn( frame_pho1ClusterTime, RooFit::Name("pho1ClusterTime_GJets"), RooFit::Components("rpGJets"), RooFit::LineColor(kAzure + 7) );
        fitModel->plotOn( frame_pho1ClusterTime, RooFit::Name("pho1ClusterTime_QCD"), RooFit::Components("rpQCD"), RooFit::LineColor(kOrange - 9) );
        fitModel->plotOn( frame_pho1ClusterTime, RooFit::Name("pho1ClusterTime_all"), RooFit::Components("fitModel"), RooFit::LineColor(kRed) );
        frame_pho1ClusterTime->SetName("pho1ClusterTime_frame");

	frame_pho1ClusterTime->SetMaximum(150.0*frame_pho1ClusterTime->GetMaximum());
	frame_pho1ClusterTime->SetMinimum(0.1);
	frame_pho1ClusterTime->Draw();

	TLegend * leg_pho1ClusterTime = new TLegend(0.18, 0.7, 0.93, 0.89);
	leg_pho1ClusterTime->SetNColumns(3);
        leg_pho1ClusterTime->SetBorderSize(0);
        leg_pho1ClusterTime->SetTextSize(0.03);
        leg_pho1ClusterTime->SetLineColor(1);
        leg_pho1ClusterTime->SetLineStyle(1);
        leg_pho1ClusterTime->SetLineWidth(1);
        leg_pho1ClusterTime->SetFillColor(0);
        leg_pho1ClusterTime->SetFillStyle(1001);
	leg_pho1ClusterTime->AddEntry("pho1ClusterTime_data","data","lep");
	leg_pho1ClusterTime->AddEntry("pho1ClusterTime_GJets","#gamma + jets","l");
	leg_pho1ClusterTime->AddEntry("pho1ClusterTime_QCD","QCD","l");
	leg_pho1ClusterTime->AddEntry("pho1ClusterTime_all","combined fit","l");
	leg_pho1ClusterTime->Draw();

	myC->SetTitle("");
	myC->SaveAs("fit_results/plots/fit_bkgonly_pho1ClusterTime.pdf");
	myC->SaveAs("fit_results/plots/fit_bkgonly_pho1ClusterTime.png");
	myC->SaveAs("fit_results/plots/fit_bkgonly_pho1ClusterTime.C");
	
	RooPlot * frame_MET = MET.frame(0, 1000.0, 100);
        data->plotOn( frame_MET, RooFit::Name("MET_data") );
        fitModel->plotOn( frame_MET, RooFit::Name("MET_GJets"), RooFit::Components("rpGJets"), RooFit::LineColor(kAzure + 7) );
        fitModel->plotOn( frame_MET, RooFit::Name("MET_QCD"), RooFit::Components("rpQCD"), RooFit::LineColor(kOrange - 9) );
        fitModel->plotOn( frame_MET, RooFit::Name("MET_all"), RooFit::Components("fitModel"), RooFit::LineColor(kRed) );
        frame_MET->SetName("MET_frame");
	
	frame_MET->SetMaximum(150.0*frame_MET->GetMaximum());
	frame_MET->SetMinimum(0.1);

	frame_MET->Draw();

	TLegend * leg_MET = new TLegend(0.18, 0.7, 0.93, 0.89);
	leg_MET->SetNColumns(3);
        leg_MET->SetBorderSize(0);
        leg_MET->SetTextSize(0.03);
        leg_MET->SetLineColor(1);
        leg_MET->SetLineStyle(1);
        leg_MET->SetLineWidth(1);
        leg_MET->SetFillColor(0);
        leg_MET->SetFillStyle(1001);
	leg_MET->AddEntry("MET_data","data","lep");
	leg_MET->AddEntry("MET_GJets","#gamma + jets","l");
	leg_MET->AddEntry("MET_QCD","QCD","l");
	leg_MET->AddEntry("MET_all","combined fit","l");
	leg_MET->Draw();

     	myC->SetTitle("");
        myC->SaveAs("fit_results/plots/fit_bkgonly_MET.pdf");
        myC->SaveAs("fit_results/plots/fit_bkgonly_MET.png");
        myC->SaveAs("fit_results/plots/fit_bkgonly_MET.C");
	
        RooPlot * frame_nGJets_LL = nGJets.frame(fracGJets-3.0*fracGJetsErr, fracGJets+3.0*fracGJetsErr, 100);
	RooAbsReal* pll_nGJets = nll->createProfile(nGJets) ;
	nll->plotOn(frame_nGJets_LL, RooFit::ShiftToZero()) ;
	pll_nGJets->plotOn(frame_nGJets_LL, RooFit::LineColor(kRed)) ;
	frame_nGJets_LL->SetName("nGJets_frame_Likelihood");
 
        RooPlot * frame_nQCD_LL = nQCD.frame(fracQCD-3.0*fracQCDErr, fracQCD+3.0*fracQCDErr, 100);
	RooAbsReal* pll_nQCD = nll->createProfile(nQCD) ;
	nll->plotOn(frame_nQCD_LL, RooFit::ShiftToZero()) ;
	pll_nQCD->plotOn(frame_nQCD_LL, RooFit::LineColor(kRed)) ;
	frame_nQCD_LL->SetName("nQCD_frame_Likelihood");


	
	myC->SetLogy(0);
	myC->SetLogz(1);
	myC->SetTheta(69.64934);
   	myC->SetPhi(-51.375);

	TH2F * ph2 = new TH2F("fit2D","; #gamma cluster time (ns); #slash{E}_{T} (GeV); PDF",50,-5,5,50,0,500);
	fitModel->fillHistogram(ph2, RooArgList(pho1ClusterTime, MET));
	ph2->GetXaxis()->SetTitleOffset(2.0);
	ph2->GetXaxis()->CenterTitle(kTRUE);
	ph2->GetYaxis()->SetTitleOffset(2.0);
	ph2->GetYaxis()->CenterTitle(kTRUE);
	ph2->GetZaxis()->SetTitleOffset(1.8);
	ph2->GetZaxis()->SetRangeUser(1e-8, 0.1);
	ph2->Draw("SURF1");
	myC->SaveAs("fit_results/plots/fit_bkgonly_2D_pdf.pdf");
	myC->SaveAs("fit_results/plots/fit_bkgonly_2D_pdf.png");
	myC->SaveAs("fit_results/plots/fit_bkgonly_2D_pdf.C");
	
	ws->import(*data);
        ws->import(*rhGJets);
        ws->import(*rhQCD);
        ws->import(*fitModel);
        ws->import(*frame_pho1ClusterTime);
        ws->import(*frame_MET);
       // ws->import(*frame_2D);
        ws->import(*frame_nGJets_LL);
        ws->import(*frame_nQCD_LL);
        ws->import(*fres);
        return ws;
	
};

RooWorkspace* Fit2DMETTimeDataBkgSig( TH2F * h2Data, TH2F * h2GJets, TH2F * h2QCD,  TH2F * h2Sig, float fracGJets, float fracQCD, TString modelName, TString modelTitle, bool useToy)
{
	RooWorkspace* ws = new RooWorkspace( "ws", "" );
	// define variables
	RooRealVar pho1ClusterTime("pho1ClusterTime","#gamma cluster time ",-15.0,15.0,"ns");
	RooRealVar MET("MET","#slash{E}_{T} ",0,1000,"GeV");

	double npoints = 1.0*h2Data->Integral();

	RooRealVar nGJets ("nGJets", "nGJets", fracGJets);
	nGJets.setConstant(kTRUE);
	RooRealVar nQCD ("nQCD", "nQCD", fracQCD);
	nQCD.setConstant(kTRUE);

	
	//RooDataHist
	RooDataHist* data = new RooDataHist("data", "data", RooArgSet(pho1ClusterTime, MET), h2Data);	
	RooDataHist* rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(pho1ClusterTime, MET), h2GJets);	
	RooDataHist* rhGJets_temp = new RooDataHist("rhGJets_temp", "rhGJets_temp", RooArgSet(pho1ClusterTime, MET), h2GJets);	
	RooDataHist* rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(pho1ClusterTime, MET), h2QCD);	
	RooDataHist* rhQCD_temp = new RooDataHist("rhQCD_temp", "rhQCD_temp", RooArgSet(pho1ClusterTime, MET), h2QCD);	
	RooDataHist* rhSig = new RooDataHist("rhSig", "rhSig", RooArgSet(pho1ClusterTime, MET), h2Sig);	
	//fill iempty background Histgrams bins with tiny value to allow fluctuation in generated toy data
	for(int i=0;i<data->numEntries() ; i++)
	{
		rhGJets_temp->get(i);
		rhQCD_temp->get(i);
		float weight_rhGJets = rhGJets_temp->weight();
		float weight_rhQCD = rhQCD_temp->weight();
		if(weight_rhGJets< 1e-5) rhGJets_temp->set(1e-3);
		if(weight_rhQCD< 1e-5) rhQCD_temp->set(1e-3);
	}


	//RooDataHist -> RooHistPdf
	RooHistPdf * rpGJets_temp = new RooHistPdf("rpGJets_temp", "rpGJets_temp", RooArgSet(pho1ClusterTime, MET), *rhGJets_temp, 0);
	RooHistPdf * rpQCD_temp = new RooHistPdf("rpQCD_temp", "rpQCD_temp", RooArgSet(pho1ClusterTime, MET), *rhQCD_temp, 0);
	//RooHistPdf -> RooAbsPdf
	RooAbsPdf * fitModelBkg_temp = new RooAddPdf("fitModelBkg_temp", "fitModelBkg_temp", RooArgSet(*rpGJets_temp, *rpQCD_temp), RooArgSet(nGJets, nQCD));	

	//create toy data
	//TRandom3* r3 = new TRandom3(0);
	//double npoints = r3->PoissonD(h2Data->Integral());	
	//RooDataHist* data_toy = fitModelBkg->generateBinned(RooArgSet(pho1ClusterTime, MET), npoints, RooFit::ExpectedData());
	RooDataHist* data_toy = fitModelBkg_temp->generateBinned(RooArgSet(pho1ClusterTime, MET), npoints);
	data_toy->SetName("data_toy");
	
	//to avoid zero likelihood, fill empty template bins with tiny values
	for(int i=0;i<data->numEntries() ; i++)
	{
		data->get(i);
		data_toy->get(i);
		rhGJets->get(i);
		rhQCD->get(i);
		rhSig->get(i);
		float weight_data = data->weight();
		float weight_data_toy = data_toy->weight();
		float weight_rhGJets = rhGJets->weight();
		float weight_rhQCD = rhQCD->weight();
		float weight_rhSig = rhSig->weight();
		if((weight_rhSig < 1e-5) && ((useToy ? weight_data_toy : weight_data) > 0))
		{
			rhSig->set(1e-3);
		}
		if((weight_rhGJets + weight_rhQCD < 1e-5) && ((useToy ? weight_data_toy : weight_data) > 0))
		{
			rhGJets->set(1e-3);
			rhQCD->set(1e-3);
		}
	
	}
	
	//new pdf after fill empty bins
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(pho1ClusterTime, MET), *rhGJets, 0);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(pho1ClusterTime, MET), *rhQCD, 0);
	RooHistPdf * rpSig = new RooHistPdf("rpSig", "rpSig", RooArgSet(pho1ClusterTime, MET), *rhSig, 0);
	
	
	RooAbsPdf * fitModelBkg = new RooAddPdf("fitModelBkg", "fitModelBkg", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));	
	
	
	RooRealVar nSig ("rpSig_yield", "rpSig_yield", 0.0, 0.0, 0.1*npoints);
	nSig.setConstant(kFALSE);
	RooRealVar nBkg ("fitModelBkg_yield", "fitModelBkg_yield", npoints, 0.0, 1.5*npoints);
	nBkg.setConstant(kFALSE);

	RooAbsPdf * fitModelBkgSig = new RooAddPdf("fitModelBkgSig", "fitModelBkgSig", RooArgSet(*fitModelBkg, *rpSig), RooArgSet(nBkg, nSig));	
	//RooAbsPdf * fitModelBkg = new RooAddPdf("fitModelBkg", "fitModelBkg", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));	
	//fit
	RooAbsReal* nll = fitModelBkgSig->createNLL(*data, RooFit::NumCPU(8)) ;
	RooFitResult * fres;
	if(useToy) fres = fitModelBkgSig->fitTo( *data_toy, RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
	else fres = fitModelBkgSig->fitTo( *data, RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
        
	nGJets.Print();
	nQCD.Print();
	nBkg.Print();
        nSig.Print();

	//draw some plot-s
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

        RooPlot * frame_pho1ClusterTime = pho1ClusterTime.frame(-15.0, 15.0, 100);
        if(useToy) data_toy->plotOn( frame_pho1ClusterTime, RooFit::Name("pho1ClusterTime_data") );
        else data->plotOn( frame_pho1ClusterTime, RooFit::Name("pho1ClusterTime_data") );
        fitModelBkgSig->plotOn( frame_pho1ClusterTime, RooFit::Name("pho1ClusterTime_Bkg"), RooFit::Components("fitModelBkg"), RooFit::LineColor(kBlue) );
        fitModelBkgSig->plotOn( frame_pho1ClusterTime, RooFit::Name("pho1ClusterTime_Sig"), RooFit::Components("rpSig"), RooFit::LineColor(kGreen) );
        fitModelBkgSig->plotOn( frame_pho1ClusterTime, RooFit::Name("pho1ClusterTime_all"), RooFit::Components("fitModelBkgSig"), RooFit::LineColor(kRed) );
        frame_pho1ClusterTime->SetName("pho1ClusterTime_frame");

	frame_pho1ClusterTime->SetMaximum(1000.0*frame_pho1ClusterTime->GetMaximum());
	frame_pho1ClusterTime->SetMinimum(1e-3);
	frame_pho1ClusterTime->Draw();

	TLegend * leg_pho1ClusterTime = new TLegend(0.18, 0.7, 0.93, 0.89);
	leg_pho1ClusterTime->SetNColumns(2);
        leg_pho1ClusterTime->SetBorderSize(0);
        leg_pho1ClusterTime->SetTextSize(0.03);
        leg_pho1ClusterTime->SetLineColor(1);
        leg_pho1ClusterTime->SetLineStyle(1);
        leg_pho1ClusterTime->SetLineWidth(1);
        leg_pho1ClusterTime->SetFillColor(0);
        leg_pho1ClusterTime->SetFillStyle(1001);
	leg_pho1ClusterTime->AddEntry("pho1ClusterTime_data","data","lep");
	leg_pho1ClusterTime->AddEntry("pho1ClusterTime_Bkg","#gamma + jets/QCD bkg","l");
	leg_pho1ClusterTime->AddEntry("pho1ClusterTime_Sig",modelTitle,"l");
	leg_pho1ClusterTime->AddEntry("pho1ClusterTime_all","combined fit","l");
	leg_pho1ClusterTime->Draw();

	myC->SetTitle("");
	myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_pho1ClusterTime.pdf");
	myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_pho1ClusterTime.png");
	myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_pho1ClusterTime.C");
	
	RooPlot * frame_MET = MET.frame(0, 1000.0, 100);
        if(useToy) data_toy->plotOn( frame_MET, RooFit::Name("MET_data") );
        else data->plotOn( frame_MET, RooFit::Name("MET_data") );
        fitModelBkgSig->plotOn( frame_MET, RooFit::Name("MET_Bkg"), RooFit::Components("fitModelBkg"), RooFit::LineColor(kBlue) );
        fitModelBkgSig->plotOn( frame_MET, RooFit::Name("MET_Sig"), RooFit::Components("rpSig"), RooFit::LineColor(kGreen) );
        fitModelBkgSig->plotOn( frame_MET, RooFit::Name("MET_all"), RooFit::Components("fitModelBkgSig"), RooFit::LineColor(kRed) );
        frame_MET->SetName("MET_frame");
	
	frame_MET->SetMaximum(1000.0*frame_MET->GetMaximum());
	frame_MET->SetMinimum(1e-3);

	frame_MET->Draw();

	TLegend * leg_MET = new TLegend(0.18, 0.7, 0.93, 0.89);
	leg_MET->SetNColumns(2);
        leg_MET->SetBorderSize(0);
        leg_MET->SetTextSize(0.03);
        leg_MET->SetLineColor(1);
        leg_MET->SetLineStyle(1);
        leg_MET->SetLineWidth(1);
        leg_MET->SetFillColor(0);
        leg_MET->SetFillStyle(1001);
	leg_MET->AddEntry("MET_data","data","lep");
	leg_MET->AddEntry("MET_Bkg","#gamma + jets/QCD bkg","l");
	leg_MET->AddEntry("MET_Sig",modelTitle,"l");
	leg_MET->AddEntry("MET_all","combined fit","l");
	leg_MET->Draw();

     	myC->SetTitle("");
        myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_MET.pdf");
        myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_MET.png");
        myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_MET.C");
	

        RooPlot * frame_nBkg_LL = nBkg.frame(0.0, 1.5*npoints, 100);
	RooAbsReal* pll_nBkg = nll->createProfile(nBkg) ;
	nll->plotOn(frame_nBkg_LL, RooFit::ShiftToZero()) ;
	pll_nBkg->plotOn(frame_nBkg_LL, RooFit::LineColor(kRed)) ;
	frame_nBkg_LL->SetName("nBkg_frame_Likelihood");

        RooPlot * frame_nSig_LL = nSig.frame(0.0, 0.1*npoints, 100);
	RooAbsReal* pll_nSig = nll->createProfile(nSig) ;
	nll->plotOn(frame_nSig_LL, RooFit::ShiftToZero()) ;
	pll_nSig->plotOn(frame_nSig_LL, RooFit::LineColor(kRed)) ;
	frame_nSig_LL->SetName("nSig_frame_Likelihood");

	
	myC->SetLogy(0);
	myC->SetLogz(1);
	myC->SetTheta(69.64934);
   	myC->SetPhi(-51.375);


	TH2F * ph2 = new TH2F("fit2D","; #gamma cluster time (ns); #slash{E}_{T} (GeV); PDF",100,-15,15,100,0,1000);
	fitModelBkgSig->fillHistogram(ph2, RooArgList(pho1ClusterTime, MET));
	ph2->GetXaxis()->SetTitleOffset(2.0);
	ph2->GetXaxis()->SetRangeUser(-5,5);
	ph2->GetXaxis()->CenterTitle(kTRUE);
	ph2->GetYaxis()->SetTitleOffset(2.0);
	ph2->GetYaxis()->SetRangeUser(0,500);
	ph2->GetYaxis()->CenterTitle(kTRUE);
	ph2->GetZaxis()->SetTitleOffset(1.8);
	ph2->GetZaxis()->SetRangeUser(1e-8, 0.1);
	ph2->Draw("SURF1");
	myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_2D_pdf.pdf");
	myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_2D_pdf.png");
	myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_2D_pdf.C");
	
	TH2F * ph2_bkg = new TH2F("fit2D_bkg","; #gamma cluster time (ns); #slash{E}_{T} (GeV); PDF",100,-15,15,100,0,1000);
	fitModelBkg->fillHistogram(ph2_bkg, RooArgList(pho1ClusterTime, MET));
	ph2_bkg->GetXaxis()->SetTitleOffset(2.0);
	ph2_bkg->GetXaxis()->SetRangeUser(-5,5);
	ph2_bkg->GetXaxis()->CenterTitle(kTRUE);
	ph2_bkg->GetYaxis()->SetTitleOffset(2.0);
	ph2_bkg->GetYaxis()->SetRangeUser(0,500);
	ph2_bkg->GetYaxis()->CenterTitle(kTRUE);
	ph2_bkg->GetZaxis()->SetTitleOffset(1.8);
	ph2_bkg->GetZaxis()->SetRangeUser(1e-8, 0.1);
	ph2_bkg->Draw("SURF1");
	myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgonly_2D_pdf.pdf");
	myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgonly_2D_pdf.png");
	myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgonly_2D_pdf.C");

		
	TH2F * h2Data_toy = new TH2F("h2Data_toy","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events",100,-15,15,100,0,1000);
	data_toy->fillHistogram(h2Data_toy, RooArgList(pho1ClusterTime, MET));
	h2Data_toy->GetXaxis()->SetTitleOffset(2.0);
	h2Data_toy->GetXaxis()->SetRangeUser(-5,5);
	h2Data_toy->GetXaxis()->CenterTitle(kTRUE);
	h2Data_toy->GetYaxis()->SetTitleOffset(2.0);
	h2Data_toy->GetYaxis()->SetRangeUser(0,500);
	h2Data_toy->GetYaxis()->CenterTitle(kTRUE);
	h2Data_toy->GetZaxis()->SetTitleOffset(1.8);
	h2Data_toy->GetZaxis()->SetRangeUser(0, 1e3);
	h2Data_toy->Draw("LEGO2");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_toy_2D.pdf");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_toy_2D.png");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_toy_2D.C");

	h2Data->GetXaxis()->SetTitleOffset(2.0);
	h2Data->GetXaxis()->SetRangeUser(-10,15);
	h2Data->GetXaxis()->CenterTitle(kTRUE);
	h2Data->GetYaxis()->SetTitleOffset(2.0);
	h2Data->GetYaxis()->SetRangeUser(0.1,600);
	h2Data->GetYaxis()->CenterTitle(kTRUE);
	h2Data->GetZaxis()->SetTitleOffset(1.8);
	h2Data->GetZaxis()->SetRangeUser(0, 1e3);
	h2Data->Draw("LEGO2");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_2D_LEGO2.pdf");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_2D_LEGO2.png");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_2D_LEGO2.C");
	h2Data->GetYaxis()->SetTitleOffset(1.8);
	h2Data->GetXaxis()->SetTitleOffset(1.5);
	h2Data->Draw("COLZ");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_2D_COLZ.pdf");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_2D_COLZ.png");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_2D_COLZ.C");
	//h2Data->SetMarkerStyle(7);
	h2Data->Draw("");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_2D.pdf");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_2D.png");
	myC->SaveAs("fit_results/plots/"+modelName+"_data_2D.C");

	
	ws->import(*data);
	ws->import(*data_toy);
        ws->import(*rhGJets);
        ws->import(*rhQCD);
	ws->import(*rpSig);
	ws->import(*fitModelBkg);
	ws->import(nSig);
	ws->import(nBkg);
        //ws->import(*fitModelBkgSig);
        ws->import(*frame_pho1ClusterTime);
        ws->import(*frame_MET);
        ws->import(*frame_nBkg_LL);
        ws->import(*frame_nSig_LL);
        ws->import(*fres);
	
	//MakeDataCard(modelName, ws);
	
        return ws;
	
};



RooWorkspace* Fit1DMETTimeDataBkgSig( TH1F * h1Data, TH1F * h1GJets, TH1F * h1QCD,  TH1F * h1Sig, float fracGJets, float fracQCD, TString modelName, TString modelTitle, bool useToy)
{
	RooWorkspace* ws = new RooWorkspace( "ws_combine", "ws_combine" );
	// define variables
	RooRealVar bin("bin","2D bin",0,h1Data->GetSize()-2,"");

	double npoints = 1.0*h1Data->Integral();

	RooRealVar nGJets ("nGJets", "nGJets", fracGJets);
	nGJets.setConstant(kTRUE);
	RooRealVar nQCD ("nQCD", "nQCD", fracQCD);
	nQCD.setConstant(kTRUE);
	
	//RooDataHist
	RooDataHist* data = new RooDataHist("data", "data", RooArgSet(bin), h1Data);	
	RooDataHist* rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(bin), h1GJets);	
	RooDataHist* rhGJets_temp = new RooDataHist("rhGJets_temp", "rhGJets_temp", RooArgSet(bin), h1GJets);	
	RooDataHist* rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(bin), h1QCD);	
	RooDataHist* rhQCD_temp = new RooDataHist("rhQCD_temp", "rhQCD_temp", RooArgSet(bin), h1QCD);	
	RooDataHist* rhSig = new RooDataHist("rhSig", "rhSig", RooArgSet(bin), h1Sig);	
	//fill iempty background Histgrams bins with tiny value to allow fluctuation in generated toy data
	for(int i=0;i<data->numEntries() ; i++)
	{
		rhGJets_temp->get(i);
		rhQCD_temp->get(i);
		float weight_rhGJets = rhGJets_temp->weight();
		float weight_rhQCD = rhQCD_temp->weight();
		if(weight_rhGJets< 1e-5) rhGJets_temp->set(1e-3);
		if(weight_rhQCD< 1e-5) rhQCD_temp->set(1e-3);
	}

	//RooDataHist -> RooHistPdf
	RooHistPdf * rpGJets_temp = new RooHistPdf("rpGJets_temp", "rpGJets_temp", RooArgSet(bin), *rhGJets_temp, 0);
	RooHistPdf * rpQCD_temp = new RooHistPdf("rpQCD_temp", "rpQCD_temp", RooArgSet(bin), *rhQCD_temp, 0);
	//RooHistPdf -> RooAbsPdf
	RooAbsPdf * fitModelBkg_temp = new RooAddPdf("fitModelBkg_temp", "fitModelBkg_temp", RooArgSet(*rpGJets_temp, *rpQCD_temp), RooArgSet(nGJets, nQCD));	

	//create toy data
	//TRandom3* r3 = new TRandom3(0);
	//double npoints = r3->PoissonD(h1Data->Integral());	
	//RooDataHist* data_toy = fitModelBkg->generateBinned(RooArgSet(bin), npoints, RooFit::ExpectedData());
	RooDataHist* data_toy = fitModelBkg_temp->generateBinned(RooArgSet(bin), npoints);
	data_toy->SetName("data_toy");
	
	//to avoid zero likelihood, fill empty template bins with tiny values
	for(int i=0;i<data->numEntries() ; i++)
	{
		data->get(i);
		data_toy->get(i);
		rhGJets->get(i);
		rhQCD->get(i);
		rhSig->get(i);
		float weight_data = data->weight();
		float weight_data_toy = data_toy->weight();
		float weight_rhGJets = rhGJets->weight();
		float weight_rhQCD = rhQCD->weight();
		float weight_rhSig = rhSig->weight();
		if((weight_rhSig < 1e-5) && ((useToy ? weight_data_toy : weight_data) > 0))
		{
			rhSig->set(1e-3);
		}
		if((weight_rhGJets + weight_rhQCD < 1e-5) && ((useToy ? weight_data_toy : weight_data) > 0))
		{
			rhGJets->set(1e-3);
			rhQCD->set(1e-3);
		}
	
	}
	
	//new pdf after fill empty bins
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(bin), *rhGJets, 0);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(bin), *rhQCD, 0);
	RooHistPdf * rpSig = new RooHistPdf("rpSig", "rpSig", RooArgSet(bin), *rhSig, 0);
	
	RooAbsPdf * fitModelBkg = new RooAddPdf("fitModelBkg", "fitModelBkg", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));	
	
	RooRealVar nSig ("rpSig_yield", "rpSig_yield", 0.0, 0.0, 0.1*npoints);
	nSig.setConstant(kFALSE);
	RooRealVar nBkg ("fitModelBkg_yield", "fitModelBkg_yield", npoints, 0.0, 1.5*npoints);
	nBkg.setConstant(kFALSE);

	RooAbsPdf * fitModelBkgSig = new RooAddPdf("fitModelBkgSig", "fitModelBkgSig", RooArgSet(*fitModelBkg, *rpSig), RooArgSet(nBkg, nSig));	
	//RooAbsPdf * fitModelBkg = new RooAddPdf("fitModelBkg", "fitModelBkg", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));	
	//fit
	RooAbsReal* nll = fitModelBkgSig->createNLL(*data, RooFit::NumCPU(8)) ;
	RooFitResult * fres;
	if(useToy) fres = fitModelBkgSig->fitTo( *data_toy, RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
	else fres = fitModelBkgSig->fitTo( *data, RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
        
	nGJets.Print();
	nQCD.Print();
	nBkg.Print();
        nSig.Print();

	//draw some plot-s
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

       
	RooPlot * frame_bin = bin.frame(0, h1Data->GetSize()-2, h1Data->GetSize()-2);
        if(useToy) data_toy->plotOn( frame_bin, RooFit::Name("bin_data") );
        else data->plotOn( frame_bin, RooFit::Name("bin_data") );
        fitModelBkgSig->plotOn( frame_bin, RooFit::Name("bin_Bkg"), RooFit::Components("fitModelBkg"), RooFit::LineColor(kBlue) );
        fitModelBkgSig->plotOn( frame_bin, RooFit::Name("bin_Sig"), RooFit::Components("rpSig"), RooFit::LineColor(kGreen) );
        fitModelBkgSig->plotOn( frame_bin, RooFit::Name("bin_all"), RooFit::Components("fitModelBkgSig"), RooFit::LineColor(kRed) );
        frame_bin->SetName("bin_frame");
	
	frame_bin->SetMaximum(1000.0*frame_bin->GetMaximum());
	frame_bin->SetMinimum(1e-3);
	frame_bin->Draw();

	TLegend * leg_bin = new TLegend(0.18, 0.7, 0.93, 0.89);
	leg_bin->SetNColumns(2);
        leg_bin->SetBorderSize(0);
        leg_bin->SetTextSize(0.03);
        leg_bin->SetLineColor(1);
        leg_bin->SetLineStyle(1);
        leg_bin->SetLineWidth(1);
        leg_bin->SetFillColor(0);
        leg_bin->SetFillStyle(1001);
	leg_bin->AddEntry("bin_data","data","lep");
	leg_bin->AddEntry("bin_Bkg","#gamma + jets/QCD bkg","l");
	leg_bin->AddEntry("bin_Sig",modelTitle,"l");
	leg_bin->AddEntry("bin_all","combined fit","l");
	leg_bin->Draw();

     	myC->SetTitle("");
        myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_bin.pdf");
        myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_bin.png");
        myC->SaveAs("fit_results/plots/"+modelName+"_fit_bkgsig_bin.C");

        RooPlot * frame_nBkg_LL = nBkg.frame(0.0, 1.5*npoints, 100);
	RooAbsReal* pll_nBkg = nll->createProfile(nBkg) ;
	nll->plotOn(frame_nBkg_LL, RooFit::ShiftToZero()) ;
	pll_nBkg->plotOn(frame_nBkg_LL, RooFit::LineColor(kRed)) ;
	frame_nBkg_LL->SetName("nBkg_frame_Likelihood");

        RooPlot * frame_nSig_LL = nSig.frame(0.0, 0.1*npoints, 100);
	RooAbsReal* pll_nSig = nll->createProfile(nSig) ;
	nll->plotOn(frame_nSig_LL, RooFit::ShiftToZero()) ;
	pll_nSig->plotOn(frame_nSig_LL, RooFit::LineColor(kRed)) ;
	frame_nSig_LL->SetName("nSig_frame_Likelihood");
	
	myC->SetLogy(0);
	myC->SetLogz(1);
	myC->SetTheta(69.64934);
   	myC->SetPhi(-51.375);

	
	ws->import(*data);
	ws->import(*data_toy);
        ws->import(*rhGJets);
        ws->import(*rhQCD);
	ws->import(*rpSig);
	ws->import(*fitModelBkg);
	ws->import(nSig);
	ws->import(nBkg);
        //ws->import(*fitModelBkgSig);
        ws->import(*frame_bin);
        ws->import(*frame_nBkg_LL);
        ws->import(*frame_nSig_LL);
        ws->import(*fres);
	
	//MakeDataCard(modelName, ws);
	
        return ws;
	
};



void MakeDataCard(TString modelName, RooWorkspace *ws, float N_obs, float N_bkg, float N_sig)
{
	std::string _modelName ((const char*) modelName);
	std::string _wsName ((const char*)ws->GetName());
	
	FILE * m_outfile = fopen(("fit_results/datacards/DelayedPhotonCard_"+_modelName+".txt").c_str(), "w");
	fprintf(m_outfile, "imax 1\n");
	fprintf(m_outfile, "jmax 1\n");
	fprintf(m_outfile, "kmax *\n");
	fprintf(m_outfile, "---------------\n");
	fprintf(m_outfile, "shapes background bin1 fit_combineWS_%s.root %s:fitModelBkg\n", _modelName.c_str(), _wsName.c_str());
	fprintf(m_outfile, "shapes signal bin1 fit_combineWS_%s.root %s:rpSig\n", _modelName.c_str(), _wsName.c_str());
	fprintf(m_outfile, "shapes data_obs bin1 fit_combineWS_%s.root %s:data_toy\n", _modelName.c_str(), _wsName.c_str());

	fprintf(m_outfile, "---------------\n");
	fprintf(m_outfile, "bin bin1\n");
	fprintf(m_outfile, "observation %6.2f\n", N_obs);
	fprintf(m_outfile, "------------------------------\n");
	fprintf(m_outfile, "bin             bin1       bin1\n");
	fprintf(m_outfile, "process         signal     background\n");
	fprintf(m_outfile, "process         0          1\n");
	fprintf(m_outfile, "rate            %6.2f          %6.2f\n", N_sig, N_bkg);
	fprintf(m_outfile, "--------------------------------\n");
	fprintf(m_outfile, "lumi     lnN    1.057       1.057\n");
	
};

void Fit1DMETTimeBiasTest( TH1F * h1Data, TH1F * h1Bkg,  TH1F * h1Sig, float SoverB, int ntoys, TString modelName)
{
	TString sSoverB = Form("%7.5f", SoverB);
	std::string _SoverB ((const char*) sSoverB);
	std::string _modelName ((const char*) modelName);		
	TFile *f_Out_bias = new TFile(("fit_results/bias/bias_"+_modelName+"_"+_SoverB+".root").c_str(),"recreate");
	
	RooRandom::randomGenerator()->SetSeed( 0 );
	
	double _bias, _biasNorm;
  	double _Ns_fit, _Ns_sigma, _Ns, _Nbkg_fit, _Nbkg_sigma, _Nbkg;
  	int _status, _covStatus;
	TTree* outTree = new TTree("biasTree", "tree containing bias tests");
	outTree->Branch("bias", &_bias, "bias/D");
	outTree->Branch("biasNorm", &_biasNorm, "biasNorm/D");
	outTree->Branch("Ns_fit", &_Ns_fit, "Ns_fit/D");
	outTree->Branch("Ns_sigma", &_Ns_sigma, "Ns_sigma/D");
	outTree->Branch("Ns", &_Ns, "Ns/D");
	outTree->Branch("Nbkg_fit", &_Nbkg_fit, "Nbkg_fit/D");
	outTree->Branch("Nbkg_sigma", &_Nbkg_sigma, "Nbkg_sigma/D");
	outTree->Branch("Nbkg", &_Nbkg, "Nbkg/D");
	outTree->Branch("status", &_status, "status/I");
	outTree->Branch("covStatus", &_covStatus, "covStatus/I");

	RooRealVar bin("bin","2D bin",0,h1Data->GetSize()-2,"");
	RooDataHist* data = new RooDataHist("data", "data", RooArgSet(bin), h1Data);	
	RooDataHist* rhBkg = new RooDataHist("rhBkg", "rhBkg", RooArgSet(bin), h1Bkg);	
	RooDataHist* rhSig = new RooDataHist("rhSig", "rhSig", RooArgSet(bin), h1Sig);	

	for(int ind_toy = 0; ind_toy<ntoys; ind_toy++)
	{
		TRandom3* r3 = new TRandom3(0);
		double nBkg_true = r3->PoissonD(h1Data->Integral());	
		double nSig_true = r3->PoissonD(SoverB*h1Data->Integral());	

		double npoints = nBkg_true + nSig_true;

		RooRealVar nSig ("rpSig_yield", "rpSig_yield", nSig_true, 0.0, 1.5*npoints);
		nSig.setConstant(kFALSE);
		RooRealVar nBkg ("fitModelBkg_yield", "fitModelBkg_yield", nBkg_true, 0.0, 1.5*npoints);
		nBkg.setConstant(kFALSE);

		//RooDataHist
		RooDataHist* rhBkg_temp = new RooDataHist("rhBkg_temp", "rhBkg_temp", RooArgSet(bin), h1Bkg);	
		RooDataHist* rhSig_temp = new RooDataHist("rhSig_temp", "rhSig_temp", RooArgSet(bin), h1Sig);	

		//fill iempty background Histgrams bins with tiny value to allow fluctuation in generated toy data
		for(int i=0;i<data->numEntries() ; i++)
		{
			rhBkg_temp->get(i);
			rhSig_temp->get(i);
			float weight_rhBkg = rhBkg_temp->weight();
			float weight_rhSig = rhSig_temp->weight();
			if(weight_rhBkg< 1e-5) rhBkg_temp->set(1e-3);
			if(weight_rhSig< 1e-5) rhSig_temp->set(1e-3);
		}

		//RooHistPdf -> RooHistPdf
		RooHistPdf * rpBkg_temp = new RooHistPdf("rpBkg_temp", "rpBkg_temp", RooArgSet(bin), *rhBkg_temp, 0);
		RooHistPdf * rpSig_temp = new RooHistPdf("rpSig_temp", "rpSig_temp", RooArgSet(bin), *rhSig_temp, 0);

		RooAbsPdf * fitModelBkgSig_temp = new RooAddPdf("fitModelBkgSig_temp", "fitModelBkgSig_temp", RooArgSet(*rpBkg_temp, *rpSig_temp), RooArgSet(nBkg, nSig));	
		//create toy data
		RooDataHist* data_toy = fitModelBkgSig_temp->generateBinned(RooArgSet(bin), npoints);
		data_toy->SetName("data_toy");
		
		//to avoid zero likelihood, fill empty template bins with tiny values
		for(int i=0;i<data->numEntries() ; i++)
		{
			data->get(i);
			data_toy->get(i);
			rhBkg->get(i);
			rhSig->get(i);
			float weight_data = data->weight();
			float weight_data_toy = data_toy->weight();
			float weight_rhBkg = rhBkg->weight();
			float weight_rhSig = rhSig->weight();
			if((weight_rhSig < 1e-5) && (weight_data_toy > 0))
			{
				rhSig->set(1e-3);
			}
			if((weight_rhBkg < 1e-5) && (weight_data_toy > 0))
			{
				rhBkg->set(1e-3);
			}
		
		}
		
		//new pdf after fill empty bins
		RooHistPdf * rpSig = new RooHistPdf("rpSig", "rpSig", RooArgSet(bin), *rhSig, 0);
		RooHistPdf * rpBkg = new RooHistPdf("rpBkg", "rpBkg", RooArgSet(bin), *rhBkg, 0);
		
		RooAbsPdf * fitModelBkgSig = new RooAddPdf("fitModelBkgSig", "fitModelBkgSig", RooArgSet(*rpBkg, *rpSig), RooArgSet(nBkg, nSig));	
		//fit
		RooAbsReal* nll = fitModelBkgSig->createNLL(*data, RooFit::NumCPU(8)) ;
		RooFitResult * fres;
		fres = fitModelBkgSig->fitTo( *data_toy, RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));
		
		//nBkg.Print();
		//nSig.Print();

		_status = fres->status();
		_covStatus = fres->covQual();
		_Ns = nSig_true;		
		_Ns_fit = nSig.getVal();
		_Ns_sigma = nSig.getError();
		_Nbkg = nBkg_true;	
		_Nbkg_fit = nBkg.getVal();	
		_Nbkg_sigma = nBkg.getError();
		_bias = _Ns - _Ns_fit;
		if(abs(_Ns_sigma) >0.0) _biasNorm = _bias/_Ns_sigma;
		else  _biasNorm = -999.0;
      		std::cout << "toy iteration:" << ind_toy << std::endl;
      		outTree->Fill();
      		delete nll;	
	}

	outTree->Write();
};
