import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_financial_advice(insights: dict) -> str:
    top_category = insights.get("top_spending_category", {}).get("category", "unknown")
    top_amount = insights.get("top_spending_category", {}).get("total", 0)
    risk_level = insights.get("spending_risk", {}).get("risk", "unknown")
    ratio = insights.get("spending_risk", {}).get("ratio", 0)
    micro_expenses = insights.get("micro_expenses", [])

    if micro_expenses:
        micro_note = (
            f"You have frequent small expenses across {len(micro_expenses)} categories, "
            f"adding up to ${sum(e['total'] for e in micro_expenses)}."
        )
    else:
        micro_note = "You don't have frequent small expenses."

    prompt = f"""
You are a supportive financial coach.

User financial summary:
- Top spending category: {top_category} (${top_amount})
- Spending risk level: {risk_level}
- Spending-to-income ratio: {ratio}%
- Micro-expense pattern: {micro_note}

Guidelines:
- Explain the situation simply
- Focus on habits, not guilt
- Give at most 2 realistic suggestions
- End with encouragement
- Do NOT mention being an AI
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )

    return response.choices[0].message.content
