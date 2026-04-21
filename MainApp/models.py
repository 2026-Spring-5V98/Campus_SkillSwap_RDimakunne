from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    # Choices are stored as short codes in the DB but displayed as readable labels in the UI
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('design', 'Design'),
        ('writing', 'Writing & Tutoring'),
        ('music', 'Music'),
        ('language', 'Language'),
        ('math', 'Math & Science'),
        ('other', 'Other'),
    ]

    CONTACT_CHOICES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('in_person', 'In Person'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ]

    # ForeignKey links each skill to one user; CASCADE means if the user is deleted, their skills are too
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    # Price is optional — null=True allows no value in the DB, blank=True allows empty form submission
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_free = models.BooleanField(default=False)

    contact_preference = models.CharField(max_length=20, choices=CONTACT_CHOICES)
    availability_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    # auto_now_add=True sets this timestamp once when the record is first saved — never changes after
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Newest posts appear first everywhere

    def __str__(self):
        return f"{self.title} by {self.owner.username}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('declined', 'Declined'),
        ('cancelled', 'Cancelled'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_made')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requester.username} → {self.skill.title} on {self.date}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient.username}: {self.message[:50]}"


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # One review per reviewer-reviewee pair
        unique_together = ('reviewer', 'reviewee')

    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewee.username} ({self.rating}★)"
