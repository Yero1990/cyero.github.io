#! /usr/bin/python

# Stephen JD Kay - 19/08/21 - University of Regina
# Script to grab info from a report file, for use in the run list shell script
# This script scans every line of the report file to find the correct info

# C. Yero - May 26, 2022
# Modified to meet the needs of CaFe 2022 Experiment.
# The modified code creates a csv file and writes the
# pertinent information from the cafe output report to
# a .csv file on a run-by-run basis

   

# Import relevant packages
import sys, math, os, subprocess, csv
from datetime import datetime
sys.path.insert(0, 'python/')

#if len(sys.argv)-1!=3:
#    print("Invalid number of arguments. \n "
#    "e.g., python reportfile.py <path/to/cafe_report_run.txt> <entry_type> \n")
#    sys.exit(1)
    
# user input
ANATYPE = sys.argv[1]
RUNNUM = sys.argv[2]
EVTNUM = sys.argv[3]

# construct generic report output file from the user input (whihc should have been generated)
cafe_report_path = "CAFE_OUTPUT/REPORT/cafe_%s_report_%s_%s.txt" % (ANATYPE, RUNNUM, EVTNUM)

#bcm_type = sys.argv[2]         # <entry_type> = "bcm_type", passed from run_cafe_prod.sh

cafe_report = open(cafe_report_path)


# general run info
run_num=0
start_of_run=0
end_of_run=0
kin_type=0
evt_num=0
beam_e=0
tgt_name=0
tgt_mass=0
hms_p=0
hms_angle=0
shms_p=0
shms_angle=0
beam_on_target=0
bcm_thrs=0
bcm_current=0
bcm_charge=0

# good events counts
heep_singles      = 0
heep_singles_rate =-1
heep_real         = 0
heep_real_rate    =-1
MF_real           = 0
MF_real_rate      =-1
SRC_real          = 0
SRC_real_rate     =-1

# trigger info (only enabled triggers, i.e PS# != -1 will be written to kin file)
PS1=-1    # SHMS 3/4
PS2=-1    # SHMS EL-REAL
PS3=-1    # HMS 3/4
PS5=-1    # SHMS EL-REAL x HMS 3/4 ( this needs to be implemented after pionLT run ends in August 2022 )
PS6=-1    # HMS 3/4 x SHMS 3/4

T1_scaler=0
T2_scaler=0
T3_scaler=0
T5_scaler=0
T6_scaler=0

T1_scaler_rate=-1
T2_scaler_rate=-1
T3_scaler_rate=-1
T5_scaler_rate=-1
T6_scaler_rate=-1

T1_accp=0
T2_accp=0
T3_accp=0
T5_accp=0
T6_accp=0

T1_accp_rate=-1
T2_accp_rate=-1
T3_accp_rate=-1
T5_accp_rate=-1
T6_accp_rate=-1

# tracking efficiency
hms_trk_eff=-1
shms_trk_eff=-1

# daq live time
T1_cpuLT=-1
T1_tLT=-1

T2_cpuLT=-1
T2_tLT=-1

T3_cpuLT=-1
T3_tLT=-1

T5_cpuLT=-1
T5_tLT=-1

T6_cpuLT=-1
T6_tLT=-1

TestVar = 0 # Counter to check the right number of variables have been set, 
for line in cafe_report:
    if (line[0]=="#"): continue;

    # general run information
    if "run_number" in line :
        run_num = int((line.split(":")[1]).strip())
        TestVar+=1
        # print(run_num)
    if "kin_type" in line :
        kin_type = (line.split(":")[1]).strip()
        TestVar+=1
        # print(kin_type)
    if "start_of_run" in line :
        start_of_run = (line.split("=")[1]).strip()
        #convert to datetime object
        start_of_run = datetime.strptime(start_of_run, '%Y-%m-%d %H:%M:%S')
        TestVar+=1
        # print(start_of_run)
    if "end_of_run" in line :
        end_of_run = (line.split("=")[1]).strip()
        #convert to datetime object
        end_of_run = datetime.strptime(end_of_run, '%Y-%m-%d %H:%M:%S') 
        TestVar+=1
        # print(end_of_run)
    if "events_replayed" in line :
        evt_num = int((line.split(":")[1]).strip())
        TestVar+=1
        # print(evt_num)
    if "beam_energy" in line :
        beam_e = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(beam_e)
    if "target_name:" in line :
        tgt_name = (line.split(":")[1]).strip()
        TestVar+=1
        # print(tgt_name)
    if "target_amu" in line :
        tgt_mass = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(tgt_mass)
    if "hms_h_momentum" in line :
        hms_p = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(hms_p)
    if "hms_h_angle" in line :
        hms_angle = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(hms_angle)
    if "shms_e_momentum" in line :
        shms_p = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(shms_p)
    if "shms_e_angle" in line :
        shms_angle = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(shms_angle)
    if "beam_on_target" in line :
        beam_on_target = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(beam_on_target_time)
    if "_Current_Threshold" in line :
        bcm_thrs = (line.split(":")[1]).strip()
        TestVar+=1
        # print(bcm_thrs)
    if "_Average_Current" in line :
        bcm_current = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(bcm_current)
    if "_Charge" in line :
        bcm_charge = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(bcm_charge)
        
    # good elastic, MF or SRC counts/rates
    if "heep_total_singles_counts" in line :
        heep_singles = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(heep_singles)
    if "heep_total_singles_rate" in line :
        heep_singles_rate = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(heep_singles_rate)
    if "heep_real_counts" in line :
        heep_real = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(heep_real)
    if "heep_real_rate" in line :
        heep_real_rate = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(heep_real_rate)
    if "MF_real_counts" in line :
        MF_real = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(MF_real)
    if "MF_real_rate" in line :
        MF_real_rate = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(MF_real_rate)
    if "SRC_real_counts" in line :
        SRC_real = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(SRC_real)
    if "SRC_real_rate" in line :
        SRC_real_rate = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(SRC_real_rate)

    # trigger info
    if "Ps1_factor" in line :
        PS1 = float(line.split(":")[1].strip())
        TestVar+=1
        # print(PS1)
    if "Ps2_factor" in line :
        PS2 = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(PS2)
    if "Ps3_factor" in line :
        PS3 = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(PS3)
    if "Ps5_factor" in line :
        PS5 = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(PS5)
    if "Ps6_factor" in line :
        PS6 = float((line.split(":")[1]).strip())
        TestVar+=1
        # print(PS6)
        
    # scaler counts
    if "T1_scaler" in line :
        T1_scaler = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T1_scaler)
    if "T2_scaler" in line :
        T2_scaler = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T2_scaler)
    if "T3_scaler" in line :
        T3_scaler = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T3_scaler)
    if "T5_scaler" in line :
        T5_scaler = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T5_scaler)
    if "T6_scaler" in line :
        T6_scaler = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T6_scaler)
        
    # scaler rates (same line, but get str within '[,]' brackets
    if "T1_scaler" in line :
        T1_scaler_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T1_scaler_rate)
    if "T2_scaler" in line :
        T2_scaler_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T2_scaler_rate)
    if "T3_scaler" in line :
        T3_scaler_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T3_scaler_rate)
    if "T5_scaler" in line :
        T5_scaler_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T5_scaler_rate)
    if "T6_scaler" in line :
        T6_scaler_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T6_scaler_rate)

    # accepted counts
    if "T1_accepted" in line :
        T1_accp = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T1_accp)
    if "T2_accepted" in line :
        T2_accp = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T2_accp)
    if "T3_accepted" in line :
        T3_accp = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T3_accp)
    if "T5_accepted" in line :
        T5_accp = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T5_accp)
    if "T6_accepted" in line :
        T6_accp = float((line.split(":")[1]).split("[")[0].strip())
        TestVar+=1
        # print(T6_accp)
        
    # accepted rates (same line, but get str within '[,]' brackets
    if "T1_accepted" in line :
        T1_accp_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T1_accp_rate)
    if "T2_accepted" in line :
        T2_accp_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T2_accp_rate)
    if "T3_accepted" in line :
        T3_accp_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T3_accp_rate)
    if "T5_accepted" in line :
        T5_accp_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T5_accp_rate)
    if "T6_accepted" in line :
        T6_accp_rate = float((line.split("[")[1]).split("kHz")[0].strip())
        TestVar+=1
        # print(T6_accp_rate)

    # tracking efficiency
    if "hms_had_track_eff" in line :
        hms_trk_eff = float(line.split(":")[1].split("+")[0].strip())
        # print(hms_trk_eff)
    if "shms_elec_track_eff" in line :
        shms_trk_eff = float(line.split(":")[1].split("+")[0].strip())
        # print(shms_trk_eff)
        
    # live times
    if "T1_cpuLT" in line :
        T1_cpuLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T1_cpuLT)
    if "T1_tLT" in line :
        T1_tLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T1_tLT)

    if "T2_cpuLT" in line :
        T2_cpuLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T2_cpuLT)
    if "T2_tLT" in line :
        T2_tLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T2_tLT)

    if "T3_cpuLT" in line :
        T3_cpuLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T3_cpuLT)
    if "T3_tLT" in line :
        T3_tLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T3_tLT)

    if "T5_cpuLT" in line :
        T5_cpuLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T5_cpuLT)
    if "T5_tLT" in line :
        T5_tLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T5_tLT)

    if "T6_cpuLT" in line :
        T6_cpuLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T6_cpuLT)
    if "T6_tLT" in line :
        T6_tLT = float(line.split(":")[1].split("+")[0].strip())
        # print(T6_tLT)


#  run list was separated into sub-categories for ease of use and more flexibility if things need to be changed


# general run entry list
header_1     = ['run\nnumber', 'start_run', 'end_run', 'kin\nstudy', 'beam_on_target\n[sec]', 'evts\nreplayed', 'beam\nenergy\n[GeV]', 'target', 'target\nmass\n[amu]', 'HMS_P\n[GeV/c]', 'HMS_Angle\n[deg]', 'SHMS_P\n[GeV/c]', 'SHMS_Angle\n[deg]', 'BCM4A\nthrs\n[uA]', 'BCM4A\ncurrent\n[uA]', 'BCM4A\ncharge\n[mC]' ]
gen_run_info = "%i,            %s,           %s,           %s,         %.3f,          %i,       %.4f,     %s,        %.6f,      %.4f,   %.3f,       %.4f,    %.3f,        %s,        %.3f,         %.3f       " % \
               (run_num, start_of_run,  end_of_run,  kin_type, beam_on_target, evt_num, beam_e,  tgt_name, tgt_mass,  hms_p, hms_angle, shms_p, shms_angle, bcm_thrs, bcm_current, bcm_charge)


# trigger info
# should probably define what these are more specifically later on . . . e.g., PS1 : SHMS 3/4 . . .
header_2   = ['PS1', 'PS2', 'PS3', 'PS5', 'PS6', 'T1\nscaler_rates\n[kHz]', 'T2\nscaler_nrates\n[kHz]','T3\nscaler_rates\n[kHz]','T5\nscaler_rates\n[kHz]','T6\nscaler_rates\n[kHz]', 'T1\naccp_rates\n[kHz]','T2\naccp_rates\n[kHz]','T3\naccp_rates\n[kHz]','T5\naccp_rates\n[kHz]','T6\naccp_rates\n[kHz]' ]
trig_info = "%i   %i   %i   %i   %i   %.3f            %.3f            %.3f            %.3f            %.3f            %.3f          %.3f          %.3f           %.3f           %.3f                        "  % \
            (PS1, PS2, PS3, PS5, PS6, T1_scaler_rate, T2_scaler_rate, T3_scaler_rate, T5_scaler_rate, T6_scaler_rate, T1_accp_rate, T2_accp_rate, T3_accp_rate,  T5_accp_rate,  T6_accp_rate                          )

# live time and trk_eff info
header_3   = ['T1_tLT', 'T2_tLT','T3_tLT','T5_tLT','T6_tLT','HMS\nTrkEff', 'SHMS\nTrkEff']
efficiency_info = "%.3f    %.3f    %.3f    %.3f    %.3f    %.3f         %.3f        " % \
           (T1_tLT, T2_tLT, T3_tLT, T5_tLT, T6_tLT, hms_trk_eff, shms_trk_eff )


# good event count info
header_4   = ['heep_singles\ncounts', 'heep_singles\nrates [Hz]', 'heep_coin\ncounts', 'heep_coin\nrates [Hz]', 'MF_real\ncounts', 'MF_real\nrates [Hz]', 'SRC_real\ncounts', 'SRC_real\nrates [Hz]', 'Comments']
good_evt_info = "%.2f           %.3f               %.2f       %.3f            %.2f     %.3f          %.2f      %.3f    " % \
                (heep_singles,  heep_singles_rate, heep_real, heep_real_rate, MF_real, MF_real_rate, SRC_real, SRC_real_rate )


 # combine headers
total_header = header_1 + header_2 + header_3 + header_4


# read user comment (raw_input is required for python 2.7, else use input())
#comment = input("Please enter any relevant comments this run: \n")
comment=""
comment = raw_input("Please enter comments for run %s \n (NOTE: all special chars/blanks will be replaced by '_' \n Press \'Enter\' to ommit comment): \n >> " %(RUNNUM))

# clean user comment out of weird characters or spaces and replace them with '_'
specialChars = "!@#$%^&*()+={[]}|\:;,<>?/\" "

for specialChar in specialChars:
    comment = comment.replace(specialChar, '_')


# convert data strings to a list
gen_run_info_list    = gen_run_info.split(',')
trig_info_list       = trig_info.split()
efficiency_info_list = efficiency_info.split()
good_evt_info_list   = good_evt_info.split()

# combine lists
total_list = gen_run_info_list + trig_info_list + efficiency_info_list + good_evt_info_list

# append user comments to list
total_list.append(comment)

# close report file
cafe_report.close()

# --- create / append data to cafe runlist .csv file ----------

fname_path='UTILS_CAFE/runlist/cafe-2022_runlist.csv'

os.system('mkdir -p UTILS_CAFE/runlist') 
#os.system('mkdir -p /home/cdaq/cyero/backup_runlist')

# check if run list exists, else create it and add a header
if os.path.isfile(fname_path):
    print (fname_path," exists !")

    with open(fname_path, "a") as f:
        wr = csv.writer(f,delimiter=",")
        wr.writerow(total_list)
        
else:
    print (fname_path," does NOT exist ! \n Will create it and add a header")
    
    with open(fname_path, "a") as f:
        wr = csv.writer(f,delimiter=",")
        wr.writerow(total_header)
        wr.writerow(total_list)
        
f.close()

fname_path_bkp='/home/cdaq/cyero/backup_runlist/cafe-2022_runlist_backup.csv'

os.system('cp %s %s' % (fname_path, fname_path_bkp))
