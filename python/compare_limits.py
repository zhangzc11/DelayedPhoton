from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import lumi
from config_noBDT import outputDir
#from config_noBDT import limits_vs_lifetime
#from config_noBDT import mass_limits_vs_lifetime
#from config_noBDT import limits_vs_mass
#from config_noBDT import lifetime_limits_vs_mass
from config_noBDT import list_limits_vs_lifetime
from config_noBDT import list_limits_vs_mass

from config_noBDT import exclusion_region_2D
from config_noBDT import grid_mass_exclusion_region_2D
from config_noBDT import grid_lambda_exclusion_region_2D
from config_noBDT import grid_lifetime_exclusion_region_2D

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
np.set_printoptions(linewidth=200)

#os.system("mkdir -p ../data")
##################exclusion region of lifetime and Lambda/mass #######################
grid_lifetime_exclusion_region_2D_inv = [a for a in reversed(grid_lifetime_exclusion_region_2D)]

N_lambda = len(grid_lambda_exclusion_region_2D)
N_lifetime = len(grid_lifetime_exclusion_region_2D_inv)
r_exp_2d_grid_smear_reweight_noBDT = np.zeros((N_lifetime, N_lambda))
r_exp_2d_grid_smear_QCDonly_noBDT = np.zeros((N_lifetime, N_lambda))
r_exp_2d_grid_nosmear_reweight_noBDT = np.zeros((N_lifetime, N_lambda))
r_exp_2d_grid_smear_reweight_withBDT = np.zeros((N_lifetime, N_lambda))

print "lifetime grid: "
print grid_lifetime_exclusion_region_2D_inv
print "mass grid: "
print grid_mass_exclusion_region_2D
print "lambda grid: "
print grid_lambda_exclusion_region_2D

for limit_2D in exclusion_region_2D:
	file_limit = TFile("../fit_results_smear_reweight/datacards_3J_noBDT/higgsCombine"+limit_2D[0]+".Asymptotic.mH120.root")
	limits = []
	limitTree = file_limit.Get("limit")
	for entry in limitTree:
		limits.append(entry.limit)
	#print limits
	ind_lambda = -1
	ind_lifetime = -1
	for i in range(0, N_lambda):
		if grid_lambda_exclusion_region_2D[i] == limit_2D[1]:
			ind_lambda = i
	
	for i in range(0, N_lifetime):
		if grid_lifetime_exclusion_region_2D_inv[i] == limit_2D[3]:
			ind_lifetime = i
	if len(limits) == 6 and ind_lambda > -1 and ind_lifetime > -1:
		r_exp_2d_grid_smear_reweight_noBDT[ind_lifetime][ind_lambda] = limits[2]


for limit_2D in exclusion_region_2D:
	file_limit = TFile("../fit_results_smear_QCDonly/datacards_3J_noBDT/higgsCombine"+limit_2D[0]+".Asymptotic.mH120.root")
	limits = []
	limitTree = file_limit.Get("limit")
	for entry in limitTree:
		limits.append(entry.limit)
	#print limits
	ind_lambda = -1
	ind_lifetime = -1
	for i in range(0, N_lambda):
		if grid_lambda_exclusion_region_2D[i] == limit_2D[1]:
			ind_lambda = i
	
	for i in range(0, N_lifetime):
		if grid_lifetime_exclusion_region_2D_inv[i] == limit_2D[3]:
			ind_lifetime = i
	if len(limits) == 6 and ind_lambda > -1 and ind_lifetime > -1:
		r_exp_2d_grid_smear_QCDonly_noBDT[ind_lifetime][ind_lambda] = limits[2]


for limit_2D in exclusion_region_2D:
	file_limit = TFile("../fit_results_nosmear_reweight/datacards_3J_noBDT/higgsCombine"+limit_2D[0]+".Asymptotic.mH120.root")
	limits = []
	limitTree = file_limit.Get("limit")
	for entry in limitTree:
		limits.append(entry.limit)
	#print limits
	ind_lambda = -1
	ind_lifetime = -1
	for i in range(0, N_lambda):
		if grid_lambda_exclusion_region_2D[i] == limit_2D[1]:
			ind_lambda = i
	
	for i in range(0, N_lifetime):
		if grid_lifetime_exclusion_region_2D_inv[i] == limit_2D[3]:
			ind_lifetime = i
	if len(limits) == 6 and ind_lambda > -1 and ind_lifetime > -1:
		r_exp_2d_grid_nosmear_reweight_noBDT[ind_lifetime][ind_lambda] = limits[2]



for limit_2D in exclusion_region_2D:
	file_limit = TFile("../fit_results_smear_reweight/datacards_3J_withBDT/higgsCombine"+limit_2D[0]+".Asymptotic.mH120.root")
	limits = []
	limitTree = file_limit.Get("limit")
	for entry in limitTree:
		limits.append(entry.limit)
	#print limits
	ind_lambda = -1
	ind_lifetime = -1
	for i in range(0, N_lambda):
		if grid_lambda_exclusion_region_2D[i] == limit_2D[1]:
			ind_lambda = i
	
	for i in range(0, N_lifetime):
		if grid_lifetime_exclusion_region_2D_inv[i] == limit_2D[3]:
			ind_lifetime = i
	if len(limits) == 6 and ind_lambda > -1 and ind_lifetime > -1:
		r_exp_2d_grid_smear_reweight_withBDT[ind_lifetime][ind_lambda] = limits[2]


print "value of the 2D r grid (exp) provided from samples: smear_reweight_noBDT"
print r_exp_2d_grid_smear_reweight_noBDT


print "value of the 2D r grid (exp) provided from samples: smear_QCDonly_noBDT"
print r_exp_2d_grid_smear_QCDonly_noBDT

print "value of the 2D r grid (exp) provided from samples: smear_reweight_withBDT"
print r_exp_2d_grid_smear_reweight_withBDT

print "value of the 2D r grid (exp) provided from samples: nosmear_reweight_noBDT"
print r_exp_2d_grid_nosmear_reweight_noBDT

print "table for noBDT (withBDT) comparision:"
for i in range(1, N_lifetime):
	if grid_lifetime_exclusion_region_2D_inv[i] < 0.9:
		print " %.2f" % grid_lifetime_exclusion_region_2D_inv[i],
	else:
		print " %.0f" % grid_lifetime_exclusion_region_2D_inv[i],

	for j in range(1, N_lambda):
		if r_exp_2d_grid_smear_reweight_noBDT[i][j] > 0.00001 and r_exp_2d_grid_smear_reweight_withBDT[i][j] > 0.00001:
			print "& %.2f" % r_exp_2d_grid_smear_reweight_noBDT[i][j] + "(%.2f" % r_exp_2d_grid_smear_reweight_withBDT[i][j] +") ",
		else:
			print "& -- ",
	print "\\\\"

print "table for smear (nosmear) comparision:"
for i in range(1, N_lifetime):
	if grid_lifetime_exclusion_region_2D_inv[i] < 0.9:
		print " %.2f" % grid_lifetime_exclusion_region_2D_inv[i],
	else:
		print " %.0f" % grid_lifetime_exclusion_region_2D_inv[i],

	for j in range(1, N_lambda):
		if r_exp_2d_grid_smear_reweight_noBDT[i][j] > 0.00001 and r_exp_2d_grid_nosmear_reweight_noBDT[i][j] > 0.00001:
			print "& %.2f" % r_exp_2d_grid_smear_reweight_noBDT[i][j] + "(%.2f" % r_exp_2d_grid_nosmear_reweight_noBDT[i][j] +") ",
		else:
			print "& -- ",
	print "\\\\"


print "table for mixture (QCDonly) comparision:"
for i in range(1, N_lifetime):
	if grid_lifetime_exclusion_region_2D_inv[i] < 0.9:
		print " %.2f" % grid_lifetime_exclusion_region_2D_inv[i],
	else:
		print " %.0f" % grid_lifetime_exclusion_region_2D_inv[i],

	for j in range(1, N_lambda):
		if r_exp_2d_grid_smear_reweight_noBDT[i][j] > 0.00001 and r_exp_2d_grid_smear_QCDonly_noBDT[i][j] > 0.00001:
			print "& %.2f" % r_exp_2d_grid_smear_reweight_noBDT[i][j] + "(%.2f" % r_exp_2d_grid_smear_QCDonly_noBDT[i][j] +") ",
		else:
			print "& -- ",
	print "\\\\"


