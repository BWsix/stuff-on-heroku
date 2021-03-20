from django.db import models

class User(models.Model):
  lineID = models.CharField(max_length=40)
  number = models.PositiveSmallIntegerField(null=True)
  name = models.CharField(max_length=20, null=True)
  job = models.CharField(max_length=30, null=True, blank=True)

  where = models.CharField(max_length=50, null=True, blank=True)
  status = models.CharField(max_length=50, null=True, blank=True)

  bank = models.PositiveIntegerField(default=0)
  memo = models.CharField(max_length=50, null=True, blank=True)

  def __str__(self):
    return f"{self.number}, {self.name}"

class LunchMenu(models.Model):
  photo_url = models.CharField(max_length=30, null=True)
  date = models.CharField(max_length=15)

  prices = models.CharField(max_length=30, null=True)

  def __str__(self):
    return self.date

class LunchOrder(models.Model):
  orderer = models.ForeignKey(User, on_delete=models.CASCADE)

  type = models.CharField(max_length=10)
  order = models.PositiveSmallIntegerField(null=True)
