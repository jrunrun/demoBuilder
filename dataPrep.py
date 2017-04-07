import numpy as np
import pandas as pd
import datetime as dt
import random

#Read in 'Inpatient' and 'Lab Results' data
file1 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/Inpatient Data (RMTD) Extract.csv'
file2 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/HCPyDiabetesClinical_excludeNone.csv'
# Read CSV into dataframe (two files)
rawDF1 = pd.read_csv(file1, encoding='utf-16', sep='\t', error_bad_lines=False)
rawDF2 = pd.read_csv(file2)


#today's date
today=pd.to_datetime('today')
#convert FromDate to proper date format
rawDF1['Admit_tmp']=pd.to_datetime(rawDF1['From Date'])
#max date in 'Inpatient' data set
maxDate=rawDF1['Admit_tmp'].max()
#calculate days to roll forward (Today-maxDate)
daysAdd = today - maxDate
#roll forward
rawDF1['Admit']=rawDF1['Admit_tmp'] + daysAdd
#random discharge dates between 0-15 days
for index, row in rawDF1.iterrows():
    daysRandom = random.randint(0,15)
    rawDF1.loc[index,'Disch'] = rawDF1.loc[index,'Admit'] + dt.timedelta(days = daysRandom)
#clear out any discharges beyond current date
rawDF1.ix[rawDF1.Disch >= today,'Disch'] = np.NaN 

#20% ReAdmit Flag
Flags = ['Yes','No','No','No','No']
for index, row in rawDF1.iterrows():
    Flag = random.sample(Flags,1)
    rawDF1.loc[index,'RA_flg'] = Flag[0]



#uniqueDiabetes = rawDF1[rawDF1['DRG Text'].str.contains('DIABETES')==True]['DRG Text'].unique().tolist()

#create list of unique diabetes releated diagnosis by searching 'DRG Text' column
uniqueDiabetes2 = rawDF1[rawDF1['DRG Text'].str.contains('DIABETES')==True]['DRG Text'].tolist()
#create list of unique months
rawDF1['Admit_month'] = rawDF1['Admit'].dt.month
months = rawDF1['Admit_month'].unique().tolist()

#create diabetes patients @ specified % of population on monthly basis
for month in months:
    #random percent between 6% and 9%
    test_frac = random.uniform(.06,.09)
    indeces = rawDF1[rawDF1['Admit_month']==month].sample(frac = test_frac).index.tolist()
    for ind in indeces:
        rawDF1.loc[rawDF1.index==ind,'DRG Text3']=random.choice(uniqueDiabetes2)
        
        #rawDF1.loc[rawDF1.index==ind,'DRG Text2']=random.choice(uniqueDiabetes2)



#uniqueDiabetes22 = rawDF1[rawDF1['DRG Text3'].str.contains('DIABETES')==True].index.tolist() 
uniqueDiabetes22 = rawDF1[rawDF1['DRG Text3'].str.contains('DIABETES')==True]['Uniqueid'].tolist() 


#Create list of indeces filtered where Admit date is >10 days old, but <90 days
start = today - dt.timedelta(days = 90)
end = today - dt.timedelta(days = 10)
#index_tmp = rawDF1[(rawDF1['Admit']>=start)&(rawDF1['Admit']<end)].index.tolist()
ID_tmp = rawDF1[(rawDF1['Admit']>=start)&(rawDF1['Admit']<end)]['Uniqueid'].tolist()

# **DO IT BASED OFF ENCOUNTERID**
# **MAKE SURE 987 OVER LAST QTR IS NOT TOO MANY DIABETES PATIENTS**
#return set with ID's common to both <90days and DRG=diabetes
x=set(uniqueDiabetes22).intersection(ID_tmp)
#randomly select 148 OR 987 indices
x_1 = random.sample(x,987)
len(x_1)

#Give it same name for Tableau "smart" join
rawDF2['Uniqueid']=pd.Series(x_1)

#output file
rawDF1.to_csv('OutPatientMar28b.csv', index = False)
rawDF2.to_csv('LabResultsMar28b.csv', index = False)






