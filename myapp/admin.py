from django.contrib import admin
from myapp.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(AppoUser)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(RicruDoctor)






## for display all field in admin table:

# @admin.register(Doctor):
# class UserAdmin(admin.ModelAdmin):
#     list_display: Sequence[Union[str, Callable[[_ModelT], Any]]]