from django.db import models
from authentication.models import User

# Create your models here.
class Income(models.Model):
    SOURCE_OPTIONS=[('Salary','Salary'),('Business','Business'),('Side-hustle','Side-hustle'),('Other','Other')]
    source=models.CharField(max_length=20,choices=SOURCE_OPTIONS)
    ammount=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    owner=models.ForeignKey(to=User,on_delete=models.CASCADE)
    date=models.DateField(null=False, blank=False)

    class Meta:
        ordering=['-date']
    
    def __str__(self):
        return str(self.owner)+'s income'