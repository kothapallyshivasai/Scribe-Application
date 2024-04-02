from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from .key import openai_api_key
from django.views.decorators.http import require_POST
import requests
from .models import Summary

def home(request):
    return render(request, 'index.html')

@require_POST
def validate_and_save(request):
    text = request.POST.get("text", "")
    if text != "":
        response_size = request.POST.get('response_size', 100)
        cleaned_text = '\n'.join(line for line in text.splitlines() if line.strip())
        cleaned_text += f"\nSummarize the given data in {response_size} words like a doctor's note. And also Upper Case all the important points or key terms."
        url = "https://api.openai.com/v1/completions"
        headers = {'Authorization': f'Bearer {openai_api_key}'}
        print(len(cleaned_text))
        cleaned_text = cleaned_text[22863:]
        print(len(cleaned_text))
        print(cleaned_text)
        data = {'prompt': cleaned_text, 'max_tokens': int(response_size), 'model': 'gpt-3.5-turbo-instruct-0914'} 
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            generated_text = result['choices'][0]['text'].strip()
            with open('summary.txt', 'w') as file:
                file.write(generated_text)
            ob = Summary()
            ob.patient_data = cleaned_text
            ob.summarized_text = generated_text 
            ob.save()
            return JsonResponse({'generated_text': generated_text})
        else:
            error_message = response.json().get('error', 'Unknown error occurred')
            print(error_message)
            return JsonResponse({'error': error_message}, status=500)

    return JsonResponse({'error': 'Text cannot be empty'}, status=400)

@require_POST
def summary(request):
    return FileResponse(open('summary.txt', 'rb'), as_attachment=True)

def history(request):
    return render(request, "history.html", {"objects": Summary.objects.all()})

{'message': "This model's maximum context length is 4097 tokens, however you requested 8077 tokens (7877 in your prompt; 200 for the completion). Please reduce your prompt; or completion length.", 'type': 'invalid_request_error', 'param': None, 'code': None}