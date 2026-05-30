from django.shortcuts import render, redirect, get_object_or_404

from files.forms import DocumentForm
from files.models import Document
# Create your views here.
def files_list(request):
    files = Document.objects.all()
    return render(request, "files/list.html", {"files": files})


def files_create(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('files_list')
        return render(request, "files/create.html", {"form": form})
    else:
        form = DocumentForm()
        return render(request, "files/create.html", {"form": form})


def files_update(request, pk=None):
    file = Document.objects.filter(pk=pk).first()
    if request.method == "POST":

        form = DocumentForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            return redirect('files_list')
        return render(request, "files/update.html", {"form": form})
    else:
        form = DocumentForm(instance=file)
        return render(request, "files/update.html", {"form": form})

def files_delete(request, pk=None):
    file = Document.objects.get(pk=pk)
    file.delete()
    return redirect('files_list')
