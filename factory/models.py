from django.db import models

# цех
class WorkShop(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# працівник
class Worker(models.Model):
    name = models.CharField(max_length=100)
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE, related_name='workers')
    position = models.CharField(max_length=50)

# відвідування
class Attendance(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    clock_in = models.TimeField(auto_now_add=True)

# замовлення
class Shipment(models.Model):
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending')
