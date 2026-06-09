from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("points", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pointsrecord",
            name="type",
            field=models.CharField(
                choices=[
                    ("blindbox_consume", "盲盒消费"),
                    ("recycle_return", "回收返还"),
                    ("system_adjust", "系统调整"),
                    ("recharge", "充值"),
                ],
                max_length=30,
                verbose_name="变动类型",
            ),
        ),
    ]
