#ifndef MakeFitMETTime_HH
#define MakeFitMETTime_HH
//C++ INCLUDES
#include <sstream>
#include <string>
#include <vector>
//ROOT INCLUDES
#include <TTree.h>
#include <TString.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TFractionFitter.h>
//ROOFIT INCLUDES
#include <RooRealVar.h>
#include <RooWorkspace.h>
#include <RooDataSet.h>
#include <RooAbsPdf.h>
//LOCAL INCLUDES

RooWorkspace* FitDataBkgFraction( TH1F * h1_Data, TString varName, TString varTitle, TString varUnit, float varLow, float varHigh, TH1F * h1_GJets, TH1F * h1_QCD);

TFractionFitter* FitDataBkgFractionFilter(TH1F * h1_data, TH1F * h1_GJets, TH1F * h1_QCD);

RooWorkspace* Fit2DMETTimeDataBkg( TTree * treeData, TTree * treeGJets, TTree * treeQCD,  float fracGJets, float fracGJetsErr, float fracQCD, float fracQCDErr); 

RooWorkspace* Fit2DMETTimeDataBkg( TH2F * h2Data, TH2F * h2GJets, TH2F * h2QCD,  float fracGJets, float fracGJetsErr, float fracQCD, float fracQCDErr); 

RooWorkspace* Fit2DMETTimeDataBkgSig( TH2F * h2Data, TH2F * h2GJets, TH2F * h2QCD,  TH2F * h2Sig, float fracGJets, float fracQCD, TString modelName, TString modelTitle, bool useToy = true); 
RooWorkspace* Fit1DMETTimeDataBkgSig( TH1F * h1Data, TH1F * h1GJets, TH1F * h1QCD,  TH1F * h1Sig, float fracGJets, float fracQCD, TString modelName, TString modelTitle, bool useToy = true); 

void Fit1DMETTimeBiasTest( TH1F * h1Data, TH1F * h1Bkg,  TH1F * h1Sig, float SoverB, int ntoys, TString modelName); 

double Fit1DMETTimeSignificance(TH1F *h1Data, TH1F * h1Bkg,  TH1F * h1Sig, int ntoys); 

void MakeDataCard(TString modelName, RooWorkspace *ws, float N_obs, float N_bkg, float N_sig);

void OptimizeBinning(std::vector<int> &timeBin, std::vector<int> &metBin, TH2F * h2Bkg, TH2F *h2Sig, float time_Low, float time_High, int time_N_fine, float met_Low, float met_High, int met_N_fine, TString modelName);

#endif

