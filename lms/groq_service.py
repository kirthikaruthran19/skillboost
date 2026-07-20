from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def generate_quiz(course_title):

    prompt = f"""
Generate 5 multiple choice questions for the course:

{course_title}

Return ONLY valid JSON.

Format:

[
    {{
        "question":"Question?",
        "options":[
            "A",
            "B",
            "C",
            "D"
        ],
        "answer":"Correct Option"
    }}
]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content