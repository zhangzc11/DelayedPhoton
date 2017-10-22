//C++ INCLUDES
#include <iostream>
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
Int_t Nbins_time = 20;
Int_t Nbins_total = Nbins_MET*Nbins_time;
Double_t xbins_MET[16] = {0.0, 10.0, 20.0, 40.0, 60.0, 80, 100.0, 125.0, 150.0, 175.0, 200.0, 250.0, 300.0, 400.0, 500.0, 1000.0};
Double_t xbins_time[21] = {-15, -10, -5, -4, -3, -2.5, -2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3, 4, 5, 10, 15};

float lumi = 31.39;
float NEvents_sig = 1.0;
bool _useToy = true;

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
std::string sigModelName = argv[3]; //"M1000GeV_500mm";
std::string sigModelTitle = argv[4]; //"#tilde{g}#rightarrow#tilde{#chi}_{1}^{0}#rightarrow#gamma#tilde{G} (500mm)";
//std::string xsec_str = argv[5];
//float xsec = strtof(xsec_str.c_str(),0);
float xsec = getXsecBR(sigModelName);
std::string treeName = "DelayedPhoton";

std::string cut = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2"; 
std::string cut_noHLT = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && n_Photons == 2"; 
std::string cut_iso = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2 && pho1sumChargedHadronPt < 1.30 && pho1sumNeutralHadronEt < 0.26 && pho1sumPhotonEt < 2.36";
std::string cut_loose = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.7 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2";
std::string cut_GJets = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (jet2Pt/pho1Pt > 0.2) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)";


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
std::cout<<"using input file for signal: "<<inputFileName_signal<<std::endl;
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

TFile *f_Out = new TFile(("fit_results/fit_ws_"+sigModelName+".root").c_str(),"recreate");

int N_obs_total = tree_data->CopyTree( cut.c_str() )->GetEntries();
float N_total_GJets_QCD_fit = 0.0;

/**********fit to get relative yield of GJets and QCD backgrounds *****/
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


/*********2D fit of time and MET to obtain signal and background yield***********/


TH2F * h2Data = new TH2F("h2Data","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 100, -15, 15, 100, 0, 1000);
TH2F * h2GJets = new TH2F("h2GJets","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 100, -15, 15, 100, 0, 1000);
TH2F * h2QCD = new TH2F("h2QCD","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 100, -15, 15, 100, 0, 1000);
TH2F * h2Sig = new TH2F("h2Sig","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 100, -15, 15, 100, 0, 1000);

tree_data->Draw("MET:pho1ClusterTime>>h2Data", cut.c_str());
tree_data->Draw("MET:pho1ClusterTime>>h2GJets", cut_GJets.c_str());
tree_data->Draw("MET:pho1ClusterTime>>h2QCD", (cut_loose + " && ! (" + cut + ")").c_str());
tree_signal->Draw("MET:pho1ClusterTime>>h2Sig", ("weight * ( "+cut+" )").c_str());

h2GJets->Scale((1.0*h2Data->Integral())/(1.0*h2GJets->Integral()));
h2QCD->Scale((1.0*h2Data->Integral())/(1.0*h2QCD->Integral()));
h2Sig->Scale((1.0*h2Data->Integral())/(1.0*h2Sig->Integral()));

cout<<"BbinsX = "<<h2GJets->GetNbinsX()<<endl;
cout<<"BbinsY = "<<h2GJets->GetNbinsY()<<endl;

//////////bkg+sig fit////////////////
RooWorkspace * w_DataBkgSig;
TString _sigModelName (sigModelName.c_str());
TString _sigModelTitle (sigModelTitle.c_str());

float frac_GJets = nGJets_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta);
float frac_QCD = nQCD_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta);

w_DataBkgSig = Fit2DMETTimeDataBkgSig( h2Data, h2GJets, h2QCD, h2Sig, frac_GJets, frac_QCD, _sigModelName, _sigModelTitle, _useToy);
w_DataBkgSig->Write("w_DataBkgSig");
float nBkg_2DFit_DataBkgSig = w_DataBkgSig->var("fitModelBkg_yield")->getValV();
float nBkg_2DFit_DataBkgSig_Err = w_DataBkgSig->var("fitModelBkg_yield")->getError();
float nSig_2DFit_DataBkgSig = w_DataBkgSig->var("rpSig_yield")->getValV();
float nSig_2DFit_DataBkgSig_Err = w_DataBkgSig->var("rpSig_yield")->getError();


//////////background only fit///////////////

RooWorkspace * w_DataBkg;
//w_DataBkg = Fit2DMETTimeDataBkg( tree_data->CopyTree( cut.c_str() ), tree_data->CopyTree( cut_GJets.c_str() ), tree_data->CopyTree( (cut_loose + " && ! (" + cut + ")").c_str() ), nGJets_value_SigmaIetaIeta, nGJets_value_SigmaIetaIeta_err, nQCD_value_SigmaIetaIeta, nQCD_value_SigmaIetaIeta_err);
w_DataBkg = Fit2DMETTimeDataBkg( h2Data, h2GJets, h2QCD, nGJets_value_SigmaIetaIeta, nGJets_value_SigmaIetaIeta_err, nQCD_value_SigmaIetaIeta, nQCD_value_SigmaIetaIeta_err);
w_DataBkg->Write("w_DataBkg");
float nGJets_2DFit_DataBkg = w_DataBkg->var("nGJets")->getValV();
float nGJets_2DFit_DataBkg_Err = w_DataBkg->var("nGJets")->getError();
float nQCD_2DFit_DataBkg = w_DataBkg->var("nQCD")->getValV();
float nQCD_2DFit_DataBkg_Err = w_DataBkg->var("nQCD")->getError();

//print out result
cout<<"result of 2D fit with background only: " <<endl;
cout<<"N_obs in data = "<<N_obs_total<<endl;
cout<<"GJets yield = "<<nGJets_2DFit_DataBkg<<" +/- "<<nGJets_2DFit_DataBkg_Err<<"  (fraction: "<<nGJets_2DFit_DataBkg/N_obs_total<<" )"<<endl;
cout<<"QCD yield = "<<nQCD_2DFit_DataBkg<<" +/- "<<nQCD_2DFit_DataBkg_Err<<"  (fraction: "<<nQCD_2DFit_DataBkg/N_obs_total<<" )"<<endl;

printf("%s & %d & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f \\\\ \n", sigModelName.c_str(), N_obs_total, nGJets_2DFit_DataBkg, nGJets_2DFit_DataBkg_Err, nQCD_2DFit_DataBkg, nQCD_2DFit_DataBkg_Err);

cout<<"result of 2D fit with bkg + sig: " <<endl;
cout<<"N_obs in data = "<<N_obs_total<<endl;
cout<<"Bkg yield = "<<nBkg_2DFit_DataBkgSig<<" +/- "<<nBkg_2DFit_DataBkgSig_Err<<"  (fraction: "<<nBkg_2DFit_DataBkgSig/N_obs_total<<" )"<<endl;
cout<<"Sig yield = "<<nSig_2DFit_DataBkgSig<<" +/- "<<nSig_2DFit_DataBkgSig_Err<<"  (fraction: "<<nSig_2DFit_DataBkgSig/N_obs_total<<" )"<<endl;

printf("%s & %d & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f \\\\ \n", sigModelName.c_str(), N_obs_total, nBkg_2DFit_DataBkgSig, nBkg_2DFit_DataBkgSig_Err, nSig_2DFit_DataBkgSig, nSig_2DFit_DataBkgSig_Err);

////////////make datacard - change to 1D fit/////////
//1. customize binning

TH2F * h2newbinData = new TH2F("h2newbinData","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, xbins_time, Nbins_MET, xbins_MET);
TH2F * h2newbinBkg = new TH2F("h2newbinBkg","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, xbins_time, Nbins_MET, xbins_MET);
TH2F * h2newbinGJets = new TH2F("h2newbinGJets","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, xbins_time, Nbins_MET, xbins_MET);
TH2F * h2newbinQCD = new TH2F("h2newbinQCD","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, xbins_time, Nbins_MET, xbins_MET);
TH2F * h2newbinSig = new TH2F("h2newbinSig","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, xbins_time, Nbins_MET, xbins_MET);

tree_data->Draw("MET:pho1ClusterTime>>h2newbinData", cut.c_str());
tree_data->Draw("MET:pho1ClusterTime>>h2newbinGJets", cut_GJets.c_str());
tree_data->Draw("MET:pho1ClusterTime>>h2newbinQCD", (cut_loose + " && ! (" + cut + ")").c_str());
tree_signal->Draw("MET:pho1ClusterTime>>h2newbinSig", ("weight * ( "+cut+" )").c_str());
/*
h2newbinGJets->Scale((1.0*nBkg_2DFit_DataBkgSig*frac_GJets)/(1.0*h2newbinGJets->Integral()));
h2newbinQCD->Scale((1.0*nBkg_2DFit_DataBkgSig*frac_QCD)/(1.0*h2newbinQCD->Integral()));
h2newbinBkg->Add(h2newbinGJets);
h2newbinBkg->Add(h2newbinQCD);
h2newbinSig->Scale((1.0*lumi*xsec)/(1.0*NEvents_sig));
*/

float N_sig_expected = 1.0*lumi*xsec*h2newbinSig->Integral()/(1.0*NEvents_sig);

h2newbinGJets->Scale((1.0*h2newbinData->Integral())/(1.0*h2newbinGJets->Integral()));
h2newbinQCD->Scale((1.0*h2newbinData->Integral())/(1.0*h2newbinQCD->Integral()));
h2newbinSig->Scale((1.0*h2newbinData->Integral())/(1.0*h2newbinSig->Integral()));


//2. convert into 1D histogram
TH1F * h1combineData = new TH1F("h1combineData","h1combineData", Nbins_total , 0, Nbins_total);
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
		h1combineSig->SetBinContent(thisBin, h2newbinSig->GetBinContent(j,i));	
	}
}

cout<<"convert 2D to 1D (integral 2D/1D): "<<h2newbinData->Integral()<<" / "<<h1combineData->Integral()<<endl;

//3. fit, and also generate toy data
RooWorkspace * ws_combine;

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

h1combineGJets->Scale((1.0*nBkg_2DFit_DataBkgSig*frac_GJets)/(1.0*h1combineGJets->Integral()));
h1combineQCD->Scale((1.0*nBkg_2DFit_DataBkgSig*frac_QCD)/(1.0*h1combineQCD->Integral()));
h1combineBkg->Add(h1combineGJets);
h1combineBkg->Add(h1combineQCD);
h1combineSig->Scale((N_sig_expected)/(1.0*h1combineSig->Integral()));

h1combineData->Write();
h1combineBkg->Write();
h1combineSig->Write();

return 0;
}
