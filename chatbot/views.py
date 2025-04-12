# chatbot/views.py
import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        headers = {
            'Authorization': f'Bearer {settings.CHATBOT_API_KEY}',
            'Content-Type': 'application/json',
        }

        payload = {
            "model": "openchat/openchat-7b",  # ✅ Use a valid model from OpenRouter
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(
                settings.CHATBOT_API_URL,  # should be https://openrouter.ai/api/v1/chat/completions
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            ai_reply = response.json()['choices'][0]['message']['content']  # ✅ Extract reply properly

        except requests.exceptions.RequestException as e:
            ai_reply = f"Error: {str(e)}"

        return JsonResponse({'reply': ai_reply})
