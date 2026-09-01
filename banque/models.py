from django.db import models
from factures.models import Facture

class LigneReleve(models.Model):
    date_operation = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2, help_text="Positif si crédit (argent reçu), négatif si débit")
    communication = models.CharField(max_length=255, blank=True)
    facture = models.ForeignKey(Facture, on_delete=models.SET_NULL, null=True, blank=True, related_name='lignes_releve')
    rapprochee = models.BooleanField(default=False)
    date_import = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_operation} - {self.montant}€ - {self.communication}"

    class Meta:
        ordering = ['-date_operation']