# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-25 17:11
from __future__ import unicode_literals

import uuid

import django.db.migrations.operations.special
import django.db.models.deletion
import django_extensions.db.fields
import djchoices.choices
import sortedm2m.fields
import sortedm2m.operations
import stdimage.models
import taggit.managers
from django.conf import settings
from django.db import migrations, models

import course_discovery.apps.course_metadata.utils

SEAT_TYPES = ('Audit', 'Credit', 'Professional', 'Verified',)

def add_seat_types(apps, schema_editor):
    SeatType = apps.get_model('course_metadata', 'SeatType')

    for name in SEAT_TYPES:
        SeatType.objects.update_or_create(name=name)

def drop_seat_types(apps, schema_editor):
    SeatType = apps.get_model('course_metadata', 'SeatType')
    SeatType.objects.filter(name__in=SEAT_TYPES).delete()

NAMES = ('threaded_metadata_write', 'parallel_refresh_pipeline')

def create_switches(apps, schema_editor):
    """Create the threaded_metadata_write and parallel_refresh_pipeline switches."""
    Switch = apps.get_model('waffle', 'Switch')

    for name in NAMES:
        Switch.objects.get_or_create(name=name, defaults={'active': False})

def delete_switches(apps, schema_editor):
    """Delete the threaded_metadata_write and parallel_refresh_pipeline switches."""
    Switch = apps.get_model('waffle', 'Switch')
    Switch.objects.filter(name__in=NAMES).delete()

class Migration(migrations.Migration):

    replaces = [('course_metadata', '0001_initial'), ('course_metadata', '0002_auto_20160406_1644'), ('course_metadata', '0003_auto_20160523_1422'), ('course_metadata', '0004_program'), ('course_metadata', '0005_auto_20160713_0113'), ('course_metadata', '0006_auto_20160719_2052'), ('course_metadata', '0007_auto_20160720_1749'), ('course_metadata', '0008_program_image'), ('course_metadata', '0009_auto_20160725_1751'), ('course_metadata', '0010_auto_20160731_0226'), ('course_metadata', '0011_auto_20160805_1949'), ('course_metadata', '0012_create_seat_types'), ('course_metadata', '0013_auto_20160809_1259'), ('course_metadata', '0014_auto_20160811_0436'), ('course_metadata', '0015_auto_20160813_2142'), ('course_metadata', '0016_auto_20160815_1438'), ('course_metadata', '0017_auto_20160815_2135'), ('course_metadata', '0018_auto_20160815_2252'), ('course_metadata', '0019_program_banner_image'), ('course_metadata', '0020_auto_20160819_1942'), ('course_metadata', '0021_auto_20160819_2005'), ('course_metadata', '0022_remove_duplicate_courses'), ('course_metadata', '0023_auto_20160826_1912'), ('course_metadata', '0024_auto_20160901_1426'), ('course_metadata', '0025_remove_program_category'), ('course_metadata', '0026_auto_20160912_2146'), ('course_metadata', '0027_auto_20160915_2038'), ('course_metadata', '0028_courserun_hidden'), ('course_metadata', '0029_auto_20160923_1306'), ('course_metadata', '0030_create_refresh_command_switches'), ('course_metadata', '0031_courserun_weeks_to_complete'), ('course_metadata', '0032_auto_20161021_1636'), ('course_metadata', '0033_courserun_mobile_available')]

    initial = True

    dependencies = [
        ('core', '0008_partner'),
        ('ietf_language_tags', '0002_language_tag_data_migration'),
        ('taggit', '0002_auto_20150616_2121'),
        ('waffle', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_populate_currencies'),
        ('core', '0010_auto_20160731_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('src', models.URLField(max_length=255, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('src', models.URLField(max_length=255, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_metadata.Image')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('given_name', models.CharField(max_length=255)),
                ('family_name', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_image_url', models.URLField(blank=True, null=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=('given_name', 'family_name'))),
                ('partner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Partner')),
            ],
            options={
                'verbose_name_plural': 'People',
            },
        ),
        migrations.CreateModel(
            name='Endorsement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('quote', models.TextField()),
                ('endorser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_metadata.Person'))
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='CorporateEndorsement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('corporation_name', models.CharField(max_length=128)),
                ('statement', models.TextField()),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_metadata.Image')),
                ('individual_endorsements', sortedm2m.fields.SortedManyToManyField(help_text=None, to='course_metadata.Endorsement')),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='ExpectedLearningItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='JobOutlookItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LevelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('key', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('marketing_url_path', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('homepage_url', models.URLField(blank=True, max_length=255, null=True)),
                ('logo_image_url', models.URLField(blank=True, null=True)),
                ('banner_image_url', models.URLField(blank=True, null=True)),
                ('partner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Partner')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='PersonSocialNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('type', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('blog', 'Blog'), ('others', 'Others')], db_index=True, max_length=15)),
                ('value', models.CharField(max_length=500)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_networks', to='course_metadata.Person')),
            ],
            options={
                'verbose_name_plural': 'Person SocialNetwork',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255)),
                ('organization_override', models.CharField(blank=True, max_length=255, null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_metadata.Organization')),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='course_metadata.Person')),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SeatType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name')),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='ProgramType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('applicable_seat_types', models.ManyToManyField(help_text='Seat types that qualify for completion of programs of this type. Learners completing associated courses, but enrolled in other seat types, will NOT have their completion of the course counted toward the completion of the program.', to='course_metadata.SeatType')),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('name', models.CharField(max_length=255)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('banner_image_url', models.URLField(blank=True, null=True)),
                ('card_image_url', models.URLField(blank=True, null=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, help_text='Leave this field blank to have the value generated automatically.', populate_from='name')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Partner')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('key', models.CharField(max_length=255)),
                ('title', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('short_description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('full_description', models.TextField(blank=True, default=None, null=True)),
                ('card_image_url', models.URLField(blank=True, null=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='key')),
                ('number', models.CharField(blank=True, help_text='Course number format e.g CS002x, BIO1.1x, BIO1.2x', max_length=50, null=True)),
                ('authoring_organizations', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='authored_courses', to='course_metadata.Organization')),
                ('expected_learning_items',sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='course_metadata.ExpectedLearningItem')),
                ('level_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_metadata.LevelType')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Partner')),
                ('prerequisites', models.ManyToManyField(blank=True, to='course_metadata.Prerequisite')),
                ('sponsoring_organizations', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='sponsored_courses', to='course_metadata.Organization')),
                ('subjects', models.ManyToManyField(blank=True, to='course_metadata.Subject')),
                ('video', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_metadata.Video')),
            ],
        ),
        migrations.CreateModel(
            name='SyllabusItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='course_metadata.SyllabusItem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('key', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('published', 'Published'), ('unpublished', 'Unpublished')], db_index=True, max_length=255, validators=[djchoices.choices.ChoicesValidator({'published': 'Published', 'unpublished': 'Unpublished'})])),
                ('title_override', models.CharField(blank=True, default=None, help_text="Title specific for this run of a course. Leave this value blank to default to the parent course's title.", max_length=255, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('enrollment_start', models.DateTimeField(blank=True, null=True)),
                ('enrollment_end', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('announcement', models.DateTimeField(blank=True, null=True)),
                ('short_description_override', models.CharField(blank=True, default=None, help_text="Short description specific for this run of a course. Leave this value blank to default to the parent course's short_description attribute.", max_length=255, null=True)),
                ('full_description_override', models.TextField(blank=True, default=None, help_text="Full description specific for this run of a course. Leave this value blank to default to the parent course's full_description attribute.", null=True)),
                ('min_effort', models.PositiveSmallIntegerField(blank=True, help_text='Estimated minimum number of hours per week needed to complete a course run.', null=True)),
                ('max_effort', models.PositiveSmallIntegerField(blank=True, help_text='Estimated maximum number of hours per week needed to complete a course run.', null=True)),
                ('weeks_to_complete', models.PositiveSmallIntegerField(blank=True, help_text='Estimated number of weeks needed to complete this course run.', null=True)),
                ('pacing_type', models.CharField(blank=True, choices=[('instructor_paced', 'Instructor-paced'), ('self_paced', 'Self-paced')], db_index=True, max_length=255, null=True, validators=[djchoices.choices.ChoicesValidator({'instructor_paced': 'Instructor-paced', 'self_paced': 'Self-paced'})])),
                ('card_image_url', models.URLField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('hidden', models.BooleanField(default=False)),
                ('mobile_available', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_runs', to='course_metadata.Course')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ietf_language_tags.LanguageTag')),
                ('staff', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='courses_staffed', to='course_metadata.Person')),
                ('syllabus', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_metadata.SyllabusItem')),
                ('transcript_languages', models.ManyToManyField(blank=True, related_name='transcript_courses', to='ietf_language_tags.LanguageTag')),
                ('video', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_metadata.Video')),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('type', models.CharField(choices=[('honor', 'Honor'), ('audit', 'Audit'), ('verified', 'Verified'), ('professional', 'Professional'), ('credit', 'Credit')], max_length=63)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('upgrade_deadline', models.DateTimeField(blank=True, null=True)),
                ('credit_provider', models.CharField(blank=True, max_length=255, null=True)),
                ('credit_hours', models.IntegerField(blank=True, null=True)),
                ('course_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='course_metadata.CourseRun')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRunSocialNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('type', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('blog', 'Blog'), ('others', 'Others')], db_index=True, max_length=15)),
                ('value', models.CharField(max_length=500)),
                ('course_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_run_networks', to='course_metadata.CourseRun')),
            ],
            options={
                'verbose_name_plural': 'CourseRun SocialNetwork',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('title', models.CharField(help_text='The user-facing display title for this Program.', max_length=255, unique=True)),
                ('subtitle', models.CharField(blank=True, help_text='A brief, descriptive subtitle for the Program.', max_length=255)),
                ('status', models.CharField(choices=[('unpublished', 'Unpublished'), ('active', 'Active'), ('retired', 'Retired'), ('deleted', 'Deleted')], db_index=True, help_text='The lifecycle status of this Program.', max_length=24, validators=[djchoices.choices.ChoicesValidator({'active': 'Active', 'deleted': 'Deleted', 'retired': 'Retired', 'unpublished': 'Unpublished'})])),
                ('marketing_slug', models.CharField(blank=True, db_index=True, help_text='Slug used to generate links to the marketing site', max_length=255)),
                ('order_courses_by_start_date', models.BooleanField(default=True, help_text='If this box is not checked, courses will be ordered as in the courses select box above.', verbose_name='Order Courses By Start Date')),
                ('overview', models.TextField(blank=True, null=True)),
                ('weeks_to_complete', models.PositiveSmallIntegerField(blank=True, help_text='This field is now deprecated (ECOM-6021).Estimated number of weeks needed to complete a course run belonging to this program.', null=True)),
                ('min_hours_effort_per_week', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('max_hours_effort_per_week', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('banner_image', stdimage.models.StdImageField(blank=True, null=True, upload_to=course_discovery.apps.course_metadata.utils.UploadToFieldNamePath('uuid', path='media/programs/banner_images'))),
                ('banner_image_url', models.URLField(blank=True, help_text='Image used atop detail pages', null=True)),
                ('card_image_url', models.URLField(blank=True, help_text='Image used for discovery cards', null=True)),
                ('credit_redemption_overview', models.TextField(blank=True, help_text='The description of credit redemption for courses in program', null=True)),
                ('authoring_organizations', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='authored_programs', to='course_metadata.Organization')),
                ('corporate_endorsements', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='course_metadata.CorporateEndorsement')),
                ('courses', sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='programs', to='course_metadata.Course')),
                ('credit_backing_organizations', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='credit_backed_programs', to='course_metadata.Organization')),
                ('excluded_course_runs', models.ManyToManyField(blank=True, to='course_metadata.CourseRun')),
                ('expected_learning_items', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='course_metadata.ExpectedLearningItem')),
                ('faq', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='course_metadata.FAQ')),
                ('individual_endorsements', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='course_metadata.Endorsement')),
                ('job_outlook_items', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='course_metadata.JobOutlookItem')),
                ('partner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Partner')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_metadata.ProgramType')),
                ('video', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_metadata.Video')),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together=set([('partner', 'name'), ('partner', 'slug'), ('partner', 'uuid')]),
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together=set([('course_run', 'type', 'currency', 'credit_provider')]),
        ),
        migrations.AlterUniqueTogether(
            name='personsocialnetwork',
            unique_together=set([('person', 'type')]),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('partner', 'uuid')]),
        ),
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together=set([('partner', 'key'), ('partner', 'uuid')]),
        ),
        migrations.AlterUniqueTogether(
            name='courserunsocialnetwork',
            unique_together=set([('course_run', 'type')]),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('partner', 'key'), ('partner', 'uuid')]),
        ),
        # Data Migrations
        migrations.RunPython(
            code=create_switches,
            reverse_code=delete_switches,
        ),
        migrations.RunPython(
            code=add_seat_types,
            reverse_code=drop_seat_types,
        ),
    ]