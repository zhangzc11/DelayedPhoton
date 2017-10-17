#ifndef MakeFitMETTime_HH
#define MakeFitMETTime_HH
//C++ INCLUDES
#include <sstream>
#include <string>
//ROOT INCLUDES
#include <TTree.h>
#include <TString.h>
#include <TFractionFitter.h>
//ROOFIT INCLUDES
#include <RooRealVar.h>
#include <RooWorkspace.h>
#include <RooDataSet.h>
#include <RooAbsPdf.h>
//LOCAL INCLUDES

RooWorkspace* FitDataBkgFraction( TTree * tree, TString varName, TString varTitle, TString varUnit, float varLow, float varHigh, TH1F * h1_GJets, TH1F * h1_QCD);

TFractionFitter* FitDataBkgFractionFilter(TH1F * h1_data, TH1F * h1_GJets, TH1F * h1_QCD);


#endif
