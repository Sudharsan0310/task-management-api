from django_filters import rest_framework as filters
from .models import Task

class TaskFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)
    due_date_after = filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')
    due_date_before = filters.DateTimeFilter(field_name='due_date', lookup_expr='lte')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Task
        fields = ['status', 'priority', 'assigned_to']
