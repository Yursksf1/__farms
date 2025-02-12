from django.db import models
from django.template.defaultfilters import slugify


class Farm(models.Model):
    name = models.CharField(
        max_length=10,
        verbose_name="Farm id"
    )

    owner = models.CharField(
        max_length=500,
        verbose_name="Nombre productor",
        null=True, blank=True
    )

    region = models.CharField(
        max_length=200,
        verbose_name="Región/ Zona o cooperativa",
        null=True, blank=True
    )

    municipio = models.CharField(
        max_length=500,
        verbose_name="Municipio",
        null=True, blank=True,
    )

    departamento = models.CharField(
        max_length=200,
        verbose_name="Departamento",
        null=True, blank=True
    )

    def __str__(self):
        return self.name


class SubFarm(models.Model):
    farm = models.ForeignKey(
        Farm,
        verbose_name="farm",
        on_delete=models.CASCADE,
        related_name="farm_subfarms"
    )

    sub_name = models.CharField(max_length=1, null=True, blank=True)  # Ej: 'A', 'B', 'C', 'D'

    technical = models.CharField(
        max_length=500,
        verbose_name="Tecnico",
        null=True, blank=True
    )
    map_date = models.DateField(
        null=True, blank=True
    )

    region = models.CharField(
        max_length=200,
        verbose_name="Region",
        null=True, blank=True
    )
    nom_pol = models.CharField(
        max_length=200,
        verbose_name="Nom_pol",
        null=True, blank=True
    )
    area_pol = models.FloatField(
        max_length=200,
        verbose_name="area_pol",
        null=True, blank=True
    )
    latitude = models.CharField(
        max_length=200,
        verbose_name="latitud",
        null=True, blank=True
    )    
    longitude = models.CharField(
        max_length=200,
        verbose_name="longitud",
        null=True, blank=True
    )

    class Meta:
        unique_together = ('farm', 'sub_name')

    def __str__(self):
        if self.sub_name:
            return f"{self.farm.name} - {self.sub_name}"
        return f"{self.farm.name}"


class Deforestation(models.Model):
    sub_farm = models.ForeignKey(
        SubFarm,
        verbose_name="sub_farm",
        on_delete=models.CASCADE,
        related_name="farm_deforestation"
    )

    level = models.CharField(
        max_length=500,
        verbose_name="Nivel riesgo deforestación desde oficina"
    )

    fase = models.CharField(
        max_length=500,
        verbose_name="Fase"
    )


class ERDA(models.Model):
    sub_farm = models.ForeignKey(
        SubFarm,
        verbose_name="sub_farm",
        on_delete=models.CASCADE,
        related_name="farm_erda"
    )

    risk = models.BooleanField(
        verbose_name="At Risk of Deforestation"
    )
    polygon_source = models.CharField(
        max_length=500,
        verbose_name="Polygono Source"
    )
    area_pol = models.FloatField(
        max_length=200,
        verbose_name="area_pol",
        null=True, blank=True
    )


