from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_response(persona, context, question):

    prompt = f"""
You are a customer support agent.

Customer Persona:
{persona}

Support Documentation:
{context}

Customer Question:
{question}

Instructions:

If persona is Technical Expert:
- Give detailed technical explanations.
- Mention troubleshooting steps.

If persona is Frustrated User:
- Be empathetic.
- Use simple language.
- Reassure the customer.

If persona is Business Executive:
- Be concise.
- Focus on business impact.
- Mention resolution timelines.

Only answer using the provided documentation.
Do not make up information.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    persona = "Technical Expert"

    context = """
API Authentication Guide

Authentication failures occur due to:
- Invalid API keys
- Expired tokens
- Incorrect configuration

Resolution:
1. Verify API key.
2. Generate a new token.
3. Check API configuration.
"""

    question = "Why is API authentication failing?"

    answer = generate_response(
        persona,
        context,
        question
    )

    print(answer)