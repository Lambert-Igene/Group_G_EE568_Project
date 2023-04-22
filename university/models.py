# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=8)
    title = models.CharField(max_length=50, blank=True, null=True)
    dept_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'


class Department(models.Model):
    dept_name = models.CharField(primary_key=True, max_length=32)
    building = models.CharField(max_length=32, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class FundingAward(models.Model):
    id = models.IntegerField(primary_key=True)
    agency = models.CharField(max_length=50, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funding_award'


class FundingAwardInvestigator(models.Model):
    funding_award = models.ForeignKey(FundingAward, models.DO_NOTHING, db_column='funding_award')
    professor = models.ForeignKey('Instructor', models.DO_NOTHING, db_column='professor')

    class Meta:
        managed = False
        db_table = 'funding_award_investigator'
        unique_together = (('funding_award', 'professor'),)


class Instructor(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=8)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor'


class Prereq(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, related_name='+')
    prereq = models.ForeignKey(Course, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'prereq'
        unique_together = (('course', 'prereq'),)


class Publication(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    venue = models.CharField(max_length=100, blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'publication'


class PublicationAuthor(models.Model):
    publication = models.ForeignKey(Publication, models.DO_NOTHING, db_column='publication')
    professor = models.ForeignKey(Instructor, models.DO_NOTHING, db_column='professor')

    class Meta:
        managed = False
        db_table = 'publication_author'
        unique_together = (('publication', 'professor'),)


class Section(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING)
    sec_id = models.CharField(max_length=32)
    semester = models.SmallIntegerField()
    year = models.IntegerField()
    building = models.CharField(max_length=32, blank=True, null=True)
    room = models.CharField(max_length=32, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section'
        unique_together = (('course', 'sec_id', 'semester', 'year'),)


class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=100, blank=True, null=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    total_credits = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class Takes(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING, related_name='+')
    course = models.ForeignKey(Section, models.DO_NOTHING, related_name='+')
    sec = models.ForeignKey(Section, models.DO_NOTHING, related_name='+')
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', related_name='+')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year')
    grade = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'takes'
        unique_together = (('student', 'course', 'sec', 'semester', 'year'),)


class Teaches(models.Model):
    course = models.ForeignKey(Section, models.DO_NOTHING, related_name='+')
    sec = models.ForeignKey(Section, models.DO_NOTHING, related_name='+')
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', related_name='+')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year', related_name='+')
    teacher = models.ForeignKey(Instructor, models.DO_NOTHING, to_field='id')

    class Meta:
        managed = False
        db_table = 'teaches'
        unique_together = (('course', 'sec', 'semester', 'year', 'teacher'),)
