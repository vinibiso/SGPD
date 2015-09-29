from __future__ import unicode_literals

from django.db import models

class Problem(models.Model):
    idproblem = models.IntegerField(db_column='idProblem', primary_key=True)
    iduser = models.ForeignKey('User', db_column='idUser')
    md5hash = models.CharField(db_column='md5Hash', max_length=32, blank=True)
    dateproblem = models.DateTimeField(db_column='dateProblem', blank=True, null=True)
    doneproblem = models.IntegerField(db_column='doneProblem', blank=True, null=True)
    answerproblem = models.CharField(db_column='answerProblem', max_length=40, blank=True)
    datedoneproblem = models.DateTimeField(db_column='dateDoneProblem', blank=True, null=True)
    idsubproblem = models.IntegerField(db_column='idSubProblem', blank=True, null=True)
    class Meta:
        db_table = 'problem'

class Status(models.Model):
    idstatus = models.IntegerField(db_column='idStatus', primary_key=True)
    descstatus = models.CharField(db_column='descStatus', max_length=20, blank=True)
    class Meta:
        db_table = 'status'

class Subproblem(models.Model):
    idsubproblem = models.IntegerField(db_column='idSubProblem', primary_key=True)
    idproblem = models.ForeignKey(Problem, db_column='idProblem')
    startstringsubproblem = models.CharField(db_column='startStringSubProblem', max_length=8, blank=True)
    stopstringsubproblem = models.CharField(db_column='stopStringSubProblem', max_length=8, blank=True)
    iduser = models.ForeignKey('User', db_column='idUser', blank=True, null=True)
    senddateproblem = models.DateTimeField(db_column='sendDateProblem', blank=True, null=True)
    receivedateproblem = models.DateTimeField(db_column='receiveDateProblem', blank=True, null=True)
    idstatus = models.ForeignKey(Status, db_column='idStatus')
    class Meta:
        db_table = 'subproblem'

class User(models.Model):
    iduser = models.IntegerField(db_column='idUser', primary_key=True)
    hashuser = models.CharField(db_column='hashUser', max_length=15, blank=True)
    dateuser = models.DateTimeField(db_column='dateUser', blank=True, null=True)
    pointsuser = models.IntegerField(db_column='pointsUser', blank=True, null=True)
    class Meta:
        db_table = 'user'

