from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
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
	path('library/delete-loan/<int:pk>', views.LoanDelete.as_view(), name='delete_loan'),
	path('signup', views.SignUpView.as_view(), name='signup'),
	path('login-error', views.login_error, name='login_error'),
	path('registered-user', views.registered_user, name='registered_user'),
	path('library/user-loans', views.list_user_loans, name='user_loans'),
	path('library/take-out-loan', views.take_out_loan, name='take_out_loan'),
	path('create-user-loan',views.create_user_loan,name='create_user_loan')
]
