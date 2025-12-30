def analyze_expense(amount: float, category: str):
    if amount > 1000:
        advice = "This expense is high. Consider whether it is necessary."
    else:
        advice = "Expense is within a normal range."

    return {
        "amount": amount,
        "category": category,
        "advice": advice
    }
