from django.db import migrations, models

class Migration(migrations.Migration):
    initial=True
    dependencies=[
    ]

    operations=[
        migrations.CreateModel(
            name='Employee',
            fields=[
                 ('name', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='name')),
                ('email', models.CharField(max_length=220)),
                ('amount', models.CharField(max_length=100)),
            ],
        ),
    ]

