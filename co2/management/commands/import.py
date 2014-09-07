# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.contrib.auth.models import User
import datetime
import csv

from co2.models import *

class Command(BaseCommand):
    args = '<file ...>'
    help = 'Load historic data'

    def handle(self, *args, **options):

        if ((len(args) == 1) 

            # Full path and name to your csv file
            #archivo ="/home/alabarga/Proyectos/BigFoot/datos2012.txt"
            archivo = args[0]

            datareader = csv.reader(open(archivo), delimiter='\t', quotechar='"')
            headerline = datareader.next()
            for row in datareader:
                print row              
                c = Consumo()
                c.ano = 2012 #row[0]
                c.mes = row[0]
                recurso = Recurso.objects.get(denominacion__iexact = row[1])
                if recurso == Recurso.objects.get(pk=2):
                    unidades = Unidad.objects.get(pk=1)
                else:
                    unidades = Unidad.objects.get(pk=3)

                #unidades = Unidad.objects.get(nombre = row[3])
                c.medida = Medida.objects.get(recurso = recurso, unidades = unidades)
                c.entidad = Entidad.objects.get(pk=1)
                c.content_type = ContentType.objects.get(model='Local')
                c.object_id = Local.objects.get(denominacion__iexact = row[4]).id
                c.valor = row[3]
                c.co2 = 0

                #try:
                #    c.co2 =  float(row[7].replace(',', '.'))
                #except ValueError:
                #    c.co2 = 0
                #c.save()

        else:        	
            print "Necesito un nombre de archivo"
            print "['Año', 'Mes', 'Recurso', 'Unidad', 'Valor', 'Local', 'KJul', 'CO2']"
            print "['2003', '11', 'gasoleo', 'litros', '5499', 'Sarasa', '217,148', '14,627']"