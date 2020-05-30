# Generated by Django 3.0.6 on 2020-05-09 09:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organ', '0001_initial'),
        ('basedata', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.DateField(blank=True, null=True, verbose_name='begin date')),
                ('end', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('creator', models.CharField(blank=True, max_length=20, null=True, verbose_name='creator')),
                ('modifier', models.CharField(blank=True, max_length=20, null=True, verbose_name='modifier')),
                ('creation', models.DateTimeField(auto_now_add=True, null=True, verbose_name='creation')),
                ('modification', models.DateTimeField(auto_now=True, null=True, verbose_name='modification')),
                ('begin_time', models.DateTimeField(verbose_name='begin time')),
                ('end_time', models.DateTimeField(verbose_name='end time')),
                ('enroll_deadline', models.DateTimeField(blank=True, null=True, verbose_name='enroll deadline')),
                ('code', models.CharField(blank=True, max_length=20, null=True, verbose_name='code')),
                ('title', models.CharField(max_length=120, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('host', models.CharField(blank=True, max_length=80, null=True, verbose_name='host')),
                ('speaker', models.CharField(blank=True, max_length=80, null=True, verbose_name='speaker')),
                ('accept_enroll', models.BooleanField(default=1, verbose_name='accept enroll')),
                ('location', models.CharField(blank=True, max_length=80, null=True, verbose_name='location')),
                ('classification', models.CharField(blank=True, choices=[('T', 'Train'), ('M', 'Meeting'), ('G', 'Community')], default='M', max_length=2, null=True, verbose_name='classification')),
                ('mail_list', models.TextField(blank=True, null=True, verbose_name='mail list')),
                ('mail_notice', models.BooleanField(default=1, verbose_name='mail notice')),
                ('short_message_notice', models.BooleanField(default=1, verbose_name='short message notice')),
                ('weixin_notice', models.BooleanField(default=1, verbose_name='weixin notice')),
                ('status', models.BooleanField(default=0, verbose_name='published')),
                ('publish_time', models.DateTimeField(blank=True, null=True, verbose_name='publish time')),
                ('attach', models.FileField(blank=True, null=True, upload_to='activity', verbose_name='attach')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='selfhelp.Activity', verbose_name='parent')),
                ('room', models.ForeignKey(blank=True, limit_choices_to={'tp': 20}, null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Material', verbose_name='room')),
            ],
            options={
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.DateField(blank=True, null=True, verbose_name='begin date')),
                ('end', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('creator', models.CharField(blank=True, max_length=20, null=True, verbose_name='creator')),
                ('modifier', models.CharField(blank=True, max_length=20, null=True, verbose_name='modifier')),
                ('creation', models.DateTimeField(auto_now_add=True, null=True, verbose_name='creation')),
                ('modification', models.DateTimeField(auto_now=True, null=True, verbose_name='modification')),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='loan code')),
                ('title', models.CharField(max_length=120, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('status', models.CharField(blank=True, choices=[('N', 'NEW'), ('I', 'IN PROGRESS'), ('A', 'APPROVED'), ('P', 'PAYED')], default='N', max_length=2, null=True, verbose_name='status')),
                ('logout_time', models.DateTimeField(blank=True, null=True, verbose_name='logout time')),
                ('loan_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='loan amount')),
                ('logout_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='logout amount')),
                ('pay_user', models.CharField(blank=True, max_length=40, null=True, verbose_name='pay user')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='pay time')),
                ('is_clear', models.BooleanField(default=False, verbose_name='is clear')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basedata.Project', verbose_name='project')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'loan',
                'verbose_name_plural': 'loans',
                'permissions': (('financial_pay', 'financial pay'),),
            },
        ),
        migrations.CreateModel(
            name='Reimbursement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.DateField(blank=True, null=True, verbose_name='begin date')),
                ('end', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('creator', models.CharField(blank=True, max_length=20, null=True, verbose_name='creator')),
                ('modifier', models.CharField(blank=True, max_length=20, null=True, verbose_name='modifier')),
                ('creation', models.DateTimeField(auto_now_add=True, null=True, verbose_name='creation')),
                ('modification', models.DateTimeField(auto_now=True, null=True, verbose_name='modification')),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='fee code')),
                ('title', models.CharField(max_length=120, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('bank_account', models.CharField(blank=True, max_length=120, null=True, verbose_name='bank account')),
                ('status', models.CharField(blank=True, choices=[('N', 'NEW'), ('I', 'IN PROGRESS'), ('A', 'APPROVED'), ('P', 'PAYED')], default='N', max_length=2, null=True, verbose_name='status')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='amount of money')),
                ('loan_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='loan amount')),
                ('logout_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='logout amount')),
                ('pay_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='pay amount')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='pay time')),
                ('pay_user', models.CharField(blank=True, max_length=40, null=True, verbose_name='pay user')),
                ('loan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='selfhelp.Loan', verbose_name='loan record')),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organ.OrgUnit', verbose_name='cost center')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basedata.Project', verbose_name='project')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'reimbursement',
                'verbose_name_plural': 'reimbursements',
                'permissions': (('financial_pay', 'financial pay'),),
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.DateField(blank=True, null=True, verbose_name='begin date')),
                ('end', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('creator', models.CharField(blank=True, max_length=20, null=True, verbose_name='creator')),
                ('modifier', models.CharField(blank=True, max_length=20, null=True, verbose_name='modifier')),
                ('creation', models.DateTimeField(auto_now_add=True, null=True, verbose_name='creation')),
                ('modification', models.DateTimeField(auto_now=True, null=True, verbose_name='modification')),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='workorder code')),
                ('title', models.CharField(max_length=120, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('business_domain', models.CharField(choices=[('HR', '人事'), ('FI', '财务'), ('AD', '行政'), ('MA', '市场'), ('BU', '商务'), ('CS', '客服'), ('OT', '其他'), ('PO', '采购')], default='OT', max_length=4, verbose_name='business domain')),
                ('classification', models.CharField(choices=[('S', '内部服务'), ('R', '设备维修'), ('Q', '问题咨询'), ('D', '采购申请')], default='D', max_length=4, verbose_name='classification')),
                ('status', models.CharField(blank=True, choices=[('NEW', '新建'), ('SCHE', '调度'), ('PROC', '处理'), ('CLOSE', '关闭')], default='NEW', max_length=6, null=True, verbose_name='status')),
                ('answer', models.TextField(blank=True, null=True, verbose_name='answer')),
                ('attach', models.FileField(blank=True, help_text='工单附件，不导入明细。', null=True, upload_to='', verbose_name='attach')),
                ('detail', models.FileField(blank=True, help_text='您可导入需求明细，模板请参考文档FD0007', null=True, upload_to='', verbose_name='to be imported detail')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Project', verbose_name='project')),
                ('refer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='selfhelp.WorkOrder', verbose_name='refer wo')),
                ('service', models.ForeignKey(blank=True, limit_choices_to={'is_virtual': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Material', verbose_name='service name')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'workorder apply',
                'verbose_name_plural': 'workorder apply',
            },
        ),
        migrations.CreateModel(
            name='WOItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='amount')),
                ('price', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='price')),
                ('material', models.ForeignKey(blank=True, limit_choices_to={'is_virtual': '0'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Material', verbose_name='material')),
                ('measure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Measure', verbose_name='measure')),
                ('workorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selfhelp.WorkOrder', verbose_name='workorder')),
            ],
            options={
                'verbose_name': 'workorder item',
                'verbose_name_plural': 'workorder items',
            },
        ),
        migrations.CreateModel(
            name='WOExtraValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('param_value', models.CharField(blank=True, max_length=40, null=True, verbose_name='param value')),
                ('param_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basedata.ExtraParam', verbose_name='extra param')),
                ('workorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selfhelp.WorkOrder', verbose_name='workorder')),
            ],
            options={
                'verbose_name': 'extra value',
                'verbose_name_plural': 'extra values',
            },
        ),
        migrations.CreateModel(
            name='ReimbursementItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.DateField(default=datetime.date.today, verbose_name='occur date')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='amount of money')),
                ('memo', models.CharField(blank=True, max_length=40, null=True, verbose_name='memo')),
                ('expense_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basedata.ExpenseAccount', verbose_name='expenses account')),
                ('reimbursement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selfhelp.Reimbursement', verbose_name='reimbursement')),
            ],
            options={
                'verbose_name': 'fee item',
                'verbose_name_plural': 'fee items',
            },
        ),
        migrations.AddField(
            model_name='reimbursement',
            name='wo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='selfhelp.WorkOrder', verbose_name='work order'),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_time', models.DateTimeField(auto_now_add=True, verbose_name='feedback time')),
                ('rank', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='B', max_length=2, null=True, verbose_name='rank')),
                ('comment', models.CharField(blank=True, max_length=80, null=True, verbose_name='suggest')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selfhelp.Activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enroll_time', models.DateTimeField(auto_now_add=True, verbose_name='enroll time')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selfhelp.Activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
