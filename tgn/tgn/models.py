from django.db import models


class Account(models.Model):
    userId = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    aboutMe = models.CharField(max_length=200, default='')
    resume = models.CharField(max_length=200, default='')

    def __unicode__(self):
        return str(self.name) + ', ' + \
               self.userId


class Nonprofit(models.Model):
    name = models.CharField(max_length=200)
    mission = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    website = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=200, default='')
    imageUrl = models.CharField(max_length=2000, default='')


class UserProfileImage(models.Model):
    account = models.ForeignKey(Account)
    url = models.URLField()


class NonprofitProfileImage(models.Model):
    nonprofit = models.ForeignKey(Nonprofit)


#    image = models.ImageField(height_field=200, width_field=200)

class NonprofitAffiliateRequest(models.Model):
    potentialAffiliate = models.ForeignKey(Account)
    nonprofit = models.ForeignKey(Nonprofit)

class NonprofitRelation(models.Model):
    userId = models.CharField(max_length=200)
    nonprofitId = models.CharField(max_length=200)


class Job(models.Model):
    nonprofit = models.ForeignKey(Nonprofit)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    compensation = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __unicode__(self):
        return str(self.name) + ', ' + str(self.nonprofit.name)


class PostedJob(Job):
    timeCreated = models.DateTimeField(auto_now_add=True)

class PostedJobApplication(models.Model):
    applicant = models.ForeignKey(Account)
    job = models.ForeignKey(PostedJob)

class CurrentJob(Job):
    employee = models.ForeignKey(Account)
    timeTaken = models.DateTimeField(auto_now_add=True)
    timeCreated = models.DateTimeField()


class CompletedJob(Job):
    employee = models.ForeignKey(Account)
    timeTaken = models.DateTimeField()
    timeCreated = models.DateTimeField()
    timeCompleted = models.DateTimeField(auto_now_add=True)


class Title(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __unicode__(self):
        return str(self.title)


class UserTitle(Title):
    account = models.ForeignKey(Account)

    def __unicode__(self):
        return str(self.title) + ', ' + str(self.account)


class PostedJobTitle(Title):
    job = models.ForeignKey(PostedJob)

    def __unicode__(self):
        return str(self.title) + ', ' + str(self.job)


class CurrentJobTitle(Title):
    job = models.ForeignKey(CurrentJob)

    def __unicode__(self):
        return str(self.title) + ', ' + str(self.job)


class CompletedJobTitle(Title):
    job = models.ForeignKey(CompletedJob)

    def __unicode__(self):
        return str(self.title) + ', ' + str(self.job)


class Skill(models.Model):
    skill = models.CharField(max_length=200)

    class Meta:
        abstract = True


class UserSkill(Skill):
    account = models.ForeignKey(Account)

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
