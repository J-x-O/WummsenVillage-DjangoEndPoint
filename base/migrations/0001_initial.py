# Generated by Django 4.1.7 on 2023-02-24 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=32)),
                ('player_tag', models.PositiveSmallIntegerField()),
                ('player_elo', models.IntegerField(blank=True, default=1000)),
            ],
            options={
                'unique_together': {('player_name', 'player_tag')},
            },
        ),
        migrations.CreateModel(
            name='PlayerSecured',
            fields=[
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.player')),
                ('player_email', models.CharField(max_length=100)),
                ('player_password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerTemporary',
            fields=[
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.player')),
                ('player_temporary_password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('patch_id', models.CharField(max_length=10)),
                ('finalized', models.BooleanField(blank=True, default=False)),
                ('players', models.ManyToManyField(blank=True, related_name='played_sessions', to='base.player')),
                ('winner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_sessions', to='base.player')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_id', models.PositiveSmallIntegerField()),
                ('outcome', models.CharField(blank=True, default='', max_length=10)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.session')),
                ('winner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.player')),
            ],
            options={
                'unique_together': {('session', 'round_id')},
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=32)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('payload', models.CharField(max_length=150)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.round')),
            ],
        ),
    ]
