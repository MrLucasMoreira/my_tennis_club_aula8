import tempfile
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from plans.models import Plan

from .models import Member


class MemberUploadTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.media_directory = tempfile.TemporaryDirectory()
        cls.media_override = override_settings(MEDIA_ROOT=cls.media_directory.name)
        cls.media_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.media_override.disable()
        cls.media_directory.cleanup()
        super().tearDownClass()

    def setUp(self):
        self.plan = Plan.objects.create(title='Básico')

    def image_upload(self, name='foto.png'):
        content = BytesIO()
        Image.new('RGB', (2, 2), color='green').save(content, format='PNG')
        return SimpleUploadedFile(name, content.getvalue(), content_type='image/png')

    def pdf_upload(self, name='documento.pdf'):
        return SimpleUploadedFile(
            name,
            b'%PDF-1.4\n%%EOF\n',
            content_type='application/pdf',
        )

    def test_create_and_display_member_files(self):
        response = self.client.post(
            reverse('addrecord'),
            {
                'first': 'Ana',
                'last': 'Silva',
                'plan': self.plan.id,
                'foto': self.image_upload(),
                'documento': self.pdf_upload(),
            },
        )

        self.assertRedirects(response, reverse('members'))
        member = Member.objects.get(firstname='Ana')
        self.assertTrue(member.foto.name.startswith('images/'))
        self.assertEqual(member.documento.name, 'documento.pdf')

        listing = self.client.get(reverse('members'))
        self.assertContains(listing, member.foto.url)

        details = self.client.get(reverse('details', args=[member.id]))
        self.assertContains(details, member.foto.url)

        update = self.client.get(reverse('update', args=[member.id]))
        self.assertContains(update, member.foto.url)
        self.assertContains(update, member.documento.url)

        self.assertTrue(member.foto.storage.exists(member.foto.name))
        self.assertTrue(member.documento.storage.exists(member.documento.name))

# Create your tests here.
