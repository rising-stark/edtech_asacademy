# Generated by Django 3.2.9 on 2021-12-30 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_code', models.CharField(max_length=10)),
                ('course_name', models.CharField(max_length=200)),
                ('course_starts_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('course_ends_at', models.DateTimeField(blank=True, null=True)),
                ('course_price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.parents')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teaches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.courses')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.teachers')),
            ],
        ),
        migrations.CreateModel(
            name='Takes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.courses')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.students')),
            ],
        ),
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('lesson_id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson_link', models.CharField(max_length=200)),
                ('lesson_starts_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('lesson_ends_at', models.DateTimeField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.courses')),
                ('lesson_taken_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.teachers')),
            ],
        ),
    ]
