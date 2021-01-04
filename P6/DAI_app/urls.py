from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('library', views.select_table, name='table_selection'),
	path('load-table',views.choose_table, name='select_table'),
	path('library/authors', views.AuthorList.as_view(), name='authors'),
	path('library/create-author',views.AuthorCreate.as_view(), name='create_author'),
	path('library/authors/<int:pk>',views.AuthorDetail.as_view(),name='author_details'),
	path('library/delete-author/<int:pk>',views.AuthorDelete.as_view(),name='delete_author'),
	path('library/update-author/<int:pk>',views.AuthorUpdate.as_view(), name='update_author'),
	path('library/books', views.BookList.as_view(), name='books'),
	path('library/create-book', views.BookCreate.as_view(), name='create_book'),
	path('library/books/<int:pk>', views.BookDetail.as_view(), name='book_details'),
	path('library/delete-book/<int:pk>', views.BookDelete.as_view(), name='delete_book'),
	path('library/update-book/<int:pk>', views.BookUpdate.as_view(), name='update_book'),
	path('library/loans', views.LoanList.as_view(), name='loans'),
	path('library/create-loan', views.LoanCreate.as_view(), name='create_loan'),
	path('library/delete-loan/<int:pk>', views.LoanDelete.as_view(), name='delete_loan')
]
