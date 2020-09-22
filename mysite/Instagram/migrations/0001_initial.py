# Generated by Django 3.1.1 on 2020-09-10 16:56

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.TextField(default='null')),
                ('Description', models.TextField(default='null')),
                ('Image', models.ImageField(default='images/dummy.png', upload_to='posts/%y/%m/%d/%H/%m/%S/')),
                ('Vedio', models.TextField(default='null')),
                ('DateTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.CharField(default='noname', max_length=30, validators=[django.core.validators.RegexValidator(code='invalid_firstname', message='First name must be Alphanumeric', regex='^[a-zA-Z]*$')])),
                ('Last_Name', models.CharField(default='noname', max_length=30, validators=[django.core.validators.RegexValidator(code='invalid_lastname', message='Last name must be Alphanumeric', regex='^[a-zA-Z]*$')])),
                ('Email', models.CharField(default='noname', max_length=200, validators=[django.core.validators.RegexValidator(code='invalid_email', message='Email must be valid', regex='^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$')])),
                ('Username', models.CharField(default='noname', max_length=200)),
                ('Password', models.CharField(max_length=256)),
                ('Role', models.CharField(default='user', max_length=256)),
                ('Status', models.BooleanField(default=False)),
                ('Is_Email_Verified', models.BooleanField(default=False)),
                ('Gender', models.CharField(default='null', max_length=256)),
                ('image', models.ImageField(default='images/dummy.png', upload_to='images/%y/%m/%d/%H/%m/%S/')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SubscribedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscibed_user', to='Instagram.user')),
                ('SubscriberUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subsciber_user', to='Instagram.user')),
            ],
        ),
        migrations.CreateModel(
            name='Seens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SeenPost', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='seen_post', to='Instagram.post')),
                ('SeenUser', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='seen_user', to='Instagram.user')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Instagram.user'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.TextField(default='null')),
                ('DateTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('Post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Instagram.post')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Instagram.user')),
            ],
        ),
    ]