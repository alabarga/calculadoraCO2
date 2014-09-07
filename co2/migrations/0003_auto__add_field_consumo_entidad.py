# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Consumo.entidad'
        db.add_column('co2_consumo', 'entidad',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['co2.Entidad'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Consumo.entidad'
        db.delete_column('co2_consumo', 'entidad_id')


    models = {
        'co2.consumo': {
            'Meta': {'ordering': "('object_id', 'ano', 'mes')", 'object_name': 'Consumo'},
            'ano': ('django.db.models.fields.IntegerField', [], {}),
            'co2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'entidad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.Entidad']", 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 11, 14, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mes': ('django.db.models.fields.IntegerField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'recurso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.Recurso']"}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        'co2.entidad': {
            'Meta': {'object_name': 'Entidad'},
            'descripcion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'co2.local': {
            'Meta': {'object_name': 'Local'},
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entidad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.Entidad']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm2': ('django.db.models.fields.FloatField', [], {}),
            'mix_electrico': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'personas': ('django.db.models.fields.IntegerField', [], {}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.TipoLocal']"})
        },
        'co2.medida': {
            'Meta': {'object_name': 'Medida'},
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'factorCO2': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recurso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.Recurso']"}),
            'unidades': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.Unidad']"})
        },
        'co2.recurso': {
            'Meta': {'object_name': 'Recurso'},
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unidades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['co2.Unidad']", 'symmetrical': 'False'})
        },
        'co2.tipolocal': {
            'Meta': {'object_name': 'TipoLocal'},
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'co2.tipovehiculo': {
            'Meta': {'object_name': 'TipoVehiculo'},
            'consumoKm': ('django.db.models.fields.FloatField', [], {}),
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'emisionesCO2': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'co2.unidad': {
            'Meta': {'object_name': 'Unidad'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'co2.vehiculo': {
            'Meta': {'object_name': 'Vehiculo'},
            'consumoKm': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'emisionesCO2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'entidad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.Entidad']"}),
            'fecha_compra': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.TipoVehiculo']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['co2']