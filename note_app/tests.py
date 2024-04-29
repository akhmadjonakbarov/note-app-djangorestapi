from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Note


# Create your tests here.
class NoteAPITests(APITestCase):
    def setUp(self):
        self.task1 = Note.objects.create(topic='Task 1', info='Description 1')
        self.task2 = Note.objects.create(topic='Task 2', info='Description 2')

    def test_list_tasks(self):
        url = reverse('all-notes')  # Assuming 'task-list' is the name of the list endpoint
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['notes']), 2)  # Assuming two tasks are created in setUp

    def test_create_task(self):
        url = reverse('add-note')
        data = {'topic': 'New Task', 'info': 'New Description'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 3)  # Assuming one task is created in the test

    def test_update_task(self):
        url = reverse('update-note', kwargs={'id': self.task1.id})
        data = {'topic': 'Updated Task', 'info': 'Updated Description'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.topic, 'Updated Task')

    def test_delete_task(self):
        url = reverse('delete-note', kwargs={'id': self.task1.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Note.objects.count(), 1)
