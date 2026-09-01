from django.db import models

class Depense(models.Model):
    CATEGORIE_CHOICES = [
        ('fournitures', 'Fournitures de bureau'),
        ('deplacement', 'Déplacement'),
        ('logiciel', 'Logiciel / Abonnement'),
        ('marketing', 'Marketing'),
        ('autre', 'Autre'),
    ]

    fournisseur = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='autre')
    montant_ht = models.DecimalField(max_digits=10, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=21.00)
    date_depense = models.DateField()
    justificatif = models.FileField(upload_to='justificatifs/%Y/%m/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fournisseur} - {self.description}"

    @property
    def montant_tva(self):
        return self.montant_ht * (self.taux_tva / 100)

    @property
    def montant_ttc(self):
        return self.montant_ht + self.montant_tva