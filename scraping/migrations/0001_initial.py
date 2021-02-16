# Generated by Django 3.0.12 on 2021-02-16 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(null=True)),
                ('squad', models.CharField(blank=True, max_length=255, null=True)),
                ('games', models.IntegerField(null=True)),
                ('wins', models.IntegerField(null=True)),
                ('draws', models.IntegerField(null=True)),
                ('losses', models.IntegerField(null=True)),
                ('goals_for', models.IntegerField(null=True)),
                ('goals_against', models.IntegerField(null=True)),
                ('goals_difference', models.IntegerField(null=True)),
                ('points', models.IntegerField(null=True)),
            ],
        ),
    ]
