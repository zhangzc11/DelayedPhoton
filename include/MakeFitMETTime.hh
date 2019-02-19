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
#include <RooRealVar.h>
#include <RooAbsPdf.h>
//LOCAL INCLUDES

RooWorkspace* FitDataBkgFraction( TH1F * h1_Data, TString varName, TString varTitle, TString varUnit, float lumi, float varLow, float varHigh, TH1F * h1_GJets, TH1F * h1_QCD, TString outPlotsDir = "plots_3J");

TFractionFitter* FitDataBkgFractionFilter(TH1F * h1_data, TH1F * h1_GJets, TH1F * h1_QCD);

RooWorkspace* Fit2DMETTimeDataBkg( TTree * treeData, TTree * treeGJets, TTree * treeQCD,  float fracGJets, float fracGJetsErr, float fracQCD, float fracQCDErr); 

RooWorkspace* Fit2DMETTimeDataBkg( TH2F * h2Data, TH2F * h2GJets, TH2F * h2QCD,  float fracGJets, float fracGJetsErr, float fracQCD, float fracQCDErr, TString outPlotsDir = "plots_3J"); 

RooWorkspace* Fit2DMETTimeDataBkgSig( TH2F * h2Data, TH2F * h2GJets, TH2F * h2QCD,  TH2F * h2Sig, float fracGJets, float fracQCD, TString modelName, TString modelTitle, bool useToy = true, TString outPlotsDir = "plots_3J"); 
RooWorkspace* Fit1DMETTimeDataBkgSig( TH1F * h1Data, TH1F * h1GJets, TH1F * h1QCD,  TH1F * h1Sig, float lumi, float fracGJets, float fracQCD, TString modelName, TString modelTitle, TString outPlotsDir = "plots_3J"); 
RooWorkspace* Fit1DMETTimeDataBkgSig( TH1F * h1Data, TH1F * h1GJets, TH1F * h1QCD,  TH1F * h1Sig, TH1F * h1EWK, float lumi, float fracGJets, float fracQCD, TString modelName, TString modelTitle, TString outPlotsDir = "plots_3J"); 
RooWorkspace* GenerateToyData( TH1F * h1Data, TH1F * h1GJets, TH1F * h1QCD,  TH1F * h1Sig, TH1F * h1EWK, float fracGJets, float fracQCD, float scaleSig); 

void Fit1DMETTimeBiasTest( TH1F * h1Data, TH1F * h1Bkg,  TH1F * h1Sig, float SoverB, int ntoys, TString modelName, float lumi, TString outBiasDir = "bias_3J"); 

double Fit1DMETTimeSignificance(TH1F *h1Data, TH1F * h1Bkg,  TH1F * h1Sig, int ntoys); 
double CalculateMETTimeSignificance(TH1F * h1Bkg,  TH1F * h1Sig); 

void MakeDataCard(TString modelName, RooWorkspace *ws, float N_obs, float N_bkg, float N_sig, TString outDataCardsDir = "datacards_3J");
void MakeDataCard(TString modelName, RooWorkspace *ws, float N_obs, float N_QCDGJets, float N_EWK, float N_sig, TString outDataCardsDir = "datacards_3J");
void MakeDataCardABCD(TH2F * h2_rate_Data, TH2F * h2_rate_Sig, int Nbins_time, int Nbins_MET, TString modelName, TString outDataCardsDir = "datacards_3J");
void AddSystematics_Norm_ABCD(TH2F * h2_sys_Sig, int Nbins_time, int Nbins_MET, TString sysName, TString distType, TString modelName, TString outDataCardsDir = "datacards_3J");

void AddSystematics_Norm(TString modelName, float N_bkg, float N_sig, TString outDataCardsDir, TString sysName, TString distType);
void AddSystematics_Norm(TString modelName, float N_QCDGJets, float N_EWK, float N_sig, TString outDataCardsDir, TString sysName, TString distType);
void AddSystematics_shape(TString modelName, TString N_bkg, TString N_sig, TString outDataCardsDir, TString sysName, TString distType);
void AddSystematics_shape(TString modelName, TString N_QCDGJets, TString N_EWK, TString N_sig, TString outDataCardsDir, TString sysName, TString distType);

void OptimizeBinning(std::vector<int> &timeBin, std::vector<int> &metBin, TH2F * h2Bkg, TH2F *h2Sig, float time_Low, float time_High, int time_N_fine, float met_Low, float met_High, int met_N_fine, TString modelName, TString ourBinningDir = "binning_3J");
void OptimizeBinningABCD(int Nbins_MET, int Nbins_time, float min_events, float min_events_sig_frac, std::vector<int> &timeBin, std::vector<int> &metBin, TH2F * h2Bkg, TH2F *h2Sig, float time_Low, float time_High, int time_N_fine, float met_Low, float met_High, int met_N_fine, TString modelName, TString ourBinningDir);

void Draw2DBinning(TH2F * h2_rate, TString plotLabel, TString modelName, TString ourBinningDir);

#endif

