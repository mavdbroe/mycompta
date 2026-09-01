from .models import CompteComptable, EcritureComptable

COMPTE_CLIENTS = '411000'
COMPTE_VENTES = '700000'
COMPTE_TVA_COLLECTEE = '451000'


def generer_ecritures_facture(facture):
    """
    Génère les écritures comptables (vente + TVA) pour une facture,
    si elles n'existent pas déjà.
    Retourne (succès: bool, message: str)
    """
    if facture.ecritures.exists():
        return False, "Des écritures existent déjà pour cette facture."

    try:
        compte_clients = CompteComptable.objects.get(numero=COMPTE_CLIENTS)
        compte_ventes = CompteComptable.objects.get(numero=COMPTE_VENTES)
        compte_tva = CompteComptable.objects.get(numero=COMPTE_TVA_COLLECTEE)
    except CompteComptable.DoesNotExist:
        return False, "Comptes comptables manquants (411000, 700000 ou 451000)."

    total_ht = facture.total_ht
    total_tva = facture.total_tva

    if total_ht > 0:
        EcritureComptable.objects.create(
            date_ecriture=facture.date_emission,
            libelle=f"Vente facture {facture.numero}",
            compte_debit=compte_clients,
            compte_credit=compte_ventes,
            montant=total_ht,
            facture=facture,
        )

    if total_tva > 0:
        EcritureComptable.objects.create(
            date_ecriture=facture.date_emission,
            libelle=f"TVA facture {facture.numero}",
            compte_debit=compte_clients,
            compte_credit=compte_tva,
            montant=total_tva,
            facture=facture,
        )

    return True, "Écritures générées avec succès."

COMPTE_FOURNISSEURS = '440000'
COMPTE_ACHATS = '604000'
COMPTE_TVA_DEDUCTIBLE = '411100'


def generer_ecritures_depense(depense):
    """
    Génère les écritures comptables (achat + TVA) pour une dépense,
    si elles n'existent pas déjà.
    Retourne (succès: bool, message: str)
    """
    if depense.ecritures.exists():
        return False, "Des écritures existent déjà pour cette dépense."

    try:
        compte_fournisseurs = CompteComptable.objects.get(numero=COMPTE_FOURNISSEURS)
        compte_achats = CompteComptable.objects.get(numero=COMPTE_ACHATS)
        compte_tva = CompteComptable.objects.get(numero=COMPTE_TVA_DEDUCTIBLE)
    except CompteComptable.DoesNotExist:
        return False, "Comptes comptables manquants (440000, 604000 ou 411100)."

    montant_ht = depense.montant_ht
    montant_tva = depense.montant_tva

    if montant_ht > 0:
        EcritureComptable.objects.create(
            date_ecriture=depense.date_depense,
            libelle=f"Achat - {depense.fournisseur}",
            compte_debit=compte_achats,
            compte_credit=compte_fournisseurs,
            montant=montant_ht,
            depense=depense,
        )

    if montant_tva > 0:
        EcritureComptable.objects.create(
            date_ecriture=depense.date_depense,
            libelle=f"TVA déductible - {depense.fournisseur}",
            compte_debit=compte_tva,
            compte_credit=compte_fournisseurs,
            montant=montant_tva,
            depense=depense,
        )

    return True, "Écritures générées avec succès."