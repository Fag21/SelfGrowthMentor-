# mentor/utils.py
import openai

openai.api_key = "AIzaSyAvoEaywWZvObSVVYqbQdkVi4ZA5irtFtI"  # ideally load from settings

def get_ai_reflection(content):
    prompt = f"""
    You are a wise self-growth mentor.
    The user wrote this journal entry:

    "{content}"

    Give a short, compassionate reflection (max 3 sentences).
    Highlight what emotion dominates and one gentle insight.
    Respond in warm, human tone.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a kind self-growth mentor."},
                      {"role": "user", "content": prompt}],
            temperature=0.8,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return "✨ (Mentor is resting today; no reflection available.)"
