import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import (
    Farm,
    SubFarm,
    Deforestation,
    ERDA,
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, 'myapp/management/commands/files/farm.csv')
        # Ie.
        # Número interno de finca MOVE;Región/ Zona o cooperativa;Técnico a cargo;Nombre productor;Municipio;Departamento
        # 1626;XXXX;XXX;XXX;XXX;XX

        with open(file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')  # Especifica el separador ";"
            next(reader)  # Salta la primera fila (encabezado)
            
            for row in reader:
                name = row[0]
                owner = row[1]
                region = row[2]
                municipio = row[3]
                departamento = row[4]
        
                farm = Farm(
                    name=name,
                    owner=owner,
                    region=region,
                    municipio=municipio,
                    departamento=departamento,
                )
                farm.save()

