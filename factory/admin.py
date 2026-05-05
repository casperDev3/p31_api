from django.contrib import admin
from .models import WorkShop, Worker, Attendance, Shipment

@admin.register(WorkShop)
class WorkShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'workshop')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'position')
    list_filter = ('workshop',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker', 'date', 'clock_in')
    list_display_links = ('id',)
    search_fields = ('worker__name',)
    list_filter = ('date',)

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'status')
    list_display_links = ('id', 'description')
    search_fields = ('description',)
    list_filter = ('status',)
