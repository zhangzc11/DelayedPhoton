#include <sys/stat.h>
#include <sys/types.h>

bool drawOnly = true;

float axisTitleSize = 0.06;
float axisTitleOffset = 0.8;
float axisTitleSizeRatioX   = 0.18;
float axisLabelSizeRatioX   = 0.12;
float axisTitleOffsetRatioX = 0.94;
float axisTitleSizeRatioY   = 0.15;
float axisLabelSizeRatioY   = 0.108;
float axisTitleOffsetRatioY = 0.32;
float leftMargin   = 0.12;
float rightMargin  = 0.05;
float topMargin    = 0.09;
float bottomMargin = 0.12;

TString outputDir="/data/zhicaiz/www/sharebox/DelayedPhoton/23Sept2018/orderByPt/";

//mkdir(outputDir, S_IRWXU | S_IRWXG | S_IRWXO);
//mkdir(outputDir+"/ZeeTiming/", S_IRWXU | S_IRWXG | S_IRWXO);

float * doubGausFit(TH1F *hist){
	if(hist->Integral() < 100.0){
		float result[4] = {0};
		float * pointer = new float[4];
		for(int i=0; i<4; i++) pointer[i] = result[i];
		return pointer;
	}

	float x_mean=hist->GetMean();
	float x_stddev=hist->GetStdDev();
	float x_min=x_mean - 3.5*x_stddev;
	float x_max=x_mean + 3.5*x_stddev;
	float sig_small = 0.7*x_stddev;
	float sig_big = 1.11*x_stddev;
	TF1 * tf1_doubGaus = new TF1("tf1_doubGaus","gaus(0)+gaus(3)", x_min,x_max);
	tf1_doubGaus->SetParameters(0.6*hist->Integral(),0.5*(x_min+x_max),sig_small, 0.4*hist->Integral(),0.5*(x_min+x_max),sig_big);
	tf1_doubGaus->SetParLimits(0,0.1,hist->Integral());
	tf1_doubGaus->SetParLimits(3,0.1,hist->Integral());
	tf1_doubGaus->SetParLimits(2,0.0520,0.500);
	tf1_doubGaus->SetParLimits(5,0.0520,0.500);
	hist->Fit("tf1_doubGaus","B","",x_min,x_max);
	float N1 = tf1_doubGaus->GetParameter(0);
	float u1 = tf1_doubGaus->GetParameter(1);
	float eu1 = tf1_doubGaus->GetParError(1);
	float s1 = abs(tf1_doubGaus->GetParameter(2));
	float es1 = tf1_doubGaus->GetParError(2);
	float N2 = tf1_doubGaus->GetParameter(3);
	float u2 = tf1_doubGaus->GetParameter(4);
	float eu2 = tf1_doubGaus->GetParError(4);
	float s2 = abs(tf1_doubGaus->GetParameter(5));
	float es2 = tf1_doubGaus->GetParError(5);
	float sigEff = 0.0;
	float esigEff = 0.0;
	float meanEff = 0.0;
	float emeanEff = 0.0;
	if (N1+N2 > 0.0) {
	 	sigEff = 1.000*(N1*s1 + N2*s2) / (N1+N2);
	 	esigEff = 1.000* sqrt(N1*N1*es1*es1 + N2*N2*es2*es2)/(N1+N2);
	 	meanEff = 1.000*(N1*u1 + N2*u2) / (N1+N2);
	 	emeanEff = 1.000* sqrt(N1*N1*eu1*eu1 + N2*N2*eu2*eu2)/(N1+N2);
	}
	float result[4] = {meanEff,emeanEff,sigEff,esigEff};

	float * pointer = new float[4];
	for(int i=0; i<4; i++) pointer[i] = result[i];
	delete tf1_doubGaus;
	return pointer;
}

float * singGausFit(TH1F *hist){
	if(hist->Integral() < 100.0 && hist->Integral() > 20.0){
		float result[4] = {float(hist->GetMean()), float(hist->GetMeanError()), float(hist->GetStdDev()), float(hist->GetStdDevError())};
		float * pointer = new float[4];
		for(int i=0; i<4; i++) pointer[i] = result[i];
		return pointer;
	}
	
	if(hist->Integral() < 20.0){
		float result[4] = {0};
		float * pointer = new float[4];
		for(int i=0; i<4; i++) pointer[i] = result[i];
		return pointer;
	}

	float x_mean=hist->GetMean();
	float x_stddev=hist->GetStdDev();
	float x_min=x_mean - 2.0*x_stddev;
	float x_max=x_mean + 2.0*x_stddev;
	TF1 * tf1_singGaus = new TF1("tf1_singGaus","gaus(0)", x_min,x_max);
	tf1_singGaus->SetParameters(hist->Integral(), x_mean, x_stddev);
	hist->Fit("tf1_singGaus","Q","",x_min,x_max);
	float sigEff = 1.000*abs(tf1_singGaus->GetParameter(2));
        float esigEff = 1.000*tf1_singGaus->GetParError(2);
        float meanEff = 1.000*tf1_singGaus->GetParameter(1);
        float emeanEff = 1.000*tf1_singGaus->GetParError(1);
	if(abs(meanEff)>1.0){
		meanEff = 0.0, emeanEff = 0.0, sigEff = 0.0, esigEff = 0.0;
	}
	float result[4] = {meanEff,emeanEff,sigEff,esigEff};

	float * pointer = new float[4];
	for(int i=0; i<4; i++) pointer[i] = result[i];
	delete tf1_singGaus;
	return pointer;
}

       
void DrawCMS(TCanvas *myC, int energy, float lumi)
{
        myC->cd();
        TLatex *tlatex =  new TLatex();

        tlatex->SetNDC();
        tlatex->SetTextAngle(0);
        tlatex->SetTextColor(kBlack);
        tlatex->SetTextFont(63);
        tlatex->SetTextAlign(11);
        tlatex->SetTextSize(25);
        tlatex->DrawLatex(0.16, 0.95, "CMS");
        tlatex->SetTextFont(53);
        tlatex->DrawLatex(0.23, 0.95, "Preliminary");
        tlatex->SetTextFont(43);
        tlatex->SetTextSize(23);

        TString lumiString = Form("%.2f pb^{-1} (%d TeV)", lumi, energy);

        if (lumi > 1000.0)
        {
                lumiString = Form("%.2f fb^{-1} (%d TeV)", lumi/1000.0, energy);
        }

        std::string Lumi ((const char*) lumiString);
        tlatex->SetTextAlign(31);
        tlatex->DrawLatex(0.9, 0.95, Lumi.c_str());
        tlatex->SetTextAlign(11);
};

void drawTimeResoVsAeff(TTree * tree_data, TTree * tree_MC, TString label){
	cout<<"draw time resolution vs Aeff plots for "<<label<<endl;
	cout<<"data sampel size  = "<<tree_data->GetEntries()<<endl;	
	cout<<"MC sampel size  = "<<tree_MC->GetEntries()<<endl;	

	gStyle->SetOptFit(1);
	gStyle->SetOptStat(0);

	TCanvas * myC = new TCanvas( "myC_Time_vs_Aeff", "myC_Time_vs_Aeff", 200, 10, 800, 800 );
	myC->SetHighLightColor(2);
	myC->SetFillColor(0);
	myC->SetBorderMode(0);
	myC->SetBorderSize(2);
	myC->SetLeftMargin( leftMargin );
	myC->SetRightMargin( rightMargin );
	myC->SetTopMargin( topMargin );
	myC->SetBottomMargin( bottomMargin );
	myC->SetFrameBorderMode(0);
	myC->SetFrameBorderMode(0);
	
	const int N_Eeff_points = 10;	
	float Eeff_divide[11] = {200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 600.0, 700.0, 900.0, 2000.0};	
	
	float x_Eeff[N_Eeff_points] = {0};
	float ex_Eeff[N_Eeff_points] = {0};
	float y_Eeff_mean_data[N_Eeff_points] = {0};
	float y_Eeff_mean_MC[N_Eeff_points] = {0};
	float y_Eeff_sigma_dt_data[N_Eeff_points] = {0};
	float y_Eeff_sigma_dt_MC[N_Eeff_points] = {0};
	float ey_Eeff_mean_data[N_Eeff_points] = {0};
	float ey_Eeff_mean_MC[N_Eeff_points] = {0};
	float ey_Eeff_sigma_dt_data[N_Eeff_points] = {0};
	float ey_Eeff_sigma_dt_MC[N_Eeff_points] = {0};

	for(int i=0; i< N_Eeff_points; i++){
		x_Eeff[i] = 0.5*(Eeff_divide[i+1]+Eeff_divide[i]);
		ex_Eeff[i] = 0.5*(Eeff_divide[i+1]-Eeff_divide[i]);
		float Eeff_low_this = Eeff_divide[i];
		float Eeff_high_this = Eeff_divide[i+1];
		TString cut_2e_this = ("(E1/pedestal1)*(E2/pedestal2)/sqrt((E1/pedestal1)*(E1/pedestal1)+(E2/pedestal2)*(E2/pedestal2)) > "+std::to_string(Eeff_low_this)+" && (E1/pedestal1)*(E2/pedestal2)/sqrt((E1/pedestal1)*(E1/pedestal1)+(E2/pedestal2)*(E2/pedestal2)) < "+std::to_string(Eeff_high_this)).c_str();
;
		TH1F * hist_2e_this_data = new TH1F(("hist_2e_this_data_"+std::to_string(i)).c_str(),("hist_2e_this_data_"+std::to_string(i)).c_str(), 60, -1.5, 1.5);
		tree_data->Draw(("t1-t2>>hist_2e_this_data_"+std::to_string(i)).c_str(), cut_2e_this);
		hist_2e_this_data->Draw();
		float * result_2e_this_data = doubGausFit(hist_2e_this_data);
		myC->SaveAs(outputDir+"/ZeeTiming/iEeffFit_xtal_"+std::to_string(i)+"_dt_data_CLK_"+label+".png");		

		TH1F * hist_2e_this_MC = new TH1F(("hist_2e_this_MC_"+std::to_string(i)).c_str(),("hist_2e_this_MC_"+std::to_string(i)).c_str(), 60, -1.5, 1.5);
		tree_MC->Draw(("t1-t2>>hist_2e_this_MC_"+std::to_string(i)).c_str(), cut_2e_this);
		hist_2e_this_MC->Draw();
		float * result_2e_this_MC = doubGausFit(hist_2e_this_MC);
		myC->SaveAs(outputDir+"/ZeeTiming/iEeffFit_xtal_"+std::to_string(i)+"_dt_MC_CLK_"+label+".png");		

		y_Eeff_sigma_dt_data[i] = (result_2e_this_data[2]);
		ey_Eeff_sigma_dt_data[i] = (result_2e_this_data[3]);
		y_Eeff_sigma_dt_MC[i] = (result_2e_this_MC[2]);
		ey_Eeff_sigma_dt_MC[i] = (result_2e_this_MC[3]);
		delete result_2e_this_data;
		delete result_2e_this_MC;
		delete hist_2e_this_data;
		delete hist_2e_this_MC;
		cout<<"===bin "<<i<<"  "<<y_Eeff_sigma_dt_data[i]<<"   "<<ey_Eeff_sigma_dt_data[i]<<"   "<<y_Eeff_sigma_dt_MC[i]<<"   "<<ey_Eeff_sigma_dt_MC[i]<<endl;
	}
	
	gStyle->SetOptFit(0);
	myC->SetGridy(1);
	myC->SetGridx(1);
	myC->SetLogx(1);

	TGraphErrors *gr_Eeff_sigma_dt_data  =  new TGraphErrors(N_Eeff_points, x_Eeff, y_Eeff_sigma_dt_data, ex_Eeff, ey_Eeff_sigma_dt_data);
	gr_Eeff_sigma_dt_data->Draw("AP");
	gr_Eeff_sigma_dt_data->SetMarkerColor(kBlue);
	gr_Eeff_sigma_dt_data->SetLineColor(kBlue);
	gr_Eeff_sigma_dt_data->SetLineWidth(2);
	gr_Eeff_sigma_dt_data->SetTitle("");
	gr_Eeff_sigma_dt_data->GetXaxis()->SetTitle("A_{eff}/#sigma_{n}");
	gr_Eeff_sigma_dt_data->GetYaxis()->SetTitle("#sigma_{t1-t2} [ns]");
	gr_Eeff_sigma_dt_data->GetXaxis()->SetTitleSize( axisTitleSize - 0.02 );
	gr_Eeff_sigma_dt_data->GetXaxis()->SetTitleOffset( axisTitleOffset  + 0.6);
	gr_Eeff_sigma_dt_data->GetYaxis()->SetTitleSize( axisTitleSize );
	gr_Eeff_sigma_dt_data->GetYaxis()->SetTitleOffset( axisTitleOffset +0.18 );
	gr_Eeff_sigma_dt_data->GetYaxis()->SetRangeUser(0.05,0.35);
	gr_Eeff_sigma_dt_data->GetXaxis()->SetRangeUser(200,2000);
	gr_Eeff_sigma_dt_data->GetXaxis()->SetMoreLogLabels();

	TF1 * tf1_dt_vs_Eeff_data = new TF1("tf1_dt_vs_Eeff_data","sqrt([0]/(x*x)+[1])", 200.0, 2000.0);
	tf1_dt_vs_Eeff_data->SetLineColor(kBlue);
	tf1_dt_vs_Eeff_data->SetParameters(50.0*50.0, 0.1*0.1);
	gr_Eeff_sigma_dt_data->Fit("tf1_dt_vs_Eeff_data","","",200.0, 2000.0);
	float fit_dt_a_data = tf1_dt_vs_Eeff_data->GetParameter(0);
	float efit_dt_a_data = tf1_dt_vs_Eeff_data->GetParError(0);
	float fit_dt_b_data = tf1_dt_vs_Eeff_data->GetParameter(1);
	float efit_dt_b_data = tf1_dt_vs_Eeff_data->GetParError(1);

	TGraphErrors * gr_Eeff_sigma_dt_MC  =  new TGraphErrors(N_Eeff_points, x_Eeff, y_Eeff_sigma_dt_MC, ex_Eeff, ey_Eeff_sigma_dt_MC);
	gr_Eeff_sigma_dt_MC->SetMarkerColor(kRed);
	gr_Eeff_sigma_dt_MC->SetLineColor(kRed);
	gr_Eeff_sigma_dt_MC->SetLineWidth(2);
	gr_Eeff_sigma_dt_MC->Draw("Psame");

	TF1 * tf1_dt_vs_Eeff_MC = new TF1("tf1_dt_vs_Eeff_MC","sqrt([0]/(x*x)+[1])", 200.0, 2000.0);
	tf1_dt_vs_Eeff_MC->SetLineColor(kRed);
	tf1_dt_vs_Eeff_MC->SetParameters(50.0*50.0, 0.01*0.01);
	gr_Eeff_sigma_dt_MC->Fit("tf1_dt_vs_Eeff_MC","","",200.0, 2000.0);
	float fit_dt_a_MC = tf1_dt_vs_Eeff_MC->GetParameter(0);
	float efit_dt_a_MC = tf1_dt_vs_Eeff_MC->GetParError(0);
	float fit_dt_b_MC = tf1_dt_vs_Eeff_MC->GetParameter(1);
	float efit_dt_b_MC = tf1_dt_vs_Eeff_MC->GetParError(1);

	TLegend * leg_sigma_dt = new TLegend(0.18,0.84,0.48,0.90);
	leg_sigma_dt->SetNColumns(3);
	leg_sigma_dt->SetBorderSize(0);
	leg_sigma_dt->SetTextSize(0.03);
	leg_sigma_dt->SetLineColor(1);
	leg_sigma_dt->SetLineStyle(1);
	leg_sigma_dt->SetLineWidth(1);
	leg_sigma_dt->SetFillColor(0);
	leg_sigma_dt->SetFillStyle(1001);
	leg_sigma_dt->AddEntry(gr_Eeff_sigma_dt_data, "data", "lep");
	leg_sigma_dt->AddEntry(gr_Eeff_sigma_dt_MC, "MC", "lep");

	leg_sigma_dt->Draw();

	TLatex * tlatex = new TLatex();
	tlatex->SetNDC();
	tlatex->SetTextAngle(0);
	tlatex->SetTextColor(1);
	tlatex->SetTextFont(63);
	tlatex->SetTextAlign(11);
	tlatex->SetTextSize(25);
	tlatex->DrawLatex(0.5, 0.85, "#sigma = #frac{N}{A_{eff}/#sigma_{n}} #oplus #sqrt{2} C");

	float N_data=sqrt(abs(fit_dt_a_data));
	float eN_data=abs(efit_dt_a_data)/(2.0*sqrt(abs(fit_dt_a_data)));
	float C_data=sqrt(abs(fit_dt_b_data)/2.0);
	float eC_data=abs(efit_dt_b_data)/(4.0*sqrt(abs(fit_dt_b_data)/2.0));

	float N_MC=sqrt(abs(fit_dt_a_MC));
	float eN_MC=abs(efit_dt_a_MC)/(2.0*sqrt(abs(fit_dt_a_MC)));
	float C_MC=sqrt(abs(fit_dt_b_MC)/2.0);
	float eC_MC=abs(efit_dt_b_MC)/(4.0*sqrt(abs(fit_dt_b_MC)/2.0));

	tlatex->SetTextColor(kBlue);
	tlatex->DrawLatex(0.5, 0.78, Form("N^{data} = %.1f #pm %.1f ns", N_data, eN_data));
	tlatex->DrawLatex(0.5, 0.71, Form("C^{data} = %.3f #pm %.3f ns", C_data, eC_data));
	tlatex->SetTextColor(kRed);
	tlatex->DrawLatex(0.5, 0.64, Form("N^{MC} = %.1f #pm %.1f ns", N_MC, eN_MC));
	tlatex->DrawLatex(0.5, 0.57, Form("C^{MC} = %.3f #pm %.3f ns", C_MC, eC_MC));

	DrawCMS(myC, 13, 35922.0);

	myC->SaveAs(outputDir+"/ZeeTiming/TimingReso_xtals_dt_vs_Eeff_sigma_Data_vs_MC_2016_select_CLK_"+label+".pdf");
	myC->SaveAs(outputDir+"/ZeeTiming/TimingReso_xtals_dt_vs_Eeff_sigma_Data_vs_MC_2016_select_CLK_"+label+".png");
	myC->SaveAs(outputDir+"/ZeeTiming/TimingReso_xtals_dt_vs_Eeff_sigma_Data_vs_MC_2016_select_CLK_"+label+".C");
	
	delete myC;
	delete gr_Eeff_sigma_dt_data;
	delete tf1_dt_vs_Eeff_data;
	delete tf1_dt_vs_Eeff_MC;

}

bool isNeighboringXtal(int iEta1, int iPhi1, int iEta2, int iPhi2){
	int distance = (iEta1-iEta2)*(iEta1-iEta2) + (iPhi1-iPhi2)*(iPhi1-iPhi2);
	if(distance == 1) return true;
	else return false;
}

bool isring1Xtal(int iEta1, int iPhi1, int iEta2, int iPhi2){
	//int distance = (iEta1-iEta2)*(iEta1-iEta2) + (iPhi1-iPhi2)*(iPhi1-iPhi2);
	int dEta = abs(iEta1-iEta2);
	int dPhi = abs(iPhi1-iPhi2);
	if((dEta == 1 && dPhi<=1) || (dPhi == 1 && dEta <=1)) return true;
	else return false;
}

bool isring2Xtal(int iEta1, int iPhi1, int iEta2, int iPhi2){
	//int distance = (iEta1-iEta2)*(iEta1-iEta2) + (iPhi1-iPhi2)*(iPhi1-iPhi2);
	int dEta = abs(iEta1-iEta2);
	int dPhi = abs(iPhi1-iPhi2);
	if((dEta == 2 && dPhi<=2) || (dPhi == 2 && dEta <=2)) return true;
	else return false;
}

bool issameTrigTowerXtal(int iEta1, int iPhi1, int iEta2, int iPhi2){
	int distance = (iEta1-iEta2)*(iEta1-iEta2) + (iPhi1-iPhi2)*(iPhi1-iPhi2);
	bool issameTrigTower = false;
	
	int iTTeta1 = (abs(iEta1)/iEta1) * ((abs(iEta1)+4)/5);// 1-5, 6-10, ...  85, and negative
	int iTTeta2 = (abs(iEta2)/iEta2) * ((abs(iEta2)+4)/5);// 1-5, 6-10, ...  85, and negative
	int iTTphi1 = (iPhi1-1)/5;// 1-5, 6-10, ... 360
	int iTTphi2 = (iPhi2-1)/5;// 1-5, 6-10, ... 360
		
	if(iTTeta1 == iTTeta2 && iTTphi1 == iTTphi2 && distance > 0) issameTrigTower = true;

	return issameTrigTower;	
}


void properScale(TH1F * hist){
	float norm = 1.0/hist->Integral();
	for(int i=0; i<hist->GetNbinsX()+1; i++){
		float v0 = hist->GetBinContent(i);
		hist->SetBinContent(i, norm*v0);
		if(v0 > 1.0) hist->SetBinError(i, norm*v0/sqrt(v0));
		else hist->SetBinError(i,0.0);
	}
}


void drawTimingMap(TH2F * h2_map, TString label){
	cout<<"draw timing map for "<<label<<endl;
	
	gStyle->SetOptStat(0);
	gStyle->SetPalette(1);

	TCanvas * myC = new TCanvas( "myC_map", "myC_map", 200, 10, 1000, 600 );
	myC->SetRightMargin( rightMargin + 0.08);

	h2_map->SetTitle("");
	h2_map->GetXaxis()->SetTitle("iEta");
	h2_map->GetYaxis()->SetTitle("iPhi");
	h2_map->GetXaxis()->SetTitleSize( axisTitleSize );
	h2_map->GetXaxis()->SetTitleOffset( axisTitleOffset);
	h2_map->GetYaxis()->SetTitleSize( axisTitleSize );
	h2_map->GetYaxis()->SetTitleOffset( axisTitleOffset);
	h2_map->GetZaxis()->SetTitle("time [ns]");	
	h2_map->GetZaxis()->SetTitleSize( axisTitleSize );
	h2_map->GetZaxis()->SetTitleOffset( axisTitleOffset - 0.2);

	float meanZ = 0.0;
	for (int ix=1;ix<=171;ix++){for(int iy=1;iy<=360;iy++){meanZ += h2_map->GetBinContent(ix,iy);}}
	meanZ = meanZ/(171.0*360.0);

	float minZ = ceil(10.0*(meanZ - 0.1))/10.0 - 0.1;
	float maxZ = ceil(10.0*(meanZ + 0.1))/10.0;

	//if(label == "MC") minZ = -0.5, maxZ = 0.5;
	//if(label == "data") minZ = -0.1, maxZ = 0.1;
	h2_map->GetZaxis()->SetRangeUser(minZ,maxZ);	
	h2_map->Draw("colz");

	//DrawCMS(myC, 13, 35922.0);
	
	myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_"+label+".pdf");
	myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_"+label+".png");
	myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_"+label+".C");

	h2_map->GetYaxis()->SetRangeUser(0.5,50.5);
        h2_map->GetXaxis()->SetRangeUser(0.5,85.5);
        h2_map->Draw("colz");
        myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_data_zoom.pdf");
	myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_"+label+"_zoom.pdf");
	myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_"+label+"_zoom.png");
	myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_"+label+"_zoom.C");

	delete myC;

}
void TimingMap_2016()
{


	TFile * file_data = new TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/All2016.root","READ");
	TTree * tree_data = (TTree*)file_data->Get("ZeeTiming");
	tree_data->SetCacheSize(12000000000);//12GB

	TFile * file_MC = new TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/MC2016_all.root","READ");
	TTree * tree_MC = (TTree*)file_MC->Get("ZeeTiming");
	tree_MC->SetCacheSize(3000000000);//3GB

	int N_entries_data = tree_data->GetEntries();	
	int N_entries_MC = tree_MC->GetEntries();	
	//import input variables
	float ele1seedE;
	float seed1_pedestal;
	bool ele1IsEB;
	float t1_seed;
	float t1raw_seed;
	int ele1seedIEta;
	int ele1seedIPhi;
	std::vector<float> *ele1Rechit_E = 0;
	std::vector<float> *ele1Rechit_pedestal = 0;
	std::vector<float> *ele1Rechit_rawT = 0;
	std::vector<float> *ele1Rechit_t = 0;
	std::vector<float> *ele1Rechit_IEtaIX = 0;
	std::vector<float> *ele1Rechit_IPhiIY = 0;

	float ele2seedE;
	float seed2_pedestal;
	bool ele2IsEB;
	float t2_seed;
	float t2raw_seed;
	int ele2seedIEta;
	int ele2seedIPhi;
	std::vector<float> *ele2Rechit_E = 0;
	std::vector<float> *ele2Rechit_pedestal = 0;
	std::vector<float> *ele2Rechit_rawT = 0;
	std::vector<float> *ele2Rechit_t = 0;
	std::vector<float> *ele2Rechit_IEtaIX = 0;
	std::vector<float> *ele2Rechit_IPhiIY = 0;

	tree_data->SetBranchStatus("ele1seedE",1);	
	tree_data->SetBranchStatus("seed1_pedestal",1);	
	tree_data->SetBranchStatus("ele1IsEB",1);	
	tree_data->SetBranchStatus("t1_seed",1);	
	tree_data->SetBranchStatus("t1raw_seed",1);	
	tree_data->SetBranchStatus("ele1seedIEta",1);	
	tree_data->SetBranchStatus("ele1seedIPhi",1);	
	tree_data->SetBranchStatus("ele1Rechit_E",1);	
	tree_data->SetBranchStatus("ele1Rechit_pedestal",1);	
	tree_data->SetBranchStatus("ele1Rechit_rawT",1);	
	tree_data->SetBranchStatus("ele1Rechit_t",1);	
	tree_data->SetBranchStatus("ele1Rechit_IEtaIX",1);	
	tree_data->SetBranchStatus("ele1Rechit_IPhiIY",1);	
	
	tree_data->SetBranchAddress("ele1seedE", & ele1seedE);
	tree_data->SetBranchAddress("seed1_pedestal", & seed1_pedestal);
	tree_data->SetBranchAddress("ele1IsEB", & ele1IsEB);
	tree_data->SetBranchAddress("t1_seed", & t1_seed);
	tree_data->SetBranchAddress("t1raw_seed", & t1raw_seed);
	tree_data->SetBranchAddress("ele1seedIEta", & ele1seedIEta);
	tree_data->SetBranchAddress("ele1seedIPhi", & ele1seedIPhi);
	tree_data->SetBranchAddress("ele1Rechit_E", & ele1Rechit_E);
	tree_data->SetBranchAddress("ele1Rechit_pedestal", & ele1Rechit_pedestal);
	tree_data->SetBranchAddress("ele1Rechit_rawT", & ele1Rechit_rawT);
	tree_data->SetBranchAddress("ele1Rechit_t", & ele1Rechit_t);
	tree_data->SetBranchAddress("ele1Rechit_IEtaIX", & ele1Rechit_IEtaIX);
	tree_data->SetBranchAddress("ele1Rechit_IPhiIY", & ele1Rechit_IPhiIY);

	tree_data->SetBranchStatus("ele2seedE",1);	
	tree_data->SetBranchStatus("seed2_pedestal",1);	
	tree_data->SetBranchStatus("ele2IsEB",1);	
	tree_data->SetBranchStatus("t2_seed",1);	
	tree_data->SetBranchStatus("t2raw_seed",1);	
	tree_data->SetBranchStatus("ele2seedIEta",1);	
	tree_data->SetBranchStatus("ele2seedIPhi",1);	
	tree_data->SetBranchStatus("ele2Rechit_E",1);	
	tree_data->SetBranchStatus("ele2Rechit_pedestal",1);	
	tree_data->SetBranchStatus("ele2Rechit_rawT",1);	
	tree_data->SetBranchStatus("ele2Rechit_t",1);	
	tree_data->SetBranchStatus("ele2Rechit_IEtaIX",1);	
	tree_data->SetBranchStatus("ele2Rechit_IPhiIY",1);	
	
	tree_data->SetBranchAddress("ele2seedE", & ele2seedE);
	tree_data->SetBranchAddress("seed2_pedestal", & seed2_pedestal);
	tree_data->SetBranchAddress("ele2IsEB", & ele2IsEB);
	tree_data->SetBranchAddress("t2_seed", & t2_seed);
	tree_data->SetBranchAddress("t2raw_seed", & t2raw_seed);
	tree_data->SetBranchAddress("ele2seedIEta", & ele2seedIEta);
	tree_data->SetBranchAddress("ele2seedIPhi", & ele2seedIPhi);
	tree_data->SetBranchAddress("ele2Rechit_E", & ele2Rechit_E);
	tree_data->SetBranchAddress("ele2Rechit_pedestal", & ele2Rechit_pedestal);
	tree_data->SetBranchAddress("ele2Rechit_rawT", & ele2Rechit_rawT);
	tree_data->SetBranchAddress("ele2Rechit_t", & ele2Rechit_t);
	tree_data->SetBranchAddress("ele2Rechit_IEtaIX", & ele2Rechit_IEtaIX);
	tree_data->SetBranchAddress("ele2Rechit_IPhiIY", & ele2Rechit_IPhiIY);


	tree_MC->SetBranchStatus("ele1seedE",1);	
	tree_MC->SetBranchStatus("seed1_pedestal",1);	
	tree_MC->SetBranchStatus("ele1IsEB",1);	
	tree_MC->SetBranchStatus("t1_seed",1);	
	tree_MC->SetBranchStatus("t1raw_seed",1);	
	tree_MC->SetBranchStatus("ele1seedIEta",1);	
	tree_MC->SetBranchStatus("ele1seedIPhi",1);	
	tree_MC->SetBranchStatus("ele1Rechit_E",1);	
	tree_MC->SetBranchStatus("ele1Rechit_pedestal",1);	
	tree_MC->SetBranchStatus("ele1Rechit_rawT",1);	
	tree_MC->SetBranchStatus("ele1Rechit_t",1);	
	tree_MC->SetBranchStatus("ele1Rechit_IEtaIX",1);	
	tree_MC->SetBranchStatus("ele1Rechit_IPhiIY",1);	
	
	tree_MC->SetBranchAddress("ele1seedE", & ele1seedE);
	tree_MC->SetBranchAddress("seed1_pedestal", & seed1_pedestal);
	tree_MC->SetBranchAddress("ele1IsEB", & ele1IsEB);
	tree_MC->SetBranchAddress("t1_seed", & t1_seed);
	tree_MC->SetBranchAddress("t1raw_seed", & t1raw_seed);
	tree_MC->SetBranchAddress("ele1seedIEta", & ele1seedIEta);
	tree_MC->SetBranchAddress("ele1seedIPhi", & ele1seedIPhi);
	tree_MC->SetBranchAddress("ele1Rechit_E", & ele1Rechit_E);
	tree_MC->SetBranchAddress("ele1Rechit_pedestal", & ele1Rechit_pedestal);
	tree_MC->SetBranchAddress("ele1Rechit_rawT", & ele1Rechit_rawT);
	tree_MC->SetBranchAddress("ele1Rechit_t", & ele1Rechit_t);
	tree_MC->SetBranchAddress("ele1Rechit_IEtaIX", & ele1Rechit_IEtaIX);
	tree_MC->SetBranchAddress("ele1Rechit_IPhiIY", & ele1Rechit_IPhiIY);
	
	
	tree_MC->SetBranchStatus("ele2seedE",1);	
	tree_MC->SetBranchStatus("seed2_pedestal",1);	
	tree_MC->SetBranchStatus("ele2IsEB",1);	
	tree_MC->SetBranchStatus("t2_seed",1);	
	tree_MC->SetBranchStatus("t2raw_seed",1);	
	tree_MC->SetBranchStatus("ele2seedIEta",1);	
	tree_MC->SetBranchStatus("ele2seedIPhi",1);	
	tree_MC->SetBranchStatus("ele2Rechit_E",1);	
	tree_MC->SetBranchStatus("ele2Rechit_pedestal",1);	
	tree_MC->SetBranchStatus("ele2Rechit_rawT",1);	
	tree_MC->SetBranchStatus("ele2Rechit_t",1);	
	tree_MC->SetBranchStatus("ele2Rechit_IEtaIX",1);	
	tree_MC->SetBranchStatus("ele2Rechit_IPhiIY",1);	
	
	tree_MC->SetBranchAddress("ele2seedE", & ele2seedE);
	tree_MC->SetBranchAddress("seed2_pedestal", & seed2_pedestal);
	tree_MC->SetBranchAddress("ele2IsEB", & ele2IsEB);
	tree_MC->SetBranchAddress("t2_seed", & t2_seed);
	tree_MC->SetBranchAddress("t2raw_seed", & t2raw_seed);
	tree_MC->SetBranchAddress("ele2seedIEta", & ele2seedIEta);
	tree_MC->SetBranchAddress("ele2seedIPhi", & ele2seedIPhi);
	tree_MC->SetBranchAddress("ele2Rechit_E", & ele2Rechit_E);
	tree_MC->SetBranchAddress("ele2Rechit_pedestal", & ele2Rechit_pedestal);
	tree_MC->SetBranchAddress("ele2Rechit_rawT", & ele2Rechit_rawT);
	tree_MC->SetBranchAddress("ele2Rechit_t", & ele2Rechit_t);
	tree_MC->SetBranchAddress("ele2Rechit_IEtaIX", & ele2Rechit_IEtaIX);
	tree_MC->SetBranchAddress("ele2Rechit_IPhiIY", & ele2Rechit_IPhiIY);

	gStyle->SetOptFit(1);
	gStyle->SetOptStat(0);

	TCanvas * myC = new TCanvas( "myC", "myC", 200, 10, 800, 800 );
	myC->SetHighLightColor(2);
	myC->SetFillColor(0);
	myC->SetBorderMode(0);
	myC->SetBorderSize(2);
	myC->SetLeftMargin( leftMargin );
	myC->SetRightMargin( rightMargin );
	myC->SetTopMargin( topMargin );
	myC->SetBottomMargin( bottomMargin );
	myC->SetFrameBorderMode(0);
	myC->SetFrameBorderMode(0);
	
	/////data
	TH2F * h2_time_iEta_vs_iPhi_data = new TH2F("h2_time_iEta_vs_iPhi_data","h2_time_iEta_vs_iPhi_data",171, -85.5, 85.5, 360, 0.5, 360.5);	
	TH1F * h1_array_time_data[171][360];
	for(int iEta = 0; iEta < 171; iEta++){
		for(int iPhi = 0; iPhi<360; iPhi++){
		h1_array_time_data[iEta][iPhi] = new TH1F(("h1_time_data_iEta_"+std::to_string(iEta)+"_iPhi_"+std::to_string(iPhi)).c_str(), ("h1_time_iEta_"+std::to_string(iEta)+"_iPhi_"+std::to_string(iPhi)).c_str(), 60, -1.5, 1.5);
		}
	}

	for(int ientry=0;ientry<N_entries_data; ientry++){	
		if(ientry%100000 ==0) cout<<"reading original tree entry "<<ientry<<"  out of "<<N_entries_data<<endl;
                tree_data->GetEntry(ientry);
		if(ele1IsEB){
			for(int i=0; i<ele1Rechit_t->size(); i++){
				if(ele1Rechit_E->at(i)<1.0) continue;
				int idx_ieta = ele1Rechit_IEtaIX->at(i) + 85;
				int idx_iphi = ele1Rechit_IPhiIY->at(i) - 1;
				if(idx_ieta>=0 && idx_ieta <171 && idx_iphi>=0 && idx_iphi < 360){
					h1_array_time_data[idx_ieta][idx_iphi]->Fill(ele1Rechit_t->at(i));
				}
			}
		}
		if(ele2IsEB){
			for(int i=0; i<ele2Rechit_t->size(); i++){
				if(ele2Rechit_E->at(i)<1.0) continue;
				int idx_ieta = ele2Rechit_IEtaIX->at(i) + 85;
				int idx_iphi = ele2Rechit_IPhiIY->at(i) - 1;
				if(idx_ieta>=0 && idx_ieta <171 && idx_iphi>=0 && idx_iphi < 360){
					h1_array_time_data[idx_ieta][idx_iphi]->Fill(ele2Rechit_t->at(i));
				}
			}
		}
	}

	// do the fit to get the mean time in each ieta iphi bin

	for(int iEta = 0; iEta < 171; iEta++){
		for(int iPhi = 0; iPhi<360; iPhi++){
		//int ieta_this = iEta - 85;
		//int iphi_this = iPhi + 1;

		if(iPhi == 11 && iEta%22==0) h1_array_time_data[iEta][iPhi]->Draw();
		float * result_singGaus = singGausFit(h1_array_time_data[iEta][iPhi]);
		if(iPhi == 11 && iEta%9==0) myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_data_iEta"+std::to_string(iEta)+"_iPhi"+std::to_string(iPhi)+".png");
		h2_time_iEta_vs_iPhi_data->SetBinContent(iEta+1, iPhi+1, result_singGaus[0]);		
		}
	}
	//draw the map
	drawTimingMap(h2_time_iEta_vs_iPhi_data, "data");		

	/////MC
	TH2F * h2_time_iEta_vs_iPhi_MC = new TH2F("h2_time_iEta_vs_iPhi_MC","h2_time_iEta_vs_iPhi_MC",171, -85.5, 85.5, 360, 0.5, 360.5);	
	TH1F * h1_array_time_MC[171][360];
	for(int iEta = 0; iEta < 171; iEta++){
		for(int iPhi = 0; iPhi<360; iPhi++){
		h1_array_time_MC[iEta][iPhi] = new TH1F(("h1_time_MC_iEta_"+std::to_string(iEta)+"_iPhi_"+std::to_string(iPhi)).c_str(), ("h1_time_iEta_"+std::to_string(iEta)+"_iPhi_"+std::to_string(iPhi)).c_str(), 60, -1.5, 1.5);
		}
	}

	for(int ientry=0;ientry<N_entries_MC; ientry++){	
		if(ientry%100000 ==0) cout<<"reading original tree entry "<<ientry<<"  out of "<<N_entries_MC<<endl;
                tree_MC->GetEntry(ientry);
		if(ele1IsEB){
			for(int i=0; i<ele1Rechit_t->size(); i++){
				if(ele1Rechit_E->at(i)<1.0) continue;
				int idx_ieta = ele1Rechit_IEtaIX->at(i) + 85;
				int idx_iphi = ele1Rechit_IPhiIY->at(i) - 1;
				if(idx_ieta>=0 && idx_ieta <171 && idx_iphi>=0 && idx_iphi < 360){
					h1_array_time_MC[idx_ieta][idx_iphi]->Fill(ele1Rechit_t->at(i));
				}
			}
		}
		if(ele2IsEB){
			for(int i=0; i<ele2Rechit_t->size(); i++){
				if(ele2Rechit_E->at(i)<1.0) continue;
				int idx_ieta = ele2Rechit_IEtaIX->at(i) + 85;
				int idx_iphi = ele2Rechit_IPhiIY->at(i) - 1;
				if(idx_ieta>=0 && idx_ieta <171 && idx_iphi>=0 && idx_iphi < 360){
					h1_array_time_MC[idx_ieta][idx_iphi]->Fill(ele2Rechit_t->at(i));
				}
			}
		}
	}

	// do the fit to get the mean time in each ieta iphi bin

	for(int iEta = 0; iEta < 171; iEta++){
		for(int iPhi = 0; iPhi<360; iPhi++){
		//int ieta_this = iEta - 85;
		//int iphi_this = iPhi + 1;

		if(iPhi == 11 && iEta%22==0) h1_array_time_MC[iEta][iPhi]->Draw();
		float * result_singGaus = singGausFit(h1_array_time_MC[iEta][iPhi]);
		if(iPhi == 11 && iEta%9==0) myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_MC_iEta"+std::to_string(iEta)+"_iPhi"+std::to_string(iPhi)+".png");
		h2_time_iEta_vs_iPhi_MC->SetBinContent(iEta+1, iPhi+1, result_singGaus[0]);		
		}
	}
	//draw the map
	drawTimingMap(h2_time_iEta_vs_iPhi_MC, "MC");		

}
