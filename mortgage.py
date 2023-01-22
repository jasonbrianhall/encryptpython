#!/usr/bin/env python

import math
import re

def mortgage_calculator(principal, rate, years, additionalPayment=0):
    r = rate/12/100
    n = years*12
    monthly_payment = principal*((r*(1+r)**n)/(((1+r)**n)-1))+additionalPayment
    remaining_balance = principal
    interest_paid = 0
    payments = []
    total_interest_paid=0
    for i in range(1, n+1):
        interest = remaining_balance * r
        principal_paid = monthly_payment - interest
        remaining_balance -= principal_paid
        interest_paid += interest
        total_interest_paid=total_interest_paid+interest
        payments.append({
            'month': i, 
            'monthly_payment': round(monthly_payment, 2), 
            'principal_paid': round(principal_paid, 2),
            'interest_paid': round(interest, 2),
            'remaining_balance': round(remaining_balance, 2),
            'total_interest_paid': round(total_interest_paid, 2) 
        })
    return payments

print("*"*12, " Welcome to the Mortgage Caculator ", "*"*12, "\n\n")

principal = input("Please enter the principal of the mortgage (e.g. 100000): ")
while not bool(re.match("^[0-9]+(\.[0-9]{1,2})?$", principal)):
    principal = input("Invalid input. Please enter a valid principal amount: ")
principal = float(principal)

rate = input("\nPlease enter the interest rate of the mortgage (e.g. 2.25 for 2.25%): ")
while not bool(re.match("^[0-9]+(\.[0-9]{1,2})?$", rate)):
    rate = input("Invalid input. Please enter a valid interest rate: ")
rate = float(rate)

years = input("\nPlease enter the number of years of the mortgage: ")
while not bool(re.match("^[0-9]+$", years)):
    years = input("Invalid input. Please enter a valid number of years: ")
years = int(years)

additionalpayment = input("\nPlease enter any additional payment above the minimum (enter 0 for none): ")
while not bool(re.match(r'^-?[0-9]+(\.[0-9]{1,2})?$', additionalpayment)):
    years = input("Invalid input. Please enter an additional payment: ")
additionalpayment = float(additionalpayment)



table = mortgage_calculator(principal, rate, years, additionalpayment)

print("\n\n\n{:<12}\t{:<12}\t{:<12}\t{:<12}\t{:<12}\t{:<12}".format("Month", "Payment", "Principal", "Interest", "Remaining", "Total Interest Paid"))
totalinterestpaid=0
for payment in table:
    month               = "{:03d}".format(payment['month'])
    payment_amount      = '${:,.2f}'.format(float(payment['monthly_payment']))
    principal_paid      = '${:,.2f}'.format(float(payment['principal_paid']))
    interest_paid       = '${:,.2f}'.format(float(payment['interest_paid']))
    remaining_balance   = '${:,.2f}'.format(float(payment['remaining_balance']))
    total_interest_paid = '${:,.2f}'.format(float(payment['total_interest_paid']))
    print("{:<12}\t{:<12}\t{:<12}\t{:<12}\t{:<12}\t{:<12}".format(month, payment_amount, principal_paid, interest_paid, remaining_balance, total_interest_paid))
