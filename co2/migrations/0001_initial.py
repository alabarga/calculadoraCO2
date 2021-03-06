# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Unidad'
        db.create_table('co2_unidad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abreviatura', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('co2', ['Unidad'])

        # Adding model 'Recurso'
        db.create_table('co2_recurso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('denominacion', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('unidades', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['co2.Unidad'])),
            ('factorCO2', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('co2', ['Recurso'])

        # Adding model 'TipoVehiculo'
        db.create_table('co2_tipovehiculo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('denominacion', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('consumoKm', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('co2', ['TipoVehiculo'])

        # Adding model 'TipoLocal'
        db.create_table('co2_tipolocal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('denominacion', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('factorCO2', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('co2', ['TipoLocal'])

        # Adding model 'Entidad'
        db.create_table('co2_entidad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('co2', ['Entidad'])

        # Adding model 'Local'
        db.create_table('co2_local', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['co2.Entidad'])),
            ('denominacion', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m2', self.gf('django.db.models.fields.FloatField')()),
            ('personas', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('co2', ['Local'])

        # Adding model 'Vehiculo'
        db.create_table('co2_vehiculo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['co2.Entidad'])),
            ('denominacion', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['co2.TipoVehiculo'])),
        ))
        db.send_create_signal('co2', ['Vehiculo'])

        # Adding model 'Medida'
        db.create_table('co2_medida', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('denominacion', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('co2', ['Medida'])

        # Adding M2M table for field unidades on 'Medida'
        db.create_table('co2_medida_unidades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('medida', models.ForeignKey(orm['co2.medida'], null=False)),
            ('unidad', models.ForeignKey(orm['co2.unidad'], null=False))
        ))
        db.create_unique('co2_medida_unidades', ['medida_id', 'unidad_id'])

        # Adding model 'Consumo'
        db.create_table('co2_consumo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ano', self.gf('django.db.models.fields.IntegerField')()),
            ('mes', self.gf('django.db.models.fields.IntegerField')()),
            ('fecha', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 11, 13, 0, 0))),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('recurso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['co2.Recurso'])),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
            ('co2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('co2', ['Consumo'])


    def backwards(self, orm):
        # Deleting model 'Unidad'
        db.delete_table('co2_unidad')

        # Deleting model 'Recurso'
        db.delete_table('co2_recurso')

        # Deleting model 'TipoVehiculo'
        db.delete_table('co2_tipovehiculo')

        # Deleting model 'TipoLocal'
        db.delete_table('co2_tipolocal')

        # Deleting model 'Entidad'
        db.delete_table('co2_entidad')

        # Deleting model 'Local'
        db.delete_table('co2_local')

        # Deleting model 'Vehiculo'
        db.delete_table('co2_vehiculo')

        # Deleting model 'Medida'
        db.delete_table('co2_medida')

        # Removing M2M table for field unidades on 'Medida'
        db.delete_table('co2_medida_unidades')

        # Deleting model 'Consumo'
        db.delete_table('co2_consumo')


    models = {
        'co2.consumo': {
            'Meta': {'object_name': 'Consumo'},
            'ano': ('django.db.models.fields.IntegerField', [], {}),
            'co2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 11, 13, 0, 0)'}),
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
            'personas': ('django.db.models.fields.IntegerField', [], {})
        },
        'co2.medida': {
            'Meta': {'object_name': 'Medida'},
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unidades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['co2.Unidad']", 'symmetrical': 'False'})
        },
        'co2.recurso': {
            'Meta': {'object_name': 'Recurso'},
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'factorCO2': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unidades': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.Unidad']"})
        },
        'co2.tipolocal': {
            'Meta': {'object_name': 'TipoLocal'},
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'factorCO2': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'co2.tipovehiculo': {
            'Meta': {'object_name': 'TipoVehiculo'},
            'consumoKm': ('django.db.models.fields.FloatField', [], {}),
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
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
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entidad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['co2.Entidad']"}),
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