import requests
from django.shortcuts import render


def upload_image(request):
    API_KEY = "3b438a42-69a1-4f7b-9abe-9a22aa672a3c"
    API_URL = "https://api.cloudmersive.com/image/ai-detection/file"

    if request.method != "POST":
        return render(request, "ai_detector/index.html")

    image = request.FILES.get("image")
    if not image:
        return render(request, "ai_detector/index.html", {"error": "Please select an image file first."})

    try:
        response = requests.post(
            API_URL,
            headers={"Apikey": API_KEY},
            files={"imageFile": image},
            timeout=30,
        )
    except requests.RequestException:
        return render(
            request,
            "ai_detector/index.html",
            {"error": "Could not reach detection service. Check your internet and try again."},
        )

    if not response.ok:
        return render(
            request,
            "ai_detector/index.html",
            {"error": f"Detection API failed ({response.status_code}). Please verify your API key."},
        )

    try:
        result = response.json()
    except ValueError:
        return render(
            request,
            "ai_detector/index.html",
            {"error": "Detection API returned invalid data. Please try again."},
        )

    is_ai = not result.get("CleanResult", True)
    confidence = result.get("AiGeneratedRiskScore", 0)
    ai_source = result.get("AiSource", "")

    return render(
        request,
        "ai_detector/index.html",
        {
            "uploaded": True,
            "is_ai": is_ai,
            "confidence": confidence,
            "ai_source": ai_source,
        },
    )
