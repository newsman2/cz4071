from django.contrib import admin
from .models import Network


# Register your models here.
class NetworkAdmin(admin.ModelAdmin):
    # exclude = ('uploaded_by',)
    list_display = ('network_file', 'created_at')

'''
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.uploaded_by:
            instance.uploaded_by = user
        instance.save()
        form.save_m2m()
        return instance
'''

admin.site.register(Network, NetworkAdmin)
