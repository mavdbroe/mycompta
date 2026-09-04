from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .forms import DepenseForm
from .models import Depense


@permission_required('depenses.add_depense', login_url='/accounts/login/')
def depense_creer(request):
    if request.method == 'POST':
        form = DepenseForm(request.POST, request.FILES)
        if form.is_valid():
            depense = form.save()
            messages.success(request, f"Dépense chez {depense.fournisseur} créée avec succès.")
            return redirect('depenses_liste')
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = DepenseForm()

    return render(request, 'depenses/depense_form.html', {'form': form})


def depenses_liste(request):
    depenses = Depense.objects.all().order_by('-date_depense')
    return render(request, 'depenses/depenses_liste.html', {'depenses': depenses})