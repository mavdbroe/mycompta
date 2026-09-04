from django.db import models
from factures.models import Facture
from depenses.models import Depense
from django.core.exceptions import ValidationError

class CompteComptable(models.Model):
    TYPE_CHOICES = [
        ('actif', 'Actif'),
        ('passif', 'Passif'),
        ('charge', 'Charge'),
        ('produit', 'Produit'),
    ]

    numero = models.CharField(max_length=10, unique=True, help_text="Ex: 700, 440, 411")
    nom = models.CharField(max_length=200)
    type_compte = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.numero} - {self.nom}"

    class Meta:
        ordering = ['numero']


class EcritureComptable(models.Model):
    date_ecriture = models.DateField()
    libelle = models.CharField(max_length=255)
    compte_debit = models.ForeignKey(CompteComptable, on_delete=models.PROTECT, related_name='ecritures_debit')
    compte_credit = models.ForeignKey(CompteComptable, on_delete=models.PROTECT, related_name='ecritures_credit')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    facture = models.ForeignKey(Facture, on_delete=models.SET_NULL, related_name='ecritures', blank=True, null=True)
    depense = models.ForeignKey(Depense, on_delete=models.SET_NULL, related_name='ecritures', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_ecriture} - {self.libelle} ({self.montant}€)"

    def clean(self):
        exercice = ExerciceComptable.objects.filter(
            date_debut__lte=self.date_ecriture,
            date_fin__gte=self.date_ecriture,
        ).first()
        if exercice and exercice.cloture:
            raise ValidationError(
                f"Impossible d'enregistrer cette écriture : l'exercice {exercice.annee} est clôturé."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_ecriture']


class ExerciceComptable(models.Model):
    annee = models.PositiveIntegerField(unique=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    cloture = models.BooleanField(default=False)
    date_cloture = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        statut = "Clôturé" if self.cloture else "Ouvert"
        return f"Exercice {self.annee} ({statut})"

    class Meta:
        ordering = ['-annee']