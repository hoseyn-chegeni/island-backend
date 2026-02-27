from django.db import models
from accounts.models import UserV2
from django.core.exceptions import ValidationError

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

    tickets_sold = models.PositiveIntegerField(default=0)
    vip_tickets_sold = models.PositiveIntegerField(default=0)
    sold_out = models.BooleanField(default=False)  # New field for sold-out status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.title

    @property
    def duration(self):
        if self.start_date and self.end_date:
            return self.end_date - self.start_date
        return None  # or return a default value like timedelta(0) if you prefer a default value
    
    @property
    def total_capacity(self):
        venue_capacity = self.venue_capacity if self.venue_capacity is not None else 0
        vip_venue_capacity = self.vip_venue_capacity if self.vip_venue_capacity is not None else 0
        return venue_capacity + vip_venue_capacity


    class Meta:
        ordering = ['start_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class Ticket(models.Model):
    user = models.ForeignKey(UserV2, on_delete=models.CASCADE, related_name="tickets")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    quantity = models.PositiveIntegerField(default=1)  # Number of tickets bought
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Price per ticket (auto-calculated)
    purchased_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the ticket was purchased
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('used', 'Used'), ('canceled', 'Canceled')], default='available')
    is_vip = models.BooleanField(default=False)  # Flag for VIP ticket

    def __str__(self):
        return f"{self.quantity} Ticket(s) for {self.event.title} purchased by {self.user.phone_number}"

    def save(self, *args, **kwargs):
        """
        Overriding save method to calculate the total price for tickets automatically 
        based on event ticket price and quantity, and ensure there's enough capacity.
        """
        try:
            if self.is_vip:
                # Check for remaining VIP capacity
                available_vip_capacity = self.event.vip_venue_capacity - self.event.vip_tickets_sold
                if self.quantity > available_vip_capacity:
                    raise ValidationError(f"Not enough VIP seats for this event. Remaining VIP capacity: {available_vip_capacity} tickets.")
                
                # Calculate price for VIP tickets
                if self.price is None:
                    if not self.event.vip_ticket_price:  # Ensure VIP ticket price is set
                        raise ValidationError("Event VIP ticket price is not set.")
                    self.price = self.event.vip_ticket_price * self.quantity

                # Update VIP tickets sold count
                self.event.vip_tickets_sold += self.quantity

            else:
                # Check for remaining regular capacity
                available_capacity = self.event.venue_capacity - self.event.tickets_sold
                if self.quantity > available_capacity:
                    raise ValidationError(
                        f"Not enough available seats for this event. Remaining regular capacity: {available_capacity} tickets. "
                        f"Remaining VIP capacity: {self.event.vip_venue_capacity - self.event.vip_tickets_sold} tickets."
                    )

                # Calculate price for regular tickets
                if self.price is None:
                    if not self.event.ticket_price:  # Ensure ticket price is set
                        raise ValidationError("Event ticket price is not set.")
                    self.price = self.event.ticket_price * self.quantity

                # Update regular tickets sold count
                self.event.tickets_sold += self.quantity

            # Save the ticket instance first
            super().save(*args, **kwargs)

            if self.event.vip_tickets_sold + self.event.tickets_sold >= self.event.venue_capacity+self.event.vip_venue_capacity:
                self.event.sold_out = True
            self.event.save()

        except ValidationError as e:
            print(f"ValidationError in Ticket.save(): {str(e)}")
            raise e  # Re-raise the error to ensure Django can catch it and return a 400 error

        except Exception as e:
            print(f"Error in Ticket.save(): {str(e)}")
            raise e  # Re-raise other errors

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'