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

using namespace std;

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
std::string sigModelName = "M1000GeV_500mm";
std::string sigModelTitle = "#tilde{g}#rightarrow#tilde{#chi}_{1}^{0}#rightarrow#gamma#tilde{G} (500mm)";

std::string treeName = "DelayedPhoton";

std::string cut = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2"; 
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


TFile *file_data;
TFile *file_signal;

TTree *tree_data;
TTree *tree_signal;

file_data = new TFile(inputFileName_data.c_str(), "READ");
tree_data = (TTree*)file_data->Get(treeName.c_str());

file_signal = new TFile(inputFileName_signal.c_str(), "READ");
tree_signal = (TTree*)file_signal->Get(treeName.c_str());


TFile *f_Out = new TFile("result.root","recreate");

int N_obs_total = tree_data->CopyTree( cut.c_str() )->GetEntries();

/**********fit SigmaIetaIeta to get relative yield of GJets and QCD backgrounds *****/
//SigmaIetaIeta
TH1F *h1_SigmaIetaIeta_Data = new TH1F("h1_SigmaIetaIeta_Data","h1_SigmaIetaIeta_Data", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_Data", cut.c_str());

TH1F *h1_SigmaIetaIeta_GJets = new TH1F("h1_SigmaIetaIeta_GJets","h1_SigmaIetaIeta_GJets", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_GJets", cut_GJets.c_str());

TH1F *h1_SigmaIetaIeta_QCD = new TH1F("h1_SigmaIetaIeta_QCD","h1_SigmaIetaIeta_QCD", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_QCD", (cut_loose + " && ! (" + cut + ")").c_str());

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

cout<<"result of fit with SigmaIetaIeta: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_SigmaIetaIeta<<" +/- "<<nGJets_value_SigmaIetaIeta_err<<" / "<<N_obs_total<<" = "<<nGJets_value_SigmaIetaIeta/N_obs_total<<" +/- "<<nGJets_value_SigmaIetaIeta_err/N_obs_total<<endl;
cout<<"fraction of Gjets = "<<nQCD_value_SigmaIetaIeta<<" +/- "<<nQCD_value_SigmaIetaIeta_err<<" / "<<N_obs_total<<" = "<<nQCD_value_SigmaIetaIeta/N_obs_total<<" +/- "<<nQCD_value_SigmaIetaIeta_err/N_obs_total<<endl;

//sigmaEOverE
TH1F *h1_sigmaEOverE_Data = new TH1F("h1_sigmaEOverE_Data","h1_sigmaEOverE_Data", 100, 0., 0.5);
tree_data->Draw("pho1sigmaEOverE>>h1_sigmaEOverE_Data", cut.c_str());

TH1F *h1_sigmaEOverE_GJets = new TH1F("h1_sigmaEOverE_GJets","h1_sigmaEOverE_GJets", 100, 0., 0.5);
tree_data->Draw("pho1sigmaEOverE>>h1_sigmaEOverE_GJets", cut_GJets.c_str());

TH1F *h1_sigmaEOverE_QCD = new TH1F("h1_sigmaEOverE_QCD","h1_sigmaEOverE_QCD", 100, 0., 0.5);
tree_data->Draw("pho1sigmaEOverE>>h1_sigmaEOverE_QCD", (cut_loose + " && ! (" + cut + ")").c_str());

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

cout<<"result of fit with sigmaEOverE: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_sigmaEOverE<<" +/- "<<nGJets_value_sigmaEOverE_err<<" / "<<N_obs_total<<" = "<<nGJets_value_sigmaEOverE/N_obs_total<<" +/- "<<nGJets_value_sigmaEOverE_err/N_obs_total<<endl;
cout<<"fraction of Gjets = "<<nQCD_value_sigmaEOverE<<" +/- "<<nQCD_value_sigmaEOverE_err<<" / "<<N_obs_total<<" = "<<nQCD_value_sigmaEOverE/N_obs_total<<" +/- "<<nQCD_value_sigmaEOverE_err/N_obs_total<<endl;

//Smajor
TH1F *h1_Smajor_Data = new TH1F("h1_Smajor_Data","h1_Smajor_Data", 100, 0., 1.0);
tree_data->Draw("pho1Smajor>>h1_Smajor_Data", cut.c_str());

TH1F *h1_Smajor_GJets = new TH1F("h1_Smajor_GJets","h1_Smajor_GJets", 100, 0., 1.0);
tree_data->Draw("pho1Smajor>>h1_Smajor_GJets", cut_GJets.c_str());

TH1F *h1_Smajor_QCD = new TH1F("h1_Smajor_QCD","h1_Smajor_QCD", 100, 0., 1.0);
tree_data->Draw("pho1Smajor>>h1_Smajor_QCD", (cut_loose + " && ! (" + cut + ")").c_str());

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

cout<<"result of fit with Smajor: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_Smajor<<" +/- "<<nGJets_value_Smajor_err<<" / "<<N_obs_total<<" = "<<nGJets_value_Smajor/N_obs_total<<" +/- "<<nGJets_value_Smajor_err/N_obs_total<<endl;
cout<<"fraction of Gjets = "<<nQCD_value_Smajor<<" +/- "<<nQCD_value_Smajor_err<<" / "<<N_obs_total<<" = "<<nQCD_value_Smajor/N_obs_total<<" +/- "<<nQCD_value_Smajor_err/N_obs_total<<endl;

//nJets
TH1F *h1_nJets_Data = new TH1F("h1_nJets_Data","h1_nJets_Data", 15,-0.5,14.5);
tree_data->Draw("nJets>>h1_nJets_Data", cut.c_str());

TH1F *h1_nJets_GJets = new TH1F("h1_nJets_GJets","h1_nJets_GJets", 15,-0.5,14.5);
tree_data->Draw("nJets>>h1_nJets_GJets", cut_GJets.c_str());

TH1F *h1_nJets_QCD = new TH1F("h1_nJets_QCD","h1_nJets_QCD", 15,-0.5,14.5);
tree_data->Draw("nJets>>h1_nJets_QCD", (cut_loose + " && ! (" + cut + ")").c_str());

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

cout<<"result of fit with nJets: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_nJets<<" +/- "<<nGJets_value_nJets_err<<" / "<<N_obs_total<<" = "<<nGJets_value_nJets/N_obs_total<<" +/- "<<nGJets_value_nJets_err/N_obs_total<<endl;
cout<<"fraction of Gjets = "<<nQCD_value_nJets<<" +/- "<<nQCD_value_nJets_err<<" / "<<N_obs_total<<" = "<<nQCD_value_nJets/N_obs_total<<" +/- "<<nQCD_value_nJets_err/N_obs_total<<endl;

//Pt
TH1F *h1_Pt_Data = new TH1F("h1_Pt_Data","h1_Pt_Data", 100, 50., 1500);
tree_data->Draw("pho1Pt>>h1_Pt_Data", cut.c_str());

TH1F *h1_Pt_GJets = new TH1F("h1_Pt_GJets","h1_Pt_GJets", 100, 50., 1500);
tree_data->Draw("pho1Pt>>h1_Pt_GJets", cut_GJets.c_str());

TH1F *h1_Pt_QCD = new TH1F("h1_Pt_QCD","h1_Pt_QCD", 100, 50., 1500);
tree_data->Draw("pho1Pt>>h1_Pt_QCD", (cut_loose + " && ! (" + cut + ")").c_str());

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

cout<<"result of fit with Pt: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_Pt<<" +/- "<<nGJets_value_Pt_err<<" / "<<N_obs_total<<" = "<<nGJets_value_Pt/N_obs_total<<" +/- "<<nGJets_value_Pt_err/N_obs_total<<endl;
cout<<"fraction of Gjets = "<<nQCD_value_Pt<<" +/- "<<nQCD_value_Pt_err<<" / "<<N_obs_total<<" = "<<nQCD_value_Pt/N_obs_total<<" +/- "<<nQCD_value_Pt_err/N_obs_total<<endl;


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
cout<<"fraction of Gjets = "<<nGJets_value_SigmaIetaIeta<<" / "<<nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta<<" = "<<nGJets_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta)<<endl;
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
tree_signal->Draw("MET:pho1ClusterTime>>h2Sig", cut.c_str());

h2GJets->Scale((1.0*h2Data->Integral())/(1.0*h2GJets->Integral()));
h2QCD->Scale((1.0*h2Data->Integral())/(1.0*h2QCD->Integral()));
h2Sig->Scale((1.0*h2Data->Integral())/(1.0*h2Sig->Integral()));

cout<<"BbinsX = "<<h2GJets->GetNbinsX()<<endl;
cout<<"BbinsY = "<<h2GJets->GetNbinsY()<<endl;

//////////bkg+sig fit////////////////
RooWorkspace * w_DataBkgSig;
TString _sigModelName (sigModelName.c_str());
TString _sigModelTitle (sigModelTitle.c_str());
w_DataBkgSig = Fit2DMETTimeDataBkgSig( h2Data, h2GJets, h2QCD, h2Sig, nGJets_value_sigmaEOverE, nGJets_value_sigmaEOverE_err, nQCD_value_sigmaEOverE, nQCD_value_sigmaEOverE_err, _sigModelName, _sigModelTitle, true);
w_DataBkgSig->Write("w_DataBkgSig");
float nGJets_2DFit_DataBkgSig = w_DataBkgSig->var("nGJets")->getValV();
float nGJets_2DFit_DataBkgSig_Err = w_DataBkgSig->var("nGJets")->getError();
float nQCD_2DFit_DataBkgSig = w_DataBkgSig->var("nQCD")->getValV();
float nQCD_2DFit_DataBkgSig_Err = w_DataBkgSig->var("nQCD")->getError();
float nSig_2DFit_DataBkgSig = w_DataBkgSig->var("nSig")->getValV();
float nSig_2DFit_DataBkgSig_Err = w_DataBkgSig->var("nSig")->getError();


//////////background only fit///////////////

RooWorkspace * w_DataBkg;
//w_DataBkg = Fit2DMETTimeDataBkg( tree_data->CopyTree( cut.c_str() ), tree_data->CopyTree( cut_GJets.c_str() ), tree_data->CopyTree( (cut_loose + " && ! (" + cut + ")").c_str() ), nGJets_value_sigmaEOverE, nGJets_value_sigmaEOverE_err, nQCD_value_sigmaEOverE, nQCD_value_sigmaEOverE_err);
w_DataBkg = Fit2DMETTimeDataBkg( h2Data, h2GJets, h2QCD, nGJets_value_sigmaEOverE, nGJets_value_sigmaEOverE_err, nQCD_value_sigmaEOverE, nQCD_value_sigmaEOverE_err);
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

printf("%s & %d & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f \\\\ \n", sigModelName.c_str(), N_obs_total, nGJets_2DFit_DataBkgSig, nGJets_2DFit_DataBkgSig_Err, nQCD_2DFit_DataBkgSig, nQCD_2DFit_DataBkgSig_Err);

cout<<"result of 2D fit with bkg + sig: " <<endl;
cout<<"N_obs in data = "<<N_obs_total<<endl;
cout<<"GJets yield = "<<nGJets_2DFit_DataBkgSig<<" +/- "<<nGJets_2DFit_DataBkgSig_Err<<"  (fraction: "<<nGJets_2DFit_DataBkgSig/N_obs_total<<" )"<<endl;
cout<<"QCD yield = "<<nQCD_2DFit_DataBkgSig<<" +/- "<<nQCD_2DFit_DataBkgSig_Err<<"  (fraction: "<<nQCD_2DFit_DataBkgSig/N_obs_total<<" )"<<endl;
cout<<"Sig yield = "<<nSig_2DFit_DataBkgSig<<" +/- "<<nSig_2DFit_DataBkgSig_Err<<"  (fraction: "<<nSig_2DFit_DataBkgSig/N_obs_total<<" )"<<endl;

printf("%s & %d & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f \\\\ \n", sigModelName.c_str(), N_obs_total, nGJets_2DFit_DataBkgSig, nGJets_2DFit_DataBkgSig_Err, nQCD_2DFit_DataBkgSig, nQCD_2DFit_DataBkgSig_Err, nSig_2DFit_DataBkgSig, nSig_2DFit_DataBkgSig_Err);

return 0;
}
