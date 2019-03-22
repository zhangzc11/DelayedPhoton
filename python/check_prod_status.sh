#!/bin/bash

for das in `dasgoclient --query="dataset=/GMSB_L*_13TeV-pythia8/zhicaiz-crab_CMSSW_*_GMSB_L*cm_GENSIM_CaltechT2_22Mar2019*/* instance=prod/phys03"`; do echo summary for ${das} :; dasgoclient --query="summary dataset=${das} instance=prod/phys03" ; done
