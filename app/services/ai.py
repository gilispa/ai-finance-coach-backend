import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_financial_advice(insights: dict) -> str:
    top_category = insights.get("top_spending_category", {}).get("category", "unknown")
    top_amount = insights.get("top_spending_category", {}).get("total", 0)
    risk_level = insights.get("spending_risk", {}).get("risk", "unknown")
    ratio = insights.get("spending_risk", {}).get("ratio", 0)
    micro_expense_note = insights.get("micro_expenses", {}).get("note", "")
    prompt = f"""
You are a supportive financial coach.

Your role is to help users understand their spending patterns and make small, realistic
improvements to their financial habits — without judgment or guilt.

User financial summary:
- Top spending category: {top_category} (${top_amount})
- Spending risk level: {risk_level}
- Spending-to-income ratio: {ratio}%
- Presence of frequent small expenses (micro-expenses): {micro_expense_note}

Response guidelines:
- Start with a brief, simple explanation of what this data means for the user
- Focus on habits and patterns, not mistakes
- Give at most 2 specific and actionable suggestions (concrete, realistic, measurable if possible)
- Adjust your tone based on the risk level (more preventive if risk is higher)
- Keep the tone calm, supportive, and practical
- Avoid generic advice or motivational clichés
- End with a short encouraging closing sentence
- Do NOT mention that you are an AI
- Do NOT sound like a financial institution or legal advisor
- If frequent small expenses are present, explain their long-term impact in a simple way
- Treat micro-expenses as habits, not mistakes
- Avoid focusing only on large purchases
- If relevant, suggest one small behavioral change related to micro-expenses
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    return response.choices[0].message.content
