from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("expenses/", views.ExpenseCreate.as_view()),
    path("expenses/<int:pk>/", views.ExpenseDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
