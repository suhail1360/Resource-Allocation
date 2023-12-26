from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.http import HttpResponseRedirect
from .models import (
    Course,
    Batch,
    Comp_Brand,
    Trainer,
    Timings,
    Computer,
    Rooms,
    Computer_Allocation,
    Room_Allocation,                
    Trainer_Allocation,
    Student,
)

# Register your models here.


class BatchAdmin(admin.ModelAdmin):
    list_display = ("Batch_name", "Timeslot", "Course_Name")


class Traineradmin(admin.ModelAdmin):
    list_display = ("TrainerName", "Course")


class TimingAdmin(admin.ModelAdmin):
    list_display = ("Start_time", "End_time")


class ComputerAdmin(admin.ModelAdmin):
    list_display = ("Brand", "Type", "Assigned_trainer", "serial_number")


class RoomsAdmin(admin.ModelAdmin):
    list_display = ("Room_name", "Room_type")


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "Student_name",
        "Batch",
        "Trainer_Name",
        "Laptop_used",
        "computer_allocation_link"
    )
    def response_add(self, request, obj, post_url_continue=None):
        if obj.Laptop_used == "1":
            # Redirect to a specific page if the condition is met
            return HttpResponseRedirect('/admin/computer_allocation/')  # Update the URL as needed
        else:
            # Continue with the default behavior
            return super().response_add(request, obj, post_url_continue)



# class MyModelAdmin(admin.ModelAdmin):
#     list_display = ['field1', 'field2']  # Customize as needed

#     def response_add(self, request, obj, post_url_continue=None):
#         # Check your condition here
#         if obj.field1 == "some_value":
#             # Redirect to a specific page if the condition is met
#             return HttpResponseRedirect('/admin/some_other_page/')  # Update the URL as needed
#         else:
#             # Continue with the default behavior
#             return super().response_add(request, obj, post_url_continue)


    # def computer_allocation_link(self, obj):
    #     link = reverse(
    #         "admin:%s_%s_add"
    #         % (obj._meta.app_label, Computer_Allocation._meta.model_name)
    #     )
    #     link += f"?Assigned_Student={obj.pk}&Trainer={obj.Trainer_Name.pk}"

    #     return format_html('<a href="{}">Allocate Computer</a>', link)

    # computer_allocation_link.short_description = "Computer Allocation"

# url=reverse('Computer_Allocation',args=[obj.id])


    def computer_allocation_link(self, obj):
        link = reverse(
            "admin:%s_%s_add"
            % (obj._meta.app_label, Computer_Allocation._meta.model_name)
        )
        link += f"?Assigned_Student={obj.pk}&Trainer={obj.Trainer_Name.pk}"
        # Replace 'your_condition' with your actual condition.
        if obj.laptop==1:           # Replace 'link' with the name of the URL pattern you want to link to.
            url = reverse('Computer_Allocation', args=[obj.id])
            return format_html('<a href="{}">Allocate Computer</a>', link)
        else:
            return ''

    computer_allocation_link.short_description = 'Computer Allocation Link' 


class CompAllocateAdmin(admin.ModelAdmin):
    list_display = ("Computer", "Assigned_Student", "Trainer")

    def response_add(self, request, obj, post_url_continue=None):
        if "_addanother" not in request.POST:
            return HttpResponseRedirect(
                reverse(
                    "admin:%s_%s_changelist"
                    % (obj._meta.app_label, Student._meta.model_name)
                )
            )

        return super().response_add(request, obj, post_url_continue)



class TrainerAllocateAdmin(admin.ModelAdmin):
    list_display = ("Trainer_Name", "Room_Allocated", "Timing", "Batch_Name")


class RoomAllocateAdmin(admin.ModelAdmin):
    list_display = ("Room", "Trainer_Name", "Timeslot", "Batch")


admin.site.register(Course)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Comp_Brand)
admin.site.register(Trainer, Traineradmin)
admin.site.register(Timings, TimingAdmin)
admin.site.register(Computer, ComputerAdmin)
admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Computer_Allocation, CompAllocateAdmin)
admin.site.register(Trainer_Allocation, TrainerAllocateAdmin)
admin.site.register(Room_Allocation, RoomAllocateAdmin)
