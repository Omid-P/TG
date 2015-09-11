# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 14:46:16 2015

@author: APAX
"""

from __future__ import division

def aprslist(Amount, Months):
    k=0.00001
    lsmpay=list()
    lsapr=list()
    while k<0.06:
        M=Amount*(k/(1-(1+k)**(-1*Months))) 
        lsmpay.append(M)
        lsapr.append(k)
        k=k+0.00001
    return (lsmpay, lsapr)
    
def calcAPR(Amount, Months, MonthlyPayments):
    tuple_list = aprslist(Amount, Months)
    lsmpay = tuple_list[0]
    lsapr = tuple_list[1]
    lstemp = []
    n=len(lsmpay)
    lstemp.append(0)
    i=0
    while i<n:
        if not MonthlyPayments-lsmpay[i]>0:
            lstemp.append(i) 
            break 
        i=i+1
    bpoint=max(lstemp)
    if bpoint==0:
        print "APR bigger than 100"
    else:
        f1=lsmpay[bpoint]-MonthlyPayments
        f0=MonthlyPayments-lsmpay[bpoint-1]
        if f1>f0:
            x=lsapr[bpoint-1]
        else:
            x=lsapr[bpoint]
        APR=((1+x)**12-1)*100
        print round(APR, 1)

def finalcalculation(Amount, Months, MonthlyPayments):
    if Months*MonthlyPayments>Amount:
        calcAPR(Amount, Months, MonthlyPayments)
    else: 
        print "monthly payments is less than or equal to the loan"


#-----------------------------------

#things that needs to be done in future:
#it could more efficient (it doesnt have to check all the results)

