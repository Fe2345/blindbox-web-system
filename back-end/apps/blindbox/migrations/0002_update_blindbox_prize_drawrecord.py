# Generated manually

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blindbox', '0001_initial'),
        ('assets', '0001_initial'),
    ]

    operations = [
        # === BlindBox: 新增字段 ===
        migrations.AddField(
            model_name='blindbox',
            name='ip_name',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='所属IP'),
        ),
        migrations.AddField(
            model_name='blindbox',
            name='max_draw_count',
            field=models.PositiveIntegerField(default=10, verbose_name='单次最大抽取次数'),
        ),
        migrations.AddField(
            model_name='blindbox',
            name='allow_simulation',
            field=models.BooleanField(default=True, verbose_name='是否允许模拟抽取'),
        ),
        migrations.AddField(
            model_name='blindbox',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='展示排序'),
        ),
        migrations.AlterModelOptions(
            name='blindbox',
            options={'ordering': ['sort_order', '-created_at'], 'verbose_name': '盲盒', 'verbose_name_plural': '盲盒'},
        ),

        # === Prize: 新增 BaseModel 时间字段 + 新业务字段 ===
        migrations.AddField(
            model_name='prize',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prize',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='prize',
            name='weight',
            field=models.PositiveIntegerField(default=0, verbose_name='抽取权重'),
        ),
        migrations.AddField(
            model_name='prize',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='奖品总数量'),
        ),
        migrations.AddField(
            model_name='prize',
            name='remaining_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='奖品剩余数量'),
        ),
        migrations.AddField(
            model_name='prize',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否参与抽取'),
        ),
        migrations.AddField(
            model_name='prize',
            name='ip_name_snapshot',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='奖品IP快照'),
        ),
        # 将旧 stock 数据迁移到 quantity 和 remaining_quantity
        migrations.RunSQL(
            sql="UPDATE blindbox_prize SET quantity = stock, remaining_quantity = stock;",
            reverse_sql="UPDATE blindbox_prize SET stock = quantity;",
        ),
        migrations.RemoveField(
            model_name='prize',
            name='stock',
        ),

        # === DrawRecord: 新增字段 ===
        migrations.AddField(
            model_name='drawrecord',
            name='asset',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='draw_records',
                to='assets.asset',
                verbose_name='关联资产',
            ),
        ),
        migrations.AddField(
            model_name='drawrecord',
            name='remaining_points',
            field=models.PositiveIntegerField(default=0, verbose_name='抽取后剩余积分'),
        ),
        migrations.AddField(
            model_name='drawrecord',
            name='batch_no',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='抽取批次号'),
        ),
        migrations.AddField(
            model_name='drawrecord',
            name='draw_type',
            field=models.CharField(
                choices=[('real', '真实抽取'), ('simulation', '模拟抽取')],
                default='real',
                max_length=20,
                verbose_name='抽取类型',
            ),
        ),
        migrations.AddField(
            model_name='drawrecord',
            name='draw_status',
            field=models.CharField(
                choices=[('success', '成功'), ('failed', '失败')],
                default='success',
                max_length=20,
                verbose_name='抽取状态',
            ),
        ),
        migrations.AddField(
            model_name='drawrecord',
            name='ip_name_snapshot',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='IP快照'),
        ),
    ]
