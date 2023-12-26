from django.db import models

# Create your models here.


class Course(models.Model):
    Course = models.CharField(max_length=220)

    def __str__(self):
        return self.Course

    class Meta:
        verbose_name_plural = "Courses"


class Trainer(models.Model):
    TrainerName = models.CharField(max_length=220)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.TrainerName

    class Meta:
        verbose_name_plural = "Trainers"


class Timings(models.Model):

    Start_time = models.TimeField()
    End_time = models.TimeField()

    # def __str__(self):
    #  return str(self.Start_time)

    def __str__(self):
        return f"{self.Start_time} - {self.End_time}"

    class Meta:
        verbose_name_plural = "Timings"


class Batch(models.Model):
    Timeslot = models.ForeignKey(Timings, on_delete=models.CASCADE)
    Course_Name = models.ForeignKey(Course, on_delete=models.CASCADE)
    Batch_name = models.CharField(max_length=220, blank=True)
    Start_date = models.DateField()

    def __str__(self):
        return self.Batch_name

    def save(self, *args, **kwargs):
        if not self.Batch_name:
            # Generate the Batch_name based on the associated Timeslots
            course_name = self.CourseName.Course
            start_time = self.Timeslots.Start_time
            started = self.Start_date
            batch_name = f"{started.strftime('%b%d')}-{course_name}-{start_time.strftime('%H')}-Offline-Batch"
            self.Batch_name = batch_name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Batches"


class Comp_Brand(models.Model):
    Brand = models.CharField(max_length=100)

    def __str__(self):
        return self.Brand

    class Meta:
        verbose_name_plural = "Computer Brands"


class Computer(models.Model):

    ownership = ((0, "owned"), (1, "rented"))

    Brand = models.ForeignKey(Comp_Brand, on_delete=models.CASCADE)
    Type = models.IntegerField(choices=ownership, null=False)
    Assigned_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['serial_number'].disabled = True

    def __str__(self):
        return self.serial_number

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate new serial number only for new instances
            last_serial_number = Computer.objects.order_by(
                '-id').values_list('serial_number', flat=True).first()
            if last_serial_number:
                last_number = int(last_serial_number[3:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.serial_number = f"OTL{new_number}"

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Computers"


class Rooms(models.Model):

    room_type = ((0, "Classroom"), (1, "Conference Rooms"))

    Room_name = models.CharField(max_length=100)
    Room_type = models.IntegerField(choices=room_type, null=False)

    def __str__(self):
        return self.Room_name

    class Meta:
        verbose_name_plural = "Rooms"


class Student(models.Model):

    laptop = ((0, "Self"), (1, "OTS owned"))

    Student_name = models.CharField(max_length=150)
    Batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    Trainer_Name = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    Laptop_used = models.IntegerField(choices=laptop, null=False)

    def __str__(self):
        return self.Student_name

    class Meta:
        verbose_name_plural = "Students"


class Trainer_Allocation(models.Model):
    Trainer_Name = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    Room_Allocated = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    Timing = models.ForeignKey(Timings, on_delete=models.CASCADE)
    Batch_Name = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Trainer_Name}"

    class Meta:
        verbose_name_plural = "Trainer Allocation"


class Room_Allocation(models.Model):
    Room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    Trainer_Name = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    Timeslot = models.ForeignKey(Timings, on_delete=models.CASCADE)
    Batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Room}"

    class Meta:
        verbose_name_plural = "Room Allocation"


class Computer_Allocation(models.Model):
    Computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    Assigned_Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Computer}"

    class Meta:
        verbose_name_plural = "Computer Allocation"
