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
