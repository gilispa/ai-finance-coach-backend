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

Your role is to help users understand their spending patterns and make small, realistic
improvements to their financial habits — without judgment or guilt.

User financial summary:
- Top spending category: {top_category} (${top_amount})
- Spending risk level: {risk_level}
- Spending-to-income ratio: {ratio}%
- Micro-expense pattern: {micro_note}

Response guidelines:
- Start with a brief, simple explanation of what this data means for the user
- Focus on habits and patterns, not mistakes
- Give at most 2 specific and actionable suggestions (concrete and realistic)
- Adjust your tone based on the spending risk level
- Avoid generic advice or motivational clichés
- End with a short, supportive closing sentence
- Do NOT mention that you are an AI
- Do NOT sound like a financial institution or legal advisor
"""


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )

    return response.choices[0].message.content
