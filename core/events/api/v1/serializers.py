from rest_framework import serializers
from ...models import EventType, Event
from accounts.models import UserV2

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'title', 'description', 'is_active']

class EventSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer()  # Nested serializer for EventType
    event_organizer = serializers.PrimaryKeyRelatedField(queryset=UserV2.objects.all())  # Linking event organizer

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_type', 'start_date', 'end_date', 
                  'location_name', 'address', 'city', 'state', 'country', 'event_organizer',
                  'event_image', 'website_url', 'registration_url', 'social_media_links', 
                  'ticket_price', 'vip_ticket_price', 'discount_code', 'age_restriction', 
                  'event_languages', 'sponsors', 'food_and_drinks_available', 'is_online_streamed',
                  'registration_deadline', 'feedback_rating', 'sponsorship_opportunities', 
                  'is_family_friendly', 'venue_capacity', 'vip_venue_capacity', 'total_capacity', 
                  'tickets_sold', 'sold_out', 'created_at', 'updated_at', 'is_active']