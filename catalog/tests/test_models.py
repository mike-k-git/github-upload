from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
import datetime

from catalog.models import Author, Book, BookInstance, Genre, Language


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        author = Author.objects.create(first_name='Big', last_name='Bob')
        language = Language.objects.create(name='English')
        genre_first = Genre.objects.create(name='Fantasy')
        genre_second = Genre.objects.create(name='Doc')
        book = Book.objects.create(title='Title', summary='Summary',
                                   isbn='isbn', author=author, language=language)
        book.genre.set([genre_first, genre_second])

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_author_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_summary_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_genre_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label, 'genre')

    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_summary_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEqual(max_length, 1000)

    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    def test_author_relation(self):
        book = Book.objects.get(id=1)
        author = Author.objects.get(id=1)
        self.assertEqual(book.author, author)

    def test_genre_relation(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.genre.count(), 2)

    def test_language_relation(self):
        book = Book.objects.get(id=1)
        language = Language.objects.get(id=1)
        self.assertEqual(book.language, language)

    def test_object_name_is_title(self):
        book = Book.objects.get(id=1)
        expected_object_name = f'{book.title}'
        self.assertEqual(expected_object_name, str(book))

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_absolute_url(), '/catalog/book/1')

    def test_display_genre(self):
        book = Book.objects.get(id=1)
        expected_display_genre = f'{book.genre.all()[0]} | {book.genre.all()[1]}'
        self.assertEqual(expected_display_genre, book.display_genre())


class BookInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        book = Book.objects.create(title='Title', summary='Summary',
                                   isbn='isbn')
        user = User.objects.create()
        BookInstance.objects.create(
            book=book,
            imprint='Imprint',
            borrower=user,
            status='o'
        )

    def test_id_label(self):
        book_instance = BookInstance.objects.first()
        field_label = book_instance._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_book_label(self):
        book_instance = BookInstance.objects.first()
        field_label = book_instance._meta.get_field('book').verbose_name
        self.assertEqual(field_label, 'book')

    def test_imprint_label(self):
        book_instance = BookInstance.objects.first()
        field_label = book_instance._meta.get_field('imprint').verbose_name
        self.assertEqual(field_label, 'imprint')

    def test_due_back_label(self):
        book_instance = BookInstance.objects.first()
        field_label = book_instance._meta.get_field('due_back').verbose_name
        self.assertEqual(field_label, 'due back')

    def test_status_label(self):
        book_instance = BookInstance.objects.first()
        field_label = book_instance._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_borrower_label(self):
        book_instance = BookInstance.objects.first()
        field_label = book_instance._meta.get_field('borrower').verbose_name
        self.assertEqual(field_label, 'borrower')

    def test_imprint_max_length(self):
        book_instance = BookInstance.objects.first()
        max_length = book_instance._meta.get_field('imprint').max_length
        self.assertEqual(max_length, 200)

    def test_book_relation(self):
        book_instance = BookInstance.objects.first()
        book = Book.objects.get(id=1)
        self.assertEqual(book_instance.book, book)

    def test_borrower_relation(self):
        book_instance = BookInstance.objects.first()
        user = User.objects.get(id=1)
        self.assertEqual(book_instance.borrower, user)

    def test_is_overdue_false(self):
        book_instance = BookInstance.objects.first()
        book_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertFalse(book_instance.is_overdue)

    def test_is_overdue_true(self):
        book_instance = BookInstance.objects.first()
        book_instance.due_back = datetime.date.today() - datetime.timedelta(weeks=4)
        self.assertTrue(book_instance.is_overdue)

    def test_object_name_title(self):
        book_instance = BookInstance.objects.first()
        expected_object_name = f'{book_instance.book.title}'
        self.assertEqual(expected_object_name, str(book_instance))


class GenreModelTest(TestCase):
    @ classmethod
    def setUpTestData(cls) -> None:
        Genre.objects.create(name='Fantasy')

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        genre = Genre.objects.get(id=1)
        expected_object_name = f'{genre.name}'
        self.assertEqual(expected_object_name, str(genre))


class LanguageModelTest(TestCase):
    @ classmethod
    def setUpTestData(cls) -> None:
        Language.objects.create(name='English')

    def test_name_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        language = Language.objects.get(id=1)
        expected_object_name = f'{language.name}'
        self.assertEqual(expected_object_name, str(language))
