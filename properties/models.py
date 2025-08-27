# properties/models.py
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Property(models.Model):
    TYPE_CHOICES = [
        ("studio", _("Studio")),
        ("appartement", _("Appartement")),
        ("maison", _("Maison")),
    ]

    STATE_CHOICES = [
        ("neuf", _("Neuf")),
        ("excellent", _("Excellent")),
        ("bon", _("Bon")),
        ("moyen", _("Moyen")),
    ]
    
    CONTRACT_DURATION_CHOICES = [
        ("1", _("1 an")),
        ("2", _("2 ans")),
        ("3", _("3 ans")),
        ("indetermine", _("Durée indéterminée")),
        ("autre", _("Autre durée")),
    ]

    title = models.CharField(_("Titre"), max_length=200)
    type = models.CharField(_("Type"), max_length=20, choices=TYPE_CHOICES, default="")
    location = models.CharField(_("Localisation"), max_length=200, default=_("Inconnue"))
    price = models.PositiveIntegerField(_("Prix"), default=0)
    bedrooms = models.PositiveIntegerField(_("Chambres"), default=1)
    bathrooms = models.PositiveIntegerField(_("Salon"), default=1)
    area = models.PositiveIntegerField(_("Surface (m²)"), default=50, blank=True)
    rating = models.FloatField(_("Note"), default=0.0)
    furnished = models.BooleanField(_("Meublé"), default=False)
    available = models.CharField(_("Disponibilité"), max_length=50, default=_("immédiate"))
    contract_duration = models.CharField(_("Durée de contrat"), max_length=20, choices=CONTRACT_DURATION_CHOICES, default="1")
    custom_contract_duration = models.CharField(_("Durée personnalisée"), max_length=100, blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)

    # Équipements
    wifi = models.BooleanField(_("Wi-Fi"), default=False)
    parking = models.BooleanField(_("Parking"), default=False)
    security = models.BooleanField(_("Sécurité"), default=False)
    pet_friendly = models.BooleanField(_("Animaux acceptés"), default=False)

    # État et règles
    state = models.CharField(_("État"), max_length=20, choices=STATE_CHOICES, default="bon")
    smoking_allowed = models.BooleanField(_("Fumeur autorisé"), default=False)
    parties_allowed = models.BooleanField(_("Fêtes autorisées"), default=False)
    pets_allowed = models.BooleanField(_("Animaux autorisés"), default=False)

    date_added = models.DateField(_("Date d'ajout"), default=datetime.date.today)

    # Coûts d'entrée
    owner_advance_months = models.PositiveIntegerField(_("Acompte propriétaire (mois)"), default=3)
    agent_fee_months = models.PositiveIntegerField(_("Frais d'agence (mois)"), default=1)
    electricity_deposit = models.CharField(_("Dépôt électricité"), max_length=200, blank=True, null=True)
    water_deposit = models.CharField(_("Dépôt eau"), max_length=100, blank=True, null=True)
    other_charges = models.CharField(_("Autres charges"), max_length=100, blank=True, null=True)

    # Vidéo
    video = models.FileField(_("Vidéo"), upload_to="properties/videos/", blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.location}"

    def get_contract_duration_display(self):
        if self.contract_duration == "autre" and self.custom_contract_duration:
            return self.custom_contract_duration
        return dict(self.CONTRACT_DURATION_CHOICES).get(self.contract_duration, self.contract_duration)

    class Meta:
        verbose_name = _("Propriété")
        verbose_name_plural = _("Propriétés")


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, verbose_name=_("Propriété"), on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(_("Image"), upload_to="properties/images/")
    is_main = models.BooleanField(_("Image principale"), default=False)

    def __str__(self):
        return f"Image pour {self.property.title}"

    class Meta:
        verbose_name = _("Image de propriété")
        verbose_name_plural = _("Images de propriétés")


class Favorite(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Utilisateur"), on_delete=models.CASCADE)
    property = models.ForeignKey(Property, verbose_name=_("Propriété"), on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'property')
        verbose_name = _("Favori")
        verbose_name_plural = _("Favoris")

    def __str__(self):
        return f"{self.user.username} a mis en favori {self.property.title}"