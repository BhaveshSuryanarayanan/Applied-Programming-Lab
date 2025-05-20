def calculate_growth_years(principal, rate, target, annual_deposit=0):
    mon = principal
    for i in range(1000):
        mon+=annual_deposit
        mon += mon * (rate/100)
        print(mon)
        if mon>=target:
            return i
    
    return -1

principal=1000
rate=5.0
target=1100
deposit=0
print(calculate_growth_years(principal, rate, target, deposit))