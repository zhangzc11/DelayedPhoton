########################################################
##common configuration parameters for all plot scripts##
########################################################

#######################input trees######################
fileNameData = [
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_DoubleEG_2016B_ver1_GoodLumi.root'
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_DoubleEG_2016B_ver2_GoodLumi.root',
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_DoubleEG_2016C_GoodLumi.root',
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_DoubleEG_2016D_GoodLumi.root',
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_DoubleEG_2016E_GoodLumi.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_DoubleEG_2016F_GoodLumi.root'
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_DoubleEG_2016G_GoodLumi.root',
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_DoubleEG_2016H_GoodLumi.root'
		]

fileNameGJets = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]
fileNameQCD = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]	
fileNameSig = [
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GluinoToNeutralinoToGratinoPhoton_M1000_CTau500mm.root',
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GluinoToNeutralinoToGratinoPhoton_M1000_CTau5000mm.root',
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_NeutralinoNeutralinoToGravitinoGravitinoPhotonPhoton_M1000_CTau500mm.root',
		#'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_NeutralinoNeutralinoToGravitinoGravitinoPhotonPhoton_M1000_CTau5000mm.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GMSB_CTau2190mm.root'
		]
################lumi and cross sections#################
lumi = 0.993 #35900 #pb^-1
xsecSig = 0.086*32.5 #pb, scaled from AN2011-081 based on gluino production xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections7TeVgluglu, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVgluglu
xsecGJets = [20790.0, 9238.0, 2305, 274.4, 93.46] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Gamma_jets
xsecQCD = [1712000, 347700, 32100, 6831, 1207, 119.9, 25.24] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD

###############cuts and outputs########################
cut = 'pho1Pt > 40 && abs(pho1Eta)<1.44 && pho1passIsoLoose && pho1passEleVeto'
cut_skim = "pho1Pt > 40 && abs(pho1Eta)<1.44 && pho1passIsoLoose && pho1passEleVeto && n_Jets >= 2"
outputDir = '/afs/cern.ch/user/z/zhicaiz/www/sharebox/DelayedPhoton/25Sept2017/'

############define the plot you want to make##########
plots = []
#variable name in the tree, output plot file name, description/title, Nbins, lowX, upX 
plots.append(["pho1Sminor", "Sminor", "S_{minor}", 50,0,1])
