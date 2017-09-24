########################################################
##common configuration parameters for all plot scripts##
########################################################

#######################input trees######################
fileNameData = '/afs/cern.ch/work/z/zhicaiz/public/release/CMSSW_9_2_5/src/RazorAnalyzer/DelayedPhoton_DoubleEG.root'
fileNameGJets = '/afs/cern.ch/work/z/zhicaiz/public/release/CMSSW_9_2_5/src/RazorAnalyzer/DelayedPhoton_GJets.root'
fileNameQCD = '/afs/cern.ch/work/z/zhicaiz/public/release/CMSSW_9_2_5/src/RazorAnalyzer/DelayedPhoton_QCD.root'
fileNameSig = '/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GluinoToNeutralinoToGratinoPhoton_M1000_CTau5000mm.root'

########################################################
lumi = 1.0 #fb^-1
cut = 'pho1Pt > 40 && abs(pho1Eta)<1.44 && pho1passIsoLoose && pho1passEleVeto'
outputDir = '/afs/cern.ch/user/z/zhicaiz/www/sharebox/DelayedPhoton/25Sept2017/'


