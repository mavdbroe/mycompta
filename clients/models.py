from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=200)
    numero_entreprise = models.CharField(max_length=20, blank=True, help_text="Numéro BCE (ex: BE0123456789)")
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=10, blank=True)
    pays = models.CharField(max_length=100, default="Belgique")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom