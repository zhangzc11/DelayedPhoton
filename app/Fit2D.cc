//C++ INCLUDES
#include <iostream>
//ROOT INCLUDES
#include <TFile.h>
#include <TTree.h>
#include <TMath.h>
#include <TH1F.h>
#include <TROOT.h>

int main( int argc, char* argv[])
{
  srand(time(NULL));
  gROOT->Reset();

  std::string inputfile_data = argv[1];
  std::string inputfile_signal = argv[2];
  std::string inputfile_qcd = argv[3];
  std::string inputfile_gjets = argv[4];

  if(inputfile_data == "")
  {
	std::cerr << "[ERROR]: please provide an input file for data" << std::endl;
        return -1;
  }
  std::cout<<"using input file for data: "<<inputfile_data<<std::endl;

  if(inputfile_signal == "")
  {
	std::cerr << "[ERROR]: please provide an input file for signal" << std::endl;
        return -1;
  }
  std::cout<<"using input file for signal: "<<inputfile_signal<<std::endl;

if(inputfile_qcd == "")
  {
	std::cerr << "[ERROR]: please provide an input file for qcd" << std::endl;
        return -1;
  }
  std::cout<<"using input file for qcd: "<<inputfile_qcd<<std::endl;

if(inputfile_gjets == "")
  {
	std::cerr << "[ERROR]: please provide an input file for gjets" << std::endl;
        return -1;
  }
  std::cout<<"using input file for gjets: "<<inputfile_gjets<<std::endl;



  return 0;
}
