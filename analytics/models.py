from django.db import models
class Sheet(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
class AvocadoAvenue(models.Model):
    grn= models.IntegerField(max_length=100, unique=True)
    type_of_fruit = models.CharField(max_length=256)
    initial_weight = models.IntegerField()
    fruid_cost = models.FloatField()
    sorted_weight = models.IntegerField()
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)
    @property
    def shrinkage_weight(self):
        return self.initial_weight - self.sorted_weight

    @property
    def shrinkage_percentage(self):
        return (self.shrinkage_weight / self.initial_weight) * 100
    
    def __str__(self):
        return f"{self.type_of_fruit} {self.grn}"
