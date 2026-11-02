from django.shortcuts import render

# Create your views here.
def spec_lab(request):
    return render(request, "spec_lab/all_teg.html")

def spec_lab_js(request):
    return render(request, "spec_lab/js_task.html")