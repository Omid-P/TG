# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 10:46:29 2015

@author: APAX
"""

from __future__ import division

def DebtBeforePayments (TuitionFeeLoan, MaintenanceLoan, CourseLength, 
                        AverageInflation, r=0.03):
    '''
    Debt before payments.
    
    Input x.
    
    Output y.
    '''
                      
    if CourseLength == 3:
        
        End1stYear = (TuitionFeeLoan + MaintenanceLoan) * (1 + AverageInflation/100 + r)
        End2ndYear = (End1stYear + (TuitionFeeLoan + MaintenanceLoan)) * (1 + AverageInflation/100 + r)
        End3rdYear = (End2ndYear + (TuitionFeeLoan + 0.90 * MaintenanceLoan)) * (1 + AverageInflation/100 + r)
        InitialDebt = (End3rdYear)*(1 + (AverageInflation/100 + r) / 2) 
        
    elif CourseLength == 4:
        
        End1stYear = (TuitionFeeLoan + MaintenanceLoan) * (1 + AverageInflation/100 + r)
        End2ndYear = (End1stYear + (TuitionFeeLoan + MaintenanceLoan)) * (1 + AverageInflation/100 + r)
        End3rdYear = (End2ndYear + (TuitionFeeLoan + MaintenanceLoan)) * (1 + AverageInflation/100 + r)
        End4thYear = (End3rdYear + (TuitionFeeLoan + 0.90 * MaintenanceLoan)) * (1 + AverageInflation/100 + r)
        InitialDebt = (End4thYear) * (1 + (AverageInflation/100 + r) / 2)
        
    else:
        raise ValueError ("the course length is incorrect")
        print 'the course lengths needs to be either 3 or 4 years'
    
    return round(InitialDebt, 2)

def SalaryCalculator (FirstYearSalary, IncreaseRate, AverageInflation):
    SalaryList = [FirstYearSalary]
    n = 0
    while n < 29:
        Salary = SalaryList[n] * (1 + IncreaseRate/100 + AverageInflation/100)
        RoundedSalary = round(Salary, 2)
        SalaryList.append(RoundedSalary)
        n += 1
        
    return SalaryList

def LoanPaymentCalculator (FirstYearSalary, IncreaseRate, AverageInflation, 
                            AverageUKSalaryIncreaseRate, Threshold = 21000,
                            PaymentRate=0.09):
    
    ThresholdList = [Threshold]
    PaymentList = []
    SalaryList = SalaryCalculator (FirstYearSalary, IncreaseRate, AverageInflation)    
    n = 0
    while n < 30:
        if SalaryList[n] > ThresholdList[n]:
            YearlyPayments = (SalaryList[n] - ThresholdList[n]) * PaymentRate
            MonthlyPayments = YearlyPayments / 12
            RoundedMonthlyPayments = round(MonthlyPayments, 2)
            PaymentList.append(RoundedMonthlyPayments)
        else: 
            PaymentList.append(0)
        NewThreshold = ThresholdList[n] * (1 + AverageUKSalaryIncreaseRate / 100)
        ThresholdList.append(NewThreshold)
        n += 1     
    return PaymentList
    

def CalculateMonthlyInterestRate (AverageInflation, PlusRate):
    YearlyRate = AverageInflation/100 + PlusRate/100
    Months = 12
    MonthlyRate = ((1 + YearlyRate) ** (1 / Months)-1) * 100
    return round(MonthlyRate, 4)

def CalculateTheStudentLoan (TuitionFeeLoan, MaintenanceLoan, CourseLength, AverageInflation, 
                FirstYearSalary, IncreaseRate, AverageUKSalaryIncreaseRate, PlusRate):
    
    TotalDebt = [DebtBeforePayments (TuitionFeeLoan, MaintenanceLoan, CourseLength, 
                        AverageInflation, r=0.03)]
    
    MonthlyPaymentList = LoanPaymentCalculator (FirstYearSalary, IncreaseRate, AverageInflation, 
                            AverageUKSalaryIncreaseRate, Threshold = 21000,
                            PaymentRate=0.09)
    
    FinalList = []
                    
    Month1to360PaymentList=[]
    
    def Mult12(alist):
        m=0
        while m < 12:
            Month1to360PaymentList.append(alist) 
            m=m+1
        return Month1to360PaymentList

    k=0
    while k < 30:
        Mult12(MonthlyPaymentList[k])
        k=k+1
    
    MonthlyInterestRate=CalculateMonthlyInterestRate (AverageInflation, PlusRate)    
    
    LastMonthPayment = 0    
    
    i=0
    n=0
    while i < 360:
        Outstanding = (TotalDebt[i] - Month1to360PaymentList[i]) * (1 + MonthlyInterestRate/100)
        if Outstanding > 0: 
            RoundedOutstanding = round(Outstanding, 2)
            TotalDebt.append(RoundedOutstanding)
            n += 1
        else: 
            LastMonthPayment = TotalDebt[i]
            break
        i += 1
    
    FullLoanAmount = (TuitionFeeLoan + MaintenanceLoan) * CourseLength - MaintenanceLoan * 0.10
    
    FullPaymentAmount=0
    p=0
    while p < n:
        FullPaymentAmount += Month1to360PaymentList[p]
        p += 1
    FullPaymentAmount = FullPaymentAmount + LastMonthPayment
    
    print 'full loan amount was %d and full payment amount was %d' %(FullLoanAmount, FullPaymentAmount)

    FinalList.append(round(FullLoanAmount, 0))
    FinalList.append(round(FullPaymentAmount, 2))
    
    AveragePayment3Years = (MonthlyPaymentList[0] + MonthlyPaymentList [1] + MonthlyPaymentList [2]) / 3
    print 'average monthly payment for the fisrt three years is %d' %AveragePayment3Years

    FinalList.append(round(AveragePayment3Years, 2))

    if n==360:
        print 'the student loan is never paid back fully and debt was written off after 30 years'
        FinalList.append(30)
        FinalList.append(0)
    else: 
        x1=str(n/12)
        x2=x1[:2]
        Year=int(x2)        
        Month=n-Year*12
        print 'the loan is paid in %d years and %d months' %(Year, Month)
        FinalList.append(Year)
        FinalList.append(Month)

    return FinalList

#FinalList = [FullLoanAmount, FullPaymentAmount, AveragePayment3Years, Year, Month]

#-----------------------------------

#things that needs to be done in future:
#Remove the last element of the function (plus rate)
   

#----------------------------------------------

#assumptions:
#the length of study is either 3 or 4 years
#the student starts working the april after graduation
#therefore 6 month loan interest will be added before the payments start
#maintenace loan is calculated at 90% for the last year
#initial debt is what the student owes the april after graduation
#the assumption is that the salary increases more than the inflation 
#therefore we add salary increase rate to the inflation rate
#salary_calculator gives a list of each years salary, [0] for the first year, etc until [29] for 30th
#the average salary increase rate affects threshold

#----------------------------------------------



        

    
    
        

        