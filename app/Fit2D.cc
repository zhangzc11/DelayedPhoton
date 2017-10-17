//C++ INCLUDES
#include <iostream>
//ROOT INCLUDES
#include <TFile.h>
#include <TTree.h>
#include <TMath.h>
#include <TH1F.h>
#include <TROOT.h>
#include <THStack.h>
#include <TColor.h>
//LOCAL INCLUDES
#include "MakeFitMETTime.hh"

using namespace std;

int main( int argc, char* argv[])
{
srand(time(NULL));
gROOT->Reset();
gROOT->SetBatch(1);


std::string inputFileName_data = argv[1];
std::string inputFileName_signal = argv[2];
//std::string inputFileName_qcd = argv[3];
//std::string inputFileName_gjets = argv[4];
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

/*
if(inputFileName_qcd == "")
{
	std::cerr << "[ERROR]: please provide an input file for qcd" << std::endl;
	return -1;
}
std::cout<<"using input file for qcd: "<<inputFileName_qcd<<std::endl;

if(inputFileName_gjets == "")
{
	std::cerr << "[ERROR]: please provide an input file for gjets" << std::endl;
	return -1;
}
std::cout<<"using input file for gjets: "<<inputFileName_gjets<<std::endl;
*/


TFile *file_data;
TFile *file_signal;
//TFile *file_qcd;
//TFile *file_gjets;

TTree *tree_data;
TTree *tree_signal;
//TTree *tree_qcd;
//TTree *tree_gjets;

file_data = new TFile(inputFileName_data.c_str(), "READ");
tree_data = (TTree*)file_data->Get(treeName.c_str());

file_signal = new TFile(inputFileName_signal.c_str(), "READ");
tree_signal = (TTree*)file_signal->Get(treeName.c_str());

//file_qcd = new TFile(inputFileName_qcd.c_str(), "READ");
//tree_qcd = (TTree*)file_qcd->Get(treeName.c_str());

//file_gjets = new TFile(inputFileName_gjets.c_str(), "READ");
//tree_gjets = (TTree*)file_gjets->Get(treeName.c_str());

TFile *f_Out = new TFile("result.root","recreate");

/**********fit SigmaIetaIeta to get relative yield of GJets and QCD backgrounds *****/
/*
TH1F *h1_SigmaIetaIeta_GJets = new TH1F("h1_SigmaIetaIeta_GJets","h1_SigmaIetaIeta_GJets", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_GJets", cut_GJets.c_str());

TH1F *h1_SigmaIetaIeta_QCD = new TH1F("h1_SigmaIetaIeta_QCD","h1_SigmaIetaIeta_QCD", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_QCD", (cut_loose + " && ! (" + cut + ")").c_str());

h1_SigmaIetaIeta_GJets->Scale(1.0/h1_SigmaIetaIeta_GJets->Integral());
h1_SigmaIetaIeta_QCD->Scale(1.0/h1_SigmaIetaIeta_QCD->Integral());

RooWorkspace * w_frac_SigmaIetaIeta;
w_frac_SigmaIetaIeta = FitDataBkgFraction(tree_data->CopyTree( cut.c_str() ), "pho1SigmaIetaIeta", "#sigma_{i#etai#eta}", "", 0.005, 0.025, h1_SigmaIetaIeta_GJets, h1_SigmaIetaIeta_QCD);
w_frac_SigmaIetaIeta->Write("w_frac_SigmaIetaIeta");

float nGJets_value_SigmaIetaIeta = w_frac_SigmaIetaIeta->var("nGJets")->getValV();
float nQCD_value_SigmaIetaIeta = w_frac_SigmaIetaIeta->var("nQCD")->getValV();
h1_SigmaIetaIeta_GJets->Scale(nGJets_value_SigmaIetaIeta);
h1_SigmaIetaIeta_QCD->Scale(nQCD_value_SigmaIetaIeta);
h1_SigmaIetaIeta_GJets->Write();
h1_SigmaIetaIeta_QCD->Write();

cout<<"result of fit with SigmaIetaIeta: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_SigmaIetaIeta<<" / "<<nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta<<" = "<<nGJets_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta)<<endl;
cout<<"fraction of Gjets = "<<nQCD_value_SigmaIetaIeta<<" / "<<nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta<<" = "<<nQCD_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta)<<endl;

*/

TH1F *h1_PhoPt_data = new TH1F("h1_PhoPt_data","h1_PhoPt_data", 100, 50, 1000);
tree_data->Draw("pho1Pt>>h1_PhoPt_data", cut.c_str());
TH1F *h1_PhoPt_GJets = new TH1F("h1_PhoPt_GJets","h1_PhoPt_GJets", 100, 50, 1000);
tree_data->Draw("pho1Pt>>h1_PhoPt_GJets", cut_GJets.c_str());
TH1F *h1_PhoPt_QCD = new TH1F("h1_PhoPt_QCD","h1_PhoPt_QCD", 100, 50, 1000);
tree_data->Draw("pho1Pt>>h1_PhoPt_QCD", (cut_loose + " && ! (" + cut + ")").c_str());
h1_PhoPt_GJets->Scale(1.0*h1_PhoPt_data->Integral()/h1_PhoPt_GJets->Integral());
h1_PhoPt_QCD->Scale(1.0*h1_PhoPt_data->Integral()/h1_PhoPt_QCD->Integral());

TFractionFitter* fit_PhoPt;
fit_PhoPt = FitDataBkgFractionFilter(h1_PhoPt_data, h1_PhoPt_GJets, h1_PhoPt_QCD);
Double_t nGJets_value_PhoPt, nGJets_value_PhoPt_err, nQCD_value_PhoPt, nQCD_value_PhoPt_err;
fit_PhoPt->GetResult(0, nGJets_value_PhoPt, nGJets_value_PhoPt_err);
fit_PhoPt->GetResult(1, nQCD_value_PhoPt, nQCD_value_PhoPt_err);

cout<<"result of fit with PhoPt: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_PhoPt<<" / "<<nGJets_value_PhoPt+nQCD_value_PhoPt<<" = "<<nGJets_value_PhoPt/(nGJets_value_PhoPt+nQCD_value_PhoPt)<<endl;
cout<<"fraction of QCD = "<<nQCD_value_PhoPt<<" / "<<nGJets_value_PhoPt+nQCD_value_PhoPt<<" = "<<nQCD_value_PhoPt/(nGJets_value_PhoPt+nQCD_value_PhoPt)<<endl;


//another fit with SigmaIetaIeta
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

//another fit with nJets
TH1F *h1_nJets_data = new TH1F("h1_nJets_data","h1_nJets_data", 15,-0.5,14.5);
tree_data->Draw("n_Jets>>h1_nJets_data", cut.c_str());
TH1F *h1_nJets_GJets = new TH1F("h1_nJets_GJets","h1_nJets_GJets", 15,-0.5,14.5);
tree_data->Draw("n_Jets>>h1_nJets_GJets", cut_GJets.c_str());
TH1F *h1_nJets_QCD = new TH1F("h1_nJets_QCD","h1_nJets_QCD", 15,-0.5,14.5);
tree_data->Draw("n_Jets>>h1_nJets_QCD", (cut_loose + " && ! (" + cut + ")").c_str());
h1_nJets_GJets->Scale(1.0*h1_nJets_data->Integral()/h1_nJets_GJets->Integral());
h1_nJets_QCD->Scale(1.0*h1_nJets_data->Integral()/h1_nJets_QCD->Integral());

TFractionFitter* fit_nJets;
fit_nJets = FitDataBkgFractionFilter(h1_nJets_data, h1_nJets_GJets, h1_nJets_QCD);
Double_t nGJets_value_nJets, nGJets_value_nJets_err, nQCD_value_nJets, nQCD_value_nJets_err;
fit_nJets->GetResult(0, nGJets_value_nJets, nGJets_value_nJets_err);
fit_nJets->GetResult(1, nQCD_value_nJets, nQCD_value_nJets_err);

cout<<"result of fit with nJets: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_nJets<<" / "<<nGJets_value_nJets+nQCD_value_nJets<<" = "<<nGJets_value_nJets/(nGJets_value_nJets+nQCD_value_nJets)<<endl;
cout<<"fraction of QCD = "<<nQCD_value_nJets<<" / "<<nGJets_value_nJets+nQCD_value_nJets<<" = "<<nQCD_value_nJets/(nGJets_value_nJets+nQCD_value_nJets)<<endl;

//another fit with sigmaEOverE
TH1F *h1_sigmaEOverE_data = new TH1F("h1_sigmaEOverE_data","h1_sigmaEOverE_data", 100,0.,0.5);
tree_data->Draw("pho1sigmaEOverE>>h1_sigmaEOverE_data", cut.c_str());
TH1F *h1_sigmaEOverE_GJets = new TH1F("h1_sigmaEOverE_GJets","h1_sigmaEOverE_GJets", 100,0.,0.5);
tree_data->Draw("pho1sigmaEOverE>>h1_sigmaEOverE_GJets", cut_GJets.c_str());
TH1F *h1_sigmaEOverE_QCD = new TH1F("h1_sigmaEOverE_QCD","h1_sigmaEOverE_QCD", 100,0.,0.5);
tree_data->Draw("pho1sigmaEOverE>>h1_sigmaEOverE_QCD", (cut_loose + " && ! (" + cut + ")").c_str());
h1_sigmaEOverE_GJets->Scale(1.0*h1_sigmaEOverE_data->Integral()/h1_sigmaEOverE_GJets->Integral());
h1_sigmaEOverE_QCD->Scale(1.0*h1_sigmaEOverE_data->Integral()/h1_sigmaEOverE_QCD->Integral());

TFractionFitter* fit_sigmaEOverE;
fit_sigmaEOverE = FitDataBkgFractionFilter(h1_sigmaEOverE_data, h1_sigmaEOverE_GJets, h1_sigmaEOverE_QCD);
Double_t nGJets_value_sigmaEOverE, nGJets_value_sigmaEOverE_err, nQCD_value_sigmaEOverE, nQCD_value_sigmaEOverE_err;
fit_sigmaEOverE->GetResult(0, nGJets_value_sigmaEOverE, nGJets_value_sigmaEOverE_err);
fit_sigmaEOverE->GetResult(1, nQCD_value_sigmaEOverE, nQCD_value_sigmaEOverE_err);

cout<<"result of fit with sigmaEOverE: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_sigmaEOverE<<" / "<<nGJets_value_sigmaEOverE+nQCD_value_sigmaEOverE<<" = "<<nGJets_value_sigmaEOverE/(nGJets_value_sigmaEOverE+nQCD_value_sigmaEOverE)<<endl;
cout<<"fraction of QCD = "<<nQCD_value_sigmaEOverE<<" / "<<nGJets_value_sigmaEOverE+nQCD_value_sigmaEOverE<<" = "<<nQCD_value_sigmaEOverE/(nGJets_value_sigmaEOverE+nQCD_value_sigmaEOverE)<<endl;

//another fit with Smajor
TH1F *h1_Smajor_data = new TH1F("h1_Smajor_data","h1_Smajor_data", 100, 0., 1.0);
tree_data->Draw("pho1Smajor>>h1_Smajor_data", cut.c_str());
TH1F *h1_Smajor_GJets = new TH1F("h1_Smajor_GJets","h1_Smajor_GJets", 100, 0., 1.0);
tree_data->Draw("pho1Smajor>>h1_Smajor_GJets", cut_GJets.c_str());
TH1F *h1_Smajor_QCD = new TH1F("h1_Smajor_QCD","h1_Smajor_QCD", 100, 0., 1.0);
tree_data->Draw("pho1Smajor>>h1_Smajor_QCD", (cut_loose + " && ! (" + cut + ")").c_str());
h1_Smajor_GJets->Scale(1.0*h1_Smajor_data->Integral()/h1_Smajor_GJets->Integral());
h1_Smajor_QCD->Scale(1.0*h1_Smajor_data->Integral()/h1_Smajor_QCD->Integral());

TFractionFitter* fit_Smajor;
fit_Smajor = FitDataBkgFractionFilter(h1_Smajor_data, h1_Smajor_GJets, h1_Smajor_QCD);
Double_t nGJets_value_Smajor, nGJets_value_Smajor_err, nQCD_value_Smajor, nQCD_value_Smajor_err;
fit_Smajor->GetResult(0, nGJets_value_Smajor, nGJets_value_Smajor_err);
fit_Smajor->GetResult(1, nQCD_value_Smajor, nQCD_value_Smajor_err);

cout<<"result of fit with Smajor: " <<endl;
cout<<"fraction of Gjets = "<<nGJets_value_Smajor<<" / "<<nGJets_value_Smajor+nQCD_value_Smajor<<" = "<<nGJets_value_Smajor/(nGJets_value_Smajor+nQCD_value_Smajor)<<endl;
cout<<"fraction of QCD = "<<nQCD_value_Smajor<<" / "<<nGJets_value_Smajor+nQCD_value_Smajor<<" = "<<nQCD_value_Smajor/(nGJets_value_Smajor+nQCD_value_Smajor)<<endl;


return 0;
}
