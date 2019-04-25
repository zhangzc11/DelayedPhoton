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

const Int_t Nbins_MET = 2;
const Int_t Nbins_time = 2;

std::vector <float> xbins_MET;
std::vector <float> xbins_time;

bool useBDT = true;

float lumi = 35922.0; //pb^-1
float NEvents_sig = 1.0;
bool _useToy = true;

std::string binningAlgorithm = "limit";//or "significance"

bool doAllBkgFracFit = false;


//binning setup for 2x2 time and met, with 6 categories

int BIN_CATEGORY = 0;
float time_split_by_CAT[7] = {1.5, 0.0, 1.5, 1.5, 0.0, 1.5, 1.0};
//float time_split_by_CAT[6] = {1.5, 0.25, 1.5, 1.5, 0.5, 1.5};
float met_split_by_CAT[7] = {300.0, 250.0, 100.0, 300.0, 250.0, 150.0, 300.0};
//float met_split_by_CAT[6] = {300.0, 200.0, 100.0, 300.0, 300.0, 125.0};


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
std::string category = argv[5];
std::string fitMode = argv[6]; 
std::string s_useBDT = argv[7]; 
std::string _SoverB = "";
std::string _nToys = "";

if(fitMode == "bias" && argc >= 9) _SoverB = argv[8]; 
if(fitMode == "bias" && argc >= 10) _nToys = argv[9]; 


if(s_useBDT == "")
{
        std::cerr << "[ERROR]: please provide the photon ID choice - whether useBDT or not (yes or no)" << std::endl;
        return -1;
}
else if (s_useBDT == "yes")
{
	useBDT = true;
	cout<<"photon ID: BDT"<<endl;
}
else if (s_useBDT == "no")
{
	useBDT = false;
	cout<<"photon ID: EGM cut-based"<<endl;
}
else
{
	std::cerr << "[ERROR]: please provide the photon ID choice - whether useBDT or not (yes or no)" << std::endl;
        return -1;
}


float SoverB = 0.0;
int nToys = 1000;

//assign binning category:
if (sigModelName.find("L100TeV") != std::string::npos || sigModelName.find("L150TeV") != std::string::npos || sigModelName.find("L200TeV") != std::string::npos || sigModelName.find("L250TeV") != std::string::npos|| sigModelName.find("L300TeV") != std::string::npos)
{
if (sigModelName.find("Ctau0_001cm") != std::string::npos || sigModelName.find("Ctau0_1cm") != std::string::npos || sigModelName.find("Ctau1cm") != std::string::npos) BIN_CATEGORY = 0;
else if (sigModelName.find("Ctau10cm") != std::string::npos) BIN_CATEGORY = 1;
else BIN_CATEGORY = 2;
}
else
{
if (sigModelName.find("Ctau0_001cm") != std::string::npos || sigModelName.find("Ctau0_1cm") != std::string::npos || sigModelName.find("Ctau1cm") != std::string::npos) BIN_CATEGORY = 3;
else if (sigModelName.find("Ctau10cm") != std::string::npos ) BIN_CATEGORY = 4;
else BIN_CATEGORY = 5;
}

if(sigModelName.find("L100TeV") != std::string::npos && sigModelName.find("Ctau10000cm") != std::string::npos) BIN_CATEGORY = 6;

TString _sigModelName (sigModelName.c_str());
TString _sigModelTitle (sigModelTitle.c_str());

float xsec = getXsecBR(sigModelName); //pb
if (sigModelName.find("L100TeV") != std::string::npos) xsec = xsec * 0.01; // for L100TeV models, give smaller xsec to reduce signal yield and stablize fit

std::string treeName = "DelayedPhoton";

std::string cut, cut_JESUp, cut_JESDown, cut_phoScaleUp, cut_phoScaleDown, cut_phoSmearUp, cut_phoSmearDown;

std::string weight_cut = "weight*pileupWeight*triggerEffSFWeight*photonEffSF* ";

std::string cut_MET_filter = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0" ;

std::string cut_pho1Tight = " && pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0";
std::string cut_pho1Tight_scaleUp = " && pho1Pt_scaleUp > 70 && pho1R9 > 0.9&& abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight ";
std::string cut_pho1Tight_scaleDown = " && pho1Pt_scaleDown > 70 && pho1R9 > 0.9&& abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight ";
std::string cut_pho1Tight_smearUp = " && pho1Pt_smearUp > 70 && pho1R9 > 0.9&& abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight ";
std::string cut_pho1Tight_smearDown = " && pho1Pt_smearDown > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight ";


if(category == "2J")
{
	if(!useBDT)
	{
		cut = "n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight;
		cut_JESUp = "n_Jets_JESUp == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight;
		cut_JESDown = "n_Jets_JESDown == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight;
		cut_phoScaleUp = "n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight_scaleUp;
		cut_phoScaleDown = "n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight_scaleDown;
		cut_phoSmearUp = "n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight_smearUp;
		cut_phoSmearDown = "n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight_smearDown;
	}
	else
	{
		cut = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_JESUp = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets_JESUp == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_JESDown = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets_JESDown == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_phoScaleUp = "pho1Pt_scaleUp > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_phoScaleDown = "pho1Pt_scaleDown > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_phoSmearUp = "pho1Pt_smearUp > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_phoSmearDown = "pho1Pt_smearDown > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
	}
}

else if(category == "3J")
{
	if(!useBDT)
	{
		cut = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight;
		cut_JESUp = "n_Jets_JESUp > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight;
		cut_JESDown = "n_Jets_JESDown > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight;
		cut_phoScaleUp = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight_scaleUp;
		cut_phoScaleDown = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight_scaleDown;
		cut_phoSmearUp = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight_smearUp;
		cut_phoSmearDown = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter + cut_pho1Tight_smearDown;
	}
	else
	{
		cut = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_JESUp = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets_JESUp > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_JESDown = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets_JESDown > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_phoScaleUp = "pho1Pt_scaleUp > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_phoScaleDown = "pho1Pt_scaleDown > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_phoSmearUp = "pho1Pt_smearUp > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
		cut_phoSmearDown = "pho1Pt_smearDown > 70 && abs(pho1Eta)<1.4442 && disc > 0.10 && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   " + cut_MET_filter;
	}
}

else
{
	std::cerr << "[ERROR]: please provide a valid category: 2J or 3J" << std::endl;
	return -1;
}


cout<<"cut --> "<<cut<<endl;

TString outPlotsDir;
if(category == "2J" && useBDT ) outPlotsDir = "plots_2J_withBDT";
if(category == "2J" && !useBDT ) outPlotsDir = "plots_2J_noBDT";
if(category == "3J" && useBDT ) outPlotsDir = "plots_3J_withBDT";
if(category == "3J" && !useBDT ) outPlotsDir = "plots_3J_noBDT";
std::string _outPlotsDir (((const char*) outPlotsDir));

TString outBinningDir;
if(category == "2J" && useBDT) outBinningDir = "binning_2J_withBDT";
if(category == "2J" && !useBDT) outBinningDir = "binning_2J_noBDT";
if(category == "3J" && useBDT) outBinningDir = "binning_3J_withBDT";
if(category == "3J" && !useBDT) outBinningDir = "binning_3J_noBDT";
std::string _outBinningDir ((const char*) outBinningDir);

TString outDataCardsDir;
if(category == "2J" && useBDT) outDataCardsDir = "datacards_2J_withBDT";
if(category == "2J" && !useBDT) outDataCardsDir = "datacards_2J_noBDT";
if(category == "3J" && useBDT) outDataCardsDir = "datacards_3J_withBDT";
if(category == "3J" && !useBDT) outDataCardsDir = "datacards_3J_noBDT";
std::string _outDataCardsDir ((const char*) outDataCardsDir);	

TString outBiasDir;
if(category == "2J" && useBDT) outBiasDir = "bias_2J_withBDT";
if(category == "2J" && !useBDT) outBiasDir = "bias_2J_noBDT";
if(category == "3J" && useBDT) outBiasDir = "bias_3J_withBDT";
if(category == "3J" && !useBDT) outBiasDir = "bias_3J_noBDT";
std::string _outBiasDir ((const char*) outBiasDir);
	
if(inputFileName_data == "")
{
	std::cerr << "[ERROR]: please provide an input file for data" << std::endl;
	return -1;
}

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

mkdir("fit_results", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/plots_2J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/plots_2J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/plots_3J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/plots_3J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/datacards_2J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/datacards_2J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/datacards_3J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/datacards_3J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/datacards_temp", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/binning_2J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/binning_2J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/binning_3J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016ABCD/binning_3J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);


std::cout<<"signal xsec*BR = "<<xsec<<endl;

TFile *file_data;
TFile *file_signal;

TTree *tree_data;
TTree *tree_signal;


std::cout<<"reading signal file......"<<endl;
file_signal = new TFile(inputFileName_signal.c_str(), "READ");
tree_signal = (TTree*)file_signal->Get(treeName.c_str());
TH1F *h1_NEvents_sig = (TH1F*) file_signal->Get("NEvents");
NEvents_sig = h1_NEvents_sig->GetBinContent(1);

if(fitMode == "scaleSys")
{
	float time_2x2_bins[3] = {-2.0, time_split_by_CAT[BIN_CATEGORY], 25.0};
	float met_2x2_bins[3] = {0.0, met_split_by_CAT[BIN_CATEGORY], 9000.0};

	TH2F *h2_2x2binsig0 = new TH2F("h2_2x2binsig0","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2_2x2binsig0", (weight_cut + "( "+cut+" )").c_str());
	float N_sig0_expected = 1.0*lumi*xsec*h2_2x2binsig0->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig0->Scale((1.0*N_sig0_expected)/(1.0*h2_2x2binsig0->Integral()));


	TH2F *h2_2x2binsig_phoScaleUp = new TH2F("h2_2x2binsig_phoScaleUp","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET_phoScaleUp:pho1ClusterTime_SmearToData>>h2_2x2binsig_phoScaleUp", (weight_cut + "( "+cut_phoScaleUp+" )").c_str());
	float N_sig_phoScaleUp_expected = 1.0*lumi*xsec*h2_2x2binsig_phoScaleUp->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_phoScaleUp->Scale((1.0*N_sig_phoScaleUp_expected)/(1.0*h2_2x2binsig_phoScaleUp->Integral()));

	TH2F *h2_2x2binsig_phoScaleDown = new TH2F("h2_2x2binsig_phoScaleDown","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET_phoScaleDown:pho1ClusterTime_SmearToData>>h2_2x2binsig_phoScaleDown", (weight_cut + "( "+cut_phoScaleDown+" )").c_str());
	float N_sig_phoScaleDown_expected = 1.0*lumi*xsec*h2_2x2binsig_phoScaleDown->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_phoScaleDown->Scale((1.0*N_sig_phoScaleDown_expected)/(1.0*h2_2x2binsig_phoScaleDown->Integral()));


	TH2F *h2_2x2binsig_phoSmearUp = new TH2F("h2_2x2binsig_phoSmearUp","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET_phoSmearUp:pho1ClusterTime_SmearToData>>h2_2x2binsig_phoSmearUp", (weight_cut + "( "+cut_phoSmearUp+" )").c_str());
	float N_sig_phoSmearUp_expected = 1.0*lumi*xsec*h2_2x2binsig_phoSmearUp->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_phoSmearUp->Scale((1.0*N_sig_phoSmearUp_expected)/(1.0*h2_2x2binsig_phoSmearUp->Integral()));

	TH2F *h2_2x2binsig_phoSmearDown = new TH2F("h2_2x2binsig_phoSmearDown","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET_phoSmearDown:pho1ClusterTime_SmearToData>>h2_2x2binsig_phoSmearDown", (weight_cut + "( "+cut_phoSmearDown+" )").c_str());
	float N_sig_phoSmearDown_expected = 1.0*lumi*xsec*h2_2x2binsig_phoSmearDown->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_phoSmearDown->Scale((1.0*N_sig_phoSmearDown_expected)/(1.0*h2_2x2binsig_phoSmearDown->Integral()));


	TH2F *h2_2x2binsig_JESUp = new TH2F("h2_2x2binsig_JESUp","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET_JESUp:pho1ClusterTime_SmearToData>>h2_2x2binsig_JESUp", (weight_cut + "( "+cut_JESUp+" )").c_str());
	float N_sig_JESUp_expected = 1.0*lumi*xsec*h2_2x2binsig_JESUp->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_JESUp->Scale((1.0*N_sig_JESUp_expected)/(1.0*h2_2x2binsig_JESUp->Integral()));


	TH2F *h2_2x2binsig_JESDown = new TH2F("h2_2x2binsig_JESDown","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET_JESDown:pho1ClusterTime_SmearToData>>h2_2x2binsig_JESDown", (weight_cut + "( "+cut_JESDown+" )").c_str());
	float N_sig_JESDown_expected = 1.0*lumi*xsec*h2_2x2binsig_JESDown->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_JESDown->Scale((1.0*N_sig_JESDown_expected)/(1.0*h2_2x2binsig_JESDown->Integral()));

	TH2F *h2_2x2binsig_timeScaleUp = new TH2F("h2_2x2binsig_timeScaleUp","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET:pho1ClusterTime_scaleUp>>h2_2x2binsig_timeScaleUp", (weight_cut + "( "+cut+" )").c_str());
	float N_sig_timeScaleUp_expected = 1.0*lumi*xsec*h2_2x2binsig_timeScaleUp->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_timeScaleUp->Scale((1.0*N_sig_timeScaleUp_expected)/(1.0*h2_2x2binsig_timeScaleUp->Integral()));


	TH2F *h2_2x2binsig_timeScaleDown = new TH2F("h2_2x2binsig_timeScaleDown","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET:pho1ClusterTime_scaleDown>>h2_2x2binsig_timeScaleDown", (weight_cut + "( "+cut+" )").c_str());
	float N_sig_timeScaleDown_expected = 1.0*lumi*xsec*h2_2x2binsig_timeScaleDown->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_timeScaleDown->Scale((1.0*N_sig_timeScaleDown_expected)/(1.0*h2_2x2binsig_timeScaleDown->Integral()));

	TH2F *h2_2x2binsig_timeSmearUp = new TH2F("h2_2x2binsig_timeSmearUp","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET:pho1ClusterTime_smearUp>>h2_2x2binsig_timeSmearUp", (weight_cut + "( "+cut+" )").c_str());
	float N_sig_timeSmearUp_expected = 1.0*lumi*xsec*h2_2x2binsig_timeSmearUp->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_timeSmearUp->Scale((1.0*N_sig_timeSmearUp_expected)/(1.0*h2_2x2binsig_timeSmearUp->Integral()));


	TH2F *h2_2x2binsig_timeSmearDown = new TH2F("h2_2x2binsig_timeSmearDown","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	tree_signal->Draw("t1MET:pho1ClusterTime_smearDown>>h2_2x2binsig_timeSmearDown", (weight_cut + "( "+cut+" )").c_str());
	float N_sig_timeSmearDown_expected = 1.0*lumi*xsec*h2_2x2binsig_timeSmearDown->Integral()/(1.0*NEvents_sig);
	h2_2x2binsig_timeSmearDown->Scale((1.0*N_sig_timeSmearDown_expected)/(1.0*h2_2x2binsig_timeSmearDown->Integral()));


	FILE * m_outfile = fopen(("fit_results/2016ABCD/"+_outDataCardsDir+"/scaleSys_"+sigModelName+".txt").c_str(), "w");

	for(int iT=1;iT<= 2; iT++)
	{
		for(int iM=1;iM<= 2; iM++)
		{
			float Nsig0 = h2_2x2binsig0->GetBinContent(iT, iM);
			float Nsig_phoScaleUp = h2_2x2binsig_phoScaleUp->GetBinContent(iT, iM);
			float Nsig_phoScaleDown = h2_2x2binsig_phoScaleDown->GetBinContent(iT, iM);
			float Nsig_phoSmearUp = h2_2x2binsig_phoSmearUp->GetBinContent(iT, iM);
			float Nsig_phoSmearDown = h2_2x2binsig_phoSmearDown->GetBinContent(iT, iM);
			float Nsig_JESUp = h2_2x2binsig_JESUp->GetBinContent(iT, iM);
			float Nsig_JESDown = h2_2x2binsig_JESDown->GetBinContent(iT, iM);
			float Nsig_timeScaleUp = h2_2x2binsig_timeScaleUp->GetBinContent(iT, iM);
			float Nsig_timeScaleDown = h2_2x2binsig_timeScaleDown->GetBinContent(iT, iM);
			float Nsig_timeSmearUp = h2_2x2binsig_timeSmearUp->GetBinContent(iT, iM);
			float Nsig_timeSmearDown = h2_2x2binsig_timeSmearDown->GetBinContent(iT, iM);
			
			float errNsig0 = h2_2x2binsig0->GetBinError(iT, iM);
			float errNsig_phoScaleUp = h2_2x2binsig_phoScaleUp->GetBinError(iT, iM);
			float errNsig_phoScaleDown = h2_2x2binsig_phoScaleDown->GetBinError(iT, iM);
			float errNsig_phoSmearUp = h2_2x2binsig_phoSmearUp->GetBinError(iT, iM);
			float errNsig_phoSmearDown = h2_2x2binsig_phoSmearDown->GetBinError(iT, iM);
			float errNsig_JESUp = h2_2x2binsig_JESUp->GetBinError(iT, iM);
			float errNsig_JESDown = h2_2x2binsig_JESDown->GetBinError(iT, iM);
			float errNsig_timeScaleUp = h2_2x2binsig_timeScaleUp->GetBinError(iT, iM);
			float errNsig_timeScaleDown = h2_2x2binsig_timeScaleDown->GetBinError(iT, iM);
			float errNsig_timeSmearUp = h2_2x2binsig_timeSmearUp->GetBinError(iT, iM);
			float errNsig_timeSmearDown = h2_2x2binsig_timeSmearDown->GetBinError(iT, iM);
			
			float r_phoScaleUp = 100.0*(Nsig_phoScaleUp/Nsig0 - 1.0);
			float r_phoScaleUp_err = 100.0*(Nsig_phoScaleUp/Nsig0 * sqrt(errNsig_phoScaleUp*errNsig_phoScaleUp/(Nsig_phoScaleUp*Nsig_phoScaleUp) + errNsig0*errNsig0/(Nsig0*Nsig0)));
			float r_phoScaleDown = 100.0*(Nsig_phoScaleDown/Nsig0 - 1.0);
			float r_phoScaleDown_err = 100.0*(Nsig_phoScaleDown/Nsig0 * sqrt(errNsig_phoScaleDown*errNsig_phoScaleDown/(Nsig_phoScaleDown*Nsig_phoScaleDown) + errNsig0*errNsig0/(Nsig0*Nsig0)));
			float r_phoSmearUp = 100.0*(Nsig_phoSmearUp/Nsig0 - 1.0);
			float r_phoSmearUp_err = 100.0*(Nsig_phoSmearUp/Nsig0 * sqrt(errNsig_phoSmearUp*errNsig_phoSmearUp/(Nsig_phoSmearUp*Nsig_phoSmearUp) + errNsig0*errNsig0/(Nsig0*Nsig0)));
			float r_phoSmearDown = 100.0*(Nsig_phoSmearDown/Nsig0 - 1.0);
			float r_phoSmearDown_err = 100.0*(Nsig_phoSmearDown/Nsig0 * sqrt(errNsig_phoSmearDown*errNsig_phoSmearDown/(Nsig_phoSmearDown*Nsig_phoSmearDown) + errNsig0*errNsig0/(Nsig0*Nsig0)));
			float r_JESUp = 100.0*(Nsig_JESUp/Nsig0 - 1.0);
			float r_JESUp_err = 100.0*(Nsig_JESUp/Nsig0 * sqrt(errNsig_JESUp*errNsig_JESUp/(Nsig_JESUp*Nsig_JESUp) + errNsig0*errNsig0/(Nsig0*Nsig0)));\
			float r_JESDown = 100.0*(Nsig_JESDown/Nsig0 - 1.0);
			float r_JESDown_err = 100.0*(Nsig_JESDown/Nsig0 * sqrt(errNsig_JESDown*errNsig_JESDown/(Nsig_JESDown*Nsig_JESDown) + errNsig0*errNsig0/(Nsig0*Nsig0)));
			float r_timeScaleUp = 100.0*(Nsig_timeScaleUp/Nsig0 - 1.0);
			float r_timeScaleUp_err = 100.0*(Nsig_timeScaleUp/Nsig0 * sqrt(errNsig_timeScaleUp*errNsig_timeScaleUp/(Nsig_timeScaleUp*Nsig_timeScaleUp) + errNsig0*errNsig0/(Nsig0*Nsig0)));
			float r_timeScaleDown = 100.0*(Nsig_timeScaleDown/Nsig0 - 1.0);
			float r_timeScaleDown_err = 100.0*(Nsig_timeScaleDown/Nsig0 * sqrt(errNsig_timeScaleDown*errNsig_timeScaleDown/(Nsig_timeScaleDown*Nsig_timeScaleDown) + errNsig0*errNsig0/(Nsig0*Nsig0)));
			float r_timeSmearUp = 100.0*(Nsig_timeSmearUp/Nsig0 - 1.0);
			float r_timeSmearUp_err = 100.0*(Nsig_timeSmearUp/Nsig0 * sqrt(errNsig_timeSmearUp*errNsig_timeSmearUp/(Nsig_timeSmearUp*Nsig_timeSmearUp) + errNsig0*errNsig0/(Nsig0*Nsig0)));
			float r_timeSmearDown = 100.0*(Nsig_timeSmearDown/Nsig0 - 1.0);
			float r_timeSmearDown_err = 100.0*(Nsig_timeSmearDown/Nsig0 * sqrt(errNsig_timeSmearDown*errNsig_timeSmearDown/(Nsig_timeSmearDown*Nsig_timeSmearDown) + errNsig0*errNsig0/(Nsig0*Nsig0)));

			fprintf(m_outfile, "ch%d%d  %5.3f pm %5.3f %5.3f pm %5.3f %5.3f pm %5.3f %5.3f pm %5.3f %5.3f pm %5.3f  %5.3f pm %5.3f %5.3f pm %5.3f %5.3f pm %5.3f %5.3f pm %5.3f %5.3f pm %5.3f\n", iT-1, iM-1, 
				r_phoScaleUp, r_phoScaleUp_err, r_phoScaleDown, r_phoScaleDown_err, 
				r_phoSmearUp, r_phoSmearUp_err, r_phoSmearDown, r_phoSmearDown_err, 
				r_JESUp, r_JESUp_err, r_JESDown, r_JESDown_err, 
				r_timeScaleUp, r_timeScaleUp_err, r_timeScaleDown, r_timeScaleDown_err,
				r_timeSmearUp, r_timeSmearUp_err, r_timeSmearDown, r_timeSmearDown_err);
		}
	}

	return 1;
}


std::cout<<"reading data file......"<<endl;
file_data = new TFile(inputFileName_data.c_str(), "READ");
tree_data = (TTree*)file_data->Get(treeName.c_str());

TH1F *h1_rate_Data_Time_inBins = new TH1F("h2_rate_Data_Time_inBins","; #gamma time bin; Events", Nbins_time, 0, 1.0*Nbins_time);
TH1F *h1_rate_Data_MET_inBins = new TH1F("h2_rate_Data_MET_inBins","; #slash{E}_{T} bin; Events", Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_rate_Data_inBins = new TH2F("h2_rate_Data_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_rate_Sig_inBins = new TH2F("h2_rate_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_rate_MCBkg_inBins = new TH2F("h2_rate_MCBkg_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_rate_SoverSqrtB_inBins = new TH2F("h2_rate_SoverSqrtB_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);

///////////////////////////////////////////////////

std::cout<<"reading background MC file......"<<endl;
std::vector <std::string> sample_MCBkg;
std::vector <float> xsec_MCBkg;
std::vector <TTree*> trees_MCBkg;
std::vector <float> NEvents_MCBkg;

ifstream is_MCBkg_list("data/all_bkg.list");
std::string prefix_filename_MCBkg;
is_MCBkg_list>>prefix_filename_MCBkg;

while(!is_MCBkg_list.eof())
{
        std::string sample_name_MCBkg_thisline;
        std::string xsec_MCBkg_thisline;
        is_MCBkg_list>>sample_name_MCBkg_thisline;
        is_MCBkg_list>>xsec_MCBkg_thisline;
	cout<<"reading MC file: "<<sample_name_MCBkg_thisline<<endl;
	if(sample_name_MCBkg_thisline != "")
        {
                sample_MCBkg.push_back(sample_name_MCBkg_thisline);
                xsec_MCBkg.push_back(strtof(xsec_MCBkg_thisline.c_str(), 0));
                TFile * file_MCBkg_this = new TFile((prefix_filename_MCBkg+sample_name_MCBkg_thisline+".root").c_str(), "READ");
                trees_MCBkg.push_back((TTree*)file_MCBkg_this->Get(treeName.c_str()));
                TH1F * h1_MCBkg_NEvents_this =  (TH1F*)file_MCBkg_this->Get("NEvents");
                NEvents_MCBkg.push_back(h1_MCBkg_NEvents_this->GetBinContent(1));
        }

}

///////////////////////////Binning optimization
cout<<"Reading MCBkg list.... sample - xsec - NEvents - NEntries : "<<endl;
for(int i=0; i<xsec_MCBkg.size(); i++)
{
        cout<<sample_MCBkg[i]<<"   "<<xsec_MCBkg[i]<<"   "<<NEvents_MCBkg[i]<<"   "<<trees_MCBkg[i]->GetEntries()<<endl;
}

if(binningAlgorithm == "significance" && fitMode == "binAndDatacard")
{
	float time_Low = -15.0;
	float time_High = 15.0;
	int time_N_fine = 600;

	float met_Low = 0.0;
	float met_High = 1000.0;
	int met_N_fine = 400;

	std::vector <int> timeBin;
	std::vector <int> metBin;

	timeBin.push_back(0);
	timeBin.push_back(time_N_fine);

	metBin.push_back(0);
	metBin.push_back(met_N_fine);

	TH2F *h2finebinData = new TH2F("h2finebinData","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinSig = new TH2F("h2finebinSig","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinMCBkg = new TH2F("h2finebinMCBkg","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);

	tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinData", cut.c_str());
	tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinSig", (weight_cut + "( "+cut+" )").c_str());
	
	for(int i=0; i<xsec_MCBkg.size(); i++)
	{
		TH2F *h2finebinMCBkg_this = new TH2F(("h2finebinMCBkg_"+std::to_string(i)).c_str(),"; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
		trees_MCBkg[i]->Draw(("t1MET:pho1ClusterTime_SmearToData>>h2finebinMCBkg_"+std::to_string(i)).c_str(), (weight_cut + "( "+cut+" )").c_str());
		float int_MCBkg_this = h2finebinMCBkg_this->Integral();
		h2finebinMCBkg_this->Scale(1.0*lumi*xsec_MCBkg[i]/NEvents_MCBkg[i]);

		cout<<"total number of events in MCBkg background "<<i<<": before cut => after cut => scaled ... "<<trees_MCBkg[i]->GetEntries()<<"   "<<trees_MCBkg[i]->GetEntries((weight_cut + "( "+cut+" )").c_str())<<"   "<<h2finebinMCBkg_this->Integral()<<" (  lumi*xsec*int/Norm = "<<lumi<<" * "<<xsec_MCBkg[i]<<" * "<<int_MCBkg_this<<" / "<<NEvents_MCBkg[i]<<" = "<<lumi*xsec_MCBkg[i]*int_MCBkg_this/NEvents_MCBkg[i]<<" )"<<endl;

		h2finebinMCBkg->Add(h2finebinMCBkg_this);
	}

	cout<<"Bkg MC Integral total = "<<h2finebinMCBkg->Integral()<<endl;
	cout<<"Data Integral total = "<<h2finebinData->Integral()<<endl;
	cout<<"applying k-factors..."<<endl;
	h2finebinMCBkg->Scale(h2finebinData->Integral()/h2finebinMCBkg->Integral());	
	

	float N_sig_expected = 1.0*lumi*xsec*h2finebinSig->Integral()/(1.0*NEvents_sig);
	h2finebinSig->Scale((1.0*N_sig_expected)/(1.0*h2finebinSig->Integral()));

	cout<<"binning optimization with data.int = "<<h2finebinData->Integral()<<", sig.Int = "<<h2finebinSig->Integral()<<endl;	

	OptimizeBinningABCD(Nbins_MET, Nbins_time, 10.0, 0.0001, timeBin, metBin, h2finebinData, h2finebinSig, time_Low, time_High, time_N_fine, met_Low, met_High, met_N_fine, _sigModelName, outBinningDir);

	cout<<"optimized met and time bin:-----------"<<endl;
	cout<<"time: ";
	for(int i=0;i<timeBin.size();i++)
	{
		xbins_time.push_back(time_Low + (time_High - time_Low) * (1.0*timeBin[i])/(1.0*time_N_fine));
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
		xbins_MET.push_back(met_Low + (met_High - met_Low) * (1.0*metBin[i])/(1.0*met_N_fine));
		cout<<met_Low + (met_High - met_Low) * (1.0*metBin[i])/(1.0*met_N_fine)<<"  ,  ";
	}
	cout<<endl;

	cout<<"met bin: ";
	for(int i=0;i<metBin.size();i++)
	{
		cout<<metBin[i]<<"   ,   ";
	}
	cout<<endl;

	
	for(int iT=1;iT<= timeBin.size()-1; iT++)
	{
		for(int iM=1;iM<= metBin.size()-1; iM++)
		{
			h2_rate_Data_inBins->SetBinContent(iT, iM, h2finebinData->Integral(timeBin[iT-1]+1, timeBin[iT], metBin[iM-1]+1, metBin[iM]));	
			h2_rate_Sig_inBins->SetBinContent(iT, iM, h2finebinSig->Integral(timeBin[iT-1]+1, timeBin[iT], metBin[iM-1]+1, metBin[iM]));	
		}
	}

}

if(binningAlgorithm == "limit" && fitMode == "binAndDatacard")
{

	//pre-defined bins:

	const int met_N_fine = 8;
	double MET_finebins[9] = {0.0, 50.0, 100.0, 150.0, 200.0, 300.0, 500.0, 1000.0, 9000.0};
	const int time_N_fine = 8;
	double Time_finebins[9]= {-2.0, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 25.0};

	std::vector <int> timeBin;
	std::vector <int> metBin;

	timeBin.push_back(0);
	timeBin.push_back(time_N_fine);

	metBin.push_back(0);
	metBin.push_back(met_N_fine);

	TH2F *h2finebinData = new TH2F("h2finebinData","; #gamma time bin; #slash{E}_{T} bin; Events", time_N_fine, Time_finebins, met_N_fine, MET_finebins);
	TH1F *h1finebinData_Time = new TH1F("h1finebinData_Time", "; #gamma time bin; Events", time_N_fine, Time_finebins);
	TH1F *h1finebinData_MET = new TH1F("h1finebinData_MET", "; #slash{E}_{T} bin; Events", met_N_fine, MET_finebins);

	TH2F *h2finebinSig = new TH2F("h2finebinSig","; #gamma time bin; #slash{E}_{T} bin; Events", time_N_fine, Time_finebins, met_N_fine, MET_finebins);
	TH2F *h2finebinMCBkg = new TH2F("h2finebinMCBkg","; #gamma time bin; #slash{E}_{T} bin; Events", time_N_fine, Time_finebins, met_N_fine, MET_finebins);

	tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinData", cut.c_str());
	tree_data->Draw("pho1ClusterTime_SmearToData>>h1finebinData_Time", (cut+" && t1MET < 100.0").c_str());
	tree_data->Draw("t1MET>>h1finebinData_MET", (cut+" && pho1ClusterTime_SmearToData < 1.0").c_str());
	tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinSig", (weight_cut + "( "+cut+" )").c_str());
	//tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinData", (weight_cut + "( "+cut+" )").c_str());

	h1finebinData_Time->Scale(1.0/h1finebinData_Time->Integral());	
	h1finebinData_MET->Scale(1.0/h1finebinData_MET->Integral());	

	for(int i=0; i<xsec_MCBkg.size(); i++)
	{
		TH2F *h2finebinMCBkg_this = new TH2F(("h2finebinMCBkg_"+std::to_string(i)).c_str(),"; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, Time_finebins, met_N_fine, MET_finebins);
		trees_MCBkg[i]->Draw(("t1MET:pho1ClusterTime_SmearToData>>h2finebinMCBkg_"+std::to_string(i)).c_str(), (weight_cut + "( "+cut+" )").c_str());
		float int_MCBkg_this = h2finebinMCBkg_this->Integral();
		h2finebinMCBkg_this->Scale(1.0*lumi*xsec_MCBkg[i]/NEvents_MCBkg[i]);

		cout<<"total number of events in MCBkg background "<<i<<": before cut => after cut => scaled ... "<<trees_MCBkg[i]->GetEntries()<<"   "<<trees_MCBkg[i]->GetEntries((weight_cut + "( "+cut+" )").c_str())<<"   "<<h2finebinMCBkg_this->Integral()<<" (  lumi*xsec*int/Norm = "<<lumi<<" * "<<xsec_MCBkg[i]<<" * "<<int_MCBkg_this<<" / "<<NEvents_MCBkg[i]<<" = "<<lumi*xsec_MCBkg[i]*int_MCBkg_this/NEvents_MCBkg[i]<<" )"<<endl;

		h2finebinMCBkg->Add(h2finebinMCBkg_this);
	}

	cout<<"Bkg MC Integral total = "<<h2finebinMCBkg->Integral()<<endl;
	cout<<"Data Integral total = "<<h2finebinData->Integral()<<endl;
	cout<<"applying k-factors... = "<<h2finebinData->Integral()/h2finebinMCBkg->Integral()<<endl;
	h2finebinMCBkg->Scale(h2finebinData->Integral()/h2finebinMCBkg->Integral());	

		
	float N_sig_expected = 1.0*lumi*xsec*h2finebinSig->Integral()/(1.0*NEvents_sig);
	h2finebinSig->Scale((1.0*N_sig_expected)/(1.0*h2finebinSig->Integral()));
	
	//blind the top cornor of the data
	
	if(_useToy)
	{
		float A = h2finebinData->GetBinContent(time_N_fine-1, met_N_fine-1);
		float B = h2finebinData->GetBinContent(time_N_fine-1, met_N_fine);
		float D = h2finebinData->GetBinContent(time_N_fine, met_N_fine-1);
		if(A > 0.0)	h2finebinData->SetBinContent(time_N_fine, met_N_fine, B*D/A);
	}			
	
	cout<<"binning optimization with data.int = "<<h2finebinData->Integral()<<", sig.Int = "<<h2finebinSig->Integral()<<endl;	
	
	OptimizeBinningABCDLimits(Nbins_MET, Nbins_time, timeBin, metBin, h2finebinData, h2finebinSig, h2finebinMCBkg, h1finebinData_Time, h1finebinData_MET, _sigModelName, outBinningDir, true);
	
	cout<<"optimized met and time bin:-----------"<<endl;
	cout<<"time: ";
	for(int i=0;i<timeBin.size();i++)
	{
		xbins_time.push_back(Time_finebins[timeBin[i]]);
		cout<<Time_finebins[timeBin[i]]<<"  ,  ";
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
		xbins_MET.push_back(MET_finebins[metBin[i]]);
		cout<<MET_finebins[metBin[i]]<<"  ,  ";
	}
	cout<<endl;

	cout<<"met bin: ";
	for(int i=0;i<metBin.size();i++)
	{
		cout<<metBin[i]<<"   ,   ";
	}
	cout<<endl;


	for(int iT=1;iT<= timeBin.size()-1; iT++)
	{
		for(int iM=1;iM<= metBin.size()-1; iM++)
		{
			h2_rate_Data_inBins->SetBinContent(iT, iM, h2finebinData->Integral(timeBin[iT-1]+1, timeBin[iT], metBin[iM-1]+1, metBin[iM]));	
			h2_rate_Sig_inBins->SetBinContent(iT, iM, h2finebinSig->Integral(timeBin[iT-1]+1, timeBin[iT], metBin[iM-1]+1, metBin[iM]));	
			h2_rate_MCBkg_inBins->SetBinContent(iT, iM, h2finebinMCBkg->Integral(timeBin[iT-1]+1, timeBin[iT], metBin[iM-1]+1, metBin[iM]));	
			if(iT==1) h1_rate_Data_MET_inBins->SetBinContent(iM, h1finebinData_MET->Integral(metBin[iM-1]+1, metBin[iM]));
		}
		h1_rate_Data_Time_inBins->SetBinContent(iT, h1finebinData_Time->Integral(timeBin[iT-1]+1, timeBin[iT]));
	}

}


if(fitMode == "datacard")
{
	xbins_MET.push_back(met_split_by_CAT[BIN_CATEGORY]);
	xbins_time.push_back(time_split_by_CAT[BIN_CATEGORY]);
	
	float time_2x2_bins[3] = {-2.0, time_split_by_CAT[BIN_CATEGORY], 25.0};
	float met_2x2_bins[3] = {0.0, met_split_by_CAT[BIN_CATEGORY], 9000.0};

	TH2F *h2_2x2binData = new TH2F("h2_2x2binData","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	TH1F *h1_2x2binData_Time = new TH1F("h1_2x2binData_Time", "; #gamma time bin; Events", 2, time_2x2_bins);
	TH1F *h1_2x2binData_MET = new TH1F("h1_2x2binData_MET", "; #slash{E}_{T} bin; Events", 2, met_2x2_bins);

	TH2F *h2_2x2binSig = new TH2F("h2_2x2binSig","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);
	TH2F *h2_2x2binMCBkg = new TH2F("h2_2x2binMCBkg","; #gamma time bin; #slash{E}_{T} bin; Events", 2, time_2x2_bins, 2, met_2x2_bins);

	tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2_2x2binData", cut.c_str());
	tree_data->Draw("pho1ClusterTime_SmearToData>>h1_2x2binData_Time", (cut+" && t1MET < 100.0").c_str());
	tree_data->Draw("t1MET>>h1_2x2binData_MET", (cut+" && pho1ClusterTime_SmearToData < 1.0").c_str());
	tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2_2x2binSig", (weight_cut + "( "+cut+" )").c_str());

	h1_2x2binData_Time->Scale(1.0/h1_2x2binData_Time->Integral());	
	h1_2x2binData_MET->Scale(1.0/h1_2x2binData_MET->Integral());	

	for(int i=0; i<xsec_MCBkg.size(); i++)
	{
		TH2F *h2_2x2binMCBkg_this = new TH2F(("h2_2x2binMCBkg_"+std::to_string(i)).c_str(),"; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 2, time_2x2_bins, 2, met_2x2_bins);
		trees_MCBkg[i]->Draw(("t1MET:pho1ClusterTime_SmearToData>>h2_2x2binMCBkg_"+std::to_string(i)).c_str(), (weight_cut + "( "+cut+" )").c_str());
		float int_MCBkg_this = h2_2x2binMCBkg_this->Integral();
		h2_2x2binMCBkg_this->Scale(1.0*lumi*xsec_MCBkg[i]/NEvents_MCBkg[i]);

		cout<<"total number of events in MCBkg background "<<i<<": before cut => after cut => scaled ... "<<trees_MCBkg[i]->GetEntries()<<"   "<<trees_MCBkg[i]->GetEntries((weight_cut + "( "+cut+" )").c_str())<<"   "<<h2_2x2binMCBkg_this->Integral()<<" (  lumi*xsec*int/Norm = "<<lumi<<" * "<<xsec_MCBkg[i]<<" * "<<int_MCBkg_this<<" / "<<NEvents_MCBkg[i]<<" = "<<lumi*xsec_MCBkg[i]*int_MCBkg_this/NEvents_MCBkg[i]<<" )"<<endl;

		h2_2x2binMCBkg->Add(h2_2x2binMCBkg_this);
	}

	cout<<"Bkg MC Integral total = "<<h2_2x2binMCBkg->Integral()<<endl;
	cout<<"Data Integral total = "<<h2_2x2binData->Integral()<<endl;
	cout<<"applying k-factors... = "<<h2_2x2binData->Integral()/h2_2x2binMCBkg->Integral()<<endl;
	h2_2x2binMCBkg->Scale(h2_2x2binData->Integral()/h2_2x2binMCBkg->Integral());	
		
	float N_sig_expected = 1.0*lumi*xsec*h2_2x2binSig->Integral()/(1.0*NEvents_sig);
	h2_2x2binSig->Scale((1.0*N_sig_expected)/(1.0*h2_2x2binSig->Integral()));


	for(int iT=1;iT<= 2; iT++)
	{
		for(int iM=1;iM<= 2; iM++)
		{
			h2_rate_Data_inBins->SetBinContent(iT, iM, h2_2x2binData->GetBinContent(iT, iM));
			h2_rate_Sig_inBins->SetBinContent(iT, iM, h2_2x2binSig->GetBinContent(iT, iM));
			h2_rate_MCBkg_inBins->SetBinContent(iT, iM, h2_2x2binMCBkg->GetBinContent(iT, iM));
			if(iT==1) h1_rate_Data_MET_inBins->SetBinContent(iM, h1_2x2binData_MET->GetBinContent(iM));
		}
		h1_rate_Data_Time_inBins->SetBinContent(iT, h1_2x2binData_Time->GetBinContent(iT));
	}

}


if(fitMode == "binAndDatacard")
{
if(xbins_MET.size() != Nbins_MET + 1) 
{
	std::cerr << "[ERROR]: binning procedure didn't manage to get the target number of MET bins..." << std::endl;
	return -1;
}

if(xbins_time.size() != Nbins_time + 1) 
{
	std::cerr << "[ERROR]: binning procedure didn't manage to get the target number of time bins..." << std::endl;
	return -1;
}
}

// B | C
// -----
// A | D
//for last bin, use blind strategy: C = B*D/A
	
if(_useToy)
{
	/*
	float A = h2_rate_Data_inBins->GetBinContent(Nbins_time-1, Nbins_MET-1);
	float B = h2_rate_Data_inBins->GetBinContent(Nbins_time-1, Nbins_MET);
	float D = h2_rate_Data_inBins->GetBinContent(Nbins_time, Nbins_MET-1);
	if(A > 0.0)	h2_rate_Data_inBins->SetBinContent(Nbins_time, Nbins_MET, B*D/A);
	*/
	float A = h2_rate_Data_inBins->GetBinContent(Nbins_time-1, Nbins_MET-1);
	//float A = h2_rate_MCBkg_inBins->GetBinContent(Nbins_time-1, Nbins_MET-1);
	float B = A*h1_rate_Data_MET_inBins->GetBinContent(2)/h1_rate_Data_MET_inBins->GetBinContent(1);
	float D = A*h1_rate_Data_Time_inBins->GetBinContent(2)/h1_rate_Data_Time_inBins->GetBinContent(1);
	if(A>0.0)
	{
		h2_rate_Data_inBins->SetBinContent(1, 1, A);
		h2_rate_Data_inBins->SetBinContent(1, 2, B);
		h2_rate_Data_inBins->SetBinContent(2, 1, D);
		h2_rate_Data_inBins->SetBinContent(2, 2, B*D/A);
	}
}			


for(int iT=1;iT<= Nbins_time; iT++)
{
	for(int iM=1;iM<= Nbins_MET; iM++)
	{
		if(h2_rate_Data_inBins->GetBinContent(iT, iM) > 0.0) h2_rate_SoverSqrtB_inBins->SetBinContent(iT, iM, h2_rate_Sig_inBins->GetBinContent(iT, iM) / sqrt(h2_rate_Data_inBins->GetBinContent(iT, iM)));
	}
}




//draw 2D binning

h2_rate_Data_inBins->GetXaxis()->SetNdivisions(100+Nbins_time);
h2_rate_Data_inBins->GetYaxis()->SetNdivisions(100+Nbins_MET);

h2_rate_Sig_inBins->GetXaxis()->SetNdivisions(100+Nbins_time);
h2_rate_Sig_inBins->GetYaxis()->SetNdivisions(100+Nbins_MET);

h2_rate_SoverSqrtB_inBins->GetXaxis()->SetNdivisions(100+Nbins_time);
h2_rate_SoverSqrtB_inBins->GetYaxis()->SetNdivisions(100+Nbins_MET);


Draw2DBinning(h2_rate_Data_inBins, ("Data_"+to_string(Nbins_time)+"x"+to_string(Nbins_MET)).c_str(), _sigModelName, outBinningDir);
Draw2DBinning(h2_rate_Sig_inBins, ("Sig_"+to_string(Nbins_time)+"x"+to_string(Nbins_MET)).c_str(), _sigModelName, outBinningDir);
Draw2DBinning(h2_rate_SoverSqrtB_inBins, ("SoverSqrtB_"+to_string(Nbins_time)+"x"+to_string(Nbins_MET)).c_str(), _sigModelName, outBinningDir);


//make the datacard


TH2F *h2_dummy = new TH2F("h2_dummy","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
for(int iT=1; iT<=Nbins_time; iT++)
{
        for(int iM=1; iM<=Nbins_MET; iM++)
        {
                h2_dummy->SetBinContent(iT, iM, 1.0*iM*iT);
        }
}

MakeDataCardABCD(h2_rate_Data_inBins,h2_rate_Sig_inBins, h2_rate_MCBkg_inBins, h1_rate_Data_Time_inBins, h1_rate_Data_MET_inBins, Nbins_time, Nbins_MET, _sigModelName, outDataCardsDir);
//MakeDataCardABCD(h2_dummy, h2_dummy,Nbins_time, Nbins_MET, _sigModelName, outDataCardsDir);

//add systematics
TH2F *h2_lumi_sys_Sig_inBins = new TH2F("h2_lumi_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_PhotonScale_sys_Sig_inBins = new TH2F("h2_PhotonScale_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_PhotonSmear_sys_Sig_inBins = new TH2F("h2_PhotonSmear_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_EGMVID_SF_sys_Sig_inBins = new TH2F("h2_EGMVID_SF_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_TriggerEff_SF_sys_Sig_inBins = new TH2F("h2_TriggerEff_SF_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_JetEScale_sys_Sig_inBins = new TH2F("h2_JetEScale_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_JetESmear_sys_Sig_inBins = new TH2F("h2_JetESmear_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_TimeScale_sys_Sig_inBins = new TH2F("h2_TimeScale_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_TimeSmear_sys_Sig_inBins = new TH2F("h2_TimeSmear_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_TimeMETCorrelation_sys_Sig_inBins = new TH2F("h2_TimeMETCorrelation_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);

for(int iT=1; iT<=Nbins_time; iT++)
{
        for(int iM=1; iM<=Nbins_MET; iM++)
        {
                h2_lumi_sys_Sig_inBins->SetBinContent(iT, iM, 1.025);
                h2_PhotonScale_sys_Sig_inBins->SetBinContent(iT, iM, 1.01);
                h2_PhotonSmear_sys_Sig_inBins->SetBinContent(iT, iM, 1.01);
                h2_EGMVID_SF_sys_Sig_inBins->SetBinContent(iT, iM, 1.020);
                h2_TriggerEff_SF_sys_Sig_inBins->SetBinContent(iT, iM, 1.020);
                h2_JetEScale_sys_Sig_inBins->SetBinContent(iT, iM, 1.015);
                h2_JetESmear_sys_Sig_inBins->SetBinContent(iT, iM, 1.015);
                h2_TimeScale_sys_Sig_inBins->SetBinContent(iT, iM, 1.015);
                h2_TimeSmear_sys_Sig_inBins->SetBinContent(iT, iM, 1.005);
                h2_TimeMETCorrelation_sys_Sig_inBins->SetBinContent(iT, iM, 1.00);
        }
}

h2_TimeMETCorrelation_sys_Sig_inBins->SetBinContent(2, 2, 1.02);

AddSystematics_Norm_ABCD(h2_lumi_sys_Sig_inBins, Nbins_time, Nbins_MET, "CMSLumi_2016", "lnN", _sigModelName, outDataCardsDir, true);
AddSystematics_Norm_ABCD(h2_PhotonScale_sys_Sig_inBins, Nbins_time, Nbins_MET, "PhotonEScale", "lnN", _sigModelName, outDataCardsDir, true);
AddSystematics_Norm_ABCD(h2_PhotonSmear_sys_Sig_inBins, Nbins_time, Nbins_MET, "PhotonESmear", "lnN", _sigModelName, outDataCardsDir, true);
AddSystematics_Norm_ABCD(h2_EGMVID_SF_sys_Sig_inBins, Nbins_time, Nbins_MET, "EGMVID_SF", "lnN", _sigModelName, outDataCardsDir, true);
AddSystematics_Norm_ABCD(h2_TriggerEff_SF_sys_Sig_inBins, Nbins_time, Nbins_MET, "TriggerEff_SF", "lnN", _sigModelName, outDataCardsDir, true);
AddSystematics_Norm_ABCD(h2_JetEScale_sys_Sig_inBins, Nbins_time, Nbins_MET, "JetECorrection", "lnN", _sigModelName, outDataCardsDir, true);
AddSystematics_Norm_ABCD(h2_JetESmear_sys_Sig_inBins, Nbins_time, Nbins_MET, "JetEResolution_2016", "lnN", _sigModelName, outDataCardsDir, true);
AddSystematics_Norm_ABCD(h2_TimeScale_sys_Sig_inBins, Nbins_time, Nbins_MET, "PhotonTimeShift", "lnN", _sigModelName, outDataCardsDir, true);
AddSystematics_Norm_ABCD(h2_TimeSmear_sys_Sig_inBins, Nbins_time, Nbins_MET, "PhotonTimeSmear", "lnN", _sigModelName, outDataCardsDir, true);
AddSystematics_Norm_ABCD(h2_TimeMETCorrelation_sys_Sig_inBins, Nbins_time, Nbins_MET, "ClosureC", "lnN", _sigModelName, outDataCardsDir, false);

//int N_obs_total = tree_data->CopyTree( cut.c_str() )->GetEntries();
//TFile *f_Out = new TFile(("fit_results/2016ABCD/"+_outPlotsDir+"/fit_ws_"+sigModelName+".root").c_str(),"recreate");

}
