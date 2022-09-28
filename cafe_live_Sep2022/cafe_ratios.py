import numpy as np
import sys


# CaFe Sanity Check Ratios

# user can pass command line argument of target to use for double ratio with C12
target = sys.argv[1]

# MF runs (Round 1)
# LD2 : 16973, 16975
# C12 : 16977
# Ca48 : 16978, 16979  (H-contaminated)
# Ca40 : 16980
# Fe54 : 16981, 16982
# Be9 : 16983
# B10 : 16984
# B11 : 16986, 16991

# MF runs (Round 2)
# Ca48 : 17093, 17094, 17096
# Ca40 : 17097
# C12  : 17098
# Be9  : 17099, 17100
# B10  : 17101
# B11  : 17102


# Target areal densities g/cm^2 (from D. Meekins email)
B4C10_sig = 0.576
B4C11_sig = 0.633
Ca48_sig = 1.051
Ca40_sig = 0.785
Fe54_sig = 0.367
Be9_sig = 0.986
C12_sig = 0.574
d2_sig = 1.67

# nuclear transparencies
C12_T = 0.56
Fe54_T = 0.4
Ca40_T = 0.4
Ca48_T = 0.4
d2_T = 1.
Be9_T = 0.6
B10_T = 0.6
B11_T = 0.6


# --- MF -to -MF Symmetric Nuclei Ratios Should be 1
# Nucleus_A / C12  Normalized by charge and nucleon number
# e.g.  (Ca40 / (Q*40*sig*T)) / (C12 / (Q*12*sig*T) )
# ratios normalized to charge, # of nucleons, areal density and transparency

# Round 1 MF data
d2_MF = 427781.596 / 73.446
C12_MF = 57911.4 / 88.807
Ca40_MF = 49564. / 94.441
Fe54_MF =  67082.8 / 285.786
Be9_MF = 112609.401 / 86.976
B4C_10_MF = 60350.6 / 76.157
B4C_11_MF = 164768.6 / 232.885

# Round 1 MF data uncertainty
d2_MF_err = np.sqrt(427781.596) / 73.446
C12_MF_err = np.sqrt(57911.4) / 88.807
Ca40_MF_err = np.sqrt(49564.) / 94.441
Fe54_MF_err =  np.sqrt(67082.8) / 285.786
Be9_MF_err = np.sqrt(112609.401) / 86.976
B4C_10_MF_err = np.sqrt(60350.6) / 76.157
B4C_11_MF_err = np.sqrt(164768.6) / 232.885

targetfac_B4C10_to_C12 = 0.2517
targetfac_B4C11_to_C12 = 0.2594

# b4c subtraction
B10_MF = B4C_10_MF  - (C12_MF * targetfac_B4C10_to_C12)
B11_MF = B4C_11_MF  - (C12_MF * targetfac_B4C11_to_C12)

# b4c subtraction uncertainty
B10_MF_err = np.sqrt( B4C_10_MF_err**2  + (C12_MF_err**2 * targetfac_B4C10_to_C12) )
B11_MF_err = np.sqrt( B4C_11_MF_err**2  + (C12_MF_err**2 * targetfac_B4C11_to_C12) )


# Round 2 MF data
Ca48_MF_round2 = 78306.6 / 161.343
Ca40_MF_round2 = 25106.8 / 54.651
C12_MF_round2 = 20001.6 / 33.641
Be9_MF_round2 = 42729.6 / 40.132
B4C_10_MF_round2 = 29890.4 / 44.24
B4C_11_MF_round2 = 18737.2 / 30.322

# Round 2 MF data uncertainty
Ca48_MF_round2_err = np.sqrt(78306.6) / 161.343
Ca40_MF_round2_err = np.sqrt(25106.8) / 54.651
C12_MF_round2_err = np.sqrt(20001.6) / 33.641
Be9_MF_round2_err = np.sqrt(42729.6) / 40.132
B4C_10_MF_round2_err = np.sqrt(29890.4) / 44.24
B4C_11_MF_round2_err = np.sqrt(18737.2) / 30.322

# b4c subtraction
B10_MF_round2 = B4C_10_MF_round2  - (C12_MF * targetfac_B4C10_to_C12)
B11_MF_round2 = B4C_11_MF_round2  - (C12_MF * targetfac_B4C11_to_C12)

# b4c subtraction uncertainty
B10_MF_round2_err = np.sqrt( B4C_10_MF_round2_err**2  + (C12_MF_err**2 * targetfac_B4C10_to_C12) )
B11_MF_round2_err = np.sqrt( B4C_11_MF_round2_err**2  + (C12_MF_err**2 * targetfac_B4C11_to_C12) )


# SRC total counts / mC
Ca40_SRC = 8247.6 / 2242.281
Ca48_SRC = 9926. / 2550.619
Fe54_SRC = 3234.2 / 1630.213  #97.68 % composition of Fe54
C12_SRC = 5060.6 / 1174.824
Be9_SRC = 1860. / 328.183
B10_SRC = 1948.8 / 457.078


# SRC total counts / mC uncertainty
Ca40_SRC_err = np.sqrt(8247.6) / 2242.281
Ca48_SRC_err = np.sqrt(9926.) / 2550.619
Fe54_SRC_err = np.sqrt(3234.2) / 1630.213  #97.68 % composition of Fe54
C12_SRC_err  = np.sqrt(5060.6) / 1174.824
Be9_SRC_err = np.sqrt(1860.) / 328.183
B10_SRC_err = np.sqrt(1948.8) / 457.078

# Calculate double ratioa:  ( A_SRC / A_MF ) / ( C_SRC / C_MF ) | T, areal density and T should cancel out
#double_R_Ca40 = (Ca40_SRC / Ca40_MF) / (C12_SRC / C12_MF)
#double_R_Ca48 = (Ca48_SRC / Ca48_MF_round2) / (C12_SRC / C12_MF)
#double_R_Fe54 = (Fe54_SRC / Fe54_MF) / (C12_SRC / C12_MF)

#Calculate double ratios and errors of double ratios
# R = A / B,   where A = a/b,   B = c/d
# dR2 =  (dR/dA)^2 dA^2  + (dR/dB)^2 dB^2,   dA^2 = (dA/da)^2 da^2 + (dA/db)^2 db^2, dB^2 = (dB/dc)^2 dc^2 + (dB/dd)^2 dd^2, 
# dR/dA = 1/B, dR/dB = -A/B^2,  dA/da = 1/b, dA/db = -a/b^2,  dB/dc = 1/d, dB/dd = -c/d^2

#numerator of super ratio (user selects target)
if(target=="Ca40"):
    a = Ca40_SRC
    b = Ca40_MF
    a_err =  Ca40_SRC_err
    b_err =  Ca40_MF_err

elif(target=="Ca48"):
    a = Ca48_SRC
    b = Ca48_MF_round2
    a_err =  Ca48_SRC_err
    b_err =  Ca48_MF_round2_err

elif(target=="Fe54"):
    a = Fe54_SRC
    b = Fe54_MF
    a_err =  Fe54_SRC_err
    b_err =  Fe54_MF_err

elif(target=="Be9"):
    a = Be9_SRC
    b = Be9_MF
    a_err =  Be9_SRC_err
    b_err =  Be9_MF_err

elif(target=="B10"):
    a = B10_SRC
    b = B10_MF
    a_err =  B10_SRC_err
    b_err =  B10_MF_err    
    
# denominator of super ratio (will be C12)
c = C12_SRC
d = C12_MF
c_err =  C12_SRC_err
d_err =  C12_MF_err


A = a / b
B = c / d

# super ratio
R = A / B

# partial derivatives
dR_dA = 1/B
dR_dB = -A/B**2
dA_da = 1/b
dA_db = -a/b**2
dB_dc = 1/d
dB_dd = -c/d**2

dA2 = (dA_da)**2 * a_err**2 + (dA_db)**2 * b_err**2
dB2 = (dB_dc)**2 * c_err**2 + (dB_dd)**2 * d_err**2

dR2 =  (dR_dA)**2 * dA2  + (dR_dB)**2 * dB2
dR = np.sqrt(dR2)

txt = "R = ({tgt}_SRC / {tgt}_MF ) / (C12_SRC / C12_MF) = {ratio} +/- {ratio_err}".format(tgt=target, ratio = R, ratio_err = dR)
print(txt)


'''
double_R_Ca48to40 = (Ca48_SRC / (48 * Ca48_sig) ) / (Ca40_SRC / (40 * Ca40_sig) )


print('double_R_Ca40 ---> ', double_R_Ca40)
print('double_R_Ca48 ---> ', double_R_Ca48)
print('double_R_Fe54 ---> ', double_R_Fe54)
print('double_R_Ca48to40 ---> ', double_R_Ca48to40)


R_Ca40_v1 = (Ca40_MF) / (C12_MF)
R_Ca40_v2 = (Ca40_MF / (40.) ) / (C12_MF / (12.))
R_Ca40_v3 = (Ca40_MF / (40.*Ca40_sig)) / (C12_MF / (12.*C12_sig))
R_Ca40_v4 = (Ca40_MF / (Ca40_sig*Ca40_T)) / (C12_MF / (C12_sig*C12_T))

print('R_Ca40_v1 --> ', R_Ca40_v1)
print('R_Ca40_v2 --> ', R_Ca40_v2)
print('R_Ca40_v3 --> ', R_Ca40_v3)
print('R_Ca40_v4 --> ', R_Ca40_v4)

R_Ca40_v1_r2 = (Ca40_MF_round2) / (C12_MF_round2)
R_Ca40_v2_r2 = (Ca40_MF_round2 / (40.) ) / (C12_MF_round2 / (12.))
R_Ca40_v3_r2 = (Ca40_MF_round2 / (40.*Ca40_sig)) / (C12_MF_round2 / (12.*C12_sig))
R_Ca40_v4_r2 = (Ca40_MF_round2 / (Ca40_sig*Ca40_T)) / (C12_MF_round2 / (C12_sig*C12_T))


print('R_Ca40_v1 --> ', R_Ca40_v1_r2)
print('R_Ca40_v2 --> ', R_Ca40_v2_r2)
print('R_Ca40_v3 --> ', R_Ca40_v3_r2)
print('R_Ca40_v4 --> ', R_Ca40_v4_r2)


'''
