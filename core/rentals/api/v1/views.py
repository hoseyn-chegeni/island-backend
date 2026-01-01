from rentals.models import VehicleAvailability
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import VehicleRentalSerializer
from ...models import VehicleRental



class CheckVehicleAvailabilityAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "vehicle_id",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="Vehicle ID",
            ),
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                format="date",
                required=True,
                description="Start date (YYYY-MM-DD)",
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                format="date",
                required=True,
                description="End date (YYYY-MM-DD)",
            ),
        ],
        responses={200: openapi.Response("Availability result")}
    )
    def get(self, request):
        vehicle_id = request.query_params.get("vehicle_id")
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        if not vehicle_id or not start_date_str or not end_date_str:
            return Response(
                {"error": "vehicle_id, start_date and end_date are required"},
                status=400
            )

        try:
            start_date = timezone.datetime.strptime(
                start_date_str, "%Y-%m-%d"
            ).date()
            end_date = timezone.datetime.strptime(
                end_date_str, "%Y-%m-%d"
            ).date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=400
            )

        if start_date > end_date:
            return Response(
                {"error": "start_date cannot be after end_date"},
                status=400
            )

        today = timezone.now().date()
        if end_date > today + timedelta(days=90):
            return Response(
                {
                    "exists": False,
                    "message": "Date range exceeds the 90-day booking window"
                },
                status=400
            )


        exists = VehicleAvailability.objects.filter(
            vehicle_id=vehicle_id,
            date__range=(start_date, end_date)
        ).exists()

        return Response({
            "exists": exists,
            "available": not exists
        })
    



class VehicleRentalListCreateAPIView(ListCreateAPIView):
    queryset = VehicleRental.objects.all()
    serializer_class = VehicleRentalSerializer


class VehicleRentalDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleRental.objects.all()
    serializer_class = VehicleRentalSerializer
    lookup_field = 'id'