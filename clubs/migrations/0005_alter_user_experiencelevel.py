<<<<<<< HEAD
# Generated by Django 3.2.5 on 2021-12-14 15:52
=======
# Generated by Django 3.2.5 on 2021-12-14 11:58
>>>>>>> 622bc270ed20f90256556e61d39eb4ec38e03074

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='experienceLevel',
            field=models.CharField(choices=[('Expert', 'Expert'), ('Advanced', 'Advanced'), ('Intermediate', 'Intermediate'), ('Beginner', 'Beginner')], default='BEGINNER', max_length=20),
        ),
    ]
