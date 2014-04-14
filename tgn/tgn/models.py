from django.db import models


class Account(models.Model):
    userId = models.CharField(max_length=200)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    aboutMe = models.CharField(max_length=200)

    def __unicode__(self):
        return str(self.firstName) + ' ' + str(self.lastName) + ', ' + \
               self.userId


class Nonprofit(models.Model):
    name = models.CharField(max_length=200)
    mission = models.CharField(max_length=200)
    description = models.CharField()

class UserProfileImage(models.Model):
    account = models.ForeignKey(Account)
    url = models.URLField()

class NonprofitProfileImage(models.Model):
    nonprofit = models.ForeignKey(Nonprofit)
    image = models.ImageField(height_field=200, width_field=200)

class NonprofitRelations(models.Model):
    userId = models.CharField(max_length=200)
    nonprofitId = models.CharField(max_length=200)


class Job(models.Model):
    nonprofit = models.ForeignKey(Nonprofit)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    compensation = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __unicode__(self):
        return str(self.title) + ', ' + str(self.nonprofit.name)


class PostedJob(Job):
    timeCreated = models.DateTimeField(auto_now_add=True)


class CurrentJob(Job):
    employee = models.ForeignKey(Account)
    timeTaken = models.DateTimeField(auto_now_add=True)
    timeCreated = models.DateTimeField()


class CompletedJob(Job):
    employee = models.ForeignKey(Account)
    timeTaken = models.DateTimeField()
    timeCreated = models.DateTimeField()
    timeCompleted = models.DateTimeField(auto_now_add=True)


class UserTitle(models.Model):
    account = models.ForeignKey(Account)
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return str(self.title) + ', ' + str(self.account)


class Skill(models.Model):
    skill = models.CharField(max_length=200)

    class Meta:
        abstract = True

class UserSkill(Skill):
    account = models.ForeignKey(Account)
    #strength = models.CharField(max_length=200) maybe add this in

    def __unicode__(self):
        return str(self.skill) + ', ' + str(self.account)

class PostedJobSkill(Skill):
    job = models.ForeignKey(PostedJob)

    def __unicode__(self):
        return str(self.skill) + ', ' + str(self.job)

class CurrentJobSkill(Skill):
    job = models.ForeignKey(CurrentJob)

    def __unicode__(self):
        return str(self.skill) + ', ' + str(self.job)

class CompletedJobSkill(Skill):
    job = models.ForeignKey(CompletedJob)

    def __unicode__(self):
        return str(self.skill) + ', ' + str(self.job)
