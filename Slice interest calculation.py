def slice_amount(x,r,y):
    d=r/(36500)
    return x*((1+d)**y)

def slice_profit(x,r,y):
    return slice_amount(x,r,y)-x

# Example:
x=100   # principal
r=5.5      # annual interest rate
y=3650       # days

final_amt=slice_amount(x,r,y)
profit=slice_profit(x,r,y)

print(f"Final Amount: {final_amt:.2f}")
print(f"Profit: {profit:.2f}")
