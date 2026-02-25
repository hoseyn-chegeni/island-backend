from django.db import models
from accounts.models import UserV2
# Create your models here.



class EventType(models.Model):
    title = models.CharField(max_length=255)  # Title of the event type (e.g., 'Music Festival')
    description = models.TextField(null=True, blank=True)  # Optional detailed description of the event type
    is_active = models.BooleanField(default=True)  # Status to check if the event type is active or not

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.ForeignKey(EventType, related_name='events', on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    event_organizer = models.ForeignKey(UserV2, related_name='organized_events', on_delete=models.SET_NULL, null=True)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    registration_url = models.URLField(null=True, blank=True)
    social_media_links = models.JSONField(default=dict, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vip_ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_code = models.CharField(max_length=50, null=True, blank=True)
    age_restriction = models.CharField(max_length=10, choices=[('all', 'All Ages'), ('18+', '18+ Only'), ('21+', '21+ Only')], default='all')
    event_languages = models.JSONField(default=list, blank=True)
    sponsors = models.TextField(null=True, blank=True)
    food_and_drinks_available = models.BooleanField(default=False)
    is_online_streamed = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    feedback_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    sponsorship_opportunities = models.BooleanField(default=False)
    is_family_friendly = models.BooleanField(default=True)
    venue_capacity = models.PositiveIntegerField()
    vip_venue_capacity = models.PositiveIntegerField(default=0)  # New field for VIP capacity
    total_capacity = models.PositiveIntegerField()

    tickets_sold = models.PositiveIntegerField(default=0)  # New field for tracking tickets sold
    sold_out = models.BooleanField(default=False)  # New field for sold-out status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.title

    @property
    def duration(self):
        return self.end_date - self.start_date
    
    @property
    def total_capacity(self):
        return self.venue_capacity + self.vip_venue_capacity

    @property
    def sold_out(self):
        return self.tickets_sold >= self.total_capacity

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'