# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 09:50:39 2015

@author: APAX
"""

from __future__ import division

def monthly_payment_calculator(Amount, Months, APR):
    r=(APR/100+1)**(1/12)-1    
    monthly_payment=Amount*(r/(1-(1+r)**(-1*Months)))
    print round(monthly_payment, 2)
 
    
