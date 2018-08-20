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
#include <Math/DistFunc.h>
#include <TFractionFitter.h>
#include <TRandom3.h>
//LOCAL INCLUDES
#include "MakeFitMETTime.hh"
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

RooWorkspace* FitDataBkgFraction( TH1F * h1_Data, TString varName, TString varTitle, TString varUnit, float lumi, float varLow, float varHigh, TH1F * h1_GJets, TH1F * h1_QCD, TString outPlotsDir)
{
	RooWorkspace* ws = new RooWorkspace( "ws", "" );

	// define variables
	RooRealVar fitVar ( varName, varTitle, varLow, varHigh, varUnit);	
	//RooRealVar nGJets ("nGJets", "nGJets", 5835.0, 0.5*5835.0, 1.5*5835.0);
	//RooRealVar nGJets ("nGJets", "nGJets", 5800.0, 0.0, tree->GetEntries());	
	//RooRealVar nGJets ("nGJets", "nGJets", 0.5, 0.0001, 10000.0);	
	RooRealVar nGJets ("nGJets", "nGJets", 0.5, 0.0001, 0.5*h1_Data->Integral());	
	//RooRealVar nQCD ("nQCD", "nQCD", 3500.0, 0.5*3500, 1.5*3500.0);
	//RooRealVar nQCD ("nQCD", "nQCD", 3500.0, 0.0, tree->GetEntries());	
	//RooRealVar nQCD ("nQCD", "nQCD", 0.5, 0.0001, 10000.0);	
	RooRealVar nQCD ("nQCD", "nQCD", 0.5, 0.0001, 0.5*h1_Data->Integral());	


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
	
	frame->SetTitle("");
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

	DrawCMS(myC, 13, lumi);
     	myC->SetTitle("");
        myC->SaveAs("fit_results/"+outPlotsDir+"/bkg_yield_fit_"+varName+".pdf");
        myC->SaveAs("fit_results/"+outPlotsDir+"/bkg_yield_fit_"+varName+".png");
        myC->SaveAs("fit_results/"+outPlotsDir+"/bkg_yield_fit_"+varName+".C");

	
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
	RooRealVar pho1ClusterTime_SmearToData("pho1ClusterTime_SmearToData","#gamma cluster time ",-15.0,15.0,"ns");
	RooRealVar MET("MET","#slash{E}_{T} ",0,1000,"GeV");

	RooRealVar nGJets ("nGJets", "nGJets", fracGJets, fracGJets-3.0*fracGJetsErr, fracGJets+3.0*fracGJetsErr);
	RooRealVar nQCD ("nQCD", "nQCD", fracQCD, fracQCD-3.0*fracQCDErr, fracQCD+3.0*fracQCDErr);
	//RooRealVar nGJets ("nGJets", "nGJets", 0.5,0.0,1.0);
	//RooRealVar nQCD ("nQCD", "nQCD", 0.5,0.0,1.0);

	RooRealVar weightGJets("weightGJets", "weightGJets", (treeData->GetEntries()*1.0)/(treeGJets->GetEntries()*1.0));
	RooRealVar weightQCD("weightQCD", "weightQCD", (treeData->GetEntries()*1.0)/(treeQCD->GetEntries()*1.0));

	//data sets
	RooDataSet data( "data", "data", RooArgSet(pho1ClusterTime_SmearToData, MET), RooFit::Import(*treeData));
	RooDataSet dataGJets( "dataGJets", "dataGJets", RooArgSet(pho1ClusterTime_SmearToData, MET), RooFit::Import(*treeGJets), RooFit::WeightVar("weightGJets"));
	RooDataSet dataQCD( "dataQCD", "dataQCD", RooArgSet(pho1ClusterTime_SmearToData, MET), RooFit::Import(*treeQCD), RooFit::WeightVar("weightQCD"));


	//RooDataSet -> RooDataHist
	RooDataHist* rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(pho1ClusterTime_SmearToData, MET), dataGJets);	
	RooDataHist* rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(pho1ClusterTime_SmearToData, MET), dataQCD);	
	//RooDataHist -> RooHistPdf
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(pho1ClusterTime_SmearToData, MET), *rhGJets);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(pho1ClusterTime_SmearToData, MET), *rhQCD);
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

        RooPlot * frame_pho1ClusterTime_SmearToData = pho1ClusterTime_SmearToData.frame(-15.0, 15.0, 100);
        data.plotOn( frame_pho1ClusterTime_SmearToData );
        fitModel->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Components("rpGJets"), RooFit::LineColor(kViolet + 10) );
        fitModel->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Components("rpQCD"), RooFit::LineColor(kOrange + 9) );
        fitModel->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Components("fitModel"), RooFit::LineColor(kGreen) );
        frame_pho1ClusterTime_SmearToData->SetName("pho1ClusterTime_SmearToData_frame");
	
        RooPlot * frame_pho1ClusterTime_SmearToData_LL = pho1ClusterTime_SmearToData.frame(-15.0, 15.0, 100);
	nll->plotOn(frame_pho1ClusterTime_SmearToData_LL, RooFit::ShiftToZero()) ;
	frame_pho1ClusterTime_SmearToData_LL->SetName("pho1ClusterTime_SmearToData_frame_Likelihood");
       
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
        ws->import(*frame_pho1ClusterTime_SmearToData);
        ws->import(*frame_pho1ClusterTime_SmearToData_LL);
        ws->import(*frame_MET);
        ws->import(*frame_MET_LL);
        ws->import(*fres);

        return ws;
	
};

RooWorkspace* Fit2DMETTimeDataBkg( TH2F * h2Data, TH2F * h2GJets, TH2F * h2QCD,  float fracGJets, float fracGJetsErr, float fracQCD, float fracQCDErr, TString outPlotsDir)
{
	
	RooWorkspace* ws = new RooWorkspace( "ws", "" );
	// define variables
	RooRealVar pho1ClusterTime_SmearToData("pho1ClusterTime_SmearToData","#gamma cluster time ",-15.0,15.0,"ns");
	RooRealVar MET("MET","#slash{E}_{T} ",0,1000,"GeV");

	RooRealVar nGJets ("nGJets", "nGJets", fracGJets, fracGJets-3.0*fracGJetsErr, fracGJets+3.0*fracGJetsErr);
	RooRealVar nQCD ("nQCD", "nQCD", fracQCD, fracQCD-3.0*fracQCDErr, fracQCD+3.0*fracQCDErr);
	//RooRealVar nGJets ("nGJets", "nGJets", 0.5,0.001,10000.0);
	//RooRealVar nQCD ("nQCD", "nQCD", 0.5,0.001,10000.0);

	//RooDataHist
	RooDataHist* data = new RooDataHist("data", "data", RooArgSet(pho1ClusterTime_SmearToData, MET), h2Data);	
	RooDataHist* rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(pho1ClusterTime_SmearToData, MET), h2GJets);	
	RooDataHist* rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(pho1ClusterTime_SmearToData, MET), h2QCD);	

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
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(pho1ClusterTime_SmearToData, MET), *rhGJets, 0);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(pho1ClusterTime_SmearToData, MET), *rhQCD, 0);
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

        RooPlot * frame_pho1ClusterTime_SmearToData = pho1ClusterTime_SmearToData.frame(-15.0, 15.0, 100);
        data->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Name("pho1ClusterTime_SmearToData_data") );
        fitModel->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Name("pho1ClusterTime_SmearToData_GJets"), RooFit::Components("rpGJets"), RooFit::LineColor(kAzure + 7) );
        fitModel->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Name("pho1ClusterTime_SmearToData_QCD"), RooFit::Components("rpQCD"), RooFit::LineColor(kOrange - 9) );
        fitModel->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Name("pho1ClusterTime_SmearToData_all"), RooFit::Components("fitModel"), RooFit::LineColor(kRed) );
        frame_pho1ClusterTime_SmearToData->SetName("pho1ClusterTime_SmearToData_frame");

	frame_pho1ClusterTime_SmearToData->SetMaximum(150.0*frame_pho1ClusterTime_SmearToData->GetMaximum());
	frame_pho1ClusterTime_SmearToData->SetMinimum(0.1);
	frame_pho1ClusterTime_SmearToData->Draw();

	TLegend * leg_pho1ClusterTime_SmearToData = new TLegend(0.18, 0.7, 0.93, 0.89);
	leg_pho1ClusterTime_SmearToData->SetNColumns(3);
        leg_pho1ClusterTime_SmearToData->SetBorderSize(0);
        leg_pho1ClusterTime_SmearToData->SetTextSize(0.03);
        leg_pho1ClusterTime_SmearToData->SetLineColor(1);
        leg_pho1ClusterTime_SmearToData->SetLineStyle(1);
        leg_pho1ClusterTime_SmearToData->SetLineWidth(1);
        leg_pho1ClusterTime_SmearToData->SetFillColor(0);
        leg_pho1ClusterTime_SmearToData->SetFillStyle(1001);
	leg_pho1ClusterTime_SmearToData->AddEntry("pho1ClusterTime_SmearToData_data","data","lep");
	leg_pho1ClusterTime_SmearToData->AddEntry("pho1ClusterTime_SmearToData_GJets","#gamma + jets","l");
	leg_pho1ClusterTime_SmearToData->AddEntry("pho1ClusterTime_SmearToData_QCD","QCD","l");
	leg_pho1ClusterTime_SmearToData->AddEntry("pho1ClusterTime_SmearToData_all","combined fit","l");
	leg_pho1ClusterTime_SmearToData->Draw();

	myC->SetTitle("");
	myC->SaveAs("fit_results/"+outPlotsDir+"/fit_bkgonly_pho1ClusterTime_SmearToData.pdf");
	myC->SaveAs("fit_results/"+outPlotsDir+"/fit_bkgonly_pho1ClusterTime_SmearToData.png");
	myC->SaveAs("fit_results/"+outPlotsDir+"/fit_bkgonly_pho1ClusterTime_SmearToData.C");
	
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
        myC->SaveAs("fit_results/"+outPlotsDir+"/fit_bkgonly_MET.pdf");
        myC->SaveAs("fit_results/"+outPlotsDir+"/fit_bkgonly_MET.png");
        myC->SaveAs("fit_results/"+outPlotsDir+"/fit_bkgonly_MET.C");
	
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
	fitModel->fillHistogram(ph2, RooArgList(pho1ClusterTime_SmearToData, MET));
	ph2->GetXaxis()->SetTitleOffset(2.0);
	ph2->GetXaxis()->CenterTitle(kTRUE);
	ph2->GetYaxis()->SetTitleOffset(2.0);
	ph2->GetYaxis()->CenterTitle(kTRUE);
	ph2->GetZaxis()->SetTitleOffset(1.8);
	ph2->GetZaxis()->SetRangeUser(1e-8, 0.1);
	ph2->Draw("SURF1");
	myC->SaveAs("fit_results/"+outPlotsDir+"/fit_bkgonly_2D_pdf.pdf");
	myC->SaveAs("fit_results/"+outPlotsDir+"/fit_bkgonly_2D_pdf.png");
	myC->SaveAs("fit_results/"+outPlotsDir+"/fit_bkgonly_2D_pdf.C");
	
	ws->import(*data);
        ws->import(*rhGJets);
        ws->import(*rhQCD);
        ws->import(*fitModel);
        ws->import(*frame_pho1ClusterTime_SmearToData);
        ws->import(*frame_MET);
       // ws->import(*frame_2D);
        ws->import(*frame_nGJets_LL);
        ws->import(*frame_nQCD_LL);
        ws->import(*fres);
        return ws;
	
};

RooWorkspace* Fit2DMETTimeDataBkgSig( TH2F * h2Data, TH2F * h2GJets, TH2F * h2QCD,  TH2F * h2Sig, float fracGJets, float fracQCD, TString modelName, TString modelTitle, bool useToy, TString outPlotsDir)
{
	RooWorkspace* ws = new RooWorkspace( "ws", "" );
	// define variables
	RooRealVar pho1ClusterTime_SmearToData("pho1ClusterTime_SmearToData","#gamma cluster time ",-15.0,15.0,"ns");
	RooRealVar MET("MET","#slash{E}_{T} ",0,1000,"GeV");

	double npoints = 1.0*h2Data->Integral();

	RooRealVar nGJets ("nGJets", "nGJets", fracGJets);
	nGJets.setConstant(kTRUE);
	RooRealVar nQCD ("nQCD", "nQCD", fracQCD);
	nQCD.setConstant(kTRUE);

	
	//RooDataHist
	RooDataHist* data = new RooDataHist("data", "data", RooArgSet(pho1ClusterTime_SmearToData, MET), h2Data);	
	RooDataHist* rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(pho1ClusterTime_SmearToData, MET), h2GJets);	
	RooDataHist* rhGJets_temp = new RooDataHist("rhGJets_temp", "rhGJets_temp", RooArgSet(pho1ClusterTime_SmearToData, MET), h2GJets);	
	RooDataHist* rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(pho1ClusterTime_SmearToData, MET), h2QCD);	
	RooDataHist* rhQCD_temp = new RooDataHist("rhQCD_temp", "rhQCD_temp", RooArgSet(pho1ClusterTime_SmearToData, MET), h2QCD);	
	RooDataHist* rhSig = new RooDataHist("rhSig", "rhSig", RooArgSet(pho1ClusterTime_SmearToData, MET), h2Sig);	
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
	RooHistPdf * rpGJets_temp = new RooHistPdf("rpGJets_temp", "rpGJets_temp", RooArgSet(pho1ClusterTime_SmearToData, MET), *rhGJets_temp, 0);
	RooHistPdf * rpQCD_temp = new RooHistPdf("rpQCD_temp", "rpQCD_temp", RooArgSet(pho1ClusterTime_SmearToData, MET), *rhQCD_temp, 0);
	//RooHistPdf -> RooAbsPdf
	RooAbsPdf * fitModelBkg_temp = new RooAddPdf("fitModelBkg_temp", "fitModelBkg_temp", RooArgSet(*rpGJets_temp, *rpQCD_temp), RooArgSet(nGJets, nQCD));	

	//create toy data
	//TRandom3* r3 = new TRandom3(0);
	//double npoints = r3->PoissonD(h2Data->Integral());	
	//RooDataHist* data_toy = fitModelBkg->generateBinned(RooArgSet(pho1ClusterTime_SmearToData, MET), npoints, RooFit::ExpectedData());
	RooDataHist* data_toy = fitModelBkg_temp->generateBinned(RooArgSet(pho1ClusterTime_SmearToData, MET), npoints);
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
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(pho1ClusterTime_SmearToData, MET), *rhGJets, 0);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(pho1ClusterTime_SmearToData, MET), *rhQCD, 0);
	RooHistPdf * rpSig = new RooHistPdf("rpSig", "rpSig", RooArgSet(pho1ClusterTime_SmearToData, MET), *rhSig, 0);
	
	
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

        RooPlot * frame_pho1ClusterTime_SmearToData = pho1ClusterTime_SmearToData.frame(-15.0, 15.0, 100);
        if(useToy) data_toy->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Name("pho1ClusterTime_SmearToData_data") );
        else data->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Name("pho1ClusterTime_SmearToData_data") );
        fitModelBkgSig->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Name("pho1ClusterTime_SmearToData_Bkg"), RooFit::Components("fitModelBkg"), RooFit::LineColor(kBlue) );
        fitModelBkgSig->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Name("pho1ClusterTime_SmearToData_Sig"), RooFit::Components("rpSig"), RooFit::LineColor(kGreen) );
        fitModelBkgSig->plotOn( frame_pho1ClusterTime_SmearToData, RooFit::Name("pho1ClusterTime_SmearToData_all"), RooFit::Components("fitModelBkgSig"), RooFit::LineColor(kRed) );
        frame_pho1ClusterTime_SmearToData->SetName("pho1ClusterTime_SmearToData_frame");

	frame_pho1ClusterTime_SmearToData->SetMaximum(1000.0*frame_pho1ClusterTime_SmearToData->GetMaximum());
	frame_pho1ClusterTime_SmearToData->SetMinimum(1e-3);
	frame_pho1ClusterTime_SmearToData->Draw();

	TLegend * leg_pho1ClusterTime_SmearToData = new TLegend(0.18, 0.7, 0.93, 0.89);
	leg_pho1ClusterTime_SmearToData->SetNColumns(2);
        leg_pho1ClusterTime_SmearToData->SetBorderSize(0);
        leg_pho1ClusterTime_SmearToData->SetTextSize(0.03);
        leg_pho1ClusterTime_SmearToData->SetLineColor(1);
        leg_pho1ClusterTime_SmearToData->SetLineStyle(1);
        leg_pho1ClusterTime_SmearToData->SetLineWidth(1);
        leg_pho1ClusterTime_SmearToData->SetFillColor(0);
        leg_pho1ClusterTime_SmearToData->SetFillStyle(1001);
	leg_pho1ClusterTime_SmearToData->AddEntry("pho1ClusterTime_SmearToData_data","data","lep");
	leg_pho1ClusterTime_SmearToData->AddEntry("pho1ClusterTime_SmearToData_Bkg","#gamma + jets/QCD bkg","l");
	leg_pho1ClusterTime_SmearToData->AddEntry("pho1ClusterTime_SmearToData_Sig",modelTitle,"l");
	leg_pho1ClusterTime_SmearToData->AddEntry("pho1ClusterTime_SmearToData_all","combined fit","l");
	leg_pho1ClusterTime_SmearToData->Draw();

	myC->SetTitle("");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_pho1ClusterTime_SmearToData.pdf");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_pho1ClusterTime_SmearToData.png");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_pho1ClusterTime_SmearToData.C");
	
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
        myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_MET.pdf");
        myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_MET.png");
        myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_MET.C");
	

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
	fitModelBkgSig->fillHistogram(ph2, RooArgList(pho1ClusterTime_SmearToData, MET));
	ph2->GetXaxis()->SetTitleOffset(2.0);
	ph2->GetXaxis()->SetRangeUser(-5,5);
	ph2->GetXaxis()->CenterTitle(kTRUE);
	ph2->GetYaxis()->SetTitleOffset(2.0);
	ph2->GetYaxis()->SetRangeUser(0,500);
	ph2->GetYaxis()->CenterTitle(kTRUE);
	ph2->GetZaxis()->SetTitleOffset(1.8);
	ph2->GetZaxis()->SetRangeUser(1e-8, 0.1);
	ph2->Draw("SURF1");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_2D_pdf.pdf");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_2D_pdf.png");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_2D_pdf.C");
	
	TH2F * ph2_bkg = new TH2F("fit2D_bkg","; #gamma cluster time (ns); #slash{E}_{T} (GeV); PDF",100,-15,15,100,0,1000);
	fitModelBkg->fillHistogram(ph2_bkg, RooArgList(pho1ClusterTime_SmearToData, MET));
	ph2_bkg->GetXaxis()->SetTitleOffset(2.0);
	ph2_bkg->GetXaxis()->SetRangeUser(-5,5);
	ph2_bkg->GetXaxis()->CenterTitle(kTRUE);
	ph2_bkg->GetYaxis()->SetTitleOffset(2.0);
	ph2_bkg->GetYaxis()->SetRangeUser(0,500);
	ph2_bkg->GetYaxis()->CenterTitle(kTRUE);
	ph2_bkg->GetZaxis()->SetTitleOffset(1.8);
	ph2_bkg->GetZaxis()->SetRangeUser(1e-8, 0.1);
	ph2_bkg->Draw("SURF1");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgonly_2D_pdf.pdf");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgonly_2D_pdf.png");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgonly_2D_pdf.C");

		
	TH2F * h2Data_toy = new TH2F("h2Data_toy","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events",100,-15,15,100,0,1000);
	data_toy->fillHistogram(h2Data_toy, RooArgList(pho1ClusterTime_SmearToData, MET));
	h2Data_toy->GetXaxis()->SetTitleOffset(2.0);
	h2Data_toy->GetXaxis()->SetRangeUser(-5,5);
	h2Data_toy->GetXaxis()->CenterTitle(kTRUE);
	h2Data_toy->GetYaxis()->SetTitleOffset(2.0);
	h2Data_toy->GetYaxis()->SetRangeUser(0,500);
	h2Data_toy->GetYaxis()->CenterTitle(kTRUE);
	h2Data_toy->GetZaxis()->SetTitleOffset(1.8);
	h2Data_toy->GetZaxis()->SetRangeUser(0, 1e3);
	h2Data_toy->Draw("LEGO2");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_toy_2D.pdf");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_toy_2D.png");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_toy_2D.C");

	h2Data->GetXaxis()->SetTitleOffset(2.0);
	h2Data->GetXaxis()->SetRangeUser(-10,15);
	h2Data->GetXaxis()->CenterTitle(kTRUE);
	h2Data->GetYaxis()->SetTitleOffset(2.0);
	h2Data->GetYaxis()->SetRangeUser(0.1,600);
	h2Data->GetYaxis()->CenterTitle(kTRUE);
	h2Data->GetZaxis()->SetTitleOffset(1.8);
	h2Data->GetZaxis()->SetRangeUser(0, 1e3);
	h2Data->Draw("LEGO2");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_2D_LEGO2.pdf");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_2D_LEGO2.png");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_2D_LEGO2.C");
	h2Data->GetYaxis()->SetTitleOffset(1.8);
	h2Data->GetXaxis()->SetTitleOffset(1.5);
	h2Data->Draw("COLZ");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_2D_COLZ.pdf");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_2D_COLZ.png");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_2D_COLZ.C");
	//h2Data->SetMarkerStyle(7);
	h2Data->Draw("");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_2D.pdf");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_2D.png");
	myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_data_2D.C");

	
	ws->import(*data);
	ws->import(*data_toy);
        ws->import(*rhGJets);
        ws->import(*rhQCD);
	ws->import(*rpSig);
	ws->import(*fitModelBkg);
	ws->import(nSig);
	ws->import(nBkg);
        //ws->import(*fitModelBkgSig);
        ws->import(*frame_pho1ClusterTime_SmearToData);
        ws->import(*frame_MET);
        ws->import(*frame_nBkg_LL);
        ws->import(*frame_nSig_LL);
        ws->import(*fres);
	
	//MakeDataCard(modelName, ws);
	
        return ws;
	
};



RooWorkspace* Fit1DMETTimeDataBkgSig( TH1F * h1Data, TH1F * h1GJets, TH1F * h1QCD,  TH1F * h1Sig, float lumi,float fracGJets, float fracQCD, TString modelName, TString modelTitle, bool useToy, TString outPlotsDir)
{
	RooWorkspace* ws = new RooWorkspace( "ws_combine", "ws_combine" );
	// define variables
	RooRealVar bin("bin","2D bin",0,h1Data->GetSize()-2,"");
	
	cout<<"DEBUG: bin size = "<<h1Data->GetSize()-2<<endl;

	double npoints = 1.0*h1Data->Integral();

	RooRealVar nGJets ("nGJets", "nGJets", fracGJets);
	nGJets.setConstant(kTRUE);
	RooRealVar nQCD ("nQCD", "nQCD", fracQCD);
	nQCD.setConstant(kTRUE);
	
	//RooDataHist
	RooDataHist* data = new RooDataHist("data", "data", RooArgSet(bin), h1Data);	
	RooDataHist* rhGJets = new RooDataHist("rhGJets", "rhGJets", RooArgSet(bin), h1GJets);	
	RooDataHist* rhQCD = new RooDataHist("rhQCD", "rhQCD", RooArgSet(bin), h1QCD);	
	RooDataHist* rhSig = new RooDataHist("rhSig", "rhSig", RooArgSet(bin), h1Sig);	

	//pdf
	RooHistPdf * rpGJets = new RooHistPdf("rpGJets", "rpGJets", RooArgSet(bin), *rhGJets, 0);
	RooHistPdf * rpQCD = new RooHistPdf("rpQCD", "rpQCD", RooArgSet(bin), *rhQCD, 0);
	RooHistPdf * rpSig = new RooHistPdf("rpSig", "rpSig", RooArgSet(bin), *rhSig, 0);
	
	RooAbsPdf * fitModelBkg = new RooAddPdf("fitModelBkg", "fitModelBkg", RooArgSet(*rpGJets, *rpQCD), RooArgSet(nGJets, nQCD));	

	//create toy data
	//TRandom3* r3 = new TRandom3(0);
	//double npoints = r3->PoissonD(h1Data->Integral());	
	//RooDataHist* data_toy = fitModelBkg->generateBinned(RooArgSet(bin), npoints, RooFit::ExpectedData());
	RooDataHist* data_toy = fitModelBkg->generateBinned(RooArgSet(bin), npoints);
	data_toy->SetName("data_toy");

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
       
	cout<<"DEBUG: fit 1D result === "<<endl; 
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
	frame_bin->SetTitle("");
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

	DrawCMS(myC, 13, lumi);

     	myC->SetTitle("");
        myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_bin.pdf");
        myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_bin.png");
        myC->SaveAs("fit_results/"+outPlotsDir+"/"+modelName+"_fit_bkgsig_bin.C");

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



void MakeDataCard(TString modelName, RooWorkspace *ws, float N_obs, float N_bkg, float N_sig, TString outDataCardsDir)
{
	std::string _modelName ((const char*) modelName);
	std::string _wsName ((const char*)ws->GetName());
	std::string _outDataCardsDir ((const char*) outDataCardsDir);
	
	FILE * m_outfile = fopen(("fit_results/"+_outDataCardsDir+"/DelayedPhotonCard_"+_modelName+".txt").c_str(), "w");
	cout<<"Writting fit result to datacard: "<<("fit_results/"+_outDataCardsDir+"/DelayedPhotonCard_"+_modelName+".txt").c_str()<<endl;
	fprintf(m_outfile, "imax 1\n");
	fprintf(m_outfile, "jmax 1\n");
	fprintf(m_outfile, "kmax *\n");
	fprintf(m_outfile, "---------------\n");
	fprintf(m_outfile, "shapes background bin1 fit_combineWS_%s.root %s:fitModelBkg %s:fitModelBkg_$SYSTEMATIC\n", _modelName.c_str(), _wsName.c_str(), _wsName.c_str());
	fprintf(m_outfile, "shapes signal bin1 fit_combineWS_%s.root %s:rpSig %s:rpSig_$SYSTEMATIC\n", _modelName.c_str(), _wsName.c_str(), _wsName.c_str());
	fprintf(m_outfile, "shapes data_obs bin1 fit_combineWS_%s.root %s:data_toy\n", _modelName.c_str(), _wsName.c_str());

	fprintf(m_outfile, "---------------\n");
	fprintf(m_outfile, "bin bin1\n");
	fprintf(m_outfile, "observation %6.2f\n", N_obs);
	fprintf(m_outfile, "------------------------------\n");
	fprintf(m_outfile, "bin             bin1       bin1\n");
	fprintf(m_outfile, "process         signal     background\n");
	fprintf(m_outfile, "process         0          1\n");
	fprintf(m_outfile, "rate            %10.6f          %6.2f\n", N_sig, N_bkg);
	fprintf(m_outfile, "--------------------------------\n");
	//fprintf(m_outfile, "lumi     lnN    1.057      1.057\n");
	fclose(m_outfile);	
};

void AddSystematics_Norm(TString modelName, float N_bkg, float N_sig, TString outDataCardsDir, TString sysName, TString distType)
{
        std::string _modelName ((const char*) modelName);
        std::string _sysName ((const char*) sysName);
        std::string _distType ((const char*) distType);
        std::string _outDataCardsDir ((const char*) outDataCardsDir);

        FILE * m_outfile = fopen(("fit_results/"+_outDataCardsDir+"/DelayedPhotonCard_"+_modelName+".txt").c_str(), "a");
	cout<<"Adding Systematic "<<sysName<<" to datacard: "<<("fit_results/"+_outDataCardsDir+"/DelayedPhotonCard_"+_modelName+".txt").c_str()<<endl;
	cout<<"N_bkg: "<<N_bkg<<"   N_sig:  "<<N_sig<<endl;
	if(N_sig > 0.001 && N_bkg > 0.001) fprintf(m_outfile, "%s   %s   %10.6f   %10.6f\n", _sysName.c_str(), _distType.c_str(), N_sig, N_bkg); // for both signal and backgrounds
	else if(N_sig > 0.001) fprintf(m_outfile, "%s   %s   %10.6f   -\n", _sysName.c_str(), _distType.c_str(), N_sig); //for signal only
	else if(N_bkg > 0.001) fprintf(m_outfile, "%s   %s   -      %10.6f\n", _sysName.c_str(), _distType.c_str(), N_bkg); //for background only
	fclose(m_outfile);	
}

void AddSystematics_shape(TString modelName, TString N_bkg, TString N_sig, TString outDataCardsDir, TString sysName, TString distType)
{
        std::string _modelName ((const char*) modelName);
        std::string _N_bkg ((const char*) N_bkg);
        std::string _N_sig ((const char*) N_sig);
        std::string _sysName ((const char*) sysName);
        std::string _distType ((const char*) distType);
        std::string _outDataCardsDir ((const char*) outDataCardsDir);

        FILE * m_outfile = fopen(("fit_results/"+_outDataCardsDir+"/DelayedPhotonCard_"+_modelName+".txt").c_str(), "a");
	cout<<"Adding Systematic "<<sysName<<" to datacard: "<<("fit_results/"+_outDataCardsDir+"/DelayedPhotonCard_"+_modelName+".txt").c_str()<<endl;
	cout<<"N_bkg: "<<N_bkg<<"   N_sig:  "<<N_sig<<endl;
	fprintf(m_outfile, "%s   %s   %s   %s\n", _sysName.c_str(), _distType.c_str(), _N_sig.c_str(), _N_bkg.c_str());
	fclose(m_outfile);	
}



void Fit1DMETTimeBiasTest( TH1F * h1Data, TH1F * h1Bkg,  TH1F * h1Sig, float SoverB, int ntoys, TString modelName, float lumi, TString outBiasDir)
{
	TString sSoverB = Form("%7.5f", SoverB);
	std::string _SoverB ((const char*) sSoverB);
	std::string _modelName ((const char*) modelName);		
	std::string _outBiasDir ((const char*) outBiasDir);
	TFile *f_Out_bias = new TFile(("fit_results/"+_outBiasDir+"/bias_"+_modelName+"_"+_SoverB+".root").c_str(),"recreate");
	
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
	
	TRandom3* r3 = new TRandom3(0);

	for(int ind_toy = 0; ind_toy<ntoys; ind_toy++)
	{
		double nBkg_true = r3->PoissonD(h1Data->Integral());	
		double nSig_true = r3->PoissonD(SoverB*h1Data->Integral());	

		double npoints = nBkg_true + nSig_true;

		RooRealVar nSig ("rpSig_yield", "rpSig_yield", nSig_true, 0.0, 1.5*npoints);
		nSig.setConstant(kFALSE);
		RooRealVar nBkg ("fitModelBkg_yield", "fitModelBkg_yield", nBkg_true, 0.0, 1.5*npoints);
		nBkg.setConstant(kFALSE);

		//RooHistPdf -> RooHistPdf
		RooHistPdf * rpSig = new RooHistPdf("rpSig", "rpSig", RooArgSet(bin), *rhSig, 0);
		RooHistPdf * rpBkg = new RooHistPdf("rpBkg", "rpBkg", RooArgSet(bin), *rhBkg, 0);
		
		RooAbsPdf * fitModelBkgSig = new RooAddPdf("fitModelBkgSig", "fitModelBkgSig", RooArgSet(*rpBkg, *rpSig), RooArgSet(nBkg, nSig));	

		//create toy data
		RooDataHist* data_toy = fitModelBkgSig->generateBinned(RooArgSet(bin), npoints);
		data_toy->SetName("data_toy");
		
		//fit
		RooAbsReal* nll = fitModelBkgSig->createNLL(*data_toy, RooFit::NumCPU(8)) ;
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

	//draw bias plot
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
        myC->SetTitle("");
	
	TH1F * histBias = new TH1F("hbias","hbias", 100, -15, 10);	
	outTree->Draw("-1.0*biasNorm>>hbias","status==0 && covStatus==3");
	
	histBias->SetTitle("");
        histBias->SetLineWidth(2);
        histBias->Draw();
        histBias->GetXaxis()->SetTitleSize( axisTitleSize );
        histBias->GetXaxis()->SetTitleOffset( axisTitleOffset );
        histBias->GetYaxis()->SetTitleSize( axisTitleSize );
        histBias->GetYaxis()->SetTitleOffset( axisTitleOffset );
        histBias->GetXaxis()->SetTitle("(N_{s}^{fit} - N_{s}^{true})/#sigma_{N_{s}}");
        histBias->GetYaxis()->SetTitle("events");
	DrawCMS(myC, 13, lumi);
	
	myC->SaveAs(("fit_results/"+_outBiasDir+"/bias_"+_modelName+"_"+_SoverB+"_plot.png").c_str());
	myC->SaveAs(("fit_results/"+_outBiasDir+"/bias_"+_modelName+"_"+_SoverB+"_plot.pdf").c_str());
	myC->SaveAs(("fit_results/"+_outBiasDir+"/bias_"+_modelName+"_"+_SoverB+"_plot.C").c_str());

};

double CalculateMETTimeSignificance(TH1F * h1Bkg,  TH1F * h1Sig)
{
	int nsteps = 2e3;
  	double mu_steps = 1.0e-2;
  	double minNll = 9999999;
	double bestMu = -1.0;	
	
	for(int i = 0; i < nsteps; i++)
	{
		double mu = mu_steps*i;
      		double nll = 0;
		for(int j=1; j<=h1Bkg->GetSize()-2;j++)
		{
			double s = h1Sig->GetBinContent(j);
			double b = h1Bkg->GetBinContent(j);
			nll += - ( (s+b)*std::log(mu*s+b)  - (mu*s+b));	
		}
		if(nll < minNll)
		{
			minNll = nll;
			bestMu = mu;
		}	
	}
		
	double qnot = 0.0;
	double qnot2 = 0.0;

	for(int j=1; j<=h1Bkg->GetSize()-2;j++)
        {
		double s = h1Sig->GetBinContent(j);
                double b = h1Bkg->GetBinContent(j);
		qnot2 += 2.0* ( (s+b) * std::log (1.0 + bestMu*s/b) - bestMu*s);
	}	
	
	if(qnot2 > 0.0) qnot = sqrt(qnot2);
	
	return qnot;	

};
double Fit1DMETTimeSignificance(TH1F *h1Data, TH1F * h1Bkg,  TH1F * h1Sig, int ntoys)
{

	RooMsgService::instance().setSilentMode(true);

	RooRandom::randomGenerator()->SetSeed( 0 );
	
	RooRealVar bin("bin","2D bin",0,h1Bkg->GetSize()-2,"");
	RooDataHist* rhData = new RooDataHist("rhData", "rhData", RooArgSet(bin), h1Data);	
	RooDataHist* rhBkg = new RooDataHist("rhBkg", "rhBkg", RooArgSet(bin), h1Bkg);	
	RooDataHist* rhSig = new RooDataHist("rhSig", "rhSig", RooArgSet(bin), h1Sig);	
		
	TRandom3* r3 = new TRandom3(0);

	double sumQnot = 0.0;
	double maxQnot = -9999.0;
	double minQnot = 9999.0;
	int nGoodTry = 0 ;
	int nTrys = 5;

  	double _Ns_fit, _Nbkg_fit;

	for(int ind_Try = 0; (ind_Try< 10*nTrys) && (nGoodTry < nTrys); ind_Try++)
	{
		double nBkg_hist = h1Bkg->Integral();//r3->PoissonD(h1Bkg->Integral());	
		//double nSig_hist = r3->PoissonD(h1Sig->Integral());	
		double nSig_hist = h1Sig->Integral();
		double npoints = h1Data->Integral();
		double frac_Sig = nSig_hist/(nSig_hist+nBkg_hist);
		double frac_Bkg = nBkg_hist/(nSig_hist+nBkg_hist);
	
		double nSig_exp = npoints*frac_Sig;	
		double nBkg_exp = npoints*frac_Bkg;	

		RooRealVar nSig ("rpSig_yield", "rpSig_yield", nSig_exp, 0.0, 1.5*npoints);
		nSig.setConstant(kFALSE);
		RooRealVar nBkg ("fitModelBkg_yield", "fitModelBkg_yield", nBkg_exp, 0.0, 1.5*npoints);
		nBkg.setConstant(kFALSE);

		//RooHistPdf -> RooHistPdf
		RooHistPdf * rpSig = new RooHistPdf("rpSig", "rpSig", RooArgSet(bin), *rhSig, 0);
		RooHistPdf * rpBkg = new RooHistPdf("rpBkg", "rpBkg", RooArgSet(bin), *rhBkg, 0);
		
		RooAbsPdf * fitModelBkgSig = new RooAddPdf("fitModelBkgSig", "fitModelBkgSig", RooArgSet(*rpBkg, *rpSig), RooArgSet(nBkg, nSig));	

		//create toy data
		//RooDataHist* data_toy = fitModelBkgSig->generateBinned(RooArgSet(bin), npoints);
		//data_toy->SetName("data_toy");
		
		//fit
		RooAbsReal* nll = fitModelBkgSig->createNLL(*rhData, RooFit::NumCPU(8)) ;
		RooFitResult * fres;
		fres = fitModelBkgSig->fitTo( *rhData, RooFit::Extended( kTRUE ), RooFit::Save( kTRUE ));

		if(fres->status() == 0)
		{		
			_Ns_fit = nSig.getVal();
			_Nbkg_fit = nBkg.getVal();	
			if( _Nbkg_fit > 0.0 && _Ns_fit < 3.0*nSig_exp)
			{
				double qnot2 =  2.0*( (_Ns_fit + _Nbkg_fit) * std::log (1.0 + _Ns_fit/_Nbkg_fit) - _Ns_fit);
				double qnot =  0.0;
				if(qnot2 < 0.0) continue;
				//if(qnot2<1e-8) qnot = 1e-4*sqrt(1e8 * qnot);
				else qnot = sqrt(qnot2);
				cout<<"DEBUG calculate significance: Ns (Ns_exp) = "<<_Ns_fit<<" ( "<<nSig_exp<<" )  Nb (Nb_exp) = "<<_Nbkg_fit<<" ( "<<nBkg_exp<<" ) qnot = "<<qnot<<" qnot2 = "<<qnot2<<endl;
				nGoodTry ++;
				sumQnot += qnot;		
				if(qnot > maxQnot) maxQnot = qnot;
				if(qnot < minQnot) minQnot = qnot;
			}
		}
		
      		delete nll;	
	}

	if(nGoodTry > 2) return (sumQnot - maxQnot - minQnot)/(nGoodTry-2);
	else return 0.0;

};

void OptimizeBinning(std::vector<int> &timeBin, std::vector<int> &metBin, TH2F * h2Bkg, TH2F *h2Sig, float time_Low, float time_High, int time_N_fine, float met_Low, float met_High, int met_N_fine, TString modelName, TString ourBinningDir)
{

	std::string _modelName ((const char*) modelName);
	std::string _outBinningDir ((const char*) ourBinningDir);
        //TFile *f_Out_binning = new TFile(("fit_results/binning/binning_"+_modelName+".root").c_str(),"recreate");

	bool debug_thisFunc = true;
	//initial status: 1 bin in time, and 1 bin in MET
	int nTotal_time = h2Bkg->GetNbinsX();
	int nTotal_met = h2Bkg->GetNbinsY();

	cout<<" binning optimization... "<<endl;	
	cout<<"time bins # "<<nTotal_time<<endl;
	cout<<"met bins # "<<nTotal_met<<endl;

	double maxSignificance = -9999.0;
	bool isConverged_time = false;
	bool isConverged_met = false;
	bool isConverged_all = false;
	
	/*************generate toy data**************/
	TH2F * h2Data = new TH2F("h2Data","h2Data", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH1F * h1ConvertData = new TH1F("h1ConvertData","h1ConvertData", time_N_fine*met_N_fine, 0, time_N_fine*met_N_fine);
	TH1 * h1ConvertData_toy = new TH1F("h1ConvertData_toy","h1ConvertData_toy", time_N_fine*met_N_fine, 0, time_N_fine*met_N_fine);
	//2D to 1D convert
	for(int i=1;i<=time_N_fine;i++)
	{
		for(int j=1;j<=met_N_fine;j++)
		{
			int thisBin = (i-1)*met_N_fine + j;
			h1ConvertData->SetBinContent(thisBin, h2Bkg->GetBinContent(i,j) + h2Sig->GetBinContent(i,j));
		}
	}		
	if(debug_thisFunc) cout<<"binning optimization: 2D data to 1D data conversion : "<<h2Bkg->Integral()+h2Sig->Integral()<<" -> "<<h1ConvertData->Integral()<<endl;
	//toy generation
	RooRealVar bin("bin","2D bin",0,h1ConvertData->GetSize()-2,"");
	RooDataHist* rhData = new RooDataHist("rhData", "rhData", RooArgSet(bin), h1ConvertData);	
	RooHistPdf * rpData = new RooHistPdf("rpData", "rpData", RooArgSet(bin), *rhData, 0);
		
	//create toy data
	TRandom3* r3 = new TRandom3(0);
	double nData_toy = r3->PoissonD(h1ConvertData->Integral());	
	
	RooDataHist* data_toy = rpData->generateBinned(RooArgSet(bin), nData_toy);
	data_toy->SetName("data_toy");

	h1ConvertData_toy = data_toy->createHistogram("bin", time_N_fine*met_N_fine);	
	
	if(debug_thisFunc) cout<<"binning optimization: 1D data vs toy data : "<<h1ConvertData->Integral()<<"  ->  "<<h1ConvertData_toy->Integral()<<endl;

	//1D to 2D convert
	for(int i=1;i<=time_N_fine;i++)
	{
		for(int j=1;j<=met_N_fine;j++)
		{
			int thisBin = (i-1)*met_N_fine + j;
			h2Data->SetBinContent(i, j, h1ConvertData_toy->GetBinContent(thisBin));
		}
	}		
	/*************end of toy data****************/
	
	//while( (!isConverged_time) || (!isConverged_met))
	
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
	myC->SetTitle("");

	int iteration = 0;
	while( !isConverged_all )
	{
		//start spliting in time dimension
		int new_idx_time = -99;
		int new_idx_met = -99;
		
		if(!isConverged_time)
		{
			TString s_hist_name = Form("_h1_qnot_time_iter_%d", iteration);
        		std::string _s_hist_name2 ((const char*) s_hist_name);
			std::string _s_hist_name = _modelName+_s_hist_name2;
			TH1F * h1_qnot_time = new TH1F(_s_hist_name.c_str(), _s_hist_name.c_str(), time_N_fine, time_Low, time_High);
			for(int idx=1;idx<nTotal_time;idx++)
			{
				double this_time = time_Low + (time_High - time_Low) * (1.0*idx)/(1.0*time_N_fine);
				if(this_time < -5.0) continue;//no further binning below -5 ns
				//if(std::find(timeBin.begin(), timeBin.end(), idx) != timeBin.end()) continue; // add a new split
				
				int dist_min = 9999;
				for(int i=0;i<timeBin.size();i++)
				{
					if(abs(timeBin[i] - idx) < dist_min) dist_min = abs(timeBin[i] - idx);
				}
				if(dist_min < 5) continue; // not too narrow binning

				std::vector <int> temp_bin_time;
				for(int idx_temp : timeBin) 
				{
					temp_bin_time.push_back(idx_temp);
				}
				temp_bin_time.push_back(idx);
				std::sort(temp_bin_time.begin(), temp_bin_time.end());
				if(debug_thisFunc) cout<<"DEBUG binningOptimization time: tring to add split at idx = "<<idx<<endl;
				for(int inx_temp : temp_bin_time)
				{
					cout<<inx_temp<<" , ";
				}
				cout<<endl;
				
				//construct 1D histogram of time and met
				TH1F *h1Data = new TH1F ("h1Data","h1Data", (temp_bin_time.size()-1)*(metBin.size()-1), 0, (temp_bin_time.size()-1)*(metBin.size()-1)*1.0);
				TH1F *h1Bkg = new TH1F ("h1Bkg","h1Bkg", (temp_bin_time.size()-1)*(metBin.size()-1), 0, (temp_bin_time.size()-1)*(metBin.size()-1)*1.0);
				TH1F *h1Sig = new TH1F ("h1Sig","h1Sig", (temp_bin_time.size()-1)*(metBin.size()-1), 0, (temp_bin_time.size()-1)*(metBin.size()-1)*1.0);
				for(int iT=1;iT<= temp_bin_time.size()-1; iT++)
				{
					for(int iM=1;iM<= metBin.size()-1; iM++)
					{
						int thisBin = (iT-1)*(metBin.size()-1) + iM;
						float NData = h2Data->Integral(temp_bin_time[iT-1]+1, temp_bin_time[iT], metBin[iM-1]+1, metBin[iM]);
						float NBkg = h2Bkg->Integral(temp_bin_time[iT-1]+1, temp_bin_time[iT], metBin[iM-1]+1, metBin[iM]);
						float NSig = h2Sig->Integral(temp_bin_time[iT-1]+1, temp_bin_time[iT], metBin[iM-1]+1, metBin[iM]);
						h1Data->SetBinContent(thisBin, NData);
						h1Bkg->SetBinContent(thisBin, NBkg);
						h1Sig->SetBinContent(thisBin, NSig);
						//cout<<"iT = "<<iT<<"  iM = "<<iM<<" thiBin = "<<thisBin<<"  NBkg = "<<NBkg<<"   NSig = "<<NSig<<endl;
					}	
				}
				
				if(debug_thisFunc) cout<<"DEBUG binningOptimization time: validation of 2D conversion (Bkg): "<<h2Bkg->Integral()<<" -> "<<h1Bkg->Integral()<<endl;
				if(debug_thisFunc) cout<<"DEBUG binningOptimization time: validation of 2D conversion (Sig): "<<h2Sig->Integral()<<" -> "<<h1Sig->Integral()<<endl;
	
				for(int i=1;i<= (temp_bin_time.size()-1)*(metBin.size()-1); i++)
				{
					if(h1Bkg->GetBinContent(i) < 1e-3 ) h1Bkg->SetBinContent(i, 1e-3);
					if(h1Sig->GetBinContent(i) < 1e-3 ) h1Sig->SetBinContent(i, 1e-3);
					//h1Data->SetBinContent(i, h1Bkg->GetBinContent(i) + h1Sig->GetBinContent(i));
				}
	
				//double qnot = Fit1DMETTimeSignificance(h1Data, h1Bkg, h1Sig, 10);
				double qnot = CalculateMETTimeSignificance(h1Bkg, h1Sig);
			
				if(debug_thisFunc) cout<<"DEBUG binningOptimization time: significance of new split = "<<qnot<<" vs. maxSignificance = "<<maxSignificance<<endl;	
				if(qnot > 1.000*maxSignificance)	
				{
					maxSignificance = qnot;
					new_idx_time = idx; 
				}
				if(qnot>0.001) h1_qnot_time->SetBinContent(idx, qnot);	

				delete 	h1Data;
				delete 	h1Bkg;
				delete 	h1Sig;
			}

			h1_qnot_time->SetLineWidth(2);
        		h1_qnot_time->SetLineColor(kBlack);
                        h1_qnot_time->SetTitle("");
        		h1_qnot_time->GetXaxis()->SetTitle("new split on #gamma cluster time [ns]");
        		h1_qnot_time->GetYaxis()->SetTitle("q_{0}");
        		h1_qnot_time->GetYaxis()->SetTitleSize(axisTitleSize);
        		h1_qnot_time->GetYaxis()->SetRangeUser(0.15, 1.2*h1_qnot_time->GetMaximum());
        		h1_qnot_time->GetXaxis()->SetRangeUser(0.2+time_Low, time_High-0.2);
        		h1_qnot_time->GetXaxis()->SetTitleSize(axisTitleSize);
        		h1_qnot_time->GetYaxis()->SetTitleOffset(axisTitleOffset);
        		h1_qnot_time->GetXaxis()->SetTitleOffset(axisTitleOffset);
			h1_qnot_time->Draw();
			for(int ih=0;ih<timeBin.size();ih++)
			{
				TString s_ih_name = Form("h1_qnot_time_iter_%d_i%d", iteration, ih);
                        	std::string _s_ih_name ((const char*) s_ih_name);
	
				TH1F *h1_temp = new TH1F(_s_ih_name.c_str(), _s_ih_name.c_str(), time_N_fine, time_Low, time_High);
				h1_temp->SetBinContent(timeBin[ih], 1.2*h1_qnot_time->GetMaximum());
				h1_temp->SetLineWidth(3);
				h1_temp->SetLineColor(kRed);
				h1_temp->Draw("same");
			}

			if(new_idx_time > 0)
			{
	
				myC->SaveAs(("fit_results/"+_outBinningDir+"/binning_"+_s_hist_name+".pdf").c_str());
				myC->SaveAs(("fit_results/"+_outBinningDir+"/binning_"+_s_hist_name+".png").c_str());
				myC->SaveAs(("fit_results/"+_outBinningDir+"/binning_"+_s_hist_name+".C").c_str());

	
				if(debug_thisFunc) cout<<"best split point added : "<<new_idx_time<<"  maxSignificance = "<<maxSignificance<<endl;
				timeBin.push_back(new_idx_time);
				std::sort(timeBin.begin(), timeBin.end());	
			}
			else isConverged_time = true;	
			
		}


		if(!isConverged_met)
		{
			TString s_hist_name = Form("_h1_qnot_met_iter_%d", iteration);
        		std::string _s_hist_name2 ((const char*) s_hist_name);
			std::string _s_hist_name = _modelName + _s_hist_name2;
			
			TH1F * h1_qnot_met = new TH1F(_s_hist_name.c_str(), _s_hist_name.c_str(), met_N_fine, met_Low, met_High);

			for(int idx=1;idx<nTotal_met;idx++)
			{
				//if(std::find(metBin.begin(), metBin.end(), idx) != metBin.end()) continue; // add a new split
				double this_met = met_Low + (met_High - met_Low) * (1.0*idx)/(1.0*met_N_fine);
				if(this_met < 50.0) continue;//no further binning below MET 50
			
				int dist_min = 9999;
				for(int i=0;i<metBin.size();i++)
				{
					if(abs(metBin[i] - idx) < dist_min) dist_min = abs(metBin[i] - idx);
				}
				if(dist_min < 5) continue; // not too narrow binning


				std::vector <int> temp_bin_met;
				for(int idx_temp : metBin) 
				{
					temp_bin_met.push_back(idx_temp);
				}
				temp_bin_met.push_back(idx);
				std::sort(temp_bin_met.begin(), temp_bin_met.end());
				if(debug_thisFunc) cout<<"DEBUG binningOptimization met: tring to add split at idx = "<<idx<<endl;
				for(int inx_temp : temp_bin_met)
				{
					cout<<inx_temp<<" , ";
				}
				cout<<endl;
				
				//construct 1D histogram of met and time
				TH1F *h1Data = new TH1F ("h1Data","h1Data", (temp_bin_met.size()-1)*(timeBin.size()-1), 0, (temp_bin_met.size()-1)*(timeBin.size()-1)*1.0);
				TH1F *h1Bkg = new TH1F ("h1Bkg","h1Bkg", (temp_bin_met.size()-1)*(timeBin.size()-1), 0, (temp_bin_met.size()-1)*(timeBin.size()-1)*1.0);
				TH1F *h1Sig = new TH1F ("h1Sig","h1Sig", (temp_bin_met.size()-1)*(timeBin.size()-1), 0, (temp_bin_met.size()-1)*(timeBin.size()-1)*1.0);
				for(int iT=1;iT<= timeBin.size()-1; iT++)
				{
					for(int iM=1;iM<= temp_bin_met.size()-1; iM++)
					{
						int thisBin = (iT-1)*(temp_bin_met.size()-1) + iM;
						float NData = h2Data->Integral(timeBin[iT-1]+1, timeBin[iT], temp_bin_met[iM-1]+1, temp_bin_met[iM]);
						float NBkg = h2Bkg->Integral(timeBin[iT-1]+1, timeBin[iT], temp_bin_met[iM-1]+1, temp_bin_met[iM]);
						float NSig = h2Sig->Integral(timeBin[iT-1]+1, timeBin[iT], temp_bin_met[iM-1]+1, temp_bin_met[iM]);
						h1Data->SetBinContent(thisBin, NData);
						h1Bkg->SetBinContent(thisBin, NBkg);
						h1Sig->SetBinContent(thisBin, NSig);
						//cout<<"iT = "<<iT<<"  iM = "<<iM<<" thiBin = "<<thisBin<<"  NBkg = "<<NBkg<<"   NSig = "<<NSig<<endl;
					}	
				}
				
				if(debug_thisFunc) cout<<"DEBUG binningOptimization met: validation of 2D conversion (Bkg): "<<h2Bkg->Integral()<<" -> "<<h1Bkg->Integral()<<endl;
				if(debug_thisFunc) cout<<"DEBUG binningOptimization met: validation of 2D conversion (Sig): "<<h2Sig->Integral()<<" -> "<<h1Sig->Integral()<<endl;
	
				for(int i=1;i<= (temp_bin_met.size()-1)*(timeBin.size()-1); i++)
				{
					if(h1Bkg->GetBinContent(i) < 1e-3 ) h1Bkg->SetBinContent(i, 1e-3);
					if(h1Sig->GetBinContent(i) < 1e-3 ) h1Sig->SetBinContent(i, 1e-3);
					//h1Data->SetBinContent(i, h1Bkg->GetBinContent(i) + h1Sig->GetBinContent(i));
				}
	
				//double qnot = Fit1DMETTimeSignificance(h1Data, h1Bkg, h1Sig, 10);
				double qnot = CalculateMETTimeSignificance(h1Bkg, h1Sig);
			
				if(debug_thisFunc) cout<<"DEBUG binningOptimization met: significance of new split = "<<qnot<<" vs. maxSignificance = "<<maxSignificance<<endl;	
				if(qnot > 1.000*maxSignificance)	
				{
					maxSignificance = qnot;
					new_idx_met = idx; 
				}
				h1_qnot_met->SetBinContent(idx, qnot);
	
				delete 	h1Data;
				delete 	h1Bkg;
				delete 	h1Sig;
			}
			
			h1_qnot_met->SetLineWidth(2);
                        h1_qnot_met->SetLineColor(kBlack);
                        h1_qnot_met->SetTitle("");
                        h1_qnot_met->GetXaxis()->SetTitle("new split on #slash{E}_{T} [GeV]");
                        h1_qnot_met->GetYaxis()->SetTitle("q_{0}");
                        h1_qnot_met->GetYaxis()->SetTitleSize(axisTitleSize);
        		h1_qnot_met->GetYaxis()->SetRangeUser(0.15, 1.2*h1_qnot_met->GetMaximum());
        		h1_qnot_met->GetXaxis()->SetRangeUser(10.0+met_Low, met_High-10.0);
                        h1_qnot_met->GetXaxis()->SetTitleSize(axisTitleSize);
                        h1_qnot_met->GetYaxis()->SetTitleOffset(axisTitleOffset);
                        h1_qnot_met->GetXaxis()->SetTitleOffset(axisTitleOffset);
                        h1_qnot_met->Draw();

			for(int ih=0;ih<metBin.size();ih++)
			{
				TString s_ih_name = Form("h1_qnot_met_iter_%d_i%d", iteration, ih);
                        	std::string _s_ih_name ((const char*) s_ih_name);
	
				TH1F *h1_temp = new TH1F(_s_ih_name.c_str(), _s_ih_name.c_str(), met_N_fine, met_Low, met_High);
				h1_temp->SetBinContent(metBin[ih], 1.2*h1_qnot_met->GetMaximum());
				h1_temp->SetLineWidth(3);
				h1_temp->SetLineColor(kRed);
				h1_temp->Draw("same");
			}

			if(new_idx_met > 0)
			{

       	                 	myC->SaveAs(("fit_results/"+_outBinningDir+"/binning_"+_s_hist_name+".pdf").c_str());
       	                 	myC->SaveAs(("fit_results/"+_outBinningDir+"/binning_"+_s_hist_name+".png").c_str());
       	                 	myC->SaveAs(("fit_results/"+_outBinningDir+"/binning_"+_s_hist_name+".C").c_str());

				if(debug_thisFunc) cout<<"best split point added met : "<<new_idx_met<<"  maxSignificance = "<<maxSignificance<<endl;
				metBin.push_back(new_idx_met);
				std::sort(metBin.begin(), metBin.end());	
			}
			else isConverged_met = true;	

		}
		
		if(isConverged_time && isConverged_met) isConverged_all = true;
		else if(metBin.size()>10 || timeBin.size()>10)  
		{
			if(metBin.size()>10) isConverged_met = true;
			if(timeBin.size()>10) isConverged_time = true;
			isConverged_all = (isConverged_met && isConverged_time);
		}
		else
		{
			isConverged_time = false;
			isConverged_met = false;
			isConverged_all = false;
		}
	
		iteration ++;
	}

};

