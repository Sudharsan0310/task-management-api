from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task, Category

User = get_user_model()

class TaskAPITests(TestCase):
    """Test task CRUD operations"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=self.user)
        
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'todo',
            'priority': 'high'
        }
    
    def test_create_task(self):
        """Test creating a task"""
        response = self.client.post('/api/tasks/', self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Test Task')
    
    def test_get_tasks(self):
        """Test retrieving tasks"""
        Task.objects.create(owner=self.user, **self.task_data)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_update_task(self):
        """Test updating a task"""
        task = Task.objects.create(owner=self.user, **self.task_data)
        updated_data = {'title': 'Updated Title', 'status': 'in_progress'}
        response = self.client.patch(f'/api/tasks/{task.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Title')
    
    def test_delete_task(self):
        """Test deleting a task"""
        task = Task.objects.create(owner=self.user, **self.task_data)
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status"""
        Task.objects.create(owner=self.user, title='Task 1', status='todo')
        Task.objects.create(owner=self.user, title='Task 2', status='completed')
        
        response = self.client.get('/api/tasks/?status=todo')
        self.assertEqual(len(response.data['results']), 1)
