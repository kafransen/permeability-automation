
import pandas as pd
import scipy.stats as st
import numpy as np

def criteria_fn(file_name):
    cell_=pd.read_csv("/Users/kfransen/PycharmProjects/pythonProject/"+file_name+".csv",header=0)
    #drop any rows with NaN in them
    cell=cell_.dropna(axis=0)
    #print(cell.columns)
    #times=[*range(2,(len(cell.index)+1)*2,2)] #this is legacy from before fixing time point values
    time_edit=cell.iloc[:, 0:1]
    #print(time_edit)
    edit=cell
    #use this to track whether the criteria have been met for each scale
    crits=[0]*16
    shutoff=0
    #check that we do indeed have enough datapoints
    if len(cell.index)<501:
        return(['too small N',crits])
    #calculate over all of the different scales
    for k in range(1,17):
        crit1=0
        crit2=0
        crit3=0
        #get number of datapoints collected
        i=len(cell.index)
        #use last collected 500 datapoints
        a = edit.iloc[(i)-500:i,2*(k-1)+1:2*(k-1)+2].to_numpy()
        #The numbers in the file run as every 4 min
        #so when the timepoints are correct in the file use above, when not edit list earlier
        #print(time_edit)
        b=(time_edit.iloc[(i)-500:i,:])
        #b = edit.iloc[:i,2*(k-1):2*(k-1)+1].to_numpy()
        a = np.reshape(a,-1)
        b = np.reshape(b,-1)
        output=st.linregress(b, a)
        #output has attributes output.slope, output.stderr, and more from scipy.stats

        #for other conditions, make sure there are enough datapoints
        if i>2000:
            #use the last 2000 datapoints to calculate values
            a = edit.iloc[(i)-2000:i,2*(k-1)+1:2*(k-1)+2].to_numpy()
            b=(time_edit.iloc[(i)-2000:i])
            #reshaping is to meet dimension constraints of stats package
            a = np.reshape(a,-1)
            b = np.reshape(b,-1)
            output2=st.linregress(b, a)
            #calculations to meet 1000 datapoint requirements
            a = edit.iloc[(i)-1000:i,2*(k-1)+1:2*(k-1)+2].to_numpy()
            b=(time_edit.iloc[(i)-1000:i])
            a = np.reshape(a,-1)
            b = np.reshape(b,-1)
            output1=st.linregress(b, a)
        #criteria 1- abs error les than 0.01 for equilibration
        if output.stderr<0.01:
            crit1=1
        #criteria 2- rel error or abs+rel+slope0
        #relative error less than 3%
        if abs(output.stderr/output.slope)<0.03:
            crit2=1
        #OR relative error less than 10%, abs. error less than 0.005, and slope close to 0
        elif i>2000:
            if abs(output2.stderr/output2.slope)<0.1 and output1.stderr<0.005 and abs(output2.slope)<0.05:
                crit2=1
        #check that we are within the min to max number of datapoint collected range
        #minpt=48*60/2
        #maxpt=7*24*60/2
        global minpt, maxpt
        if i>minpt: #minimum number of samplings
            crit3=1
        if crit1==1 and crit2==1 and crit3==1:
            crits[k-1]=1
    #indicate when run should be stopped
    if len(cell.index)>=maxpt or all(ele == 1 for ele in crits):
        shutoff=1
    return ([crits,shutoff])


print(criteria_fn('with_watchdogandmac_edits_1'))