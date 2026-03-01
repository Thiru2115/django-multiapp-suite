import os
from django.shortcuts import render
import base64
from huggingface_hub import InferenceClient
from huggingface_hub.utils import HfHubHTTPError

def hub_home(request):
    """Renders the main selection dashboard."""
    return render(request, 'ai_hub/hub_home.html')

def chatbot_view(request):
    """Handles the Chatbot Interface using Hugging Face."""
    context = {"response": None, "error": None, "user_input": ""}
    
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        context["user_input"] = user_input
        
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            context["error"] = "Hugging Face API Key is missing. Please add it to your .env file."
            return render(request, 'ai_hub/chatbot.html', context)
            
        try:
            client = InferenceClient(token=api_key)
            # Using Qwen2.5-72B-Instruct which is officially supported on the serverless inference API
            response = client.chat_completion(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=600,
                seed=42
            )
            
            context["response"] = response.choices[0].message.content
                
        except HfHubHTTPError as e:
            if "Authorization header is correct, but the token seems invalid" in str(e) or e.response.status_code == 401:
                context["error"] = "Invalid Hugging Face API Key."
            elif e.response.status_code == 503:
                context["error"] = "Model is currently loading on Hugging Face servers. Please try again in 30 seconds."
            else:
                 context["error"] = f"API Error ({e.response.status_code}): {getattr(e, 'server_message', str(e))}"
        except Exception as e:
            context["error"] = f"An unexpected error occurred: {e}"
            
    return render(request, 'ai_hub/chatbot.html', context)

def summarizer_view(request):
    """Handles the text summarization using Hugging Face."""
    context = {"summary": None, "error": None, "original_text": ""}
    
    if request.method == "POST":
        original_text = request.POST.get("original_text", "")
        context["original_text"] = original_text
        
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
             context["error"] = "Hugging Face API Key is missing. Please add it to your .env file."
             return render(request, 'ai_hub/summarizer.html', context)

        try:
             client = InferenceClient(token=api_key)
             # Using BART for specialized summarization
             summary_result = client.summarization(
                 original_text, 
                 model="facebook/bart-large-cnn"
             )
             context["summary"] = summary_result.summary_text
             
        except HfHubHTTPError as e:
             if "Authorization header is correct, but the token seems invalid" in str(e) or e.response.status_code == 401:
                 context["error"] = "Invalid Hugging Face API Key."
             elif e.response.status_code == 503:
                 context["error"] = "Model is currently loading. Please try again in 30 seconds."
             else:
                 context["error"] = f"API Error: {getattr(e, 'server_message', str(e))}"
        except Exception as e:
            context["error"] = f"An error occurred: {str(e)}"
            
    return render(request, 'ai_hub/summarizer.html', context)

def image_generator_view(request):
    """Handles AI Image generation using Hugging Face."""
    context = {"image_data": None, "error": None, "prompt": ""}
    
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        context["prompt"] = prompt
        
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
             context["error"] = "Hugging Face API Key is missing. Please add it to your .env file."
             return render(request, 'ai_hub/image_generator.html', context)
             
        try:
            # Using standard requests to completely avoid huggingface_hub SDK limitations and Pillow
            import requests
            API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
            headers = {"Authorization": f"Bearer {api_key}"}
            payload = {"inputs": prompt}
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 503:
                context["error"] = "Model is currently loading on Hugging Face servers. Please try again in 1 minute."
            elif response.status_code != 200:
                try:
                    err_data = response.json()
                    context["error"] = f"API Error: {err_data.get('error', 'Bad Request')}"
                except:
                    context["error"] = f"API Error ({response.status_code})"
            else:
                # Response body contains raw image bytes
                image_bytes = response.content
                img_str = base64.b64encode(image_bytes).decode("utf-8")
                context["image_data"] = f"data:image/jpeg;base64,{img_str}"
            
        except Exception as e:
            context["error"] = f"An error occurred: {str(e)}"
            
    return render(request, 'ai_hub/image_generator.html', context)
