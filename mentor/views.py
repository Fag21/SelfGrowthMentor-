import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

HUGGINGFACE_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
HUGGINGFACE_API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"

# Optional: set your own token if needed (some models don’t require one)
# HUGGINGFACE_TOKEN = "your_token_here"

conversation_memory = {}

@csrf_exempt
def ai_mentor_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id", "guest")
        user_message = data.get("message", "")

        if user_id not in conversation_memory:
            conversation_memory[user_id] = []

        # Add user message to memory
        conversation_memory[user_id].append({"role": "user", "content": user_message})

        # Prepare context (last 5 messages)
        context = "\n".join([f"{m['role']}: {m['content']}" for m in conversation_memory[user_id][-5:]])

        prompt = f"""
        You are Filebar's personal AI growth mentor.
        You help the user plan their day, improve mindset, and track growth.
        Context:
        {context}
        Mentor:
        """

        response = requests.post(
            HUGGINGFACE_API_URL,
            headers={"Content-Type": "application/json"},
            json={"inputs": prompt},
        )

        result = response.json()
        ai_reply = result[0]["generated_text"].split("Mentor:")[-1].strip()

        # Add mentor reply to memory
        conversation_memory[user_id].append({"role": "mentor", "content": ai_reply})

        return JsonResponse({"reply": ai_reply})

    return JsonResponse({"error": "Invalid request"}, status=400)
from habits.models import Habit

def get_user_context(user):
    habits = Habit.objects.filter(user=user)
    context_data = [
        {"name": h.name, "reason": h.reason, "plan": h.plan, "commitment": h.commitment}
        for h in habits
    ]
    return context_data
