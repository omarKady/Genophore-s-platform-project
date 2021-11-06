from django.test import TestCase
from .models import Document, Notification, Protein, Comment
from django.contrib.auth.models import User

# Create your tests here.

class ProteinModelTest(TestCase):

    def setUp(self):
        # Create a user
        testuser1 = User.objects.create_user(
            username='testuser1', password='abc132'
        )
        testuser1.save()
        Protein.objects.create(author=testuser1, amino_acid_seq='test', dna_seq='testtesttest')
    
    def test_protein_amino_acid_seq(self):
        protein = Protein.objects.get(id=1)
        expected_protein_amino_acid_seq = f'{protein.amino_acid_seq}'
        self.assertEqual(expected_protein_amino_acid_seq, 'test')

    def test_protein_dna_seq(self):
        protein = Protein.objects.get(id=1)
        expected_protein_dna_seq = f'{protein.dna_seq}'
        self.assertEqual(expected_protein_dna_seq, 'testtesttest')
    
    def test_valid_size_dna_to_amino_acid(self):
        protein = Protein.objects.get(id=1)
        dna_seq_length = len(protein.dna_seq)
        amino_acid_seq_length = len(protein.amino_acid_seq)
        self.assertEqual(dna_seq_length, 3*amino_acid_seq_length)


class DocumentModelTest(TestCase):

    def setUp(self):
        # Create a user
        testuser1 = User.objects.create_user(
            username='testuser1', password='abc132'
        )
        testuser1.save()
        Document.objects.create(author=testuser1, content='document test content')
    
    def test_document_content(self):
        document = Document.objects.get(id=1)
        expected_document_content = f'{document.content}'
        self.assertEqual(expected_document_content, 'document test content')

class CommentModelTest(TestCase):

    def setUp(self):
        testuser1 = User.objects.create_user(
            username='testuser1', password='abc132'
        )
        testuser1.save()
        protein = Protein.objects.create(author=testuser1, amino_acid_seq='te', dna_seq='tetete')
        Comment.objects.create(author=testuser1,content='test comment',content_object=protein)
    
    def test_comment_content(self):
        comment = Comment.objects.get(id=1)
        expected_comment_content = f'{comment.content}'
        self.assertEqual(expected_comment_content, 'test comment')
    
    def test_comment_object_id_fk(self):
        comment = Comment.objects.get(id=1)
        protein = Protein.objects.get(id=1)
        self.assertEqual(comment.object_id, protein.id)
    
    def test_comment_content_type_fk(self):
        comment = Comment.objects.get(id=1)
        protein = Protein.objects.get(id=1)
        self.assertEqual((comment.content_type.model).capitalize(), protein.__class__.__name__)

class NotificationModelTest(TestCase):

    def setUp(self):
        testuser1 = User.objects.create_user(
            username='testuser1', password='abc132'
        )
        testuser1.save()
        doc = Document.objects.create(author=testuser1, content='document content')
        Notification.objects.create(message='test notification', notification_type='sm', icon='font icon', content_object=doc)
    
    def test_notification_content(self):
        notification = Notification.objects.get(id=1)
        expected_message = f'{notification.message}'
        self.assertEqual(expected_message, 'test notification')
    
    def test_notification_type(self):
        notification = Notification.objects.get(id=1)
        expected_type = f'{notification.notification_type}'
        self.assertEqual(expected_type, 'sm')
    
    def test_notification_icon(self):
        notification = Notification.objects.get(id=1)
        expected_icon = f'{notification.icon}'
        self.assertEqual(expected_icon, 'font icon')
    
    def test_notification_object_id_fk(self):
        notification = Notification.objects.get(id=1)
        document = Document.objects.get(id=1)
        self.assertEqual(notification.object_id, document.id)
    
    def test_notification_content_type_fk(self):
        notification = Notification.objects.get(id=1)
        document = Document.objects.get(id=1)
        self.assertEqual((notification.content_type.model).capitalize(), document.__class__.__name__)
