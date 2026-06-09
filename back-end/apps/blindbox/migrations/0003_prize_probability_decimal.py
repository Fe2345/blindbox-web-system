from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blindbox", "0002_update_blindbox_prize_drawrecord"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prize",
            name="probability",
            field=models.DecimalField(decimal_places=4, max_digits=7, verbose_name="概率(%)"),
        ),
    ]
