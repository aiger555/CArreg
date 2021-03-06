from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters import rest_framework as django_filter

from cars.tasks import send_mail_to_worker
from cars.models import Car
from cars.permissions import DiversePermission
from cars.serializers import CarSerializer
from accounts.tasks import send_mail_to_worker


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (django_filter.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('legal_number', 'year_issue', 'owner__id', )
    search_fields = ('owner__first_name', 'legal_number', 'mark__name', )

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @action(methods=['get', ], detail=True)
    def worker_reminder(self, request, *args, **kwargs):
        car = self.get_object()
        send_mail_to_worker.delay(car.worker.email, car.id)
        return Response({'success': True})


