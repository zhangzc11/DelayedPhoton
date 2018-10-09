#include <sys/stat.h>
#include <sys/types.h>

bool drawOnly = false;

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

//float * singGausFit(TH1F *hist){
float singGausFit(TH1F *hist){
	if(hist->Integral() < 100.0 && hist->Integral() > 20.0){
		//float result[4] = {float(hist->GetMean()), float(hist->GetMeanError()), float(hist->GetStdDev()), float(hist->GetStdDevError())};
		//float * pointer = new float[4];
		//for(int i=0; i<4; i++) pointer[i] = result[i];
		//return pointer;
		return float(hist->GetMean());
	}
	
	if(hist->Integral() < 20.0){
		//float result[4] = {0};
		//float * pointer = new float[4];
		//for(int i=0; i<4; i++) pointer[i] = result[i];
		//return pointer;
		return 0.0;
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

	//float result[4] = {meanEff,emeanEff,sigEff,esigEff};

	//float * pointer = new float[4];
	//for(int i=0; i<4; i++) pointer[i] = result[i];
	//delete tf1_singGaus;
	//return pointer;
	return meanEff;
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


void drawTimingMap(TH2F * h2_map, TString label, TString title="time [ns]", float minZ=-5.0, float maxZ=5.0){
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
	h2_map->GetZaxis()->SetTitle(title);	
	h2_map->GetZaxis()->SetTitleSize( axisTitleSize );
	h2_map->GetZaxis()->SetTitleOffset( axisTitleOffset - 0.2);

	float meanZ = 0.0;
	for (int ix=1;ix<=171;ix++){for(int iy=1;iy<=360;iy++){meanZ += h2_map->GetBinContent(ix,iy);}}
	meanZ = meanZ/(171.0*360.0);

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
	h2_map->GetYaxis()->SetRangeUser(0.5,360.5);
        h2_map->GetXaxis()->SetRangeUser(-85.5,85.5);
        h2_map->Draw("colz");

}
void TimingMap_2016()
{


	TFile * file_data = new TFile("/data/zhicaiz/data/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/ElectronTiming_All2016.root","READ");
	TTree * tree_data = (TTree*)file_data->Get("ElectronTiming");
	tree_data->SetCacheSize(12000000000);//12GB


	int N_entries_data = tree_data->GetEntries();	
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
	TH2F * h2_time_iEta_vs_iPhi_data;
	TH2F * h2_timeAll_iEta_vs_iPhi_data;
	TH2F * h2_timeTT_iEta_vs_iPhi_data;
	TH2F * h2_dt0_iEta_vs_iPhi_data;
	TH2F * h2_dt1_iEta_vs_iPhi_data;
	TH2F * h2_dt2_iEta_vs_iPhi_data;
	TH2F * h2_dt3_iEta_vs_iPhi_data;

	if(!drawOnly) h2_time_iEta_vs_iPhi_data = new TH2F("h2_time_iEta_vs_iPhi_data","h2_time_iEta_vs_iPhi_data",171, -85.5, 85.5, 360, 0.5, 360.5);	
	if(!drawOnly) h2_timeAll_iEta_vs_iPhi_data = new TH2F("h2_timeAll_iEta_vs_iPhi_data","h2_timeAll_iEta_vs_iPhi_data",171, -85.5, 85.5, 360, 0.5, 360.5);	
	if(!drawOnly) h2_timeTT_iEta_vs_iPhi_data = new TH2F("h2_timeTT_iEta_vs_iPhi_data","h2_timeTT_iEta_vs_iPhi_data",171, -85.5, 85.5, 360, 0.5, 360.5);	
	if(!drawOnly) h2_dt0_iEta_vs_iPhi_data = new TH2F("h2_dt0_iEta_vs_iPhi_data","h2_dt0_iEta_vs_iPhi_data",171, -85.5, 85.5, 360, 0.5, 360.5);	
	if(!drawOnly) h2_dt1_iEta_vs_iPhi_data = new TH2F("h2_dt1_iEta_vs_iPhi_data","h2_dt1_iEta_vs_iPhi_data",171, -85.5, 85.5, 360, 0.5, 360.5);	
	if(!drawOnly) h2_dt2_iEta_vs_iPhi_data = new TH2F("h2_dt2_iEta_vs_iPhi_data","h2_dt2_iEta_vs_iPhi_data",171, -85.5, 85.5, 360, 0.5, 360.5);	
	if(!drawOnly) h2_dt3_iEta_vs_iPhi_data = new TH2F("h2_dt3_iEta_vs_iPhi_data","h2_dt3_iEta_vs_iPhi_data",171, -85.5, 85.5, 360, 0.5, 360.5);	

	TH1F * h1_array_time_data[171][360][6];//0: to the right; 1: to the top; 2: to the left; 3: to the bottom
	float dt_array_time_data[171][360][6]={0};//0: to the right; 1: to the top; 2: to the left; 3: to the bottom
	for(int iEta = 0; iEta < 171; iEta++){
		for(int iPhi = 0; iPhi<360; iPhi++){
			for(int ineighb = 0; ineighb<6; ineighb++){
				h1_array_time_data[iEta][iPhi][ineighb] = new TH1F(("h1_time_data_iEta_"+std::to_string(iEta)+"_iPhi_"+std::to_string(iPhi)+"_ineighb_"+std::to_string(ineighb)).c_str(), ("h1_time_iEta_"+std::to_string(iEta)+"_iPhi_"+std::to_string(iPhi)+"_ineighb_"+std::to_string(ineighb)).c_str(), 60, -1.5, 1.5);
			}
		}
	}
	if(!drawOnly){
	for(int ientry=0;ientry<N_entries_data; ientry++){	
		if(ientry%1000000 ==0) cout<<"reading original tree entry "<<ientry<<"  out of "<<N_entries_data<<endl;
                tree_data->GetEntry(ientry);
		if(ele1IsEB && ele1seedE<120.0){
			float t1 = 0, t2 = 0;
			int ieta1 = 0, iphi1 = 0;
			int ieta2 = 0, iphi2 = 0;
			for(int isd=0;isd<ele1Rechit_IEtaIX->size(); isd++){
				if(ele1seedIEta == ele1Rechit_IEtaIX->at(isd) && ele1seedIPhi == ele1Rechit_IPhiIY->at(isd)){
					ieta1 = ele1Rechit_IEtaIX->at(isd);
                                        iphi1 = ele1Rechit_IPhiIY->at(isd);
					t1 = ele1Rechit_rawT->at(isd);
				}	
			}

			for(int i=0; i<ele1Rechit_rawT->size(); i++){
				if(ele1Rechit_E->at(i)<10.0) continue;
				if(ele1Rechit_E->at(i) > 120.0) continue;
				//bool pass_neighboring = isNeighboringXtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
				ieta2 = ele1Rechit_IEtaIX->at(i);
				iphi2 = ele1Rechit_IPhiIY->at(i);
				t2 = ele1Rechit_rawT->at(i);	

				int ieta2_TTlow = int((abs(ieta2)-1)/5)*5+1;
				int iphi2_TTlow	= int((abs(iphi2)-1)/5)*5+1;
				
				h1_array_time_data[ieta2+85][iphi2-1][4]->Fill(t2);
				if(ieta2>0){
					for(int ieta2_this=ieta2_TTlow; ieta2_this<ieta2_TTlow+5; ieta2_this++){
						for(int iphi2_this=iphi2_TTlow; iphi2_this<iphi2_TTlow+5; iphi2_this++){
							h1_array_time_data[ieta2_this+85][iphi2_this-1][5]->Fill(t2);
						}
					}
				}
				else{
					for(int ieta2_this=-1*ieta2_TTlow-4; ieta2_this<-1*ieta2_TTlow+1; ieta2_this++){
						for(int iphi2_this=iphi2_TTlow; iphi2_this<iphi2_TTlow+5; iphi2_this++){
							h1_array_time_data[ieta2_this+85][iphi2_this-1][5]->Fill(t2);
						}
					}
				}

				int idx_neighboring = -999;
				if(ieta2-ieta1 == 1 && iphi2-iphi1 == 0) idx_neighboring = 0;
				if(ieta2-ieta1 == 0 && iphi2-iphi1 == 1) idx_neighboring = 1;
				if(ieta2-ieta1 == -1 && iphi2-iphi1 == 0) idx_neighboring = 2;
				if(ieta2-ieta1 == 0 && iphi2-iphi1 == -1) idx_neighboring = 3;
				if(idx_neighboring > -1){
					if(ieta2 >= -85 && ieta2<= 85 && iphi2>0 && iphi2<=360){
						h1_array_time_data[ieta1+85][iphi1-1][idx_neighboring]->Fill(t1-t2);
						int idx_neighboring_opposite = -999;
						if(idx_neighboring == 0) idx_neighboring_opposite = 2;
						if(idx_neighboring == 1) idx_neighboring_opposite = 3;
						if(idx_neighboring == 2) idx_neighboring_opposite = 0;
						if(idx_neighboring == 3) idx_neighboring_opposite = 1;
						h1_array_time_data[ieta2+85][iphi2-1][idx_neighboring_opposite]->Fill(t2-t1);
					}
				}
			}
		}
	}

	// do the fit to get the mean time in each ieta iphi bin
	for(int iEta = 0; iEta < 171; iEta++){
		for(int iPhi = 0; iPhi<360; iPhi++){
			for(int idx_neighb = 0; idx_neighb < 6; idx_neighb++){
				if(iPhi == 11 && iEta%9==0) h1_array_time_data[iEta][iPhi][idx_neighb]->Draw();
				//float * result_singGaus = singGausFit(h1_array_time_data[iEta][iPhi][idx_neighb]);
				float result_singGaus = singGausFit(h1_array_time_data[iEta][iPhi][idx_neighb]);
				if(iPhi == 11 && iEta%9==0) myC->SaveAs(outputDir+"/ZeeTiming/Timing_vs_iEta_iPhi_data_iEta"+std::to_string(iEta)+"_iPhi"+std::to_string(iPhi)+"_ineighb_"+std::to_string(idx_neighb)+".png");
				//dt_array_time_data[iEta][iPhi][idx_neighb] = result_singGaus[0];
				dt_array_time_data[iEta][iPhi][idx_neighb] = result_singGaus;
				//h2_time_iEta_vs_iPhi_data->SetBinContent(iEta+1, iPhi+1, result_singGaus[0]);		
			}
		}
	}
	for(int iPhi = 0; iPhi<360; iPhi++){
		for(int iEta = 0; iEta < 171; iEta++){
			float time_this = 0.0;
			if(iEta ==0 && iPhi == 0) time_this = 0.0;// first bin, make it zero
			if(iEta ==0 && iPhi>0){//first iEta bin, compare with the one iphi below
				float time_below = -1.0*h2_time_iEta_vs_iPhi_data->GetBinContent(iEta+1, iPhi);
				time_this = time_below + dt_array_time_data[iEta][iPhi][3];
			}
			else{//normal bin, compare with the one on the left
				float time_left = -1.0*h2_time_iEta_vs_iPhi_data->GetBinContent(iEta, iPhi+1);
				time_this = time_left + dt_array_time_data[iEta][iPhi][2];
			}

			h2_time_iEta_vs_iPhi_data->SetBinContent(iEta+1, iPhi+1, -1.0*time_this); // calibration is the opposite of the time 
			h2_timeAll_iEta_vs_iPhi_data->SetBinContent(iEta+1, iPhi+1, dt_array_time_data[iEta][iPhi][4]); 
			h2_timeTT_iEta_vs_iPhi_data->SetBinContent(iEta+1, iPhi+1, dt_array_time_data[iEta][iPhi][5]); 
			h2_dt0_iEta_vs_iPhi_data->SetBinContent(iEta+1, iPhi+1, dt_array_time_data[iEta][iPhi][0]); 
			h2_dt1_iEta_vs_iPhi_data->SetBinContent(iEta+1, iPhi+1, dt_array_time_data[iEta][iPhi][1]); 
			h2_dt2_iEta_vs_iPhi_data->SetBinContent(iEta+1, iPhi+1, dt_array_time_data[iEta][iPhi][2]); 
			h2_dt3_iEta_vs_iPhi_data->SetBinContent(iEta+1, iPhi+1, dt_array_time_data[iEta][iPhi][3]); 
		}
	}
	}

	//draw the map
	TFile * file_out;
	if(!drawOnly) file_out = new TFile ("IC_maps/IC_average_timing_2016.root","RECREATE");
	else {
		file_out = new TFile ("IC_maps/IC_average_timing_2016.root","READ");
		h2_time_iEta_vs_iPhi_data = (TH2F*)file_out->Get("h2_time_iEta_vs_iPhi_data");
		h2_timeAll_iEta_vs_iPhi_data = (TH2F*)file_out->Get("h2_timeAll_iEta_vs_iPhi_data");
		h2_timeTT_iEta_vs_iPhi_data = (TH2F*)file_out->Get("h2_timeTT_iEta_vs_iPhi_data");
		h2_dt0_iEta_vs_iPhi_data = (TH2F*)file_out->Get("h2_dt0_iEta_vs_iPhi_data");
		h2_dt1_iEta_vs_iPhi_data = (TH2F*)file_out->Get("h2_dt1_iEta_vs_iPhi_data");
		h2_dt2_iEta_vs_iPhi_data = (TH2F*)file_out->Get("h2_dt2_iEta_vs_iPhi_data");
		h2_dt3_iEta_vs_iPhi_data = (TH2F*)file_out->Get("h2_dt3_iEta_vs_iPhi_data");
	}

	drawTimingMap(h2_time_iEta_vs_iPhi_data, "data_dtIC", "time calibration / ns", -5.0, 2.0);		
	drawTimingMap(h2_timeAll_iEta_vs_iPhi_data, "data_dt4", "rechit time / ns", -0.1, 0.1);		
	drawTimingMap(h2_timeTT_iEta_vs_iPhi_data, "data_dt5", "rechit time / ns", -0.1, 0.1);		
	drawTimingMap(h2_dt0_iEta_vs_iPhi_data, "data_dt0", "#Delta T(iEta, iEtaa+1) / ns", -0.1, 0.1);		
	drawTimingMap(h2_dt1_iEta_vs_iPhi_data, "data_dt1", "#Delta T(iPhi, iPhi+1) / ns", -0.1, 0.1);		
	drawTimingMap(h2_dt2_iEta_vs_iPhi_data, "data_dt2", "#Delta T(iEta, iEta-1) / ns", -0.1, 0.1);		
	drawTimingMap(h2_dt3_iEta_vs_iPhi_data, "data_dt3", "#Delta T(iPhi, iPhi-1) / ns", -0.1, 0.1);

	if(!drawOnly) h2_time_iEta_vs_iPhi_data->Write();
	if(!drawOnly) h2_timeAll_iEta_vs_iPhi_data->Write();
	if(!drawOnly) h2_timeTT_iEta_vs_iPhi_data->Write();
	if(!drawOnly) h2_dt0_iEta_vs_iPhi_data->Write();
	if(!drawOnly) h2_dt1_iEta_vs_iPhi_data->Write();
	if(!drawOnly) h2_dt2_iEta_vs_iPhi_data->Write();
	if(!drawOnly) h2_dt3_iEta_vs_iPhi_data->Write();

	file_out->Close();

}
