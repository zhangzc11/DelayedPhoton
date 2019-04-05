#!/bin/bash

for das in `dasgoclient --query="dataset=/GMSB_L*_13TeV-pythia8/zhicaiz-crab_CMSSW_*_GMSB_L*cm_AODSIM_CaltechT2_02Apr2019*/* instance=prod/phys03"`; do echo summary for ${das} :; dasgoclient --query="summary dataset=${das} instance=prod/phys03" ; done
for das in `dasgoclient --query="dataset=/GMSB_L*_13TeV-pythia8/zhicaiz-crab_CMSSW_*_GMSB_L*cm_GEN-SIM-RAW_CaltechT2_29Mar2019*/* instance=prod/phys03"`; do echo summary for ${das} :; dasgoclient --query="summary dataset=${das} instance=prod/phys03" ; done
