//C++ INCLUDES
#include <iostream>
#include <sys/stat.h>
#include <vector>
//ROOT INCLUDES
#include <TFile.h>
#include <TTree.h>
#include <TMath.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TROOT.h>
#include <THStack.h>
#include <TStyle.h>
#include <TColor.h>
//LOCAL INCLUDES
#include "MakeFitMETTime.hh"
#include "Aux.hh"

using namespace std;

Int_t Nbins_MET = 15;
Int_t Nbins_MET_lowT = 6;
Int_t Nbins_MET_highT = 5;
Int_t Nbins_time = 20;
Int_t Nbins_time_lowT = 5;
Int_t Nbins_time_highT = 7;
Int_t Nbins_total = Nbins_MET*Nbins_time;
Double_t xbins_MET[16] = {0.0, 10.0, 20.0, 40.0, 60.0, 80, 100.0, 125.0, 150.0, 175.0, 200.0, 250.0, 300.0, 400.0, 500.0, 1000.0};
Double_t xbins_MET_lowT[7] = {0.0, 70, 130, 225.0, 295.0, 320.0, 1000.0};
Double_t xbins_MET_highT[6] = {0.0, 55.0, 85.0, 185.0, 500.0, 1000.0};
Double_t xbins_time[21] = {-15, -10, -5, -4, -3, -2.5, -2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3, 4, 5, 10, 15};
Double_t xbins_time_lowT[6] = {-15.0, -0.7, 0.3, 0.8, 1.4, 15.0};
Double_t xbins_time_highT[8] = {-15.0, -0.7, 0.0, 0.9, 1.6, 2.1, 10.0, 15.0};

bool useLowTBinning = false;

float lumi = 31336.5; //pb^-1
float NEvents_sig = 1.0;
bool _useToy = true;

bool doAllBkgFracFit = false;

int main( int argc, char* argv[])
{
srand(time(NULL));
gROOT->Reset();
gROOT->SetBatch(1);
gStyle->SetOptStat(0);
gStyle->SetOptFit(111);
gStyle->SetPalette(1);

std::string inputFileName_data = argv[1];
std::string inputFileName_signal = argv[2];
std::string sigModelName = argv[3]; 
std::string sigModelTitle = argv[4]; 
std::string fitMode = argv[5]; //options: "datacard", "bias"
std::string _SoverB = "";
std::string _nToys = "";

if(fitMode == "bias" && argc >= 7) _SoverB = argv[6]; 
if(fitMode == "bias" && argc >= 8) _nToys = argv[7]; 

float SoverB = 0.0;
int nToys = 1000;

if (sigModelName.find("0p") != std::string::npos || sigModelName.find("10cm") != std::string::npos) useLowTBinning = true;

if(useLowTBinning)
{
	Nbins_MET = Nbins_MET_lowT;
	Nbins_time = Nbins_time_lowT;
	Nbins_total = Nbins_MET_lowT*Nbins_time_lowT;
}
else
{
	Nbins_MET = Nbins_MET_highT;
	Nbins_time = Nbins_time_highT;
	Nbins_total = Nbins_MET_highT*Nbins_time_highT;
}

TString _sigModelName (sigModelName.c_str());
TString _sigModelTitle (sigModelTitle.c_str());

float xsec = getXsecBR(sigModelName); //pb
std::string treeName = "DelayedPhoton";

std::string cut = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2"; 
std::string cut_noHLT = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && n_Photons == 2"; 
std::string cut_iso = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2 && pho1sumChargedHadronPt < 1.30 && pho1sumNeutralHadronEt < 0.26 && pho1sumPhotonEt < 2.36";
std::string cut_loose = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.7 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2";
std::string cut_GJets = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (jet2Pt/pho1Pt > 0.2) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)";


if(inputFileName_data == "")
{
	std::cerr << "[ERROR]: please provide an input file for data" << std::endl;
	return -1;
}
std::cout<<"using input file for data: "<<inputFileName_data<<std::endl;

if(inputFileName_signal == "")
{
	std::cerr << "[ERROR]: please provide an input file for signal" << std::endl;
	return -1;
}

if(sigModelName == "")
{
	std::cerr << "[ERROR]: please provide the name of the signal model" << std::endl;
	return -1;
}

if(sigModelTitle == "")
{
	std::cerr << "[ERROR]: please provide the title of the signal model" << std::endl;
	return -1;
}

if(fitMode == "")
{
	std::cerr << "[ERROR]: please provide the fit mode (datacard or bias)" << std::endl;
	return -1;
}

std::cout<<"using input file for data: "<<inputFileName_data<<std::endl;
std::cout<<"using input file for signal: "<<inputFileName_signal<<std::endl;
std::cout<<"signal model: "<<sigModelName<<std::endl;
std::cout<<"signal title: "<<sigModelTitle<<std::endl;
std::cout<<"fit mode: "<<fitMode<<std::endl;

if(fitMode == "bias")
{
	if(_SoverB == "")
	{
		cout<<" bias test: SoverB not specified, setting to default: 0"<<endl;
	}
	else
	{
		SoverB = strtof(_SoverB.c_str(), 0);
		cout<<"bias test: SoverB ="<<SoverB<<endl;
	}

	if(_nToys == "")
	{
		cout<<" bias test: nToys not specified, setting to default: 1000"<<endl;
	}
	else
	{
		nToys = stoi(_nToys.c_str(), 0);
		cout<<"bias test: nToys ="<<nToys<<endl;
	}

}

std::cout<<"signal xsec*BR = "<<xsec<<endl;

TFile *file_data;
TFile *file_signal;

TTree *tree_data;
TTree *tree_signal;

file_data = new TFile(inputFileName_data.c_str(), "READ");
tree_data = (TTree*)file_data->Get(treeName.c_str());

file_signal = new TFile(inputFileName_signal.c_str(), "READ");
tree_signal = (TTree*)file_signal->Get(treeName.c_str());

TH1F *h1_NEvents_sig = (TH1F*) file_signal->Get("NEvents");
NEvents_sig = h1_NEvents_sig->GetBinContent(1);

TFile *file_shape = new TFile("data/shapes.root","READ");

mkdir("fit_results", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/plots", S_IRWXU | S_IRWXG | S_IRWXO);

TFile *f_Out = new TFile(("fit_results/plots/fit_ws_"+sigModelName+".root").c_str(),"recreate");

int N_obs_total = tree_data->CopyTree( cut.c_str() )->GetEntries();
float N_total_GJets_QCD_fit = 0.0;

/**********fit to get relative yield of GJets and QCD backgrounds *****/
//SigmaIetaIeta
TH1F *h1_SigmaIetaIeta_Data = new TH1F("h1_SigmaIetaIeta_Data","h1_SigmaIetaIeta_Data", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_Data", cut.c_str());

TH1F *h1_SigmaIetaIeta_GJets = (TH1F*)file_shape->Get("phoSigmaIetaIeta_histGJets"); 
TH1F *h1_SigmaIetaIeta_QCD = (TH1F*)file_shape->Get("phoSigmaIetaIeta_histQCD"); 

h1_SigmaIetaIeta_GJets->Scale((1.0*h1_SigmaIetaIeta_Data->Integral())/h1_SigmaIetaIeta_GJets->Integral());
h1_SigmaIetaIeta_QCD->Scale((1.0*h1_SigmaIetaIeta_Data->Integral())/h1_SigmaIetaIeta_QCD->Integral());

RooWorkspace * w_frac_SigmaIetaIeta;
w_frac_SigmaIetaIeta = FitDataBkgFraction(h1_SigmaIetaIeta_Data, "pho1SigmaIetaIeta", "#sigma_{i#etai#eta}", "", 0.005, 0.025, h1_SigmaIetaIeta_GJets, h1_SigmaIetaIeta_QCD);
w_frac_SigmaIetaIeta->Write("w_frac_SigmaIetaIeta");

float nGJets_value_SigmaIetaIeta = w_frac_SigmaIetaIeta->var("nGJets")->getValV();
float nGJets_value_SigmaIetaIeta_err = w_frac_SigmaIetaIeta->var("nGJets")->getError();
float nQCD_value_SigmaIetaIeta = w_frac_SigmaIetaIeta->var("nQCD")->getValV();
float nQCD_value_SigmaIetaIeta_err = w_frac_SigmaIetaIeta->var("nQCD")->getError();
h1_SigmaIetaIeta_GJets->Scale(nGJets_value_SigmaIetaIeta);
h1_SigmaIetaIeta_QCD->Scale(nQCD_value_SigmaIetaIeta);
h1_SigmaIetaIeta_GJets->Write();
h1_SigmaIetaIeta_QCD->Write();

N_total_GJets_QCD_fit = nGJets_value_SigmaIetaIeta + nQCD_value_SigmaIetaIeta;

cout<<"result of fit with SigmaIetaIeta: " <<endl;
cout<<"fraction of GJets = "<<nGJets_value_SigmaIetaIeta<<" +/- "<<nGJets_value_SigmaIetaIeta_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_SigmaIetaIeta/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_SigmaIetaIeta_err/N_total_GJets_QCD_fit<<endl;
cout<<"fraction of QCD = "<<nQCD_value_SigmaIetaIeta<<" +/- "<<nQCD_value_SigmaIetaIeta_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_SigmaIetaIeta/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_SigmaIetaIeta_err/N_total_GJets_QCD_fit<<endl;

if(doAllBkgFracFit)
{
	//sumChargedHadronPt
	TH1F *h1_sumChargedHadronPt_Data = new TH1F("h1_sumChargedHadronPt_Data","h1_sumChargedHadronPt_Data", 100, -0.1, 1.30);
	tree_data->Draw("pho1sumChargedHadronPt>>h1_sumChargedHadronPt_Data", cut_iso.c_str());

	TH1F *h1_sumChargedHadronPt_GJets = (TH1F*)file_shape->Get("phosumChargedHadronPt_histGJets"); 
	TH1F *h1_sumChargedHadronPt_QCD = (TH1F*)file_shape->Get("phosumChargedHadronPt_histQCD"); 

	float tightFraction_Data = (1.0*h1_sumChargedHadronPt_Data->Integral(1,15))/(h1_sumChargedHadronPt_Data->Integral()*1.0);
	float tightFraction_GJets = (1.0*h1_sumChargedHadronPt_GJets->Integral(1,15))/(h1_sumChargedHadronPt_GJets->Integral()*1.0);
	float tightFraction_QCD = (1.0*h1_sumChargedHadronPt_QCD->Integral(1,15))/(h1_sumChargedHadronPt_QCD->Integral()*1.0);

	h1_sumChargedHadronPt_GJets->Scale((1.0*h1_sumChargedHadronPt_Data->Integral())/h1_sumChargedHadronPt_GJets->Integral());
	h1_sumChargedHadronPt_QCD->Scale((1.0*h1_sumChargedHadronPt_Data->Integral())/h1_sumChargedHadronPt_QCD->Integral());

	RooWorkspace * w_frac_sumChargedHadronPt;
	w_frac_sumChargedHadronPt = FitDataBkgFraction(h1_sumChargedHadronPt_Data, "pho1sumChargedHadronPt", "charged isolation", "GeV", -0.1, 1.30, h1_sumChargedHadronPt_GJets, h1_sumChargedHadronPt_QCD);
	w_frac_sumChargedHadronPt->Write("w_frac_sumChargedHadronPt");

	float nGJets_value_sumChargedHadronPt = w_frac_sumChargedHadronPt->var("nGJets")->getValV();
	float nGJets_value_sumChargedHadronPt_err = w_frac_sumChargedHadronPt->var("nGJets")->getError();
	float nQCD_value_sumChargedHadronPt = w_frac_sumChargedHadronPt->var("nQCD")->getValV();
	float nQCD_value_sumChargedHadronPt_err = w_frac_sumChargedHadronPt->var("nQCD")->getError();
	h1_sumChargedHadronPt_GJets->Scale(nGJets_value_sumChargedHadronPt);
	h1_sumChargedHadronPt_QCD->Scale(nQCD_value_sumChargedHadronPt);
	h1_sumChargedHadronPt_GJets->Write();
	h1_sumChargedHadronPt_QCD->Write();

	N_total_GJets_QCD_fit = nGJets_value_sumChargedHadronPt + nQCD_value_sumChargedHadronPt;

	cout<<"result of fit with sumChargedHadronPt: " <<endl;

	cout<<"fraction of GJets (full region) = "<<nGJets_value_sumChargedHadronPt<<" +/- "<<nGJets_value_sumChargedHadronPt_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_sumChargedHadronPt/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_sumChargedHadronPt_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD (full region) = "<<nQCD_value_sumChargedHadronPt<<" +/- "<<nQCD_value_sumChargedHadronPt_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_sumChargedHadronPt/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_sumChargedHadronPt_err/N_total_GJets_QCD_fit<<endl;


	nGJets_value_sumChargedHadronPt = nGJets_value_sumChargedHadronPt*tightFraction_GJets;
	nGJets_value_sumChargedHadronPt_err = nGJets_value_sumChargedHadronPt_err*tightFraction_GJets;
	nQCD_value_sumChargedHadronPt = nQCD_value_sumChargedHadronPt*tightFraction_QCD;
	nQCD_value_sumChargedHadronPt_err = nQCD_value_sumChargedHadronPt_err*tightFraction_QCD;
	N_total_GJets_QCD_fit = nGJets_value_sumChargedHadronPt + nQCD_value_sumChargedHadronPt;

	cout<<"fraction of GJets (full region) = "<<nGJets_value_sumChargedHadronPt<<" +/- "<<nGJets_value_sumChargedHadronPt_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_sumChargedHadronPt/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_sumChargedHadronPt_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD (full region) = "<<nQCD_value_sumChargedHadronPt<<" +/- "<<nQCD_value_sumChargedHadronPt_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_sumChargedHadronPt/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_sumChargedHadronPt_err/N_total_GJets_QCD_fit<<endl;


	//sigmaEOverE
	TH1F *h1_sigmaEOverE_Data = new TH1F("h1_sigmaEOverE_Data","h1_sigmaEOverE_Data", 100, 0., 0.5);
	tree_data->Draw("pho1sigmaEOverE>>h1_sigmaEOverE_Data", cut.c_str());

	TH1F *h1_sigmaEOverE_GJets = (TH1F*)file_shape->Get("phosigmaEOverE_histGJets"); 
	TH1F *h1_sigmaEOverE_QCD = (TH1F*)file_shape->Get("phosigmaEOverE_histQCD"); 

	h1_sigmaEOverE_GJets->Scale((1.0*h1_sigmaEOverE_Data->Integral())/h1_sigmaEOverE_GJets->Integral());
	h1_sigmaEOverE_QCD->Scale((1.0*h1_sigmaEOverE_Data->Integral())/h1_sigmaEOverE_QCD->Integral());

	RooWorkspace * w_frac_sigmaEOverE;
	w_frac_sigmaEOverE = FitDataBkgFraction(h1_sigmaEOverE_Data, "pho1sigmaEOverE", "#sigma_{E}/E", "", 0., 0.5, h1_sigmaEOverE_GJets, h1_sigmaEOverE_QCD);
	w_frac_sigmaEOverE->Write("w_frac_sigmaEOverE");

	float nGJets_value_sigmaEOverE = w_frac_sigmaEOverE->var("nGJets")->getValV();
	float nGJets_value_sigmaEOverE_err = w_frac_sigmaEOverE->var("nGJets")->getError();
	float nQCD_value_sigmaEOverE = w_frac_sigmaEOverE->var("nQCD")->getValV();
	float nQCD_value_sigmaEOverE_err = w_frac_sigmaEOverE->var("nQCD")->getError();
	h1_sigmaEOverE_GJets->Scale(nGJets_value_sigmaEOverE);
	h1_sigmaEOverE_QCD->Scale(nQCD_value_sigmaEOverE);
	h1_sigmaEOverE_GJets->Write();
	h1_sigmaEOverE_QCD->Write();

	N_total_GJets_QCD_fit = nGJets_value_sigmaEOverE + nQCD_value_sigmaEOverE;
	cout<<"result of fit with sigmaEOverE: " <<endl;
	cout<<"fraction of GJets = "<<nGJets_value_sigmaEOverE<<" +/- "<<nGJets_value_sigmaEOverE_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_sigmaEOverE/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_sigmaEOverE_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD = "<<nQCD_value_sigmaEOverE<<" +/- "<<nQCD_value_sigmaEOverE_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_sigmaEOverE/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_sigmaEOverE_err/N_total_GJets_QCD_fit<<endl;

	//Smajor
	TH1F *h1_Smajor_Data = new TH1F("h1_Smajor_Data","h1_Smajor_Data", 100, 0., 1.0);
	tree_data->Draw("pho1Smajor>>h1_Smajor_Data", cut.c_str());

	TH1F *h1_Smajor_GJets = (TH1F*)file_shape->Get("Smajor_histGJets"); 
	TH1F *h1_Smajor_QCD = (TH1F*)file_shape->Get("Smajor_histQCD"); 

	h1_Smajor_GJets->Scale((1.0*h1_Smajor_Data->Integral())/h1_Smajor_GJets->Integral());
	h1_Smajor_QCD->Scale((1.0*h1_Smajor_Data->Integral())/h1_Smajor_QCD->Integral());

	RooWorkspace * w_frac_Smajor;
	w_frac_Smajor = FitDataBkgFraction(h1_Smajor_Data, "pho1Smajor", "S_{major}", "", 0., 1.0, h1_Smajor_GJets, h1_Smajor_QCD);
	w_frac_Smajor->Write("w_frac_Smajor");

	float nGJets_value_Smajor = w_frac_Smajor->var("nGJets")->getValV();
	float nGJets_value_Smajor_err = w_frac_Smajor->var("nGJets")->getError();
	float nQCD_value_Smajor = w_frac_Smajor->var("nQCD")->getValV();
	float nQCD_value_Smajor_err = w_frac_Smajor->var("nQCD")->getError();
	h1_Smajor_GJets->Scale(nGJets_value_Smajor);
	h1_Smajor_QCD->Scale(nQCD_value_Smajor);
	h1_Smajor_GJets->Write();
	h1_Smajor_QCD->Write();

	N_total_GJets_QCD_fit = nGJets_value_Smajor + nQCD_value_Smajor;
	cout<<"result of fit with Smajor: " <<endl;
	cout<<"fraction of GJets = "<<nGJets_value_Smajor<<" +/- "<<nGJets_value_Smajor_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_Smajor/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_Smajor_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD = "<<nQCD_value_Smajor<<" +/- "<<nQCD_value_Smajor_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_Smajor/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_Smajor_err/N_total_GJets_QCD_fit<<endl;

	//nJets
	TH1F *h1_nJets_Data = new TH1F("h1_nJets_Data","h1_nJets_Data", 15,-0.5,14.5);
	tree_data->Draw("n_Jets>>h1_nJets_Data", cut.c_str());

	TH1F *h1_nJets_GJets = (TH1F*)file_shape->Get("nJets_histGJets"); 
	TH1F *h1_nJets_QCD = (TH1F*)file_shape->Get("nJets_histQCD"); 

	//TH1F *h1_nJets_GJets = new TH1F("h1_nJets_GJets","h1_nJets_GJets", 15,-0.5,14.5);
	//tree_data->Draw("n_Jets>>h1_nJets_GJets", cut_GJets.c_str());

	//TH1F *h1_nJets_QCD = new TH1F("h1_nJets_QCD","h1_nJets_QCD", 15,-0.5,14.5);
	//tree_data->Draw("n_Jets>>h1_nJets_QCD", (cut_loose + " && ! (" + cut + ")").c_str());

	h1_nJets_GJets->Scale((1.0*h1_nJets_Data->Integral())/h1_nJets_GJets->Integral());
	h1_nJets_QCD->Scale((1.0*h1_nJets_Data->Integral())/h1_nJets_QCD->Integral());

	RooWorkspace * w_frac_nJets;
	w_frac_nJets = FitDataBkgFraction(h1_nJets_Data, "nJets", "number of jets", "", -0.5, 14.5, h1_nJets_GJets, h1_nJets_QCD);
	w_frac_nJets->Write("w_frac_nJets");

	float nGJets_value_nJets = w_frac_nJets->var("nGJets")->getValV();
	float nGJets_value_nJets_err = w_frac_nJets->var("nGJets")->getError();
	float nQCD_value_nJets = w_frac_nJets->var("nQCD")->getValV();
	float nQCD_value_nJets_err = w_frac_nJets->var("nQCD")->getError();
	h1_nJets_GJets->Scale(nGJets_value_nJets);
	h1_nJets_QCD->Scale(nQCD_value_nJets);
	h1_nJets_GJets->Write();
	h1_nJets_QCD->Write();

	N_total_GJets_QCD_fit = nGJets_value_nJets + nQCD_value_nJets;
	cout<<"result of fit with nJets: " <<endl;
	cout<<"fraction of GJets = "<<nGJets_value_nJets<<" +/- "<<nGJets_value_nJets_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_nJets/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_nJets_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD = "<<nQCD_value_nJets<<" +/- "<<nQCD_value_nJets_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_nJets/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_nJets_err/N_total_GJets_QCD_fit<<endl;

	//Pt
	TH1F *h1_Pt_Data = new TH1F("h1_Pt_Data","h1_Pt_Data", 100, 50., 1500);
	tree_data->Draw("pho1Pt>>h1_Pt_Data", cut.c_str());

	TH1F *h1_Pt_GJets = (TH1F*)file_shape->Get("phoPt_histGJets"); 
	TH1F *h1_Pt_QCD = (TH1F*)file_shape->Get("phoPt_histQCD"); 

	h1_Pt_GJets->Scale((1.0*h1_Pt_Data->Integral())/h1_Pt_GJets->Integral());
	h1_Pt_QCD->Scale((1.0*h1_Pt_Data->Integral())/h1_Pt_QCD->Integral());

	RooWorkspace * w_frac_Pt;
	w_frac_Pt = FitDataBkgFraction(h1_Pt_Data, "pho1Pt", "p_{T}^{#gamma}", "GeV", 50., 1500, h1_Pt_GJets, h1_Pt_QCD);
	w_frac_Pt->Write("w_frac_Pt");

	float nGJets_value_Pt = w_frac_Pt->var("nGJets")->getValV();
	float nGJets_value_Pt_err = w_frac_Pt->var("nGJets")->getError();
	float nQCD_value_Pt = w_frac_Pt->var("nQCD")->getValV();
	float nQCD_value_Pt_err = w_frac_Pt->var("nQCD")->getError();
	h1_Pt_GJets->Scale(nGJets_value_Pt);
	h1_Pt_QCD->Scale(nQCD_value_Pt);
	h1_Pt_GJets->Write();
	h1_Pt_QCD->Write();

	N_total_GJets_QCD_fit = nGJets_value_Pt + nQCD_value_Pt;
	cout<<"result of fit with Pt: " <<endl;
	cout<<"fraction of GJets = "<<nGJets_value_Pt<<" +/- "<<nGJets_value_Pt_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_Pt/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_Pt_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD = "<<nQCD_value_Pt<<" +/- "<<nQCD_value_Pt_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_Pt/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_Pt_err/N_total_GJets_QCD_fit<<endl;

}

/*
//TFractionFitter fit with SigmaIetaIeta
TH1F *h1_SigmaIetaIeta_data = new TH1F("h1_SigmaIetaIeta_data","h1_SigmaIetaIeta_data", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_data", cut.c_str());
TH1F *h1_SigmaIetaIeta_GJets = new TH1F("h1_SigmaIetaIeta_GJets","h1_SigmaIetaIeta_GJets", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_GJets", cut_GJets.c_str());
TH1F *h1_SigmaIetaIeta_QCD = new TH1F("h1_SigmaIetaIeta_QCD","h1_SigmaIetaIeta_QCD", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_QCD", (cut_loose + " && ! (" + cut + ")").c_str());
h1_SigmaIetaIeta_GJets->Scale(1.0*h1_SigmaIetaIeta_data->Integral()/h1_SigmaIetaIeta_GJets->Integral());
h1_SigmaIetaIeta_QCD->Scale(1.0*h1_SigmaIetaIeta_data->Integral()/h1_SigmaIetaIeta_QCD->Integral());

TFractionFitter* fit_SigmaIetaIeta;
fit_SigmaIetaIeta = FitDataBkgFractionFilter(h1_SigmaIetaIeta_data, h1_SigmaIetaIeta_GJets, h1_SigmaIetaIeta_QCD);
Double_t nGJets_value_SigmaIetaIeta, nGJets_value_SigmaIetaIeta_err, nQCD_value_SigmaIetaIeta, nQCD_value_SigmaIetaIeta_err;
fit_SigmaIetaIeta->GetResult(0, nGJets_value_SigmaIetaIeta, nGJets_value_SigmaIetaIeta_err);
fit_SigmaIetaIeta->GetResult(1, nQCD_value_SigmaIetaIeta, nQCD_value_SigmaIetaIeta_err);

cout<<"result of fit with SigmaIetaIeta: " <<endl;
cout<<"fraction of GJets = "<<nGJets_value_SigmaIetaIeta<<" / "<<nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta<<" = "<<nGJets_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta)<<endl;
cout<<"fraction of QCD = "<<nQCD_value_SigmaIetaIeta<<" / "<<nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta<<" = "<<nQCD_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta)<<endl;
*/

float frac_GJets = nGJets_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta);
float frac_QCD = nQCD_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta);



/***************************Binning optimization*********************************/

float time_Low = -15.0;
float time_High = 15.0;
int time_N_fine = 300;

float met_Low = 0.0;
float met_High = 1000.0;
int met_N_fine = 200;

std::vector <int> timeBin;
std::vector <int> metBin;

timeBin.push_back(0);
timeBin.push_back(time_N_fine);

metBin.push_back(0);
metBin.push_back(met_N_fine);

if(fitMode == "binning")
{
	mkdir("fit_results/binning", S_IRWXU | S_IRWXG | S_IRWXO);

	TH2F *h2finebinData = new TH2F("h2finebinData","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinBkg = new TH2F("h2finebinBkg","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinGJets = new TH2F("h2finebinGJets","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinQCD = new TH2F("h2finebinQCD","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinSig = new TH2F("h2finebinSig","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);

	tree_data->Draw("MET:pho1ClusterTime>>h2finebinData", cut.c_str());
	tree_data->Draw("MET:pho1ClusterTime>>h2finebinGJets", cut_GJets.c_str());
	tree_data->Draw("MET:pho1ClusterTime>>h2finebinQCD", (cut_loose + " && ! (" + cut + ")").c_str());
	tree_signal->Draw("MET:pho1ClusterTime>>h2finebinSig", ("weight*pileupWeight * ( "+cut+" )").c_str());

	float N_sig_expected = 1.0*lumi*xsec*h2finebinSig->Integral()/(1.0*NEvents_sig);
	h2finebinGJets->Scale((1.0*h2finebinData->Integral()*frac_GJets)/(1.0*h2finebinGJets->Integral()));
	h2finebinQCD->Scale((1.0*h2finebinData->Integral()*frac_QCD)/(1.0*h2finebinQCD->Integral()));
	h2finebinSig->Scale((1.0*N_sig_expected)/(1.0*h2finebinSig->Integral()));

	for(int i=1; i<=time_N_fine;i++)
	{
		for(int j=1;j<=met_N_fine;j++)
		{
			h2finebinBkg->SetBinContent(i,j, h2finebinGJets->GetBinContent(i,j) + h2finebinQCD->GetBinContent(i,j));	
		}
	}

	OptimizeBinning(timeBin, metBin, h2finebinBkg, h2finebinSig, time_Low, time_High, time_N_fine, met_Low, met_High, met_N_fine, _sigModelName);
	
	cout<<"optimized met and time bin:-----------"<<endl;
	cout<<"time: ";
	for(int i=0;i<timeBin.size();i++)
	{
		cout<<time_Low + (time_High - time_Low) * (1.0*timeBin[i])/(1.0*time_N_fine)<<"  ,  ";
	}
	cout<<endl;
	
	cout<<"time bin: ";
	for(int i=0;i<timeBin.size();i++)
	{
		cout<<timeBin[i]<<"  ,  ";
	}
	cout<<endl;
	
	cout<<"met: ";
	for(int i=0;i<metBin.size();i++)
	{
		cout<<met_Low + (met_High - met_Low) * (1.0*metBin[i])/(1.0*met_N_fine)<<"  ,  ";
	}
	cout<<endl;

	cout<<"met bin: ";
	for(int i=0;i<metBin.size();i++)
	{
		cout<<metBin[i]<<"   ,   ";
	}
	cout<<endl;


}

/*********2D fit of time and MET to obtain signal and background yield***********/

//2D to 1D conversion, with customize binning

TH2F * h2newbinData = new TH2F("h2newbinData","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinBkg = new TH2F("h2newbinBkg","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinGJets = new TH2F("h2newbinGJets","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinQCD = new TH2F("h2newbinQCD","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinSig = new TH2F("h2newbinSig","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);

TH1F * h1newbinData_time = new TH1F("h1newbinData_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinData_toy_time = new TH1F("h1newbinData_toy_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinBkg_time = new TH1F("h1newbinBkg_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinSig_time = new TH1F("h1newbinSig_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinAll_time = new TH1F("h1newbinAll_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinGJets_time = new TH1F("h1newbinGJets_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinQCD_time = new TH1F("h1newbinQCD_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);


TH1F * h1newbinData_MET = new TH1F("h1newbinData_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinData_toy_MET = new TH1F("h1newbinData_toy_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinBkg_MET = new TH1F("h1newbinBkg_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinSig_MET = new TH1F("h1newbinSig_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinAll_MET = new TH1F("h1newbinAll_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinGJets_MET = new TH1F("h1newbinGJets_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinQCD_MET = new TH1F("h1newbinQCD_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);

tree_data->Draw("MET:pho1ClusterTime>>h2newbinData", cut.c_str());
tree_data->Draw("MET:pho1ClusterTime>>h2newbinGJets", cut_GJets.c_str());
tree_data->Draw("MET:pho1ClusterTime>>h2newbinQCD", (cut_loose + " && ! (" + cut + ")").c_str());
tree_signal->Draw("MET:pho1ClusterTime>>h2newbinSig", ("weight*pileupWeight * ( "+cut+" )").c_str());

tree_data->Draw("pho1ClusterTime>>h1newbinData_time", cut.c_str());
tree_signal->Draw("pho1ClusterTime>>h1newbinSig_time", ("weight*pileupWeight * ( "+cut+" )").c_str());
tree_data->Draw("pho1ClusterTime>>h1newbinGJets_time", cut_GJets.c_str());
tree_data->Draw("pho1ClusterTime>>h1newbinQCD_time", (cut_loose + " && ! (" + cut + ")").c_str());

tree_data->Draw("MET>>h1newbinData_MET", cut.c_str());
tree_signal->Draw("MET>>h1newbinSig_MET", ("weight*pileupWeight * ( "+cut+" )").c_str());
tree_data->Draw("MET>>h1newbinGJets_MET", cut_GJets.c_str());
tree_data->Draw("MET>>h1newbinQCD_MET", (cut_loose + " && ! (" + cut + ")").c_str());

float N_sig_expected = 1.0*lumi*xsec*h2newbinSig->Integral()/(1.0*NEvents_sig);

h2newbinGJets->Scale((1.0*h2newbinData->Integral()*frac_GJets)/(1.0*h2newbinGJets->Integral()));
h2newbinQCD->Scale((1.0*h2newbinData->Integral()*frac_QCD)/(1.0*h2newbinQCD->Integral()));
h2newbinSig->Scale((1.0*N_sig_expected)/(1.0*h2newbinSig->Integral()));

h1newbinGJets_time->Scale((1.0*h1newbinData_time->Integral()*frac_GJets)/(1.0*h1newbinGJets_time->Integral()));
h1newbinQCD_time->Scale((1.0*h1newbinData_time->Integral()*frac_QCD)/(1.0*h1newbinQCD_time->Integral()));
h1newbinSig_time->Scale((1.0*N_sig_expected)/(1.0*h1newbinSig_time->Integral()));

h1newbinGJets_MET->Scale((1.0*h1newbinData_MET->Integral()*frac_GJets)/(1.0*h1newbinGJets_MET->Integral()));
h1newbinQCD_MET->Scale((1.0*h1newbinData_MET->Integral()*frac_QCD)/(1.0*h1newbinQCD_MET->Integral()));
h1newbinSig_MET->Scale((1.0*N_sig_expected)/(1.0*h1newbinSig_MET->Integral()));


TH1F * h1combineData = new TH1F("h1combineData","h1combineData", Nbins_total , 0, Nbins_total);
TH1 * h1combineData_toy = new TH1F("h1combineData_toy","h1combineData_toy", Nbins_total , 0, Nbins_total);
TH1F * h1combineBkg = new TH1F("h1combineBkg","h1combineBkg", Nbins_total , 0, Nbins_total);
TH1F * h1combineGJets = new TH1F("h1combineGJets","h1combineGJets", Nbins_total , 0, Nbins_total);
TH1F * h1combineQCD = new TH1F("h1combineQCD","h1combineQCD", Nbins_total , 0, Nbins_total);
TH1F * h1combineSig = new TH1F("h1combineSig","h1combineSig", Nbins_total , 0, Nbins_total);

for(int i=1;i<=Nbins_MET;i++)
{
	for(int j=1;j<=Nbins_time;j++)
	{
		int thisBin = (i-1)*Nbins_time+j;
		h1combineData->SetBinContent(thisBin, h2newbinData->GetBinContent(j,i));	
		h1combineGJets->SetBinContent(thisBin, h2newbinGJets->GetBinContent(j,i));	
		h1combineQCD->SetBinContent(thisBin, h2newbinQCD->GetBinContent(j,i));	
		h1combineBkg->SetBinContent(thisBin, h2newbinQCD->GetBinContent(j,i) + h2newbinGJets->GetBinContent(j,i));
		h1combineSig->SetBinContent(thisBin, h2newbinSig->GetBinContent(j,i));	
	}
}

for(int i=1; i<=Nbins_total; i++)
{
	//float ndata = h1combineData->GetBinContent(i);
	float nbkg = h1combineBkg->GetBinContent(i);
	float nsig = h1combineSig->GetBinContent(i);
	if(nbkg < 1e-3 ) h1combineBkg->SetBinContent(i, 1e-3);
	if(nsig < 1e-3 ) h1combineSig->SetBinContent(i, 1e-3);
}

cout<<"convert 2D to 1D (integral 2D/1D): "<<h2newbinData->Integral()<<" / "<<h1combineData->Integral()<<endl;

for(int i=1;i<=Nbins_MET;i++)
{
	float nbkg = h1newbinGJets_MET->GetBinContent(i)+h1newbinQCD_MET->GetBinContent(i);
	if(nbkg<1e-3) nbkg = 1e-3;
	h1newbinBkg_MET->SetBinContent(i, nbkg);
	
	h1newbinData_toy_MET->SetBinContent(i,0.0);
}

for(int i=1;i<=Nbins_time;i++)
{
	float nbkg = h1newbinGJets_time->GetBinContent(i)+h1newbinQCD_time->GetBinContent(i);
	if(nbkg<1e-3) nbkg = 1e-3;
	h1newbinBkg_time->SetBinContent(i, nbkg);
	
	h1newbinData_toy_time->SetBinContent(i,0.0);
}

if(fitMode == "datacard")
{
	mkdir("fit_results/datacards", S_IRWXU | S_IRWXG | S_IRWXO);
	TFile *f_Out_combineWS = new TFile(("fit_results/datacards/fit_combineWS_"+sigModelName+".root").c_str(),"recreate");

	////////////make datacard - 2D->1D fit/////////
	RooWorkspace * ws_combine;
	
	cout<<"DEBUG fit: input histogram ===="<<endl;
	cout<<"data: int = "<<h1combineData->Integral()<<endl;
	cout<<"GJets: int = "<<h1combineGJets->Integral()<<endl;
	cout<<"QCD: int = "<<h1combineQCD->Integral()<<endl;
	cout<<"Sig: int = "<<h1combineSig->Integral()<<endl;
	
	ws_combine = Fit1DMETTimeDataBkgSig( h1combineData, h1combineGJets, h1combineQCD, h1combineSig, frac_GJets, frac_QCD, _sigModelName, _sigModelTitle, _useToy);

	ws_combine->SetName("ws_combine");
	ws_combine->Write("ws_combine");
	
	float nBkg_2DFit_combine_DataBkgSig = ws_combine->var("fitModelBkg_yield")->getValV();
	float nBkg_2DFit_combine_DataBkgSig_Err = ws_combine->var("fitModelBkg_yield")->getError();
	float nSig_2DFit_combine_DataBkgSig = ws_combine->var("rpSig_yield")->getValV();
	float nSig_2DFit_combine_DataBkgSig_Err = ws_combine->var("rpSig_yield")->getError();

	cout<<"result of 1D combined fit with bkg + sig: " <<endl;
	cout<<"N_obs in data = "<<N_obs_total<<endl;
	cout<<"Bkg yield = "<<nBkg_2DFit_combine_DataBkgSig<<" +/- "<<nBkg_2DFit_combine_DataBkgSig_Err<<"  (fraction: "<<nBkg_2DFit_combine_DataBkgSig/N_obs_total<<" )"<<endl;
	cout<<"Sig yield = "<<nSig_2DFit_combine_DataBkgSig<<" +/- "<<nSig_2DFit_combine_DataBkgSig_Err<<"  (fraction: "<<nSig_2DFit_combine_DataBkgSig/N_obs_total<<" )"<<endl;

	printf("%s & %d & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f \\\\ \n", sigModelName.c_str(), N_obs_total, nBkg_2DFit_combine_DataBkgSig, nBkg_2DFit_combine_DataBkgSig_Err, nSig_2DFit_combine_DataBkgSig, nSig_2DFit_combine_DataBkgSig_Err);

	MakeDataCard(_sigModelName, ws_combine, h1combineData->Integral(), nBkg_2DFit_combine_DataBkgSig, N_sig_expected);
	
	//save the histograms
	h1combineData_toy = ws_combine->data("data_toy")->createHistogram("bin", Nbins_total);
	
	for(int i=1;i<=Nbins_total;i++)
	{
		int bin_time = (i-1)%Nbins_time + 1;//1->20
		int bin_MET = int((i-1)/Nbins_time) + 1; // 1->15
	
		//cout<<"DEBUG: 2Dbin = "<<i<<" time bin = "<<bin_time<<"  MET bin = "<<bin_MET<<endl;
			
		float newMET = h1newbinData_toy_MET->GetBinContent(bin_MET) + h1combineData_toy->GetBinContent(i);
		float newtime = h1newbinData_toy_time->GetBinContent(bin_time) + h1combineData_toy->GetBinContent(i);
		h1newbinData_toy_MET->SetBinContent(bin_MET,newMET);
		h1newbinData_toy_time->SetBinContent(bin_time,newtime);
	}
	
	cout<<"DEBUG: comparing real data and toy data:"<<endl;
	cout<<"toy data, 2D int = "<<h1combineData_toy->Integral()<<endl;
	cout<<"real data, MET int = "<<h1newbinData_MET->Integral()<<endl;
	cout<<"toy data, MET int = "<<h1newbinData_toy_MET->Integral()<<endl;
	cout<<"real data, time int = "<<h1newbinData_time->Integral()<<endl;
	cout<<"toy data, time int = "<<h1newbinData_toy_time->Integral()<<endl;
	
	h1newbinBkg_time->Scale((1.0*nBkg_2DFit_combine_DataBkgSig)/(1.0*h1newbinBkg_time->Integral()));
	h1newbinBkg_MET->Scale((1.0*nBkg_2DFit_combine_DataBkgSig)/(1.0*h1newbinBkg_MET->Integral()));
	h1newbinSig_time->Scale((1.0*nSig_2DFit_combine_DataBkgSig)/(1.0*h1newbinSig_time->Integral()));
	h1newbinSig_MET->Scale((1.0*nSig_2DFit_combine_DataBkgSig)/(1.0*h1newbinSig_MET->Integral()));

	for(int i=1;i<=Nbins_MET;i++)
	{
		h1newbinAll_MET->SetBinContent(i, h1newbinBkg_MET->GetBinContent(i)+h1newbinSig_MET->GetBinContent(i));
	}

	for(int i=1;i<=Nbins_time;i++)
	{
		h1newbinAll_time->SetBinContent(i, h1newbinBkg_time->GetBinContent(i)+h1newbinSig_time->GetBinContent(i));
	}

	if(_useToy)
	{	
		DrawDataBkgSig(h1newbinData_toy_time, h1newbinBkg_time, h1newbinSig_time, h1newbinAll_time, lumi, sigModelTitle, sigModelName, "time");
		DrawDataBkgSig(h1newbinData_toy_MET, h1newbinBkg_MET, h1newbinSig_MET, h1newbinAll_MET, lumi, sigModelTitle, sigModelName, "MET");
	}
	else
	{
		DrawDataBkgSig(h1newbinData_time, h1newbinBkg_time, h1newbinSig_time, h1newbinAll_time, lumi, sigModelTitle, sigModelName, "time");
		DrawDataBkgSig(h1newbinData_MET, h1newbinBkg_MET, h1newbinSig_MET, h1newbinAll_MET, lumi, sigModelTitle, sigModelName, "MET");

	}
	
	h1newbinData_time->Write();
	h1newbinBkg_time->Write();
	h1newbinSig_time->Write();
	h1newbinData_MET->Write();
	h1newbinBkg_MET->Write();
	h1newbinSig_MET->Write();
		
	h1combineData->Write();
	h1combineBkg->Write();
	h1combineSig->Write();

}

//do the bias test
if(fitMode == "bias")
{
	mkdir("fit_results/bias", S_IRWXU | S_IRWXG | S_IRWXO);

	Fit1DMETTimeBiasTest( h1combineData, h1combineBkg, h1combineSig, SoverB, nToys, _sigModelName, lumi);	
		
}
return 0;
}
