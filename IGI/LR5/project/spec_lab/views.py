from django.shortcuts import render
import math

def build_points():
    count = 60

    x_min = -0.9
    x_max = 0.9

    step = (x_max - x_min) / (count - 1)

    x_values = [
        x_min + i * step
        for i in range(count)
    ]

    return [
        {
            "x": x,
            "math_fx": math.log1p(-x)
        }
        for x in x_values
    ]

def spec_lab(request):
    return render(request, "spec_lab/all_teg.html")

def spec_lab_js(request):
    context = {
    "ln_chart_points": build_points(),}
    
    return render(request, "spec_lab/js_task.html", context)