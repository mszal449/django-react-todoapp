from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse
from .models import Task


class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # sample data testing
        self.task1 = Task.objects.create(
            title='Eat dinner',
            description='Eat sushi for dinner',
            done=True,
            fav=False)
        self.task2 = Task.objects.create(
            title='Walk the dog',
            description='Walk the dog at 9:30',
            done=False,
            fav=True)
        self.task3 = Task.objects.create(
            title='Go jogging',
            description='Go joggin with Micheal',
            done=False,
            fav=False)

    def test_tasks_view(self):
        # Without filters
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['tasks']), 3)

        # With filters
        params = {'title': 'Walk the dog', 'description': 'Walk', 'done': False}
        url = reverse('tasks') + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['tasks'][0]['title'], 'Walk the dog')

    def test_task_view(self):
        response = self.client.get(reverse('task_single', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['task']['title'], 'Eat dinner')
        self.assertEqual(response.json()['task']['id'], 1)

    def test_task_creation(self):
        url = reverse('task_create')

        data_all_args = {
            'title': 'Clean dishes',
            'description': 'clean the dishes in the sink',
            'done': False,
            'fav': False,
        }

        data_required_args = {
            'title': 'Clean dishes',
            'description': 'clean the dishes in the sink',
        }

        response_all_args = self.client.post(url, data_all_args, content_type='application/json')
        response_required_args = self.client.post(url, data_required_args, content_type='application/json')
        self.assertEqual(response_all_args.status_code, 201)
        self.assertEqual(response_required_args.status_code, 201)

    def test_task_update(self):
        url = reverse('task_update', kwargs={'pk': self.task1.id})
        data = {
            'title': 'Put dishes back into the sink'
        }
        response = self.client.post(url, data, content_type='application/json')

        updated_task = Task.objects.get(id=self.task1.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(updated_task.title, 'Put dishes back into the sink')

    def test_task_delete(self):
        url = reverse('task_delete', kwargs={'pk': self.task1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=self.task1.id)
