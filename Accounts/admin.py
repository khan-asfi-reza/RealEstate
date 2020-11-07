from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from Accounts.forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Renter, Renter_Property_Pref, Owner, Agent, Agency


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # The fields to be used in displaying the User model.
    # that reference specific fields on auth.User.
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('admin', 'staff')}),
        ('Verification', {'fields': ('verified',)}),
        ('Account Type', {'fields': ('account_type',)})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'account_type')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


class __Admin__(admin.ModelAdmin):
    list_display = ('email', 'admin', 'staff')


class Admin(User):
    class Meta:
        proxy = True


class MyAdmin(__Admin__):
    def get_queryset(self, request):
        return self.model.objects.filter(admin=True, staff=True)


admin.site.register(Admin, MyAdmin)
admin.site.register(Renter)
admin.site.register(Renter_Property_Pref)
admin.site.register(Agent)
admin.site.register(Agency)
admin.site.register(Owner)
admin.site.unregister(Group)
