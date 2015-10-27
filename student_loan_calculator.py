# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 10:46:29 2015

@author: APAX
"""

# gets seven variables and returns four results. 
# Tuition Fee Loan: between £6,000 to £9,000 per year 
# Mainetnance Loan: Normally £6,904 living with parents, £8,200 away, £10,702 in London
# maintenace loan is calculated at 90% for the last year
# Salary increase rate will be added/(deducted from) to inflation rate (RPI)
# Interest rate: 3% + RPI during the course and anything between RPI and RPI + 3% after that
# Course lenght is either 3 or 4 years
# It returns total amount received and paid back, average monthly payment in the first three years and 
# how long it will take until the loan is cleared. Any outstanding amount will be cleared after 30 years


from __future__ import division

def DebtBeforePayments (tuition_fee_loan, maintenance_loan, course_length, 
                        average_inflation, R = 0.03):
    """Returns the initial debt which is what the student owes the April after graduationthe 
    (6 months after graduation). Thats when the student will need to make the first payment.
    R is the interest rate that will be added to the inflation rate to calculate the loan during the course.
    """
                    
    if course_length == 3:
        
        end_1st_year = (tuition_fee_loan + maintenance_loan) * (1 + average_inflation/100 + R)
        end_2nd_year = (end_1st_year + (tuition_fee_loan + maintenance_loan)) * (1 + average_inflation/100 + R)
        end_3rd_year = (end_2nd_year + (tuition_fee_loan + 0.90 * maintenance_loan)) * (1 + average_inflation/100 + R)
        initial_debt = (end_3rd_year)*(1 + (average_inflation/100 + R) / 2) 
        
    elif course_length == 4:
        
        end_1st_year = (tuition_fee_loan + maintenance_loan) * (1 + average_inflation/100 + R)
        end_2nd_year = (end_1st_year + (tuition_fee_loan + maintenance_loan)) * (1 + average_inflation/100 + R)
        end_3rd_year = (end_2nd_year + (tuition_fee_loan + maintenance_loan)) * (1 + average_inflation/100 + R)
        end_4th_year = (end_3rd_year + (tuition_fee_loan + 0.90 * maintenance_loan)) * (1 + average_inflation/100 + R)
        initial_debt = (end_4th_year) * (1 + (average_inflation/100 + R) / 2)
        
    else:
        raise ValueError ("the course length is incorrect")        
    
    return round(initial_debt, 2)

def SalaryCalculator (first_year_salary, salary_increase_rate, average_inflation):
    
    """Returns a list of yearly salary for 30 years, [0] for the first year, [29] for 30th year.
    Calculates that based on salary increase rate and inflation rate.   
    """   
    salary_list = [first_year_salary]
    
    for n in range(29):    
        salary = salary_list[n] * (1 + salary_increase_rate/100 + average_inflation/100)
        rounded_salary = round(salary, 2)
        salary_list.append(rounded_salary)
        
    return salary_list

def LoanPaymentCalculator (first_year_salary, salary_increase_rate, average_inflation, 
                            average_UK_salary_increase_rate, THRESHOLD = 21000,
                            PAYMENT_RATE=0.09):
    """Returns a list of monthly payments for each year for 30 years. 
    Loan payments are 0.09 (PAYMENT_RATE) of the earnings above Threshold. 
    Threshold is 21,000 for the first year but increases based on average_UK_salary_increase_rate.
    
    """
    
    threshold_list = [THRESHOLD]
    payment_list = []
    salary_list = SalaryCalculator (first_year_salary, salary_increase_rate, average_inflation)    
    
    for n in range(30):
        if salary_list[n] > threshold_list[n]:
            yearly_payments = (salary_list[n] - threshold_list[n]) * PAYMENT_RATE
            monthly_payments = yearly_payments / 12
            rounded_monthly_payments = round(monthly_payments, 2)
            payment_list.append(rounded_monthly_payments)
        else: 
            payment_list.append(0)
        new_threshold = threshold_list[n] * (1 + average_inflation / 100 + average_UK_salary_increase_rate / 100)
        threshold_list.append(new_threshold)    
        
    return payment_list

def CalculateMonthlyInterestRate (first_year_salary, salary_increase_rate, average_inflation):
    """Returns a list of monthly interest rates for each year based on the yearly interest year. 
    Formula: monthly interest rate = ((1 + yearly interest rate) ** (1 / 12)-1) * 100
    Anybody with salary of below £21,000 per year will need to pay only Inflation rate towards interest. 
    Anybody with salary of over £41,000 per year will need to pay 3% plus Inflation rate towards interest. 
    For salaries betwwen 21 to 41k the rate that will be added to the inflation rate will varies  betwwen 0 to 3%. 
    This will checks the salarys and calculates the monthly interest rate. 
    """
    LOWEST_RATE = 21000
    HIGHEST_RATE = 41000
    MAXIMUM_ADDED_INTEREST_RATE = 3
    MONTHS = 12
    salary_list = SalaryCalculator (first_year_salary, salary_increase_rate, average_inflation)
    monthly_interest_rate_list = []
    
    for salary in salary_list: 
        if salary <= LOWEST_RATE: 
            added_rate = 0          
            yearly_rate = average_inflation / 100  + added_rate / 100
            monthly_rate = ((1 + yearly_rate) ** (1 / MONTHS)-1) * 100
            monthly_interest_rate_list.append(round(monthly_rate, 4))
        
        elif LOWEST_RATE < salary < LOWEST_RATE:
            added_rate = ((salary - LOWEST_RATE) / (HIGHEST_RATE - LOWEST_RATE)) *  MAXIMUM_ADDED_INTEREST_RATE        
            # the added interest rate has a linear relation with the salary.             
            yearly_rate = average_inflation / 100 + added_rate / 100
            monthly_rate = ((1 + yearly_rate) ** (1 / MONTHS)-1) * 100
            monthly_interest_rate_list.append(round(monthly_rate, 4))
            
        else: 
            added_rate = MAXIMUM_ADDED_INTEREST_RATE
            yearly_rate = average_inflation / 100 + added_rate / 100
            monthly_rate = ((1 + yearly_rate) ** (1 / MONTHS)-1) * 100
            monthly_interest_rate_list.append(round(monthly_rate, 4))
    
    return monthly_interest_rate_list
    
    
def ConvertYearlyListToMonthlyList(a_list):
    """repeats each item 12 times in the list. 
    This will be used to convert the monthly payment list for each year to a list of 360 
    months (30 years) monthly payments. Then the payment list will contain 360 items Instead of 30. 
    The same with the monthly interest rate. 
    """
    new_list = []
    for k in a_list:    
        for m in range(12):
            new_list.append(k) 
    return new_list


def CalculateTheStudentLoan (tuition_fee_loan, maintenance_loan, course_length, first_year_salary, 
                             average_inflation, salary_increase_rate, average_UK_salary_increase_rate):
    """Returns the total loan amount received, total amount paid, average first 3 years monthly payment 
    and the length in which the loan was paid fully. 
    If the loan is not paid fully in 30 years the balance would be written off.
    In that case this would return an answer of 30 years for the loan length.
    """
    total_debt = [DebtBeforePayments (tuition_fee_loan, maintenance_loan, course_length, 
                        average_inflation, R=0.03)]
    
    monthly_payment_list = LoanPaymentCalculator (first_year_salary, salary_increase_rate, average_inflation, 
                            average_UK_salary_increase_rate, THRESHOLD = 21000,
                            PAYMENT_RATE=0.09)    
    month_1_to_360_payment_list = ConvertYearlyListToMonthlyList(monthly_payment_list)  

    monthly_interest_rate_list = CalculateMonthlyInterestRate (first_year_salary, 
                                                               salary_increase_rate, average_inflation)                                
    month_1_to_360_interest_rate_list = ConvertYearlyListToMonthlyList (monthly_interest_rate_list)
    
    last_month_payment = 0    
    number_of_payments = 0
    
    for i in range(360):  # deducts each month payment from the outstanding amount
                          # and adds one month interest to that to calculate the new outstanding amount. 
        outstanding = (total_debt[i] - month_1_to_360_payment_list[i]) * \
                        (1 + month_1_to_360_interest_rate_list[i] / 100)
        if outstanding > 0: 
            total_debt.append(round(outstanding, 2))
            number_of_payments += 1
        else: 
            last_month_payment = total_debt[i]
            break
    
    full_loan_amount = (tuition_fee_loan + maintenance_loan) * course_length - maintenance_loan * 0.10
    
    full_payment_amount=0
    
    for j in range(number_of_payments): # adds all monthly payments up until the month before the last month.
        full_payment_amount += month_1_to_360_payment_list[j]
    
    full_payment_amount = full_payment_amount + last_month_payment

    average_payment_3_years = (monthly_payment_list[0] + monthly_payment_list[1] + monthly_payment_list[2]) / 3

    if number_of_payments == 360:
        year = 30        
        month = 0
        print 'the student loan is never paid back fully and debt was written off after 30 years'

    else: 
        x1 = str(number_of_payments / 12)
        x2 = x1[:2]
        year = int(x2)        
        month = number_of_payments - year * 12
        print 'the loan is paid in %d years and %d months' %(year, month)
       
    loan_length = "%d years, %d months" %(year, month)
    loan_amount = round(full_loan_amount, 0)
    loan_paid = round(full_payment_amount, 0)
    first_3y_monthly_payment = round(average_payment_3_years, 2)

    print 'full loan amount was %d and full payment amount was %d' %(full_loan_amount, full_payment_amount)
    print 'average monthly payment for the fisrt three years is %d' %average_payment_3_years
    
    return loan_amount, loan_paid, first_3y_monthly_payment, loan_length
    

#CalculateTheStudentLoan (7000, 5000, 3, 25000, 3, 2, 1)     

    
    
        

        