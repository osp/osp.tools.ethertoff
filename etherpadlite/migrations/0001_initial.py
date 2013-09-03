# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PadServer'
        db.create_table(u'etherpadlite_padserver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=256)),
            ('apikey', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'etherpadlite', ['PadServer'])

        # Adding model 'PadGroup'
        db.create_table(u'etherpadlite_padgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('groupID', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['etherpadlite.PadServer'])),
        ))
        db.send_create_signal(u'etherpadlite', ['PadGroup'])

        # Adding model 'PadAuthor'
        db.create_table(u'etherpadlite_padauthor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('authorID', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['etherpadlite.PadServer'])),
        ))
        db.send_create_signal(u'etherpadlite', ['PadAuthor'])

        # Adding M2M table for field group on 'PadAuthor'
        m2m_table_name = db.shorten_name(u'etherpadlite_padauthor_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('padauthor', models.ForeignKey(orm[u'etherpadlite.padauthor'], null=False)),
            ('padgroup', models.ForeignKey(orm[u'etherpadlite.padgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['padauthor_id', 'padgroup_id'])

        # Adding model 'Pad'
        db.create_table(u'etherpadlite_pad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['etherpadlite.PadServer'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['etherpadlite.PadGroup'])),
        ))
        db.send_create_signal(u'etherpadlite', ['Pad'])


    def backwards(self, orm):
        # Deleting model 'PadServer'
        db.delete_table(u'etherpadlite_padserver')

        # Deleting model 'PadGroup'
        db.delete_table(u'etherpadlite_padgroup')

        # Deleting model 'PadAuthor'
        db.delete_table(u'etherpadlite_padauthor')

        # Removing M2M table for field group on 'PadAuthor'
        db.delete_table(db.shorten_name(u'etherpadlite_padauthor_group'))

        # Deleting model 'Pad'
        db.delete_table(u'etherpadlite_pad')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'etherpadlite.pad': {
            'Meta': {'object_name': 'Pad'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['etherpadlite.PadGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['etherpadlite.PadServer']"})
        },
        u'etherpadlite.padauthor': {
            'Meta': {'object_name': 'PadAuthor'},
            'authorID': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'authors'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['etherpadlite.PadGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['etherpadlite.PadServer']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'etherpadlite.padgroup': {
            'Meta': {'object_name': 'PadGroup'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            'groupID': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['etherpadlite.PadServer']"})
        },
        u'etherpadlite.padserver': {
            'Meta': {'object_name': 'PadServer'},
            'apikey': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['etherpadlite']