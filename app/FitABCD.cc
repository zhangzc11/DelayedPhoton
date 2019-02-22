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

const Int_t Nbins_MET_lowT = 3;
const Int_t Nbins_MET_highT = 3;
const Int_t Nbins_time_lowT = 3;
const Int_t Nbins_time_highT = 3;
Int_t Nbins_total_lowT = Nbins_MET_lowT*Nbins_time_lowT;
Int_t Nbins_total_highT = Nbins_MET_highT*Nbins_time_highT;

Int_t Nbins_MET = 0;
Int_t Nbins_time = 0;

std::vector <float> xbins_MET;
std::vector <float> xbins_time;

bool useLowTBinning = false;
bool useBDT = true;

float lumi = 35922.0; //pb^-1
float NEvents_sig = 1.0;
bool _useToy = true;

std::string binningAlgorithm = "limit";//or "significance"

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

if (sigModelName.find("0p") != std::string::npos || sigModelName.find("5cm") != std::string::npos || sigModelName.find("10cm") != std::string::npos || sigModelName.find("50cm") != std::string::npos) useLowTBinning = true;

Nbins_MET = useLowTBinning ? Nbins_MET_lowT : Nbins_MET_highT;
Nbins_time = useLowTBinning ? Nbins_time_lowT : Nbins_time_highT;

TString _sigModelName (sigModelName.c_str());
TString _sigModelTitle (sigModelTitle.c_str());

float xsec = getXsecBR(sigModelName); //pb
std::string treeName = "DelayedPhoton";

std::string cut, cut_JESUp, cut_JESDown;

std::string weight_cut = "weight*pileupWeight*triggerEffSFWeight*photonEffSF*triggerEffWeight*";

std::string cut_MET_filter = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0" ;

std::string cut_pho1Tight = " && pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && pho1SigmaIetaIeta < 0.00994";
std::string cut_pho1Tight_noSigmaIetaIeta = " && pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3";
std::string cut_pho1Loose = " && pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.7 && pho1SigmaIetaIeta < 0.01031";
std::string cut_pho1Loose_noSigmaIetaIeta = " && pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.7";


if(category == "2J")
{
	if(!useBDT)
	{
		cut = "n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_JESUp = "n_Jets_JESUp == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_JESDown = "n_Jets_JESDown == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
	}
	else
	{
		cut = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_JESUp = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets_JESUp == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_JESDown = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets_JESDown == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
	}
}

else if(category == "3J")
{
	if(!useBDT)
	{
		cut = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_JESUp = "n_Jets_JESUp > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_JESDown = "n_Jets_JESDown > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
	}
	else
	{
		cut = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_JESUp = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets_JESUp > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_JESDown = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets_JESDown > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
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

std::cout<<"reading data file......"<<endl;
file_data = new TFile(inputFileName_data.c_str(), "READ");
tree_data = (TTree*)file_data->Get(treeName.c_str());

std::cout<<"reading signal file......"<<endl;
file_signal = new TFile(inputFileName_signal.c_str(), "READ");
tree_signal = (TTree*)file_signal->Get(treeName.c_str());

TH1F *h1_NEvents_sig = (TH1F*) file_signal->Get("NEvents");
NEvents_sig = h1_NEvents_sig->GetBinContent(1);
///////////////////////////Binning optimization
std::vector <float> rate_Data_inBins;
std::vector <float> rate_Sig_inBins;

if(binningAlgorithm == "significance")
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

	tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinData", cut.c_str());
	tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinSig", (weight_cut + "( "+cut+" )").c_str());

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
			rate_Data_inBins.push_back(h2finebinData->Integral(timeBin[iT-1]+1, timeBin[iT], metBin[iM-1]+1, metBin[iM]));
			rate_Sig_inBins.push_back(h2finebinSig->Integral(timeBin[iT-1]+1, timeBin[iT], metBin[iM-1]+1, metBin[iM]));
		}
	}

}

if(binningAlgorithm == "limit")
{

	//pre-defined bins:

	const int met_N_fine = 8;
	double MET_finebins[9] = {0.0, 50.0, 100.0, 150.0, 200.0, 300.0, 500.0, 1000.0, 3000.0};
	const int time_N_fine = 8;
	double Time_finebins[9]= {-2.0, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 25.0};

	std::vector <int> timeBin;
	std::vector <int> metBin;

	timeBin.push_back(0);
	timeBin.push_back(time_N_fine);

	metBin.push_back(0);
	metBin.push_back(met_N_fine);

	TH2F *h2finebinData = new TH2F("h2finebinData","; #gamma time bin; #slash{E}_{T} bin; Events", time_N_fine, Time_finebins, met_N_fine, MET_finebins);
	TH2F *h2finebinSig = new TH2F("h2finebinSig","; #gamma time bin; #slash{E}_{T} bin; Events", time_N_fine, Time_finebins, met_N_fine, MET_finebins);

	tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinData", cut.c_str());
	tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinSig", (weight_cut + "( "+cut+" )").c_str());
	//tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinData", (weight_cut + "( "+cut+" )").c_str());

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
	
	OptimizeBinningABCDLimits(Nbins_MET, Nbins_time, timeBin, metBin, h2finebinData, h2finebinSig, _sigModelName, outBinningDir);
	
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
			rate_Data_inBins.push_back(h2finebinData->Integral(timeBin[iT-1]+1, timeBin[iT], metBin[iM-1]+1, metBin[iM]));
			rate_Sig_inBins.push_back(h2finebinSig->Integral(timeBin[iT-1]+1, timeBin[iT], metBin[iM-1]+1, metBin[iM]));
		}
	}

}

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

// B | C
// -----
// A | D
//for last bin, use blind strategy: C = B*D/A
if(_useToy)
{
	rate_Data_inBins[Nbins_time*Nbins_MET-1] = rate_Data_inBins[Nbins_time*Nbins_MET-2]*rate_Data_inBins[(Nbins_time-1)*Nbins_MET-1]/rate_Data_inBins[(Nbins_time-1)*Nbins_MET-2];
}

cout<<"in ABCD bins...."<<endl;
float sum_rate_Data = 0.0;
float sum_rate_Sig = 0.0;

for(int i=0; i<rate_Data_inBins.size(); i++)
{
	cout<<"bin "<<i<<": "<<rate_Data_inBins[i]<<", "<<rate_Sig_inBins[i]<<endl;
	sum_rate_Data += rate_Data_inBins[i];
	sum_rate_Sig += rate_Sig_inBins[i];
}
cout<<"ABCD sum = "<<sum_rate_Data<<", "<<sum_rate_Sig<<endl;

//draw 2D binning
TH2F *h2_rate_Data_inBins = new TH2F("h2_rate_Data_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_rate_Sig_inBins = new TH2F("h2_rate_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_rate_SoverSqrtB_inBins = new TH2F("h2_rate_SoverSqrtB_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
for(int iT=1; iT<=Nbins_time; iT++)
{
	for(int iM=1; iM<=Nbins_MET; iM++)
	{
		h2_rate_Data_inBins->SetBinContent(iT, iM, rate_Data_inBins[Nbins_time*(iM-1)+iT-1]);
		h2_rate_Sig_inBins->SetBinContent(iT, iM, rate_Sig_inBins[Nbins_time*(iM-1)+iT-1]);
		h2_rate_SoverSqrtB_inBins->SetBinContent(iT, iM, rate_Sig_inBins[Nbins_time*(iM-1)+iT-1]/sqrt(rate_Data_inBins[Nbins_time*(iM-1)+iT-1]));
	}
}

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

MakeDataCardABCD(h2_rate_Data_inBins,h2_rate_Sig_inBins,Nbins_time, Nbins_MET, _sigModelName, outDataCardsDir);
//MakeDataCardABCD(h2_dummy, h2_dummy,Nbins_time, Nbins_MET, _sigModelName, outDataCardsDir);

//add systematics
TH2F *h2_lumi_sys_Sig_inBins = new TH2F("h2_lumi_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_Photon_sys_Sig_inBins = new TH2F("h2_Photon_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);
TH2F *h2_Trigger_sys_Sig_inBins = new TH2F("h2_Trigger_sys_Sig_inBins","; #gamma time bin; #slash{E}_{T} bin; Events", Nbins_time, 0, 1.0*Nbins_time, Nbins_MET, 0, 1.0*Nbins_MET);

for(int iT=1; iT<=Nbins_time; iT++)
{
        for(int iM=1; iM<=Nbins_MET; iM++)
        {
                h2_lumi_sys_Sig_inBins->SetBinContent(iT, iM, 1.025);
                h2_Photon_sys_Sig_inBins->SetBinContent(iT, iM, 1.01);
                h2_Trigger_sys_Sig_inBins->SetBinContent(iT, iM, 1.01);
        }
}

AddSystematics_Norm_ABCD(h2_lumi_sys_Sig_inBins, Nbins_time, Nbins_MET, "lumi", "lnN", _sigModelName, outDataCardsDir);
AddSystematics_Norm_ABCD(h2_Photon_sys_Sig_inBins, Nbins_time, Nbins_MET, "Photon", "lnN", _sigModelName, outDataCardsDir);
AddSystematics_Norm_ABCD(h2_Trigger_sys_Sig_inBins, Nbins_time, Nbins_MET, "Trigger", "lnN", _sigModelName, outDataCardsDir);

//int N_obs_total = tree_data->CopyTree( cut.c_str() )->GetEntries();
//TFile *f_Out = new TFile(("fit_results/2016ABCD/"+_outPlotsDir+"/fit_ws_"+sigModelName+".root").c_str(),"recreate");

}
