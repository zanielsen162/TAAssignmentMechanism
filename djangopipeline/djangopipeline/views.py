# myapp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Professor
from .forms import ProfessorForm

# List all professors
def professor_list(request):
    professors = Professor.objects.all()
    return render(request, 'professor_list.html', {'professors': professors})

# View details of a single professor
def professor_detail(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    return render(request, 'professor_detail.html', {'professor': professor})

# Add a new professor
def professor_add(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('professor_list')
    else:
        form = ProfessorForm()
    return render(request, 'professor_form.html', {'form': form})

# Edit an existing professor
def professor_edit(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('professor_list')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'professor_form.html', {'form': form})
