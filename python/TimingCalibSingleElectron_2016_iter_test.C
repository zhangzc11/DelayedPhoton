#include <sys/stat.h>
#include <sys/types.h>

bool drawOnly = true;
const int starting_iter = 20;
const int max_iter = 20;

const int nIetaTotal = 171;//-85 to 85
const int nIphiTotal = 360;// 1 to 360

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

void drawTimingICMap(TH2F * h2_map, TString label, TString title, float range){
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

        float minZ = ceil(10.0*(meanZ - range))/10.0 - 0.1;
        float maxZ = ceil(10.0*(meanZ + range))/10.0;

	h2_map->GetZaxis()->SetRangeUser(minZ,maxZ);
        h2_map->Draw("colz");
	myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_"+label+"_test.pdf");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_"+label+"_test.png");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_"+label+"_test.C");

        h2_map->GetYaxis()->SetRangeUser(0.5,50.5);
        h2_map->GetXaxis()->SetRangeUser(0.5,85.5);
        h2_map->Draw("colz");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_data_zoom.pdf");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_"+label+"_zoom_test.pdf");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_"+label+"_zoom_test.png");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_"+label+"_zoom_test.C");

        delete myC;
        h2_map->GetYaxis()->SetRangeUser(0.5,360.5);
        h2_map->GetXaxis()->SetRangeUser(-85.5,85.5);
        h2_map->Draw("colz");
}
void draw1DICDiff(TH1F * h1_map, TString label, TString title){
        cout<<"draw timing IC diff 1D for "<<label<<endl;

        //gStyle->SetOptFit(1);
        gStyle->SetOptStat(1);

        TCanvas * myC = new TCanvas( "myC_1DDiff", "myC_1DDiff", 200, 10, 800, 800 );
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

        myC->SetLogy(1);

        h1_map->SetTitle("");
        h1_map->GetXaxis()->SetTitle(title);
        h1_map->GetYaxis()->SetTitle("Events");
        h1_map->GetXaxis()->SetTitleSize( axisTitleSize - 0.02);
        h1_map->GetXaxis()->SetTitleOffset( axisTitleOffset + 0.6);
        h1_map->GetYaxis()->SetTitleSize( axisTitleSize );
        h1_map->GetYaxis()->SetTitleOffset( axisTitleOffset + 0.18);
        h1_map->SetLineWidth(2);

        h1_map->Draw("");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_1DDiff_"+label+"_test.pdf");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_1DDiff_"+label+"_test.png");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_1DDiff_"+label+"_test.C");
        delete myC;
}

void TimingCalibSingleElectron_2016_iter_test()
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

	//calibration map

	float IC_map_N_1[nIetaTotal][nIphiTotal] = {0};
	float IC_map_N[nIetaTotal][nIphiTotal] = {0};
	float mean_IC_diff[max_iter] = {0};
	float mean_IC_residual[max_iter] = {0};
        float emean_IC_diff[max_iter] = {0};
        float emean_IC_residual[max_iter] = {0};

        TH1F * h1_array_IC_map_diff[max_iter];
        TH1F * h1_array_IC_map_residual[max_iter];

	for(int iIter = 0; iIter < max_iter; iIter++){
		if(iIter <= starting_iter) drawOnly = true;
		else drawOnly = false;

		TFile * file_start;
		if(starting_iter >= 0) file_start = new TFile(("IC_maps/IC_map_SingleElectron_2016_test_iter"+std::to_string(starting_iter)+".root").c_str(),"READ");

		TFile * file_out;
		TFile * file_previous;
		if(!drawOnly)  file_out = new TFile(("IC_maps/IC_map_SingleElectron_2016_test_iter"+std::to_string(iIter)+".root").c_str(),"RECREATE");
		else  file_out = new TFile(("IC_maps/IC_map_SingleElectron_2016_test_iter"+std::to_string(iIter)+".root").c_str(),"READ");
		if(iIter > 0) file_previous = new TFile(("IC_maps/IC_map_SingleElectron_2016_test_iter"+std::to_string(iIter-1)+".root").c_str(),"READ");

        	file_out->cd();
                if(!drawOnly) h1_array_IC_map_residual[iIter] = new TH1F(("h1_IC_map_residual_iter"+std::to_string(iIter)).c_str(),("h1_IC_map_residual_iter"+std::to_string(iIter)).c_str(), 1000, -0.01, 2.0);
		else h1_array_IC_map_residual[iIter] = (TH1F*)file_out->Get(("h1_IC_map_residual_iter"+std::to_string(iIter)).c_str());

		if(!drawOnly){
		//loading starting IC map
		if(iIter == starting_iter+1 && iIter > 0){
			TH2F * h2_IC_map_start =  (TH2F*)file_start->Get(("h2_IC_map_iter"+std::to_string(starting_iter)).c_str());
			for(int ieta=0;ieta<nIetaTotal;ieta++){
                        	for(int iphi=0;iphi<nIphiTotal;iphi++){
					IC_map_N_1[ieta][iphi] = h2_IC_map_start->GetBinContent(ieta+1, iphi+1);
					IC_map_N[ieta][iphi] = h2_IC_map_start->GetBinContent(ieta+1, iphi+1);
				}
			}
		}
		//convergence test
		float meanDiff = 0.0;
		for(int ieta=0;ieta<nIetaTotal;ieta++){
                	for(int iphi=0;iphi<nIphiTotal;iphi++){
				meanDiff += abs(IC_map_N[ieta][iphi] - IC_map_N_1[ieta][iphi]);
				IC_map_N_1[ieta][iphi] = IC_map_N[ieta][iphi];
			}
		}
		meanDiff = meanDiff/(1.0*nIetaTotal*nIphiTotal);
		if(iIter>starting_iter+1 && meanDiff < 0.002 && iIter>0) break;//converged, threshold is 10 ps
		cout<<"calculating Timing calibration for iter "<<iIter<<endl;
		cout<<"meanDiff wrt previous iteration: "<<meanDiff<<endl;
	
		for(int ientry=0;ientry<N_entries_data; ientry++){
			if(ientry%1000000 ==0) cout<<"reading original tree entry "<<ientry<<"  out of "<<N_entries_data<<endl;
			tree_data->GetEntry(ientry);
			
			float t1 = 0, t2 = 0;
			int ieta1 = 0, iphi1 = 0;
			int ieta2 = 0, iphi2 = 0;

			if(ele1IsEB && ele1seedE<120.0){
				int seed_index = 0;
				for(int i=0;i<ele1Rechit_IEtaIX->size(); i++){
					if(ele1seedIEta == ele1Rechit_IEtaIX->at(i) && ele1seedIPhi == ele1Rechit_IPhiIY->at(i)){
						ieta1 = ele1Rechit_IEtaIX->at(i);
						iphi1 = ele1Rechit_IPhiIY->at(i);
						seed_index = i;
					}
				}
				for(int i=0;i<ele1Rechit_IEtaIX->size(); i++){
					if(ele1Rechit_E->at(i) < 10.0) continue;
					if(ele1Rechit_E->at(i) > 120.0) continue;
					bool pass_neighboring = isNeighboringXtal(ele1seedIEta, ele1seedIPhi, ele1Rechit_IEtaIX->at(i), ele1Rechit_IPhiIY->at(i));
					if(pass_neighboring){
						ieta2 = ele1Rechit_IEtaIX->at(i);
						iphi2 = ele1Rechit_IPhiIY->at(i);
						t1 = ele1Rechit_t->at(seed_index) + IC_map_N[ieta1+85][iphi1-1];
						t2 = ele1Rechit_t->at(i) + IC_map_N[ieta2+85][iphi2-1];
						IC_map_N[ieta1+85][iphi1-1] += -0.5*(t1-t2);
                                		IC_map_N[ieta2+85][iphi2-1] += 0.5*(t1-t2);
						h1_array_IC_map_residual[iIter]->Fill(ele1Rechit_t->at(seed_index) + IC_map_N_1[ieta1+85][iphi1-1] - ele1Rechit_t->at(i) - IC_map_N_1[ieta2+85][iphi2-1]);
					}			
				}
			}
					
		}	
		}

		//draw IC map after this iteration
		TH2F * h2_IC_map_this;
		if(!drawOnly) h2_IC_map_this =  new TH2F(("h2_IC_map_iter"+std::to_string(iIter)).c_str(),("h2_IC_map_iter"+std::to_string(iIter)).c_str(),171, -85.5, 85.5, 360, 0.5, 360.5);
		else h2_IC_map_this =  (TH2F*)file_out->Get(("h2_IC_map_iter"+std::to_string(iIter)).c_str());
		TH2F * h2_IC_map_diff_this = new TH2F(("h2_IC_map_diff_iter"+std::to_string(iIter)).c_str(),("h2_IC_map_diff_iter"+std::to_string(iIter)).c_str(),171, -85.5, 85.5, 360, 0.5, 360.5);

                TH2F * h2_IC_map_previous_this;// = new TH2F(("h2_IC_map_previous_iter"+std::to_string(iIter)).c_str(),("h2_IC_map_previous_iter"+std::to_string(iIter)).c_str(),171, -85.5, 85.5, 360, 0.5, 360.5);

                if(iIter>0) h2_IC_map_previous_this =  (TH2F*)file_previous->Get(("h2_IC_map_iter"+std::to_string(iIter-1)).c_str());

                h1_array_IC_map_diff[iIter] = new TH1F(("h1_IC_map_diff_iter"+std::to_string(iIter)).c_str(),("h1_IC_map_diff_iter"+std::to_string(iIter)).c_str(), 1000, -0.01, 0.5);

		for(int ieta=0;ieta<nIetaTotal;ieta++){
			for(int iphi=0;iphi<nIphiTotal;iphi++){
				if(!drawOnly){
					h2_IC_map_this->SetBinContent(ieta+1, iphi+1, IC_map_N[ieta][iphi]);
					h2_IC_map_diff_this->SetBinContent(ieta+1, iphi+1, IC_map_N[ieta][iphi]-IC_map_N_1[ieta][iphi]);
					h1_array_IC_map_diff[iIter]->Fill(abs(IC_map_N[ieta][iphi]-IC_map_N_1[ieta][iphi]));
				}
				else{
					if(iIter>0) {
                                                h2_IC_map_diff_this->SetBinContent(ieta+1, iphi+1, h2_IC_map_this->GetBinContent(ieta+1, iphi+1) - h2_IC_map_previous_this->GetBinContent(ieta+1, iphi+1));
                                                h1_array_IC_map_diff[iIter]->Fill(abs(h2_IC_map_diff_this->GetBinContent(ieta+1, iphi+1)));
                                        }
                                        else {
                                                h2_IC_map_diff_this->SetBinContent(ieta+1, iphi+1, h2_IC_map_this->GetBinContent(ieta+1, iphi+1));
                                                h1_array_IC_map_diff[iIter]->Fill(abs(h2_IC_map_this->GetBinContent(ieta+1, iphi+1)));
                                        }
				}
			}
		}
		drawTimingICMap(h2_IC_map_this, ("data_SingleElectron_iter"+std::to_string(iIter)).c_str(), ("IC timing iter "+std::to_string(iIter)+" / ns").c_str(), 1.5);
		drawTimingICMap(h2_IC_map_diff_this, ("data_SingleElectron_diff_iter"+std::to_string(iIter)).c_str(), "#Delta IC (iter "+std::to_string(iIter)+", iter "+std::to_string(iIter-1)+") / ns", 0.1);
		if(!drawOnly) {
			h2_IC_map_this->Write();
			h1_array_IC_map_residual[iIter]->Write();
		}
		//draw 1D IC diff
		draw1DICDiff(h1_array_IC_map_diff[iIter], ("data_SingleElectron_iter"+std::to_string(iIter)).c_str(), "|#Delta IC (iter "+std::to_string(iIter)+", iter "+std::to_string(iIter-1)+")| / ns");
		draw1DICDiff(h1_array_IC_map_residual[iIter], ("residual_data_SingleElectron_iter"+std::to_string(iIter)).c_str(), "| residual #Delta T | / ns");
                mean_IC_diff[iIter] = h1_array_IC_map_diff[iIter]->GetMean();
                mean_IC_residual[iIter] = h1_array_IC_map_residual[iIter]->GetMean();
                emean_IC_diff[iIter] = h1_array_IC_map_diff[iIter]->GetMeanError();	
                emean_IC_residual[iIter] = h1_array_IC_map_residual[iIter]->GetMeanError();	
		file_out->Close();
	}
	
	//draw convergence plot
	float iter_x[max_iter] = {0};
        float eiter_x[max_iter] = {0};
        for(int i=0;i<max_iter;i++) iter_x[i] = i+1;

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

        TGraphErrors *gr_IC_diff_vs_iter  =  new TGraphErrors(max_iter,iter_x, mean_IC_diff, eiter_x, emean_IC_diff);
        gr_IC_diff_vs_iter->Draw("APL");
        gr_IC_diff_vs_iter->SetMarkerColor(kBlue);
        gr_IC_diff_vs_iter->SetLineColor(kBlue);
        gr_IC_diff_vs_iter->SetLineWidth(2);
        gr_IC_diff_vs_iter->SetTitle("");
        gr_IC_diff_vs_iter->GetXaxis()->SetTitle("iteration");
        gr_IC_diff_vs_iter->GetYaxis()->SetTitle("IC precision [ns]");
        gr_IC_diff_vs_iter->GetXaxis()->SetTitleSize( axisTitleSize - 0.02 );
        gr_IC_diff_vs_iter->GetXaxis()->SetTitleOffset( axisTitleOffset  + 0.6);
	gr_IC_diff_vs_iter->GetYaxis()->SetTitleSize( axisTitleSize );
        gr_IC_diff_vs_iter->GetYaxis()->SetTitleOffset( axisTitleOffset +0.18 );
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_convergence_SingleElectron_test.pdf");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_convergence_SingleElectron_test.png");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_convergence_SingleElectron_test.C");


        TGraphErrors *gr_IC_residual_vs_iter  =  new TGraphErrors(max_iter,iter_x, mean_IC_residual, eiter_x, emean_IC_residual);
        gr_IC_residual_vs_iter->Draw("APL");
        gr_IC_residual_vs_iter->SetMarkerColor(kBlue);
        gr_IC_residual_vs_iter->SetLineColor(kBlue);
        gr_IC_residual_vs_iter->SetLineWidth(2);
        gr_IC_residual_vs_iter->SetTitle("");
        gr_IC_residual_vs_iter->GetXaxis()->SetTitle("iteration");
        gr_IC_residual_vs_iter->GetYaxis()->SetTitle("| residual #Delta T | / ns");
        gr_IC_residual_vs_iter->GetXaxis()->SetTitleSize( axisTitleSize - 0.02 );
        gr_IC_residual_vs_iter->GetXaxis()->SetTitleOffset( axisTitleOffset  + 0.6);
	gr_IC_residual_vs_iter->GetYaxis()->SetTitleSize( axisTitleSize );
        gr_IC_residual_vs_iter->GetYaxis()->SetTitleOffset( axisTitleOffset +0.18 );
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_residual_convergence_SingleElectron_test.pdf");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_residual_convergence_SingleElectron_test.png");
        myC->SaveAs(outputDir+"/ZeeTiming/IC_Timing_vs_iEta_iPhi_residual_convergence_SingleElectron_test.C");

}
