# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 14:46:16 2015

@author: APAX
"""
# calculates the APR based on the loan details (loan amount, monthly payments and number of monthly payments)
# loan formula: Payments = interest.rate * present.value / (1 - (1 + interest.rate) ^ (-number.of.periods))
# it fisrt calculates the interest rate then APR using: APR = (1 + interest.rate) ^ number.of.periods - 1
# the assumption is that the APR is less than 100

from __future__ import division

def InterestRateList(amount, months):
    """ Return two lists, monthly_payment_list and interest_rate_list.
    Caclculate monthly payments based on different interest rates.
    Interest rate is less than 0.06 which gives an APR of 100.
    """
    INTEREST_RATE_MIN = 0.00001  #anything less than this would give an APR of less than 0.05 (0 after rounding)
    INTEREST_RATE_MAX = 0.06     #this gives an APR of 100
    INTEREST_RATE_INCREMENT = 0.00001
    interest_rate = INTEREST_RATE_MIN
    monthly_payment_list = []
    interest_rate_list = []
    while interest_rate < INTEREST_RATE_MAX:
        monthly_payment = amount * (interest_rate / (1 - (1 + interest_rate) ** (-1*months))) 
        monthly_payment_list.append(monthly_payment) 
        interest_rate_list.append(interest_rate)
        interest_rate += INTEREST_RATE_INCREMENT
    return (monthly_payment_list, interest_rate_list)
    
    
def CalcAPR(amount, months, monthly_payment):
    """Return the APR.
    Check where a peyment in monthly_payment_list become more than actual monthly_payment.
    Chech which one is the closest one to the actuall monthly_payment.
    Calculates the APR based on the interest_rate for that particular monthly_payment.
    """    
    monthly_payment_list, interest_rate_list = InterestRateList(amount, months)
    breaking_point = 0
    for listed_payment_amount in monthly_payment_list:  
        if monthly_payment > listed_payment_amount:
            breaking_point += 1
        else: 
            break

    if breaking_point == len(monthly_payment_list):
        print "APR bigger than 100"
        
    else:
        difference_with_the_higher_monthly_payment = monthly_payment_list[breaking_point] - monthly_payment
        difference_with_the_lower_monthly_payment = monthly_payment - monthly_payment_list[breaking_point-1]
        if difference_with_the_higher_monthly_payment > difference_with_the_lower_monthly_payment:
            interest_rate = interest_rate_list[breaking_point-1]
        else:
            interest_rate = interest_rate_list[breaking_point]
        APR = ((1 + interest_rate) ** 12 - 1) * 100
        print round(APR, 1)


def CheckPaymentsAndCalculateAPR(amount, months, monthly_payment):
    """Return the APR if the monthly_payment cover the full loan amount."""
    if months * monthly_payment > amount:
        CalcAPR(amount, months, monthly_payment)
    else: 
        print "monthly payments is less than or equal to the loan"



