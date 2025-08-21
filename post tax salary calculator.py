import math


def format_inr(amount):
    """Format a number in Indian comma style, e.g., ₹12,34,567.89"""
    amount = round(amount, 2)
    int_part, _, frac_part = f"{amount:.2f}".partition(".")
    if len(int_part) <= 3:
        return f"₹{int_part}.{frac_part}"
    else:
        last3 = int_part[-3:]
        rest = int_part[:-3]
        rest_with_commas = ",".join([rest[max(i - 2, 0):i] for i in range(len(rest), 0, -2)][::-1])
        return f"₹{rest_with_commas},{last3}.{frac_part}"


def calculate_new_regime_tax(income):
    slabs = [
        (0, 400000, 0.00),
        (400000, 800000, 0.05),
        (800000, 1200000, 0.10),
        (1200000, 1600000, 0.15),
        (1600000, 2000000, 0.20),
        (2000000, 2400000, 0.25),
        (2400000, float('inf'), 0.30)
    ]

    standard_deduction = 75000
    taxable_income = max(0, income - standard_deduction)
    tax = 0

    for lower, upper, rate in slabs:
        if taxable_income > lower:
            tax += (min(taxable_income, upper) - lower) * rate
        else:
            break

    return income - tax


def calculate_old_regime_tax(income):
    slabs = [
        (0, 250000, 0.00),
        (250000, 500000, 0.05),
        (500000, 1000000, 0.20),
        (1000000, float('inf'), 0.30)
    ]

    tax = 0
    for lower, upper, rate in slabs:
        if income > lower:
            tax += (min(income, upper) - lower) * rate
        else:
            break

    if income <= 500000:
        tax = 0

    return income - tax


if __name__ == "__main__":
    salary = 24_00_000

    post_tax_new = calculate_new_regime_tax(salary)
    post_tax_old = calculate_old_regime_tax(salary)

    print("\n--- Tax Calculation Summary ---")

    print(f"\n🧾 Old Regime:")
    print(f"  • Post-tax annual salary: {format_inr(post_tax_old)}")
    print(f"  • Post-tax monthly salary: {format_inr(post_tax_old / 12)}")

    print(f"🆕 New Regime:")
    print(f"  • Post-tax annual salary: {format_inr(post_tax_new)}")
    print(f"  • Post-tax monthly salary: {format_inr(post_tax_new / 12)}")

    # print("\n💡 Suggestion:")
    # if post_tax_new > post_tax_old:
    #     print("👉 The New Regime is better for you.")
    # elif post_tax_old > post_tax_new:
    #     print("👉 The Old Regime is better for you.")
    # else:
    #     print("👉 Both regimes yield the same post-tax salary.")