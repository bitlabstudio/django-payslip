# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table('payslip_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('payslip', ['Company'])

        # Adding M2M table for field extra_fields on 'Company'
        db.create_table('payslip_company_extra_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('company', models.ForeignKey(orm['payslip.company'], null=False)),
            ('extrafield', models.ForeignKey(orm['payslip.extrafield'], null=False))
        ))
        db.create_unique('payslip_company_extra_fields', ['company_id', 'extrafield_id'])

        # Adding model 'Employee'
        db.create_table('payslip_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='employees', to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='employees', to=orm['payslip.Company'])),
            ('hr_number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('payslip', ['Employee'])

        # Adding M2M table for field extra_fields on 'Employee'
        db.create_table('payslip_employee_extra_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('employee', models.ForeignKey(orm['payslip.employee'], null=False)),
            ('extrafield', models.ForeignKey(orm['payslip.extrafield'], null=False))
        ))
        db.create_unique('payslip_employee_extra_fields', ['employee_id', 'extrafield_id'])

        # Adding model 'ExtraFieldType'
        db.create_table('payslip_extrafieldtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('payslip', ['ExtraFieldType'])

        # Adding model 'ExtraField'
        db.create_table('payslip_extrafield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='extra_fields', to=orm['payslip.ExtraFieldType'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('payslip', ['ExtraField'])

        # Adding model 'PaymentType'
        db.create_table('payslip_paymenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('payslip', ['PaymentType'])

        # Adding model 'Payment'
        db.create_table('payslip_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments', to=orm['payslip.PaymentType'])),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments', to=orm['payslip.Employee'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 5, 0, 0))),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('payslip', ['Payment'])

        # Adding M2M table for field extra_fields on 'Payment'
        db.create_table('payslip_payment_extra_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('payment', models.ForeignKey(orm['payslip.payment'], null=False)),
            ('extrafield', models.ForeignKey(orm['payslip.extrafield'], null=False))
        ))
        db.create_unique('payslip_payment_extra_fields', ['payment_id', 'extrafield_id'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table('payslip_company')

        # Removing M2M table for field extra_fields on 'Company'
        db.delete_table('payslip_company_extra_fields')

        # Deleting model 'Employee'
        db.delete_table('payslip_employee')

        # Removing M2M table for field extra_fields on 'Employee'
        db.delete_table('payslip_employee_extra_fields')

        # Deleting model 'ExtraFieldType'
        db.delete_table('payslip_extrafieldtype')

        # Deleting model 'ExtraField'
        db.delete_table('payslip_extrafield')

        # Deleting model 'PaymentType'
        db.delete_table('payslip_paymenttype')

        # Deleting model 'Payment'
        db.delete_table('payslip_payment')

        # Removing M2M table for field extra_fields on 'Payment'
        db.delete_table('payslip_payment_extra_fields')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'payslip.company': {
            'Meta': {'object_name': 'Company'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['payslip.ExtraField']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'payslip.employee': {
            'Meta': {'object_name': 'Employee'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employees'", 'to': "orm['payslip.Company']"}),
            'extra_fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['payslip.ExtraField']", 'null': 'True', 'blank': 'True'}),
            'hr_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employees'", 'to': "orm['auth.User']"})
        },
        'payslip.extrafield': {
            'Meta': {'object_name': 'ExtraField'},
            'field_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extra_fields'", 'to': "orm['payslip.ExtraFieldType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'payslip.extrafieldtype': {
            'Meta': {'object_name': 'ExtraFieldType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'payslip.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 5, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments'", 'to': "orm['payslip.Employee']"}),
            'extra_fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['payslip.ExtraField']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments'", 'to': "orm['payslip.PaymentType']"})
        },
        'payslip.paymenttype': {
            'Meta': {'object_name': 'PaymentType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['payslip']