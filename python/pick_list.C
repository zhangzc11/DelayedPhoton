
void pick_list(){

	TFile * file_data = new TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root","READ");
	
	TTree * tree_data = (TTree*)file_data->Get("DelayedPhoton");
	//TString cut = "pho1Pt > 40 && abs(pho1Eta)<1.44 && pho1passEleVeto && (HLTDecision[81] == 1)&&pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && pho1SigmaIetaIeta < 0.00994 &&n_Jets > 2&&n_Photons == 2&& Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==0 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0";
	TString cut = "pho1Pt > 40 && abs(pho1Eta)<1.44 && pho1passEleVeto && (HLTDecision[81] == 1)&&pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && pho1SigmaIetaIeta < 0.00994 &&n_Jets > 2&&n_Photons == 2&& Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 0 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0";
	
	TTree * tree_copy = tree_data->CopyTree(cut);

	UInt_t run;
	UInt_t lumi;
	UInt_t event;
	
	tree_copy->SetBranchAddress("run",&run);	
	tree_copy->SetBranchAddress("lumi",&lumi);	
	tree_copy->SetBranchAddress("event",&event);	
	
	int N_entries = tree_copy->GetEntries();
	for(int i =0; i<N_entries; i++){
		tree_copy->GetEntry(i);
		
		cout<<run<<":"<<lumi<<":"<<event<<", ";
	}

}

