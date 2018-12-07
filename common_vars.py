SELmtr_ch_data = []
ch_data = []
ch_ids = []
vssi_data = []
ldp_report_data = []
 
wh3_del = []
wh3_rec = []
qh3_del = []
qh3_rec = []

startDate = "2016/01/01"
endDate = "2018/11/15"

base_api = "http://localhost:5630"

ldp_report_file = "ldp_report.csv"

mtr_list = ["LEW_735","Zocholl_M_735"] #LEW_735 #Zocholl_M_735

ldlist1 =  ["WH3_DEL","WH3_REC","QH3_DEL","QH3_REC","QD3_DEL","QD3_REC","WD3_DEL","WD3_REC"]
ldlist2 =  ["VA","VB","VC","IA","IB","IC","IN"] 
ldlist3 =  ["VA","VB","VC","PFTA","PFTB","PFTC,FREQ"]  
ldlist4 =  ["VA","VB","VC","IA","IB","IC","IN","PFT3","FREQ"]  
ldlist5 =  ["PST_10MIN_VA","PST_10MIN_VB","PST_10MIN_VC","PLT_VA","PLT_VB,PLT_VC"]
ldlist6 =  ["PST_1MIN_VA","PST_1MIN_VB","PST_1MIN_VC","PLT_VA","PLT_VB","PLT_VC"]
ldlist7 =  ["CFG0203","CFG0204"]
ldlist8 =  ["WA","WB","WC","W3","QA","QB","QC","Q3","THDVA","THDVB","THDVC","THDIA","THDIB","THDIC,THDIN"]
ldlist9 =  ["V_IMB","I_IMB","V1_MAG","V1_ANG","I1_MAG","I1_ANG"]
ldlist10 = ["VA","VB","VC","V_AVE","V0_IMB","V_IMB","IA","IB","IC","I_AVE","I0_IMB","I_IMB","I1_MAG","3I0_MAG","3I2_MAG"]
ldlist11 = ["HRMM3_IA","HRMA3_IA","HRMM3_IB","HRMA3_IB","HRMM3_IC","HRMA3_IC","HRMM3_VA","HRMA3_VA","HRMM3_VB","HRMA3_VB","HRMM3_VC","HRMA3_VC","HRMM7_IA","HRMM7_VA","HRMA7_IA,HRMA7_VA"]
ldlist12 = ["HRMM5_IA","HRMA5_IA","HRMM5_IB","HRMA5_IB","HRMM5_IC","HRMA5_IC","HRMM5_VA","HRMA5_VA","HRMM5_VB","HRMA5_VB","HRMM5_VC","HRMA5_VC","HRMM7_IB","HRMA7_IB","HRMM7_VB","HRMA7_VB"]
