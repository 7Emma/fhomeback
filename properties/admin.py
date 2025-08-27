# properties/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Property, Favorite, PropertyImage

# Admin inline pour les images
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return _("Aucune image")
    image_preview.short_description = _("Aperçu")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    
    # Configuration de l'affichage de la liste
    list_display = (
        'titre', 'type_bien', 'localisation', 'prix', 
        'chambres', 'salles_de_bain', 'meuble', 
        'disponibilite', 'duree_contrat', 'etat', 'date_ajout'
    )
    list_filter = ('type', 'location', 'furnished', 'available', 'state', 'contract_duration')
    search_fields = ('title', 'location', 'description')
    ordering = ('-date_added',)
    list_per_page = 20

    # Configuration du formulaire d'édition
    fieldsets = (
        (_('Informations principales'), {
            'fields': (
                'title', 'type', 'location', 'price', 
                'bedrooms', 'bathrooms', 'area', 'rating', 
                'description', 'furnished', 'available', 'state'
            )
        }),
        (_('Durée de contrat'), {
            'fields': ('contract_duration', 'custom_contract_duration')
        }),
        (_('Équipements'), {
            'fields': ('wifi', 'parking', 'security', 'pet_friendly'),
            'classes': ('collapse',)
        }),
        (_('Règles'), {
            'fields': ('smoking_allowed', 'parties_allowed', 'pets_allowed'),
            'classes': ('collapse',)
        }),
        (_('Coûts d\'entrée'), {
            'fields': (
                'owner_advance_months', 'agent_fee_months', 
                'electricity_deposit', 'water_deposit', 'other_charges'
            ),
            'classes': ('collapse',)
        }),
        (_('Médias'), {
            'fields': ('video',),
            'classes': ('collapse',)
        }),
    )

    # Méthodes pour traduire les champs dans l'admin
    def titre(self, obj):
        return obj.title
    titre.short_description = _("Titre")

    def type_bien(self, obj):
        return obj.get_type_display()
    type_bien.short_description = _("Type")

    def localisation(self, obj):
        return obj.location
    localisation.short_description = _("Localisation")

    def prix(self, obj):
        return f"{obj.price} FCFA"
    prix.short_description = _("Prix")

    def chambres(self, obj):
        return obj.bedrooms
    chambres.short_description = _("Chambres")

    def salles_de_bain(self, obj):
        return obj.bathrooms
    salles_de_bain.short_description = _("Salles de bain")

    def meuble(self, obj):
        return obj.furnished  # retourne un booléen
    meuble.boolean = True
    meuble.short_description = _("Meublé")


    def disponibilite(self, obj):
        return obj.available
    disponibilite.short_description = _("Disponibilité")
    
    def duree_contrat(self, obj):
        return obj.get_contract_duration_display()
    duree_contrat.short_description = _("Durée de contrat")

    def etat(self, obj):
        return obj.get_state_display()
    etat.short_description = _("État")

    def date_ajout(self, obj):
        return obj.date_added
    date_ajout.short_description = _("Date d'ajout")


# Admin pour les images de propriétés
@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('propriete', 'is_main', 'apercu_image')
    list_filter = ('property__location', 'is_main')
    search_fields = ('property__title',)
    list_editable = ('is_main',)
    
    def propriete(self, obj):
        return obj.property.title
    propriete.short_description = _("Propriété")
    propriete.admin_order_field = 'property__title'
    
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return _("Aucune image")
    apercu_image.short_description = _("Aperçu")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'bien', 'localisation_du_bien')
    list_filter = ('property__location',)
    search_fields = ('user__username', 'property__title')

    def utilisateur(self, obj):
        return obj.user.username
    utilisateur.short_description = _("Utilisateur")

    def bien(self, obj):
        return obj.property.title
    bien.short_description = _("Bien")

    def localisation_du_bien(self, obj):
        return obj.property.location
    localisation_du_bien.short_description = _('Localisation')
    localisation_du_bien.admin_order_field = 'property__location'