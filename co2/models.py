# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from datetime import date

from django.db.models import Max, Sum, Avg

import locale
locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")

class Acumulado(models.Model):
    ano = models.IntegerField()
    mes = models.IntegerField()
    co2 = models.FloatField()
    acumulado = models.FloatField()

class Unidad(models.Model):
    abreviatura = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        #ordering = ('-creation_date',)

    def __unicode__(self):
        return self.nombre

class Recurso(models.Model):
    denominacion = models.CharField(max_length=20)
    unidades = models.ManyToManyField("Unidad")

    def __unicode__(self):
        return self.denominacion

class Medida(models.Model):

    denominacion = models.CharField(max_length=30)
    recurso = models.ForeignKey("Recurso")
    unidades  = models.ForeignKey("Unidad")
    factorCO2 = models.FloatField()
    descripcion = models.TextField()

    def __unicode__(self):
        return "%s (%s)" % (self.denominacion,self.unidades.abreviatura)

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'unidad' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['unidad'].pk
            del(kwargs['unidad'])
        return super(ItemManager, self).get(*args, **kwargs)

class Consumo(models.Model):
    ano = models.IntegerField()
    mes = models.IntegerField()
    fecha = models.DateField(default = date.today())    

    # unidad de coste as generic relation
    content_type = models.ForeignKey(ContentType, limit_choices_to = {'model__in': ['Vehiculo','Local']})
    object_id = models.PositiveIntegerField()
    unidad = generic.GenericForeignKey('content_type', 'object_id')
    entidad = models.ForeignKey("Entidad", blank=True, null=True, related_name="consumos")
    medida = models.ForeignKey("Medida")
    valor = models.FloatField()
    co2 = models.FloatField(blank=True, null=True)

    objects = ItemManager()

    def save(self):
        if self.id is None:
            if self.co2 is None:
                self.co2 = self.valor * self.medida.factorCO2
            if self.entidad is None:    
                self.entidad = self.unidad.entidad

        super(Consumo, self).save()    

    def __unicode__(self):
        return "%s (%s) en %s" % (self.medida.denominacion,self.medida.unidades.abreviatura,date(self.ano,self.mes,1).strftime("%B de %Y"))

    class Meta:
        ordering = ('object_id','-ano','-mes')

    # unidad
    #def get_unidad(self):
    #    return self.content_type.get_object_for_this_type(id=self.object_id)

    #def set_unidad(self, unidad):
    #    self.content_type = ContentType.objects.get_for_model(type(unidad))
    #    self.object_id = unidad.pk

    #unidad = property(get_unidad, set_unidad)

class TipoVehiculo(models.Model):

    denominacion = models.CharField(max_length=30)
    consumoKm = models.FloatField()
    emisionesCO2 = models.FloatField()
    def __unicode__(self):
        return self.denominacion

class Vehiculo(models.Model):

    entidad = models.ForeignKey("Entidad",related_name="vehiculos")  
    denominacion = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, null=True)    
    tipo = models.ForeignKey("TipoVehiculo")
    consumoKm = models.FloatField(blank=True, null=True)
    emisionesCO2 = models.FloatField(blank=True, null=True)
    fecha_compra = models.IntegerField(blank=True, null=True)
    consumos = generic.GenericRelation(Consumo)

    def get_years(self):
        #a = Consumo.objects.filter(content_type__name = 'Vehiculo', object_id=self.id).aggregate(year=Max('ano'))
        a = list(set(self.consumos.values_list('ano', flat=True)))
        return sorted(a, reverse=True)

    def save(self):
        if self.id is None:
            self.emisionesCO2 = self.tipo.emisionesCO2
            self.consumoKm = self.tipo.consumoKm
        super(Vehiculo, self).save()    


    class Meta:
        verbose_name = 'Vehiculo'
        verbose_name_plural = 'Vehiculos'
        #ordering = ('-creation_date',)

    def __unicode__(self):
        return self.denominacion    

class TipoLocal(models.Model):

    denominacion = models.CharField(max_length=30)

    def __unicode__(self):
        return self.denominacion


class Local(models.Model):

    entidad = models.ForeignKey("Entidad",related_name="locales")
    tipo = models.ForeignKey("TipoLocal")
    denominacion = models.CharField(max_length=30)
    descripcion = models.TextField(blank=True, null=True)

    mix_electrico = models.FloatField(default=1.0)
    m2 = models.FloatField()
    personas = models.IntegerField()

    consumos = generic.GenericRelation(Consumo)

    def get_years(self):
        #a = Consumo.objects.filter(content_type__name = 'Local', object_id=self.id).aggregate(year=Max('ano'))
        a = list(set(self.consumos.values_list('ano', flat=True)))
        return sorted(a, reverse=True)

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locales'
        #ordering = ('-creation_date',)

    def consumos(self):
        return Consumo.objects.filter(entidad__id=self.entidad.id,content_type__name='Local',object_id=self.id)

    def __unicode__(self):
        return self.denominacion

class Entidad(models.Model):

    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(blank=True, null=True)

    @property
    def ultimos_consumos(self):

        a = self.consumos.all().aggregate(year=Max('ano'))
        year = int(a['year'])

        a = self.consumos.filter(ano=year).aggregate(consumos=Sum('co2'))

        consumos = a['consumos'] / 1000
        return consumos

    @property
    def reduccion_consumo(self):

        a = self.consumos.all().aggregate(year=Max('ano'))
        previous_year = a['year']

        a = self.consumos.filter(ano=previous_year).aggregate(consumos=Sum('co2'))
        consumo_ultimo = a['consumos'] 
 
        a = self.consumos.filter(ano=2011).aggregate(consumos=Sum('co2'))
        consumo_2011 = a['consumos'] 

        reduccion = 100 * (consumo_2011 - consumo_ultimo) / consumo_2011

        return reduccion

    class Meta:
        verbose_name = 'Entidad'        
        verbose_name_plural = 'Entidades'
        #ordering = ('-creation_date',)

    def __unicode__(self):
        return self.nombre

###################################################################### 

from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):  
    user = models.OneToOneField(User)  
    #other fields here

    def __str__(self):  
          return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 

User.profile = property(lambda u: u.get_profile() )

######################################################################        
