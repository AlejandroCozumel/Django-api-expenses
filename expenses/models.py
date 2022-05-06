from django.db import models
from authentication.models import User

# Create your models here.
class Expense(models.Model):
    CATEGORY_OPTIONS=[('Food','Food'),('Transport','Transport'),('Entertainment','Entertainment'),('Health','Health'),('Other','Other')]
    category=models.CharField(max_length=20,choices=CATEGORY_OPTIONS)
    ammount=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    owner=models.ForeignKey(to=User,on_delete=models.CASCADE)
    date=models.DateField(null=False, blank=False)

    class Meta:
        ordering=['-date']
    
    def __str__(self):
        return str(self.owner)+'s expense'