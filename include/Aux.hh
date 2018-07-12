#ifndef Aux_HH
#define Aux_HH
//C++ INCLUDES
#include <sstream>
#include <string>
//ROOT INCLUDES
#include <TTree.h>
#include <TString.h>
#include <TH1F.h>
#include <TH2F.h>

float getXsecBR(std::string sigModelName);

void DrawDataBkgSig(TH1F *h1Data, TH1F *h1Bkg, TH1F *h1Sig, TH1F *h1all, float lumi, std::string sigModelTitle, std::string sigModelName, std::string suffix, TString outPlotsDir);

void DrawCMS(TCanvas *myC, int energy, float lumi);

#endif

