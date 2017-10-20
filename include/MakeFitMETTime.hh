#ifndef MakeFitMETTime_HH
#define MakeFitMETTime_HH
//C++ INCLUDES
#include <sstream>
#include <string>
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
#endif
