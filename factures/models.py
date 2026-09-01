from django.db import models
from clients.models import Client

class Facture(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('envoyee', 'Envoyée'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='factures')
    numero = models.CharField(max_length=20, unique=True)
    date_emission = models.DateField()
    date_echeance = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    notes = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.numero} - {self.client.nom}"

    @property
    def total_ht(self):
        return sum(ligne.total_ht for ligne in self.lignes.all())

    @property
    def total_tva(self):
        return sum(ligne.total_tva for ligne in self.lignes.all())

    @property
    def total_ttc(self):
        return self.total_ht + self.total_tva

    @property
    def est_en_retard(self):
        from datetime import date
        return self.date_echeance < date.today() and self.statut not in ['payee', 'annulee']


class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    description = models.CharField(max_length=255)
    quantite = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    prix_unitaire_ht = models.DecimalField(max_digits=10, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=21.00, help_text="Taux en % (ex: 21 pour 21%)")

    def __str__(self):
        return self.description

    @property
    def total_ht(self):
        return self.quantite * self.prix_unitaire_ht

    @property
    def total_tva(self):
        return self.total_ht * (self.taux_tva / 100)