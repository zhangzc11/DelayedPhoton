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
float leftMargin   = 0.15;
float rightMargin  = 0.05;
float topMargin    = 0.09;
float bottomMargin = 0.12;

TString outputDir="/data/zhicaiz/www/sharebox/DelayedPhoton/ARCReview_June2019/orderByPt/";

//mkdir(outputDir, S_IRWXU | S_IRWXG | S_IRWXO);
//mkdir(outputDir+"/ZeeTiming/", S_IRWXU | S_IRWXG | S_IRWXO);

float * singGausFit(TH1F *hist){
	if(hist->Integral() < 100.0){
		float result[4] = {0};
		float * pointer = new float[4];
		for(int i=0; i<4; i++) pointer[i] = result[i];
		return pointer;
	}

	float x_mean=hist->GetMean();
	float x_stddev=hist->GetStdDev();
	float x_min=x_mean - 2.0*x_stddev;
	float x_max=x_mean + 2.0*x_stddev;
	float sig = x_stddev;
	TF1 * tf1_singGaus = new TF1("tf1_singGaus","gaus(0)", x_min,x_max);
	tf1_singGaus->SetParameters(hist->Integral(),0.5*(x_min+x_max),sig);
	hist->Fit("tf1_singGaus","B","",x_min,x_max);
	float meanEff = tf1_singGaus->GetParameter(1);
	float emeanEff = tf1_singGaus->GetParError(1);
	float sigEff = abs(tf1_singGaus->GetParameter(2));
	float esigEff = tf1_singGaus->GetParError(2);

	float result[4] = {meanEff,emeanEff,sigEff,esigEff};

	float * pointer = new float[4];
	for(int i=0; i<4; i++) pointer[i] = result[i];
	delete tf1_singGaus;
	return pointer;
}


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

void DrawCMSstyle(TCanvas *myC, int energy, float lumi, TString title)
{
        myC->cd();
  auto cms_pave = new TPaveText(0.20,0.855,0.3,0.895,"NDC");
  cms_pave->SetFillColorAlpha(0,0);
  cms_pave->SetTextFont(61);
  cms_pave->AddText("CMS");
  cms_pave->Draw("same");

  auto prelim_pave = new TPaveText(0.25,0.855,0.45,0.89,"NDC");
  prelim_pave->SetFillColorAlpha(0,0);
  prelim_pave->SetTextFont(52);
  prelim_pave->AddText("Preliminary");
  prelim_pave->Draw("same");

  auto lumi_pave = new TPaveText(0.218,0.80,0.478,0.86,"NDC");
  lumi_pave->SetFillColorAlpha(0,0);
  lumi_pave->SetTextFont(42);
  lumi_pave->AddText("2016: 35.9 fb^{-1} (13 TeV)");
  lumi_pave->Draw("same");
 
  auto label_pave = new TPaveText(0.6,0.855,0.8,0.895,"NDC");
  label_pave->SetFillColorAlpha(0,0);
  label_pave->SetTextFont(42);
  label_pave->AddText(title);
  label_pave->Draw("same");

};

void drawTimeResoVsAeff(TTree * tree_data, TTree * tree_MC, TString label, TString title){
	cout<<"draw time resolution vs Aeff plots for "<<label<<endl;
	cout<<"data sampel size  = "<<tree_data->GetEntries()<<endl;	
	cout<<"MC sampel size  = "<<tree_MC->GetEntries()<<endl;	

	gStyle->SetOptFit(1);
	gStyle->SetOptStat(0);
	gStyle->SetOptTitle(0);

	TCanvas * myC = new TCanvas( "myC", "myC", 0, 0, 700, 600 );

	myC->Range(1.478223,-1.31174,3.682881,0.1140644);
	myC->SetFillColor(0);
	myC->SetBorderMode(0);
	myC->SetBorderSize(2);
	myC->SetLogy(1);
	myC->SetGridx();
	myC->SetGridy();
	myC->SetLeftMargin(0.18);
	myC->SetRightMargin(0.15);
	myC->SetTopMargin(0.08);
	myC->SetFrameFillStyle(0);
	myC->SetFrameBorderMode(0);
	myC->SetFrameFillStyle(0);
	myC->SetFrameBorderMode(0);

	const int N_Eeff_points = 12;	
	float Eeff_divide[13] = {75.0, 100.0, 125.0, 150.0, 175.0, 225.0, 275.0, 325.0, 375.0, 475.0, 600.0, 750.0, 1700.0};
	
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
	
	float min_aeff = 0.0;
	float max_aeff = 0.0;

	for(int i=0; i< N_Eeff_points; i++){
		x_Eeff[i] = 0.5*(Eeff_divide[i+1]+Eeff_divide[i]);
		ex_Eeff[i] = 0.5*(Eeff_divide[i+1]-Eeff_divide[i]);
		float Eeff_low_this = Eeff_divide[i];
		float Eeff_high_this = Eeff_divide[i+1];
		TString cut_2e_this = ("E2>1.0 && (E1/pedestal1)*(E2/pedestal2)/sqrt((E1/pedestal1)*(E1/pedestal1)+(E2/pedestal2)*(E2/pedestal2)) > "+std::to_string(Eeff_low_this)+" && (E1/pedestal1)*(E2/pedestal2)/sqrt((E1/pedestal1)*(E1/pedestal1)+(E2/pedestal2)*(E2/pedestal2)) < "+std::to_string(Eeff_high_this)).c_str();
		TString cut_2e_this_MC = ("E2>1.0 && (E1/(1.47*pedestal1))*(E2/(1.47*pedestal2))/sqrt((E1/(1.47*pedestal1))*(E1/(1.47*pedestal1))+(E2/(1.47*pedestal2))*(E2/(1.47*pedestal2))) > "+std::to_string(Eeff_low_this)+" && (E1/(1.47*pedestal1))*(E2/(1.47*pedestal2))/sqrt((E1/(1.47*pedestal1))*(E1/(1.47*pedestal1))+(E2/(1.47*pedestal2))*(E2/(1.47*pedestal2))) < "+std::to_string(Eeff_high_this)).c_str();
;
		TH1F * hist_2e_this_data = new TH1F(("hist_2e_this_data_"+std::to_string(i)).c_str(),("hist_2e_this_data_"+std::to_string(i)).c_str(), 60, -1.5, 1.5);
		tree_data->Draw(("t1-t2>>hist_2e_this_data_"+std::to_string(i)).c_str(), cut_2e_this);
		hist_2e_this_data->Draw();
		float * result_2e_this_data = singGausFit(hist_2e_this_data);
		myC->SaveAs(outputDir+"/ZeeTiming/style_plots/fits/iEeffFit_xtal_"+std::to_string(i)+"_dt_data_CLK_"+label+".png");		

		TH1F * hist_2e_this_MC = new TH1F(("hist_2e_this_MC_"+std::to_string(i)).c_str(),("hist_2e_this_MC_"+std::to_string(i)).c_str(), 60, -1.5, 1.5);
		tree_MC->Draw(("t1-t2>>hist_2e_this_MC_"+std::to_string(i)).c_str(), cut_2e_this_MC);
		hist_2e_this_MC->Draw();
		float * result_2e_this_MC = singGausFit(hist_2e_this_MC);
		myC->SaveAs(outputDir+"/ZeeTiming/style_plots/fits/iEeffFit_xtal_"+std::to_string(i)+"_dt_MC_CLK_"+label+".png");		

		y_Eeff_sigma_dt_data[i] = (result_2e_this_data[2]);
		ey_Eeff_sigma_dt_data[i] = (result_2e_this_data[3]);
		y_Eeff_sigma_dt_MC[i] = (result_2e_this_MC[2]);
		ey_Eeff_sigma_dt_MC[i] = (result_2e_this_MC[3]);
		delete result_2e_this_data;
		delete result_2e_this_MC;
		delete hist_2e_this_data;
		delete hist_2e_this_MC;
		cout<<"===bin "<<i<<"  "<<y_Eeff_sigma_dt_data[i]<<"   "<<ey_Eeff_sigma_dt_data[i]<<"   "<<y_Eeff_sigma_dt_MC[i]<<"   "<<ey_Eeff_sigma_dt_MC[i]<<endl;
		if(y_Eeff_sigma_dt_data[i]>0.05 && y_Eeff_sigma_dt_data[i]<0.5 && y_Eeff_sigma_dt_MC[i]>0.05 && y_Eeff_sigma_dt_MC[i] < 0.5) max_aeff = Eeff_divide[i+1];
	}
	for(int i=N_Eeff_points-1; i>=0; i--){
		if(y_Eeff_sigma_dt_data[i]>0.05 && y_Eeff_sigma_dt_data[i]<0.5 && y_Eeff_sigma_dt_MC[i]>0.05 && y_Eeff_sigma_dt_MC[i] < 0.5) min_aeff = Eeff_divide[i];
	}

	
	gStyle->SetOptFit(0);
	myC->SetGridy(1);
	myC->SetGridx(1);
	myC->SetLogx(1);
	myC->SetLogy(1);

	TGraphErrors *gr_Eeff_sigma_dt_data  =  new TGraphErrors(N_Eeff_points, x_Eeff, y_Eeff_sigma_dt_data, ex_Eeff, ey_Eeff_sigma_dt_data);
	gr_Eeff_sigma_dt_data->Draw("AEPZ");
	gr_Eeff_sigma_dt_data->SetMarkerColor(kRed);
	gr_Eeff_sigma_dt_data->SetLineColor(kRed);
	gr_Eeff_sigma_dt_data->SetLineWidth(1);
	gr_Eeff_sigma_dt_data->SetMarkerStyle(20);
	gr_Eeff_sigma_dt_data->SetMarkerSize(0.6);
	gr_Eeff_sigma_dt_data->SetTitle("");
	gr_Eeff_sigma_dt_data->GetXaxis()->SetTitle("A_{eff}/#sigma_{n}");
	gr_Eeff_sigma_dt_data->GetXaxis()->SetNdivisions(505);
	gr_Eeff_sigma_dt_data->GetXaxis()->SetTitleSize( 0.035 );
	gr_Eeff_sigma_dt_data->GetXaxis()->SetTitleOffset( 1.0 );
	gr_Eeff_sigma_dt_data->GetXaxis()->SetTitleFont( 42 );
	gr_Eeff_sigma_dt_data->GetXaxis()->SetLabelFont( 42 );
	gr_Eeff_sigma_dt_data->GetXaxis()->SetLabelOffset( 0.007 );
	gr_Eeff_sigma_dt_data->GetYaxis()->SetTitle("#sigma(#Deltat) (ns)");
	gr_Eeff_sigma_dt_data->GetYaxis()->SetTitleSize( 0.035 );
	gr_Eeff_sigma_dt_data->GetYaxis()->SetTitleOffset( 1.0 );
	gr_Eeff_sigma_dt_data->GetYaxis()->SetLabelFont( 42 );
	gr_Eeff_sigma_dt_data->GetYaxis()->SetTitleFont( 42 );
	gr_Eeff_sigma_dt_data->GetYaxis()->SetLabelOffset( 0.007 );
	gr_Eeff_sigma_dt_data->GetYaxis()->SetRangeUser(0.07,1.00);
	gr_Eeff_sigma_dt_data->GetXaxis()->SetLimits(75.,2250.);
	//gr_Eeff_sigma_dt_data->GetXaxis()->SetMoreLogLabels();
	//gr_Eeff_sigma_dt_data->GetYaxis()->SetMoreLogLabels();

	TF1 * tf1_dt_vs_Eeff_data = new TF1("tf1_dt_vs_Eeff_data","sqrt([0]/(x*x)+[1])",75, 2250);
	tf1_dt_vs_Eeff_data->SetLineColor(kBlack);
	tf1_dt_vs_Eeff_data->SetParameters(25.0*25.0, 0.1*0.1);
	gr_Eeff_sigma_dt_data->Fit("tf1_dt_vs_Eeff_data","","",min_aeff, max_aeff);
	tf1_dt_vs_Eeff_data->Draw("same");
	float fit_dt_a_data = tf1_dt_vs_Eeff_data->GetParameter(0);
	float efit_dt_a_data = tf1_dt_vs_Eeff_data->GetParError(0);
	float fit_dt_b_data = tf1_dt_vs_Eeff_data->GetParameter(1);
	float efit_dt_b_data = tf1_dt_vs_Eeff_data->GetParError(1);

	TGraphErrors * gr_Eeff_sigma_dt_MC  =  new TGraphErrors(N_Eeff_points, x_Eeff, y_Eeff_sigma_dt_MC, ex_Eeff, ey_Eeff_sigma_dt_MC);
	gr_Eeff_sigma_dt_MC->SetMarkerColor(kBlue);
	gr_Eeff_sigma_dt_MC->SetLineColor(kBlue);
	gr_Eeff_sigma_dt_MC->SetMarkerStyle(21);
	gr_Eeff_sigma_dt_MC->SetMarkerSize(0.6);
	gr_Eeff_sigma_dt_MC->SetLineWidth(1);
	gr_Eeff_sigma_dt_MC->Draw("EPZsame");

	TF1 * tf1_dt_vs_Eeff_MC = new TF1("tf1_dt_vs_Eeff_MC","sqrt([0]/(x*x)+[1])", 75, 2250);
	tf1_dt_vs_Eeff_MC->SetLineColor(kBlack);
	tf1_dt_vs_Eeff_MC->SetParameters(40.0*40.0, 0.1*0.1);
	gr_Eeff_sigma_dt_MC->Fit("tf1_dt_vs_Eeff_MC","","",min_aeff, max_aeff);
	tf1_dt_vs_Eeff_MC->Draw("same");
	float fit_dt_a_MC = tf1_dt_vs_Eeff_MC->GetParameter(0);
	float efit_dt_a_MC = tf1_dt_vs_Eeff_MC->GetParError(0);
	float fit_dt_b_MC = tf1_dt_vs_Eeff_MC->GetParameter(1);
	float efit_dt_b_MC = tf1_dt_vs_Eeff_MC->GetParError(1);

	auto leg = new TLegend(0.215,0.715,0.415,0.80);
  	leg->SetFillColorAlpha(0,0);
	leg->SetBorderSize(0);
        leg->SetLineColor(1);
        leg->SetLineStyle(1);
        leg->SetFillStyle(1001);
	leg->SetTextFont(42);
  	leg->AddEntry(gr_Eeff_sigma_dt_data,"Data","epl");
  	leg->AddEntry(gr_Eeff_sigma_dt_MC,"Simulation","epl");

	leg->Draw("same");

	float N_data=sqrt(abs(fit_dt_a_data));
	float eN_data=abs(efit_dt_a_data)/(2.0*sqrt(abs(fit_dt_a_data)));
	float C_data=sqrt(abs(fit_dt_b_data)/2.0);
	float eC_data=abs(efit_dt_b_data)/(4.0*sqrt(abs(fit_dt_b_data)/2.0));

	float N_MC=sqrt(abs(fit_dt_a_MC));
	float eN_MC=abs(efit_dt_a_MC)/(2.0*sqrt(abs(fit_dt_a_MC)));
	float C_MC=sqrt(abs(fit_dt_b_MC)/2.0);
	float eC_MC=abs(efit_dt_b_MC)/(4.0*sqrt(abs(fit_dt_b_MC)/2.0));

	auto form_pave = new TPaveText(0.55,0.73,0.8,0.85,"NDC");
	form_pave->SetFillColorAlpha(0,0);
	form_pave->SetTextFont(42);
	form_pave->SetTextAlign(11);
	form_pave->AddText("#sigma(#Deltat)=#frac{N}{A_{eff}/#sigma_{n}} #oplus #sqrt{2}C");
	form_pave->Draw("same");

	auto fit_pave = new TPaveText(0.55,0.565,0.8,0.735,"NDC");
	fit_pave->SetFillColorAlpha(0,0);
	fit_pave->SetTextAlign(11);
	fit_pave->SetTextFont(42);
	fit_pave->AddText(Form("N^{Data} = %.1f #pm %.1f ns", N_data, eN_data));
	fit_pave->AddText(Form("C^{Data} = %.3f #pm %.3f ns", C_data, eC_data));
	fit_pave->AddText(Form("N^{Sim} = %.1f #pm %.1f ns", N_MC, eN_MC));
	fit_pave->AddText(Form("C^{Sim} = %.3f #pm %.3f ns", C_MC, eC_MC));
	fit_pave->Draw("same");


	TGaxis *gaxis = new TGaxis(75,1,2250,1,75*0.0618, 2250*0.0618,505,"-G");
	gaxis->SetLabelOffset(0.005);
	gaxis->SetLabelSize(0.035);
	gaxis->SetTickSize(0.03);
	gaxis->SetGridLength(0);
	gaxis->SetTitleOffset(1);
	gaxis->SetTitleSize(0.035);
	gaxis->SetTitleColor(1);
	gaxis->SetTitleFont(42);
	gaxis->SetLabelFont(42);
	gaxis->SetTitle("E (GeV)");
	gaxis->SetNoExponent(1);
	gaxis->Draw("same");
	myC->Modified();
	myC->cd();

	DrawCMSstyle(myC, 13, 35922.0, title);

	myC->SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_xtals_dt_vs_Eeff_sigma_Data_vs_MC_"+label+".pdf");
	myC->SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_xtals_dt_vs_Eeff_sigma_Data_vs_MC_"+label+".png");
	myC->SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_xtals_dt_vs_Eeff_sigma_Data_vs_MC_"+label+".C");

	//TFile *file_plot = new TFile((outputDir+"/ZeeTiming/TimingReso_xtals_dt_vs_Eeff_sigma_Data_vs_MC_"+label+".root"), "RECREATE");
	//gr_Eeff_sigma_dt_data->Write("gr_data");
	//gr_Eeff_sigma_dt_MC->Write("gr_mc");
	//file_plot->Close();

	//data onlu
	delete fit_pave;
	delete tf1_dt_vs_Eeff_MC;
	delete leg;
	
	gr_Eeff_sigma_dt_data->Draw("AEPZ");
	tf1_dt_vs_Eeff_data->Draw("same");

	gr_Eeff_sigma_dt_data->SetMarkerColor(kBlack);
        gr_Eeff_sigma_dt_data->SetLineColor(kBlack);
	tf1_dt_vs_Eeff_data->SetLineColor(kRed+1);
	DrawCMSstyle(myC, 13, 35922.0, title);
	gaxis->Draw("same");
	form_pave->Draw("same");
	
	auto fit_pave2 = new TPaveText(0.55,0.650,0.8,0.735,"NDC");
	fit_pave2->SetFillColorAlpha(0,0);
	fit_pave2->SetTextAlign(11);
	fit_pave2->SetTextFont(42);
	fit_pave2->AddText(Form("N = %.1f #pm %.1f ns", N_data, eN_data));
	fit_pave2->AddText(Form("C = %.3f #pm %.3f ns", C_data, eC_data));
	fit_pave2->Draw("same");

	myC->SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_xtals_dt_vs_Eeff_sigma_DataOnly_"+label+".pdf");
	myC->SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_xtals_dt_vs_Eeff_sigma_DataOnly_"+label+".png");
	myC->SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_xtals_dt_vs_Eeff_sigma_DataOnly_"+label+".C");
	
	
	delete myC;
	delete gr_Eeff_sigma_dt_data;
	delete tf1_dt_vs_Eeff_data;

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

void TimingCorr_crystal_rings_vs_Eeff()
{

	TString cut = "ele1IsEB && ele1seedE<120.0";

	TFile * file_data = new TFile("/data/zhicaiz/data/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/All2016.root","READ");
	TTree * tree_data = (TTree*)file_data->Get("ZeeTiming");
	tree_data->SetCacheSize(12000000000);//12GB

	TFile * file_MC = new TFile("/data/zhicaiz/data/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/MC2016_all.root","READ");
	TTree * tree_MC = (TTree*)file_MC->Get("ZeeTiming");
	tree_MC->SetCacheSize(3000000000);//3GB

	TFile * file_out;
	if(!drawOnly) file_out = new TFile("temp_TimingCorr_crystal_rings_vs_Eeff.root","RECREATE");
	else file_out = new TFile("temp_TimingCorr_crystal_rings_vs_Eeff.root","READ");
	file_out->cd();
	//TTree * tree_data_skim = tree_data->CopyTree(cut);
	//TTree * tree_MC_skim = tree_MC->CopyTree(cut);

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
	
	//define output variables	
	float E1_neighboring=0, E2_neighboring=0;
	int iEta1_neighboring=0, iEta2_neighboring=0;
	int iPhi1_neighboring=0, iPhi2_neighboring=0;
	float t1_neighboring=0, t2_neighboring=0;
	float pedestal1_neighboring=0.042, pedestal2_neighboring=0.042;
	TTree * tree_out_neighboring_data;
	TTree * tree_out_neighboring_MC;

	float E1_ring1=0, E2_ring1=0;
	int iEta1_ring1=0, iEta2_ring1=0;
	int iPhi1_ring1=0, iPhi2_ring1=0;
	float t1_ring1=0, t2_ring1=0;
	float pedestal1_ring1=0.042, pedestal2_ring1=0.042;
	TTree * tree_out_ring1_data;
	TTree * tree_out_ring1_MC;

	float E1_ring2=0, E2_ring2=0;
	int iEta1_ring2=0, iEta2_ring2=0;
	int iPhi1_ring2=0, iPhi2_ring2=0;
	float t1_ring2=0, t2_ring2=0;
	float pedestal1_ring2=0.042, pedestal2_ring2=0.042;
	TTree * tree_out_ring2_data;
	TTree * tree_out_ring2_MC;

	float E1_sameTrigTower=0, E2_sameTrigTower=0;
	int iEta1_sameTrigTower=0, iEta2_sameTrigTower=0;
	int iPhi1_sameTrigTower=0, iPhi2_sameTrigTower=0;
	float t1_sameTrigTower=0, t2_sameTrigTower=0;
	float pedestal1_sameTrigTower=0.042, pedestal2_sameTrigTower=0.042;
	TTree * tree_out_sameTrigTower_data;
	TTree * tree_out_sameTrigTower_MC;

	float E1_diffTrigTower=0, E2_diffTrigTower=0;
	int iEta1_diffTrigTower=0, iEta2_diffTrigTower=0;
	int iPhi1_diffTrigTower=0, iPhi2_diffTrigTower=0;
	float t1_diffTrigTower=0, t2_diffTrigTower=0;
	float pedestal1_diffTrigTower=0.042, pedestal2_diffTrigTower=0.042;
	TTree * tree_out_diffTrigTower_data;
	TTree * tree_out_diffTrigTower_MC;


	float E1_sameTrigTowerNeighbor=0, E2_sameTrigTowerNeighbor=0;
	int iEta1_sameTrigTowerNeighbor=0, iEta2_sameTrigTowerNeighbor=0;
	int iPhi1_sameTrigTowerNeighbor=0, iPhi2_sameTrigTowerNeighbor=0;
	float t1_sameTrigTowerNeighbor=0, t2_sameTrigTowerNeighbor=0;
	float pedestal1_sameTrigTowerNeighbor=0.042, pedestal2_sameTrigTowerNeighbor=0.042;
	TTree * tree_out_sameTrigTowerNeighbor_data;
	TTree * tree_out_sameTrigTowerNeighbor_MC;

	float E1_diffTrigTowerNeighbor=0, E2_diffTrigTowerNeighbor=0;
	int iEta1_diffTrigTowerNeighbor=0, iEta2_diffTrigTowerNeighbor=0;
	int iPhi1_diffTrigTowerNeighbor=0, iPhi2_diffTrigTowerNeighbor=0;
	float t1_diffTrigTowerNeighbor=0, t2_diffTrigTowerNeighbor=0;
	float pedestal1_diffTrigTowerNeighbor=0.042, pedestal2_diffTrigTowerNeighbor=0.042;
	TTree * tree_out_diffTrigTowerNeighbor_data;
	TTree * tree_out_diffTrigTowerNeighbor_MC;


	if(!drawOnly){

		tree_out_neighboring_data = new TTree("ZeeTiming_neighboring_data","second crystal from neighboring crystals");
		tree_out_neighboring_data->Branch("E1", &E1_neighboring, "E1/F");	
		tree_out_neighboring_data->Branch("E2", &E2_neighboring, "E2/F");	
		tree_out_neighboring_data->Branch("t1", &t1_neighboring, "t1/F");	
		tree_out_neighboring_data->Branch("t2", &t2_neighboring, "t2/F");	
		tree_out_neighboring_data->Branch("pedestal1", &pedestal1_neighboring, "pedestal1/F");	
		tree_out_neighboring_data->Branch("pedestal2", &pedestal2_neighboring, "pedestal2/F");	
		tree_out_neighboring_data->Branch("iEta1", &iEta1_neighboring, "iEta1/I");	
		tree_out_neighboring_data->Branch("iEta2", &iEta2_neighboring, "iEta2/I");	
		tree_out_neighboring_data->Branch("iPhi1", &iPhi1_neighboring, "iPhi1/I");	
		tree_out_neighboring_data->Branch("iPhi2", &iPhi2_neighboring, "iPhi2/I");	

		tree_out_ring1_data = new TTree("ZeeTiming_ring1_data","second crystal from ring1 crystals");
		tree_out_ring1_data->Branch("E1", &E1_ring1, "E1/F");	
		tree_out_ring1_data->Branch("E2", &E2_ring1, "E2/F");	
		tree_out_ring1_data->Branch("t1", &t1_ring1, "t1/F");	
		tree_out_ring1_data->Branch("t2", &t2_ring1, "t2/F");	
		tree_out_ring1_data->Branch("pedestal1", &pedestal1_ring1, "pedestal1/F");	
		tree_out_ring1_data->Branch("pedestal2", &pedestal2_ring1, "pedestal2/F");	
		tree_out_ring1_data->Branch("iEta1", &iEta1_ring1, "iEta1/I");	
		tree_out_ring1_data->Branch("iEta2", &iEta2_ring1, "iEta2/I");	
		tree_out_ring1_data->Branch("iPhi1", &iPhi1_ring1, "iPhi1/I");	
		tree_out_ring1_data->Branch("iPhi2", &iPhi2_ring1, "iPhi2/I");	



		tree_out_ring2_data = new TTree("ZeeTiming_ring2_data","second crystal from ring2 crystals");
		tree_out_ring2_data->Branch("E1", &E1_ring2, "E1/F");	
		tree_out_ring2_data->Branch("E2", &E2_ring2, "E2/F");	
		tree_out_ring2_data->Branch("t1", &t1_ring2, "t1/F");	
		tree_out_ring2_data->Branch("t2", &t2_ring2, "t2/F");	
		tree_out_ring2_data->Branch("pedestal1", &pedestal1_ring2, "pedestal1/F");	
		tree_out_ring2_data->Branch("pedestal2", &pedestal2_ring2, "pedestal2/F");	
		tree_out_ring2_data->Branch("iEta1", &iEta1_ring2, "iEta1/I");	
		tree_out_ring2_data->Branch("iEta2", &iEta2_ring2, "iEta2/I");	
		tree_out_ring2_data->Branch("iPhi1", &iPhi1_ring2, "iPhi1/I");	
		tree_out_ring2_data->Branch("iPhi2", &iPhi2_ring2, "iPhi2/I");	



		tree_out_sameTrigTower_data = new TTree("ZeeTiming_sameTrigTower_data","second crystal from sameTrigTower crystals");
		tree_out_sameTrigTower_data->Branch("E1", &E1_sameTrigTower, "E1/F");	
		tree_out_sameTrigTower_data->Branch("E2", &E2_sameTrigTower, "E2/F");	
		tree_out_sameTrigTower_data->Branch("t1", &t1_sameTrigTower, "t1/F");	
		tree_out_sameTrigTower_data->Branch("t2", &t2_sameTrigTower, "t2/F");	
		tree_out_sameTrigTower_data->Branch("pedestal1", &pedestal1_sameTrigTower, "pedestal1/F");	
		tree_out_sameTrigTower_data->Branch("pedestal2", &pedestal2_sameTrigTower, "pedestal2/F");	
		tree_out_sameTrigTower_data->Branch("iEta1", &iEta1_sameTrigTower, "iEta1/I");	
		tree_out_sameTrigTower_data->Branch("iEta2", &iEta2_sameTrigTower, "iEta2/I");	
		tree_out_sameTrigTower_data->Branch("iPhi1", &iPhi1_sameTrigTower, "iPhi1/I");	
		tree_out_sameTrigTower_data->Branch("iPhi2", &iPhi2_sameTrigTower, "iPhi2/I");	


		tree_out_diffTrigTower_data = new TTree("ZeeTiming_diffTrigTower_data","second crystal from diffTrigTower crystals");
		tree_out_diffTrigTower_data->Branch("E1", &E1_diffTrigTower, "E1/F");	
		tree_out_diffTrigTower_data->Branch("E2", &E2_diffTrigTower, "E2/F");	
		tree_out_diffTrigTower_data->Branch("t1", &t1_diffTrigTower, "t1/F");	
		tree_out_diffTrigTower_data->Branch("t2", &t2_diffTrigTower, "t2/F");	
		tree_out_diffTrigTower_data->Branch("pedestal1", &pedestal1_diffTrigTower, "pedestal1/F");	
		tree_out_diffTrigTower_data->Branch("pedestal2", &pedestal2_diffTrigTower, "pedestal2/F");	
		tree_out_diffTrigTower_data->Branch("iEta1", &iEta1_diffTrigTower, "iEta1/I");	
		tree_out_diffTrigTower_data->Branch("iEta2", &iEta2_diffTrigTower, "iEta2/I");	
		tree_out_diffTrigTower_data->Branch("iPhi1", &iPhi1_diffTrigTower, "iPhi1/I");	
		tree_out_diffTrigTower_data->Branch("iPhi2", &iPhi2_diffTrigTower, "iPhi2/I");	


		tree_out_sameTrigTowerNeighbor_data = new TTree("ZeeTiming_sameTrigTowerNeighbor_data","second crystal from sameTrigTowerNeighbor crystals");
		tree_out_sameTrigTowerNeighbor_data->Branch("E1", &E1_sameTrigTowerNeighbor, "E1/F");	
		tree_out_sameTrigTowerNeighbor_data->Branch("E2", &E2_sameTrigTowerNeighbor, "E2/F");	
		tree_out_sameTrigTowerNeighbor_data->Branch("t1", &t1_sameTrigTowerNeighbor, "t1/F");	
		tree_out_sameTrigTowerNeighbor_data->Branch("t2", &t2_sameTrigTowerNeighbor, "t2/F");	
		tree_out_sameTrigTowerNeighbor_data->Branch("pedestal1", &pedestal1_sameTrigTowerNeighbor, "pedestal1/F");	
		tree_out_sameTrigTowerNeighbor_data->Branch("pedestal2", &pedestal2_sameTrigTowerNeighbor, "pedestal2/F");	
		tree_out_sameTrigTowerNeighbor_data->Branch("iEta1", &iEta1_sameTrigTowerNeighbor, "iEta1/I");	
		tree_out_sameTrigTowerNeighbor_data->Branch("iEta2", &iEta2_sameTrigTowerNeighbor, "iEta2/I");	
		tree_out_sameTrigTowerNeighbor_data->Branch("iPhi1", &iPhi1_sameTrigTowerNeighbor, "iPhi1/I");	
		tree_out_sameTrigTowerNeighbor_data->Branch("iPhi2", &iPhi2_sameTrigTowerNeighbor, "iPhi2/I");	


		tree_out_diffTrigTowerNeighbor_data = new TTree("ZeeTiming_diffTrigTowerNeighbor_data","second crystal from diffTrigTowerNeighbor crystals");
		tree_out_diffTrigTowerNeighbor_data->Branch("E1", &E1_diffTrigTowerNeighbor, "E1/F");	
		tree_out_diffTrigTowerNeighbor_data->Branch("E2", &E2_diffTrigTowerNeighbor, "E2/F");	
		tree_out_diffTrigTowerNeighbor_data->Branch("t1", &t1_diffTrigTowerNeighbor, "t1/F");	
		tree_out_diffTrigTowerNeighbor_data->Branch("t2", &t2_diffTrigTowerNeighbor, "t2/F");	
		tree_out_diffTrigTowerNeighbor_data->Branch("pedestal1", &pedestal1_diffTrigTowerNeighbor, "pedestal1/F");	
		tree_out_diffTrigTowerNeighbor_data->Branch("pedestal2", &pedestal2_diffTrigTowerNeighbor, "pedestal2/F");	
		tree_out_diffTrigTowerNeighbor_data->Branch("iEta1", &iEta1_diffTrigTowerNeighbor, "iEta1/I");	
		tree_out_diffTrigTowerNeighbor_data->Branch("iEta2", &iEta2_diffTrigTowerNeighbor, "iEta2/I");	
		tree_out_diffTrigTowerNeighbor_data->Branch("iPhi1", &iPhi1_diffTrigTowerNeighbor, "iPhi1/I");	
		tree_out_diffTrigTowerNeighbor_data->Branch("iPhi2", &iPhi2_diffTrigTowerNeighbor, "iPhi2/I");	



		for(int ientry=0;ientry<N_entries_data; ientry++){
			if(ientry%100000 ==0) cout<<"reading original tree entry "<<ientry<<"  out of "<<N_entries_data<<endl;
			tree_data->GetEntry(ientry);
			
			float maxE_neighboring = -999.0;
			bool pass_neighboring_all = false;
			bool pass_ring1_all = false;
			float maxE_ring1 = -999.0;
			bool pass_ring2_all = false;
			float maxE_ring2 = -999.0;
			bool pass_sameTrigTower_all = false;
			float maxE_sameTrigTower = -999.0;
			bool pass_diffTrigTower_all = false;
			float maxE_diffTrigTower = -999.0;
	
			bool pass_sameTrigTowerNeighbor_all = false;
			float maxE_sameTrigTowerNeighbor = -999.0;
			bool pass_diffTrigTowerNeighbor_all = false;
			float maxE_diffTrigTowerNeighbor = -999.0;
			
			if(ele1IsEB && ele1seedE < 120){
				for(int i=0;i<ele1Rechit_IEtaIX->size(); i++){
					if(ele1seedIEta == ele1Rechit_IEtaIX->at(i) && ele1seedIPhi == ele1Rechit_IPhiIY->at(i)){
						E1_neighboring=ele1Rechit_E->at(i);
						pedestal1_neighboring=ele1Rechit_pedestal->at(i);
						t1_neighboring=ele1Rechit_t->at(i);
						iEta1_neighboring=ele1Rechit_IEtaIX->at(i);
						iPhi1_neighboring=ele1Rechit_IPhiIY->at(i);
						E1_ring1=ele1Rechit_E->at(i);
						pedestal1_ring1=ele1Rechit_pedestal->at(i);
						t1_ring1=ele1Rechit_t->at(i);
						iEta1_ring1=ele1Rechit_IEtaIX->at(i);
						iPhi1_ring1=ele1Rechit_IPhiIY->at(i);

						E1_ring2=ele1Rechit_E->at(i);
						pedestal1_ring2=ele1Rechit_pedestal->at(i);
						t1_ring2=ele1Rechit_t->at(i);
						iEta1_ring2=ele1Rechit_IEtaIX->at(i);
						iPhi1_ring2=ele1Rechit_IPhiIY->at(i);

						E1_sameTrigTower=ele1Rechit_E->at(i);
						pedestal1_sameTrigTower=ele1Rechit_pedestal->at(i);
						t1_sameTrigTower=ele1Rechit_t->at(i);
						iEta1_sameTrigTower=ele1Rechit_IEtaIX->at(i);
						iPhi1_sameTrigTower=ele1Rechit_IPhiIY->at(i);

						E1_diffTrigTower=ele1Rechit_E->at(i);
						pedestal1_diffTrigTower=ele1Rechit_pedestal->at(i);
						t1_diffTrigTower=ele1Rechit_t->at(i);
						iEta1_diffTrigTower=ele1Rechit_IEtaIX->at(i);
						iPhi1_diffTrigTower=ele1Rechit_IPhiIY->at(i);
						E1_sameTrigTowerNeighbor=ele1Rechit_E->at(i);
						pedestal1_sameTrigTowerNeighbor=ele1Rechit_pedestal->at(i);
						t1_sameTrigTowerNeighbor=ele1Rechit_t->at(i);
						iEta1_sameTrigTowerNeighbor=ele1Rechit_IEtaIX->at(i);
						iPhi1_sameTrigTowerNeighbor=ele1Rechit_IPhiIY->at(i);

						E1_diffTrigTowerNeighbor=ele1Rechit_E->at(i);
						pedestal1_diffTrigTowerNeighbor=ele1Rechit_pedestal->at(i);
						t1_diffTrigTowerNeighbor=ele1Rechit_t->at(i);
						iEta1_diffTrigTowerNeighbor=ele1Rechit_IEtaIX->at(i);
						iPhi1_diffTrigTowerNeighbor=ele1Rechit_IPhiIY->at(i);


					}

					if(ele1Rechit_E->at(i) < 1.0) continue;
					//neighboring
					bool pass_neighboring = isNeighboringXtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
					if(pass_neighboring && ele1Rechit_E->at(i) > maxE_neighboring){
						pass_neighboring_all = true;
						E2_neighboring=ele1Rechit_E->at(i);
						pedestal2_neighboring=ele1Rechit_pedestal->at(i);
						t2_neighboring=ele1Rechit_t->at(i);
						iEta2_neighboring=ele1Rechit_IEtaIX->at(i);
						iPhi2_neighboring=ele1Rechit_IPhiIY->at(i);
						maxE_neighboring = E2_neighboring;
					}
		
					//ring1
					bool pass_ring1 = isring1Xtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
					if(pass_ring1 && ele1Rechit_E->at(i) > maxE_ring1){
						pass_ring1_all = pass_ring1;
						E2_ring1=ele1Rechit_E->at(i);
						pedestal2_ring1=ele1Rechit_pedestal->at(i);
						t2_ring1=ele1Rechit_t->at(i);
						iEta2_ring1=ele1Rechit_IEtaIX->at(i);
						iPhi2_ring1=ele1Rechit_IPhiIY->at(i);

						maxE_ring1 = E2_ring1;
					}
				
					//ring2
					bool pass_ring2 = isring2Xtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
					if(pass_ring2 && ele1Rechit_E->at(i) > maxE_ring2){
						pass_ring2_all = pass_ring2;
						E2_ring2=ele1Rechit_E->at(i);
						pedestal2_ring2=ele1Rechit_pedestal->at(i);
						t2_ring2=ele1Rechit_t->at(i);
						iEta2_ring2=ele1Rechit_IEtaIX->at(i);
						iPhi2_ring2=ele1Rechit_IPhiIY->at(i);

						maxE_ring2 = E2_ring2;
					}

					//sameTrigTower
					bool pass_sameTrigTower = issameTrigTowerXtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
					if(pass_sameTrigTower && ele1Rechit_E->at(i) > maxE_sameTrigTower){
						pass_sameTrigTower_all = pass_sameTrigTower;
						E2_sameTrigTower=ele1Rechit_E->at(i);
						pedestal2_sameTrigTower=ele1Rechit_pedestal->at(i);
						t2_sameTrigTower=ele1Rechit_t->at(i);
						iEta2_sameTrigTower=ele1Rechit_IEtaIX->at(i);
						iPhi2_sameTrigTower=ele1Rechit_IPhiIY->at(i);

						maxE_sameTrigTower = E2_sameTrigTower;
					}


					//diffTrigTower
					int distance = (ele1seedIEta-ele1Rechit_IEtaIX->at(i))*(ele1seedIEta-ele1Rechit_IEtaIX->at(i)) + (ele1seedIPhi-ele1Rechit_IPhiIY->at(i))*(ele1seedIPhi-ele1Rechit_IPhiIY->at(i));
					bool pass_diffTrigTower = (!(pass_sameTrigTower)) && (distance > 0) ;
					if(pass_diffTrigTower && ele1Rechit_E->at(i) > maxE_diffTrigTower){
						pass_diffTrigTower_all = pass_diffTrigTower;
						E2_diffTrigTower=ele1Rechit_E->at(i);
						pedestal2_diffTrigTower=ele1Rechit_pedestal->at(i);
						t2_diffTrigTower=ele1Rechit_t->at(i);
						iEta2_diffTrigTower=ele1Rechit_IEtaIX->at(i);
						iPhi2_diffTrigTower=ele1Rechit_IPhiIY->at(i);

						maxE_diffTrigTower = E2_diffTrigTower;
					}

					//sameTrigTowerNeighbor
					bool pass_sameTrigTowerNeighbor = issameTrigTowerXtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i))  && pass_neighboring;
					if(pass_sameTrigTowerNeighbor && ele1Rechit_E->at(i) > maxE_sameTrigTowerNeighbor){
						pass_sameTrigTowerNeighbor_all = pass_sameTrigTowerNeighbor;
						E2_sameTrigTowerNeighbor=ele1Rechit_E->at(i);
						pedestal2_sameTrigTowerNeighbor=ele1Rechit_pedestal->at(i);
						t2_sameTrigTowerNeighbor=ele1Rechit_t->at(i);
						iEta2_sameTrigTowerNeighbor=ele1Rechit_IEtaIX->at(i);
						iPhi2_sameTrigTowerNeighbor=ele1Rechit_IPhiIY->at(i);

						maxE_sameTrigTowerNeighbor = E2_sameTrigTowerNeighbor;
					}


					//diffTrigTowerNeighbor
					bool pass_diffTrigTowerNeighbor = (!(pass_sameTrigTowerNeighbor)) && (distance > 0) && pass_neighboring ;
					if(pass_diffTrigTowerNeighbor && ele1Rechit_E->at(i) > maxE_diffTrigTowerNeighbor){
						pass_diffTrigTowerNeighbor_all = pass_diffTrigTowerNeighbor;
						E2_diffTrigTowerNeighbor=ele1Rechit_E->at(i);
						pedestal2_diffTrigTowerNeighbor=ele1Rechit_pedestal->at(i);
						t2_diffTrigTowerNeighbor=ele1Rechit_t->at(i);
						iEta2_diffTrigTowerNeighbor=ele1Rechit_IEtaIX->at(i);
						iPhi2_diffTrigTowerNeighbor=ele1Rechit_IPhiIY->at(i);

						maxE_diffTrigTowerNeighbor = E2_diffTrigTowerNeighbor;
					}

				}
			}	
			//fill tree
			if(pass_neighboring_all) tree_out_neighboring_data->Fill();
			if(pass_ring1_all) tree_out_ring1_data->Fill();
			if(pass_ring2_all) tree_out_ring2_data->Fill();
			if(pass_sameTrigTower_all) tree_out_sameTrigTower_data->Fill();
			if(pass_diffTrigTower_all) tree_out_diffTrigTower_data->Fill();
			if(pass_sameTrigTowerNeighbor_all) tree_out_sameTrigTowerNeighbor_data->Fill();
			if(pass_diffTrigTowerNeighbor_all) tree_out_diffTrigTowerNeighbor_data->Fill();
	
			maxE_neighboring = -999.0;
			pass_neighboring_all = false;
			pass_ring1_all = false;
			maxE_ring1 = -999.0;
			pass_ring2_all = false;
			maxE_ring2 = -999.0;
			pass_sameTrigTower_all = false;
			maxE_sameTrigTower = -999.0;
			pass_diffTrigTower_all = false;
			maxE_diffTrigTower = -999.0;
			pass_sameTrigTowerNeighbor_all = false;
			maxE_sameTrigTowerNeighbor = -999.0;
			pass_diffTrigTowerNeighbor_all = false;
			maxE_diffTrigTowerNeighbor = -999.0;

			if(ele2IsEB && ele2seedE < 120){
				for(int i=0;i<ele2Rechit_IEtaIX->size(); i++){
					if(ele2seedIEta == ele2Rechit_IEtaIX->at(i) && ele2seedIPhi == ele2Rechit_IPhiIY->at(i)){
						E1_neighboring=ele2Rechit_E->at(i);
						pedestal1_neighboring=ele2Rechit_pedestal->at(i);
						t1_neighboring=ele2Rechit_t->at(i);
						iEta1_neighboring=ele2Rechit_IEtaIX->at(i);
						iPhi1_neighboring=ele2Rechit_IPhiIY->at(i);

						E1_ring1=ele2Rechit_E->at(i);
						pedestal1_ring1=ele2Rechit_pedestal->at(i);
						t1_ring1=ele2Rechit_t->at(i);
						iEta1_ring1=ele2Rechit_IEtaIX->at(i);
						iPhi1_ring1=ele2Rechit_IPhiIY->at(i);

						E1_ring2=ele2Rechit_E->at(i);
						pedestal1_ring2=ele2Rechit_pedestal->at(i);
						t1_ring2=ele2Rechit_t->at(i);
						iEta1_ring2=ele2Rechit_IEtaIX->at(i);
						iPhi1_ring2=ele2Rechit_IPhiIY->at(i);

						E1_sameTrigTower=ele2Rechit_E->at(i);
						pedestal1_sameTrigTower=ele2Rechit_pedestal->at(i);
						t1_sameTrigTower=ele2Rechit_t->at(i);
						iEta1_sameTrigTower=ele2Rechit_IEtaIX->at(i);
						iPhi1_sameTrigTower=ele2Rechit_IPhiIY->at(i);

						E1_diffTrigTower=ele2Rechit_E->at(i);
						pedestal1_diffTrigTower=ele2Rechit_pedestal->at(i);
						t1_diffTrigTower=ele2Rechit_t->at(i);
						iEta1_diffTrigTower=ele2Rechit_IEtaIX->at(i);
						iPhi1_diffTrigTower=ele2Rechit_IPhiIY->at(i);

						E1_sameTrigTowerNeighbor=ele2Rechit_E->at(i);
						pedestal1_sameTrigTowerNeighbor=ele2Rechit_pedestal->at(i);
						t1_sameTrigTowerNeighbor=ele2Rechit_t->at(i);
						iEta1_sameTrigTowerNeighbor=ele2Rechit_IEtaIX->at(i);
						iPhi1_sameTrigTowerNeighbor=ele2Rechit_IPhiIY->at(i);

						E1_diffTrigTowerNeighbor=ele2Rechit_E->at(i);
						pedestal1_diffTrigTowerNeighbor=ele2Rechit_pedestal->at(i);
						t1_diffTrigTowerNeighbor=ele2Rechit_t->at(i);
						iEta1_diffTrigTowerNeighbor=ele2Rechit_IEtaIX->at(i);
						iPhi1_diffTrigTowerNeighbor=ele2Rechit_IPhiIY->at(i);


					}

					if(ele2Rechit_E->at(i) < 1.0) continue;
					//neighboring
					bool pass_neighboring = isNeighboringXtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i));
					if(pass_neighboring && ele2Rechit_E->at(i) > maxE_neighboring){
						pass_neighboring_all = true;
						E2_neighboring=ele2Rechit_E->at(i);
						pedestal2_neighboring=ele2Rechit_pedestal->at(i);
						t2_neighboring=ele2Rechit_t->at(i);
						iEta2_neighboring=ele2Rechit_IEtaIX->at(i);
						iPhi2_neighboring=ele2Rechit_IPhiIY->at(i);

						maxE_neighboring = E2_neighboring;
					}
		
					//ring1
					bool pass_ring1 = isring1Xtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i));
					if(pass_ring1 && ele2Rechit_E->at(i) > maxE_ring1){
						pass_ring1_all = pass_ring1;
						E2_ring1=ele2Rechit_E->at(i);
						pedestal2_ring1=ele2Rechit_pedestal->at(i);
						t2_ring1=ele2Rechit_t->at(i);
						iEta2_ring1=ele2Rechit_IEtaIX->at(i);
						iPhi2_ring1=ele2Rechit_IPhiIY->at(i);

						maxE_ring1 = E2_ring1;
					}
				
					//ring2
					bool pass_ring2 = isring2Xtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i));
					if(pass_ring2 && ele2Rechit_E->at(i) > maxE_ring2){
						pass_ring2_all = pass_ring2;
						E2_ring2=ele2Rechit_E->at(i);
						pedestal2_ring2=ele2Rechit_pedestal->at(i);
						t2_ring2=ele2Rechit_t->at(i);
						iEta2_ring2=ele2Rechit_IEtaIX->at(i);
						iPhi2_ring2=ele2Rechit_IPhiIY->at(i);

						maxE_ring2 = E2_ring2;
					}

					//sameTrigTower
					bool pass_sameTrigTower = issameTrigTowerXtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i));
					if(pass_sameTrigTower && ele2Rechit_E->at(i) > maxE_sameTrigTower){
						pass_sameTrigTower_all = pass_sameTrigTower;
						E2_sameTrigTower=ele2Rechit_E->at(i);
						pedestal2_sameTrigTower=ele2Rechit_pedestal->at(i);
						t2_sameTrigTower=ele2Rechit_t->at(i);
						iEta2_sameTrigTower=ele2Rechit_IEtaIX->at(i);
						iPhi2_sameTrigTower=ele2Rechit_IPhiIY->at(i);

						maxE_sameTrigTower = E2_sameTrigTower;
					}

					//diffTrigTower
					int distance = (ele2seedIEta-ele2Rechit_IEtaIX->at(i))*(ele2seedIEta-ele2Rechit_IEtaIX->at(i)) + (ele2seedIPhi-ele2Rechit_IPhiIY->at(i))*(ele2seedIPhi-ele2Rechit_IPhiIY->at(i));
					bool pass_diffTrigTower = (!(pass_sameTrigTower)) && (distance > 0) ;
					if(pass_diffTrigTower && ele2Rechit_E->at(i) > maxE_diffTrigTower){
						pass_diffTrigTower_all = pass_diffTrigTower;
						E2_diffTrigTower=ele2Rechit_E->at(i);
						pedestal2_diffTrigTower=ele2Rechit_pedestal->at(i);
						t2_diffTrigTower=ele2Rechit_t->at(i);
						iEta2_diffTrigTower=ele2Rechit_IEtaIX->at(i);
						iPhi2_diffTrigTower=ele2Rechit_IPhiIY->at(i);

						maxE_diffTrigTower = E2_diffTrigTower;
					}

					//sameTrigTowerNeighbor
					bool pass_sameTrigTowerNeighbor = issameTrigTowerXtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i)) && pass_neighboring;
					if(pass_sameTrigTowerNeighbor && ele2Rechit_E->at(i) > maxE_sameTrigTowerNeighbor){
						pass_sameTrigTowerNeighbor_all = pass_sameTrigTowerNeighbor;
						E2_sameTrigTowerNeighbor=ele2Rechit_E->at(i);
						pedestal2_sameTrigTowerNeighbor=ele2Rechit_pedestal->at(i);
						t2_sameTrigTowerNeighbor=ele2Rechit_t->at(i);
						iEta2_sameTrigTowerNeighbor=ele2Rechit_IEtaIX->at(i);
						iPhi2_sameTrigTowerNeighbor=ele2Rechit_IPhiIY->at(i);

						maxE_sameTrigTowerNeighbor = E2_sameTrigTowerNeighbor;
					}

					//diffTrigTowerNeighbor
					bool pass_diffTrigTowerNeighbor = (!(pass_sameTrigTowerNeighbor)) && (distance > 0) && pass_neighboring;
					if(pass_diffTrigTowerNeighbor && ele2Rechit_E->at(i) > maxE_diffTrigTowerNeighbor){
						pass_diffTrigTowerNeighbor_all = pass_diffTrigTowerNeighbor;
						E2_diffTrigTowerNeighbor=ele2Rechit_E->at(i);
						pedestal2_diffTrigTowerNeighbor=ele2Rechit_pedestal->at(i);
						t2_diffTrigTowerNeighbor=ele2Rechit_t->at(i);
						iEta2_diffTrigTowerNeighbor=ele2Rechit_IEtaIX->at(i);
						iPhi2_diffTrigTowerNeighbor=ele2Rechit_IPhiIY->at(i);

						maxE_diffTrigTowerNeighbor = E2_diffTrigTowerNeighbor;
					}


				}
			}	
			
			//fill tree
			if(pass_neighboring_all) tree_out_neighboring_data->Fill();
			if(pass_ring1_all) tree_out_ring1_data->Fill();
			if(pass_ring2_all) tree_out_ring2_data->Fill();
			if(pass_sameTrigTower_all) tree_out_sameTrigTower_data->Fill();
			if(pass_diffTrigTower_all) tree_out_diffTrigTower_data->Fill();
			if(pass_sameTrigTowerNeighbor_all) tree_out_sameTrigTowerNeighbor_data->Fill();
			if(pass_diffTrigTowerNeighbor_all) tree_out_diffTrigTowerNeighbor_data->Fill();

		}	
		tree_out_neighboring_data->Write();
		tree_out_ring1_data->Write();
		tree_out_ring2_data->Write();
		tree_out_sameTrigTower_data->Write();
		tree_out_diffTrigTower_data->Write();
		tree_out_sameTrigTowerNeighbor_data->Write();
		tree_out_diffTrigTowerNeighbor_data->Write();

		tree_out_neighboring_MC = new TTree("ZeeTiming_neighboring_MC","second crystal from neighboring crystals");
		tree_out_neighboring_MC->Branch("E1", &E1_neighboring, "E1/F");	
		tree_out_neighboring_MC->Branch("E2", &E2_neighboring, "E2/F");	
		tree_out_neighboring_MC->Branch("t1", &t1_neighboring, "t1/F");	
		tree_out_neighboring_MC->Branch("t2", &t2_neighboring, "t2/F");	
		tree_out_neighboring_MC->Branch("pedestal1", &pedestal1_neighboring, "pedestal1/F");	
		tree_out_neighboring_MC->Branch("pedestal2", &pedestal2_neighboring, "pedestal2/F");	
		tree_out_neighboring_MC->Branch("iEta1", &iEta1_neighboring, "iEta1/I");	
		tree_out_neighboring_MC->Branch("iEta2", &iEta2_neighboring, "iEta2/I");	
		tree_out_neighboring_MC->Branch("iPhi1", &iPhi1_neighboring, "iPhi1/I");	
		tree_out_neighboring_MC->Branch("iPhi2", &iPhi2_neighboring, "iPhi2/I");	

		tree_out_ring1_MC = new TTree("ZeeTiming_ring1_MC","second crystal from ring1 crystals");
		tree_out_ring1_MC->Branch("E1", &E1_ring1, "E1/F");	
		tree_out_ring1_MC->Branch("E2", &E2_ring1, "E2/F");	
		tree_out_ring1_MC->Branch("t1", &t1_ring1, "t1/F");	
		tree_out_ring1_MC->Branch("t2", &t2_ring1, "t2/F");	
		tree_out_ring1_MC->Branch("pedestal1", &pedestal1_ring1, "pedestal1/F");	
		tree_out_ring1_MC->Branch("pedestal2", &pedestal2_ring1, "pedestal2/F");	
		tree_out_ring1_MC->Branch("iEta1", &iEta1_ring1, "iEta1/I");	
		tree_out_ring1_MC->Branch("iEta2", &iEta2_ring1, "iEta2/I");	
		tree_out_ring1_MC->Branch("iPhi1", &iPhi1_ring1, "iPhi1/I");	
		tree_out_ring1_MC->Branch("iPhi2", &iPhi2_ring1, "iPhi2/I");	



		tree_out_ring2_MC = new TTree("ZeeTiming_ring2_MC","second crystal from ring2 crystals");
		tree_out_ring2_MC->Branch("E1", &E1_ring2, "E1/F");	
		tree_out_ring2_MC->Branch("E2", &E2_ring2, "E2/F");	
		tree_out_ring2_MC->Branch("t1", &t1_ring2, "t1/F");	
		tree_out_ring2_MC->Branch("t2", &t2_ring2, "t2/F");	
		tree_out_ring2_MC->Branch("pedestal1", &pedestal1_ring2, "pedestal1/F");	
		tree_out_ring2_MC->Branch("pedestal2", &pedestal2_ring2, "pedestal2/F");	
		tree_out_ring2_MC->Branch("iEta1", &iEta1_ring2, "iEta1/I");	
		tree_out_ring2_MC->Branch("iEta2", &iEta2_ring2, "iEta2/I");	
		tree_out_ring2_MC->Branch("iPhi1", &iPhi1_ring2, "iPhi1/I");	
		tree_out_ring2_MC->Branch("iPhi2", &iPhi2_ring2, "iPhi2/I");	



		tree_out_sameTrigTower_MC = new TTree("ZeeTiming_sameTrigTower_MC","second crystal from sameTrigTower crystals");
		tree_out_sameTrigTower_MC->Branch("E1", &E1_sameTrigTower, "E1/F");	
		tree_out_sameTrigTower_MC->Branch("E2", &E2_sameTrigTower, "E2/F");	
		tree_out_sameTrigTower_MC->Branch("t1", &t1_sameTrigTower, "t1/F");	
		tree_out_sameTrigTower_MC->Branch("t2", &t2_sameTrigTower, "t2/F");	
		tree_out_sameTrigTower_MC->Branch("pedestal1", &pedestal1_sameTrigTower, "pedestal1/F");	
		tree_out_sameTrigTower_MC->Branch("pedestal2", &pedestal2_sameTrigTower, "pedestal2/F");	
		tree_out_sameTrigTower_MC->Branch("iEta1", &iEta1_sameTrigTower, "iEta1/I");	
		tree_out_sameTrigTower_MC->Branch("iEta2", &iEta2_sameTrigTower, "iEta2/I");	
		tree_out_sameTrigTower_MC->Branch("iPhi1", &iPhi1_sameTrigTower, "iPhi1/I");	
		tree_out_sameTrigTower_MC->Branch("iPhi2", &iPhi2_sameTrigTower, "iPhi2/I");	


		tree_out_diffTrigTower_MC = new TTree("ZeeTiming_diffTrigTower_MC","second crystal from diffTrigTower crystals");
		tree_out_diffTrigTower_MC->Branch("E1", &E1_diffTrigTower, "E1/F");	
		tree_out_diffTrigTower_MC->Branch("E2", &E2_diffTrigTower, "E2/F");	
		tree_out_diffTrigTower_MC->Branch("t1", &t1_diffTrigTower, "t1/F");	
		tree_out_diffTrigTower_MC->Branch("t2", &t2_diffTrigTower, "t2/F");	
		tree_out_diffTrigTower_MC->Branch("pedestal1", &pedestal1_diffTrigTower, "pedestal1/F");	
		tree_out_diffTrigTower_MC->Branch("pedestal2", &pedestal2_diffTrigTower, "pedestal2/F");	
		tree_out_diffTrigTower_MC->Branch("iEta1", &iEta1_diffTrigTower, "iEta1/I");	
		tree_out_diffTrigTower_MC->Branch("iEta2", &iEta2_diffTrigTower, "iEta2/I");	
		tree_out_diffTrigTower_MC->Branch("iPhi1", &iPhi1_diffTrigTower, "iPhi1/I");	
		tree_out_diffTrigTower_MC->Branch("iPhi2", &iPhi2_diffTrigTower, "iPhi2/I");	


		tree_out_sameTrigTowerNeighbor_MC = new TTree("ZeeTiming_sameTrigTowerNeighbor_MC","second crystal from sameTrigTowerNeighbor crystals");
		tree_out_sameTrigTowerNeighbor_MC->Branch("E1", &E1_sameTrigTowerNeighbor, "E1/F");	
		tree_out_sameTrigTowerNeighbor_MC->Branch("E2", &E2_sameTrigTowerNeighbor, "E2/F");	
		tree_out_sameTrigTowerNeighbor_MC->Branch("t1", &t1_sameTrigTowerNeighbor, "t1/F");	
		tree_out_sameTrigTowerNeighbor_MC->Branch("t2", &t2_sameTrigTowerNeighbor, "t2/F");	
		tree_out_sameTrigTowerNeighbor_MC->Branch("pedestal1", &pedestal1_sameTrigTowerNeighbor, "pedestal1/F");	
		tree_out_sameTrigTowerNeighbor_MC->Branch("pedestal2", &pedestal2_sameTrigTowerNeighbor, "pedestal2/F");	
		tree_out_sameTrigTowerNeighbor_MC->Branch("iEta1", &iEta1_sameTrigTowerNeighbor, "iEta1/I");	
		tree_out_sameTrigTowerNeighbor_MC->Branch("iEta2", &iEta2_sameTrigTowerNeighbor, "iEta2/I");	
		tree_out_sameTrigTowerNeighbor_MC->Branch("iPhi1", &iPhi1_sameTrigTowerNeighbor, "iPhi1/I");	
		tree_out_sameTrigTowerNeighbor_MC->Branch("iPhi2", &iPhi2_sameTrigTowerNeighbor, "iPhi2/I");	


		tree_out_diffTrigTowerNeighbor_MC = new TTree("ZeeTiming_diffTrigTowerNeighbor_MC","second crystal from diffTrigTowerNeighbor crystals");
		tree_out_diffTrigTowerNeighbor_MC->Branch("E1", &E1_diffTrigTowerNeighbor, "E1/F");	
		tree_out_diffTrigTowerNeighbor_MC->Branch("E2", &E2_diffTrigTowerNeighbor, "E2/F");	
		tree_out_diffTrigTowerNeighbor_MC->Branch("t1", &t1_diffTrigTowerNeighbor, "t1/F");	
		tree_out_diffTrigTowerNeighbor_MC->Branch("t2", &t2_diffTrigTowerNeighbor, "t2/F");	
		tree_out_diffTrigTowerNeighbor_MC->Branch("pedestal1", &pedestal1_diffTrigTowerNeighbor, "pedestal1/F");	
		tree_out_diffTrigTowerNeighbor_MC->Branch("pedestal2", &pedestal2_diffTrigTowerNeighbor, "pedestal2/F");	
		tree_out_diffTrigTowerNeighbor_MC->Branch("iEta1", &iEta1_diffTrigTowerNeighbor, "iEta1/I");	
		tree_out_diffTrigTowerNeighbor_MC->Branch("iEta2", &iEta2_diffTrigTowerNeighbor, "iEta2/I");	
		tree_out_diffTrigTowerNeighbor_MC->Branch("iPhi1", &iPhi1_diffTrigTowerNeighbor, "iPhi1/I");	
		tree_out_diffTrigTowerNeighbor_MC->Branch("iPhi2", &iPhi2_diffTrigTowerNeighbor, "iPhi2/I");	



		for(int ientry=0;ientry<N_entries_MC; ientry++){
			if(ientry%100000 ==0) cout<<"reading original tree entry "<<ientry<<"  out of "<<N_entries_MC<<endl;
			tree_MC->GetEntry(ientry);
			
			float maxE_neighboring = -999.0;
			bool pass_neighboring_all = false;
			bool pass_ring1_all = false;
			float maxE_ring1 = -999.0;
			bool pass_ring2_all = false;
			float maxE_ring2 = -999.0;
			bool pass_sameTrigTower_all = false;
			float maxE_sameTrigTower = -999.0;
			bool pass_diffTrigTower_all = false;
			float maxE_diffTrigTower = -999.0;
	
			bool pass_sameTrigTowerNeighbor_all = false;
			float maxE_sameTrigTowerNeighbor = -999.0;
			bool pass_diffTrigTowerNeighbor_all = false;
			float maxE_diffTrigTowerNeighbor = -999.0;
			
			if(ele1IsEB && ele1seedE < 120){
				for(int i=0;i<ele1Rechit_IEtaIX->size(); i++){
					if(ele1seedIEta == ele1Rechit_IEtaIX->at(i) && ele1seedIPhi == ele1Rechit_IPhiIY->at(i)){
						E1_neighboring=ele1Rechit_E->at(i);
						pedestal1_neighboring=ele1Rechit_pedestal->at(i);
						t1_neighboring=ele1Rechit_t->at(i);
						iEta1_neighboring=ele1Rechit_IEtaIX->at(i);
						iPhi1_neighboring=ele1Rechit_IPhiIY->at(i);
						E1_ring1=ele1Rechit_E->at(i);
						pedestal1_ring1=ele1Rechit_pedestal->at(i);
						t1_ring1=ele1Rechit_t->at(i);
						iEta1_ring1=ele1Rechit_IEtaIX->at(i);
						iPhi1_ring1=ele1Rechit_IPhiIY->at(i);

						E1_ring2=ele1Rechit_E->at(i);
						pedestal1_ring2=ele1Rechit_pedestal->at(i);
						t1_ring2=ele1Rechit_t->at(i);
						iEta1_ring2=ele1Rechit_IEtaIX->at(i);
						iPhi1_ring2=ele1Rechit_IPhiIY->at(i);

						E1_sameTrigTower=ele1Rechit_E->at(i);
						pedestal1_sameTrigTower=ele1Rechit_pedestal->at(i);
						t1_sameTrigTower=ele1Rechit_t->at(i);
						iEta1_sameTrigTower=ele1Rechit_IEtaIX->at(i);
						iPhi1_sameTrigTower=ele1Rechit_IPhiIY->at(i);

						E1_diffTrigTower=ele1Rechit_E->at(i);
						pedestal1_diffTrigTower=ele1Rechit_pedestal->at(i);
						t1_diffTrigTower=ele1Rechit_t->at(i);
						iEta1_diffTrigTower=ele1Rechit_IEtaIX->at(i);
						iPhi1_diffTrigTower=ele1Rechit_IPhiIY->at(i);
						E1_sameTrigTowerNeighbor=ele1Rechit_E->at(i);
						pedestal1_sameTrigTowerNeighbor=ele1Rechit_pedestal->at(i);
						t1_sameTrigTowerNeighbor=ele1Rechit_t->at(i);
						iEta1_sameTrigTowerNeighbor=ele1Rechit_IEtaIX->at(i);
						iPhi1_sameTrigTowerNeighbor=ele1Rechit_IPhiIY->at(i);

						E1_diffTrigTowerNeighbor=ele1Rechit_E->at(i);
						pedestal1_diffTrigTowerNeighbor=ele1Rechit_pedestal->at(i);
						t1_diffTrigTowerNeighbor=ele1Rechit_t->at(i);
						iEta1_diffTrigTowerNeighbor=ele1Rechit_IEtaIX->at(i);
						iPhi1_diffTrigTowerNeighbor=ele1Rechit_IPhiIY->at(i);


					}
					if(ele1Rechit_E->at(i) < 1.0) continue;
					//neighboring
					bool pass_neighboring = isNeighboringXtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
					if(pass_neighboring && ele1Rechit_E->at(i) > maxE_neighboring){
						pass_neighboring_all = true;
						E2_neighboring=ele1Rechit_E->at(i);
						pedestal2_neighboring=ele1Rechit_pedestal->at(i);
						t2_neighboring=ele1Rechit_t->at(i);
						iEta2_neighboring=ele1Rechit_IEtaIX->at(i);
						iPhi2_neighboring=ele1Rechit_IPhiIY->at(i);
						maxE_neighboring = E2_neighboring;
					}
		
					//ring1
					bool pass_ring1 = isring1Xtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
					if(pass_ring1 && ele1Rechit_E->at(i) > maxE_ring1){
						pass_ring1_all = pass_ring1;
						E2_ring1=ele1Rechit_E->at(i);
						pedestal2_ring1=ele1Rechit_pedestal->at(i);
						t2_ring1=ele1Rechit_t->at(i);
						iEta2_ring1=ele1Rechit_IEtaIX->at(i);
						iPhi2_ring1=ele1Rechit_IPhiIY->at(i);

						maxE_ring1 = E2_ring1;
					}
				
					//ring2
					bool pass_ring2 = isring2Xtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
					if(pass_ring2 && ele1Rechit_E->at(i) > maxE_ring2){
						pass_ring2_all = pass_ring2;
						E2_ring2=ele1Rechit_E->at(i);
						pedestal2_ring2=ele1Rechit_pedestal->at(i);
						t2_ring2=ele1Rechit_t->at(i);
						iEta2_ring2=ele1Rechit_IEtaIX->at(i);
						iPhi2_ring2=ele1Rechit_IPhiIY->at(i);

						maxE_ring2 = E2_ring2;
					}

					//sameTrigTower
					bool pass_sameTrigTower = issameTrigTowerXtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
					if(pass_sameTrigTower && ele1Rechit_E->at(i) > maxE_sameTrigTower){
						pass_sameTrigTower_all = pass_sameTrigTower;
						E2_sameTrigTower=ele1Rechit_E->at(i);
						pedestal2_sameTrigTower=ele1Rechit_pedestal->at(i);
						t2_sameTrigTower=ele1Rechit_t->at(i);
						iEta2_sameTrigTower=ele1Rechit_IEtaIX->at(i);
						iPhi2_sameTrigTower=ele1Rechit_IPhiIY->at(i);

						maxE_sameTrigTower = E2_sameTrigTower;
					}


					//diffTrigTower
					int distance = (ele1seedIEta-ele1Rechit_IEtaIX->at(i))*(ele1seedIEta-ele1Rechit_IEtaIX->at(i)) + (ele1seedIPhi-ele1Rechit_IPhiIY->at(i))*(ele1seedIPhi-ele1Rechit_IPhiIY->at(i));
					bool pass_diffTrigTower = (!(pass_sameTrigTower)) && (distance > 0) ;
					if(pass_diffTrigTower && ele1Rechit_E->at(i) > maxE_diffTrigTower){
						pass_diffTrigTower_all = pass_diffTrigTower;
						E2_diffTrigTower=ele1Rechit_E->at(i);
						pedestal2_diffTrigTower=ele1Rechit_pedestal->at(i);
						t2_diffTrigTower=ele1Rechit_t->at(i);
						iEta2_diffTrigTower=ele1Rechit_IEtaIX->at(i);
						iPhi2_diffTrigTower=ele1Rechit_IPhiIY->at(i);

						maxE_diffTrigTower = E2_diffTrigTower;
					}

					//sameTrigTowerNeighbor
					bool pass_sameTrigTowerNeighbor = issameTrigTowerXtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i))  && pass_neighboring;
					if(pass_sameTrigTowerNeighbor && ele1Rechit_E->at(i) > maxE_sameTrigTowerNeighbor){
						pass_sameTrigTowerNeighbor_all = pass_sameTrigTowerNeighbor;
						E2_sameTrigTowerNeighbor=ele1Rechit_E->at(i);
						pedestal2_sameTrigTowerNeighbor=ele1Rechit_pedestal->at(i);
						t2_sameTrigTowerNeighbor=ele1Rechit_t->at(i);
						iEta2_sameTrigTowerNeighbor=ele1Rechit_IEtaIX->at(i);
						iPhi2_sameTrigTowerNeighbor=ele1Rechit_IPhiIY->at(i);

						maxE_sameTrigTowerNeighbor = E2_sameTrigTowerNeighbor;
					}


					//diffTrigTowerNeighbor
					bool pass_diffTrigTowerNeighbor = (!(pass_sameTrigTowerNeighbor)) && (distance > 0) && pass_neighboring ;
					if(pass_diffTrigTowerNeighbor && ele1Rechit_E->at(i) > maxE_diffTrigTowerNeighbor){
						pass_diffTrigTowerNeighbor_all = pass_diffTrigTowerNeighbor;
						E2_diffTrigTowerNeighbor=ele1Rechit_E->at(i);
						pedestal2_diffTrigTowerNeighbor=ele1Rechit_pedestal->at(i);
						t2_diffTrigTowerNeighbor=ele1Rechit_t->at(i);
						iEta2_diffTrigTowerNeighbor=ele1Rechit_IEtaIX->at(i);
						iPhi2_diffTrigTowerNeighbor=ele1Rechit_IPhiIY->at(i);

						maxE_diffTrigTowerNeighbor = E2_diffTrigTowerNeighbor;
					}

				}
			}	
			//fill tree
			if(pass_neighboring_all) tree_out_neighboring_MC->Fill();
			if(pass_ring1_all) tree_out_ring1_MC->Fill();
			if(pass_ring2_all) tree_out_ring2_MC->Fill();
			if(pass_sameTrigTower_all) tree_out_sameTrigTower_MC->Fill();
			if(pass_diffTrigTower_all) tree_out_diffTrigTower_MC->Fill();
			if(pass_sameTrigTowerNeighbor_all) tree_out_sameTrigTowerNeighbor_MC->Fill();
			if(pass_diffTrigTowerNeighbor_all) tree_out_diffTrigTowerNeighbor_MC->Fill();
	
			maxE_neighboring = -999.0;
			pass_neighboring_all = false;
			pass_ring1_all = false;
			maxE_ring1 = -999.0;
			pass_ring2_all = false;
			maxE_ring2 = -999.0;
			pass_sameTrigTower_all = false;
			maxE_sameTrigTower = -999.0;
			pass_diffTrigTower_all = false;
			maxE_diffTrigTower = -999.0;
			pass_sameTrigTowerNeighbor_all = false;
			maxE_sameTrigTowerNeighbor = -999.0;
			pass_diffTrigTowerNeighbor_all = false;
			maxE_diffTrigTowerNeighbor = -999.0;

			if(ele2IsEB && ele2seedE < 120){
				for(int i=0;i<ele2Rechit_IEtaIX->size(); i++){
					if(ele2seedIEta == ele2Rechit_IEtaIX->at(i) && ele2seedIPhi == ele2Rechit_IPhiIY->at(i)){
						E1_neighboring=ele2Rechit_E->at(i);
						pedestal1_neighboring=ele2Rechit_pedestal->at(i);
						t1_neighboring=ele2Rechit_t->at(i);
						iEta1_neighboring=ele2Rechit_IEtaIX->at(i);
						iPhi1_neighboring=ele2Rechit_IPhiIY->at(i);

						E1_ring1=ele2Rechit_E->at(i);
						pedestal1_ring1=ele2Rechit_pedestal->at(i);
						t1_ring1=ele2Rechit_t->at(i);
						iEta1_ring1=ele2Rechit_IEtaIX->at(i);
						iPhi1_ring1=ele2Rechit_IPhiIY->at(i);

						E1_ring2=ele2Rechit_E->at(i);
						pedestal1_ring2=ele2Rechit_pedestal->at(i);
						t1_ring2=ele2Rechit_t->at(i);
						iEta1_ring2=ele2Rechit_IEtaIX->at(i);
						iPhi1_ring2=ele2Rechit_IPhiIY->at(i);

						E1_sameTrigTower=ele2Rechit_E->at(i);
						pedestal1_sameTrigTower=ele2Rechit_pedestal->at(i);
						t1_sameTrigTower=ele2Rechit_t->at(i);
						iEta1_sameTrigTower=ele2Rechit_IEtaIX->at(i);
						iPhi1_sameTrigTower=ele2Rechit_IPhiIY->at(i);

						E1_diffTrigTower=ele2Rechit_E->at(i);
						pedestal1_diffTrigTower=ele2Rechit_pedestal->at(i);
						t1_diffTrigTower=ele2Rechit_t->at(i);
						iEta1_diffTrigTower=ele2Rechit_IEtaIX->at(i);
						iPhi1_diffTrigTower=ele2Rechit_IPhiIY->at(i);

						E1_sameTrigTowerNeighbor=ele2Rechit_E->at(i);
						pedestal1_sameTrigTowerNeighbor=ele2Rechit_pedestal->at(i);
						t1_sameTrigTowerNeighbor=ele2Rechit_t->at(i);
						iEta1_sameTrigTowerNeighbor=ele2Rechit_IEtaIX->at(i);
						iPhi1_sameTrigTowerNeighbor=ele2Rechit_IPhiIY->at(i);

						E1_diffTrigTowerNeighbor=ele2Rechit_E->at(i);
						pedestal1_diffTrigTowerNeighbor=ele2Rechit_pedestal->at(i);
						t1_diffTrigTowerNeighbor=ele2Rechit_t->at(i);
						iEta1_diffTrigTowerNeighbor=ele2Rechit_IEtaIX->at(i);
						iPhi1_diffTrigTowerNeighbor=ele2Rechit_IPhiIY->at(i);


					}

					if(ele2Rechit_E->at(i) < 1.0) continue;
					//neighboring
					bool pass_neighboring = isNeighboringXtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i));
					if(pass_neighboring && ele2Rechit_E->at(i) > maxE_neighboring){
						pass_neighboring_all = true;
						E2_neighboring=ele2Rechit_E->at(i);
						pedestal2_neighboring=ele2Rechit_pedestal->at(i);
						t2_neighboring=ele2Rechit_t->at(i);
						iEta2_neighboring=ele2Rechit_IEtaIX->at(i);
						iPhi2_neighboring=ele2Rechit_IPhiIY->at(i);

						maxE_neighboring = E2_neighboring;
					}
		
					//ring1
					bool pass_ring1 = isring1Xtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i));
					if(pass_ring1 && ele2Rechit_E->at(i) > maxE_ring1){
						pass_ring1_all = pass_ring1;
						E2_ring1=ele2Rechit_E->at(i);
						pedestal2_ring1=ele2Rechit_pedestal->at(i);
						t2_ring1=ele2Rechit_t->at(i);
						iEta2_ring1=ele2Rechit_IEtaIX->at(i);
						iPhi2_ring1=ele2Rechit_IPhiIY->at(i);

						maxE_ring1 = E2_ring1;
					}
				
					//ring2
					bool pass_ring2 = isring2Xtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i));
					if(pass_ring2 && ele2Rechit_E->at(i) > maxE_ring2){
						pass_ring2_all = pass_ring2;
						E2_ring2=ele2Rechit_E->at(i);
						pedestal2_ring2=ele2Rechit_pedestal->at(i);
						t2_ring2=ele2Rechit_t->at(i);
						iEta2_ring2=ele2Rechit_IEtaIX->at(i);
						iPhi2_ring2=ele2Rechit_IPhiIY->at(i);

						maxE_ring2 = E2_ring2;
					}

					//sameTrigTower
					bool pass_sameTrigTower = issameTrigTowerXtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i));
					if(pass_sameTrigTower && ele2Rechit_E->at(i) > maxE_sameTrigTower){
						pass_sameTrigTower_all = pass_sameTrigTower;
						E2_sameTrigTower=ele2Rechit_E->at(i);
						pedestal2_sameTrigTower=ele2Rechit_pedestal->at(i);
						t2_sameTrigTower=ele2Rechit_t->at(i);
						iEta2_sameTrigTower=ele2Rechit_IEtaIX->at(i);
						iPhi2_sameTrigTower=ele2Rechit_IPhiIY->at(i);

						maxE_sameTrigTower = E2_sameTrigTower;
					}

					//diffTrigTower
					int distance = (ele2seedIEta-ele2Rechit_IEtaIX->at(i))*(ele2seedIEta-ele2Rechit_IEtaIX->at(i)) + (ele2seedIPhi-ele2Rechit_IPhiIY->at(i))*(ele2seedIPhi-ele2Rechit_IPhiIY->at(i));
					bool pass_diffTrigTower = (!(pass_sameTrigTower)) && (distance > 0) ;
					if(pass_diffTrigTower && ele2Rechit_E->at(i) > maxE_diffTrigTower){
						pass_diffTrigTower_all = pass_diffTrigTower;
						E2_diffTrigTower=ele2Rechit_E->at(i);
						pedestal2_diffTrigTower=ele2Rechit_pedestal->at(i);
						t2_diffTrigTower=ele2Rechit_t->at(i);
						iEta2_diffTrigTower=ele2Rechit_IEtaIX->at(i);
						iPhi2_diffTrigTower=ele2Rechit_IPhiIY->at(i);

						maxE_diffTrigTower = E2_diffTrigTower;
					}

					//sameTrigTowerNeighbor
					bool pass_sameTrigTowerNeighbor = issameTrigTowerXtal(ele2seedIEta, ele2seedIPhi, ele2Rechit_IEtaIX->at(i), ele2Rechit_IPhiIY->at(i)) && pass_neighboring;
					if(pass_sameTrigTowerNeighbor && ele2Rechit_E->at(i) > maxE_sameTrigTowerNeighbor){
						pass_sameTrigTowerNeighbor_all = pass_sameTrigTowerNeighbor;
						E2_sameTrigTowerNeighbor=ele2Rechit_E->at(i);
						pedestal2_sameTrigTowerNeighbor=ele2Rechit_pedestal->at(i);
						t2_sameTrigTowerNeighbor=ele2Rechit_t->at(i);
						iEta2_sameTrigTowerNeighbor=ele2Rechit_IEtaIX->at(i);
						iPhi2_sameTrigTowerNeighbor=ele2Rechit_IPhiIY->at(i);

						maxE_sameTrigTowerNeighbor = E2_sameTrigTowerNeighbor;
					}

					//diffTrigTowerNeighbor
					bool pass_diffTrigTowerNeighbor = (!(pass_sameTrigTowerNeighbor)) && (distance > 0) && pass_neighboring;
					if(pass_diffTrigTowerNeighbor && ele2Rechit_E->at(i) > maxE_diffTrigTowerNeighbor){
						pass_diffTrigTowerNeighbor_all = pass_diffTrigTowerNeighbor;
						E2_diffTrigTowerNeighbor=ele2Rechit_E->at(i);
						pedestal2_diffTrigTowerNeighbor=ele2Rechit_pedestal->at(i);
						t2_diffTrigTowerNeighbor=ele2Rechit_t->at(i);
						iEta2_diffTrigTowerNeighbor=ele2Rechit_IEtaIX->at(i);
						iPhi2_diffTrigTowerNeighbor=ele2Rechit_IPhiIY->at(i);

						maxE_diffTrigTowerNeighbor = E2_diffTrigTowerNeighbor;
					}


				}
			}	
			
			//fill tree
			if(pass_neighboring_all) tree_out_neighboring_MC->Fill();
			if(pass_ring1_all) tree_out_ring1_MC->Fill();
			if(pass_ring2_all) tree_out_ring2_MC->Fill();
			if(pass_sameTrigTower_all) tree_out_sameTrigTower_MC->Fill();
			if(pass_diffTrigTower_all) tree_out_diffTrigTower_MC->Fill();
			if(pass_sameTrigTowerNeighbor_all) tree_out_sameTrigTowerNeighbor_MC->Fill();
			if(pass_diffTrigTowerNeighbor_all) tree_out_diffTrigTowerNeighbor_MC->Fill();

		}	
		tree_out_neighboring_MC->Write();
		tree_out_ring1_MC->Write();
		tree_out_ring2_MC->Write();
		tree_out_sameTrigTower_MC->Write();
		tree_out_diffTrigTower_MC->Write();
		tree_out_sameTrigTowerNeighbor_MC->Write();
		tree_out_diffTrigTowerNeighbor_MC->Write();

	}
	else{
		tree_out_neighboring_data = (TTree*)file_out->Get("ZeeTiming_neighboring_data");	
		tree_out_neighboring_MC = (TTree*)file_out->Get("ZeeTiming_neighboring_MC");	
		tree_out_ring1_data = (TTree*)file_out->Get("ZeeTiming_ring1_data");	
		tree_out_ring1_MC = (TTree*)file_out->Get("ZeeTiming_ring1_MC");	
		tree_out_ring2_data = (TTree*)file_out->Get("ZeeTiming_ring2_data");	
		tree_out_ring2_MC = (TTree*)file_out->Get("ZeeTiming_ring2_MC");	
		tree_out_sameTrigTower_data = (TTree*)file_out->Get("ZeeTiming_sameTrigTower_data");	
		tree_out_sameTrigTower_MC = (TTree*)file_out->Get("ZeeTiming_sameTrigTower_MC");	
		tree_out_diffTrigTower_data = (TTree*)file_out->Get("ZeeTiming_diffTrigTower_data");	
		tree_out_diffTrigTower_MC = (TTree*)file_out->Get("ZeeTiming_diffTrigTower_MC");	
		tree_out_sameTrigTowerNeighbor_data = (TTree*)file_out->Get("ZeeTiming_sameTrigTowerNeighbor_data");	
		tree_out_sameTrigTowerNeighbor_MC = (TTree*)file_out->Get("ZeeTiming_sameTrigTowerNeighbor_MC");	
		tree_out_diffTrigTowerNeighbor_data = (TTree*)file_out->Get("ZeeTiming_diffTrigTowerNeighbor_data");	
		tree_out_diffTrigTowerNeighbor_MC = (TTree*)file_out->Get("ZeeTiming_diffTrigTowerNeighbor_MC");	

	}
	//draw time resolution vs. effective amplitude
	drawTimeResoVsAeff(tree_out_neighboring_data, tree_out_neighboring_MC, "inclusive", "EB");
	
	//drawTimeResoVsAeff(tree_out_ring1_data, tree_out_ring1_MC, "ring1");
	//drawTimeResoVsAeff(tree_out_ring2_data, tree_out_ring2_MC, "ring2");
	//drawTimeResoVsAeff(tree_out_sameTrigTower_data, tree_out_sameTrigTower_MC, "sameTT", "EB same RO unit");
	//drawTimeResoVsAeff(tree_out_diffTrigTower_data, tree_out_diffTrigTower_MC, "diffTT", "EB diff. RO unit");
	drawTimeResoVsAeff(tree_out_sameTrigTowerNeighbor_data, tree_out_sameTrigTowerNeighbor_MC, "sameTT", "EB same RO unit");
	drawTimeResoVsAeff(tree_out_diffTrigTowerNeighbor_data, tree_out_diffTrigTowerNeighbor_MC, "diffTT", "EB diff. RO unit");

	file_out->Close();
}
