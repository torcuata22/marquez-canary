# Generated by Django 5.1.1 on 2024-09-22 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_github', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitHubRepository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo_name', models.CharField(max_length=255)),
                ('repo_url', models.URLField()),
                ('retrievd_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='google_github.user')),
            ],
        ),
    ]
