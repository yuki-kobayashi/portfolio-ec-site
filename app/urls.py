from django.urls import path
from app import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("product/<slug>", views.ItemDetailView.as_view(), name="product"),
    path("additem/<slug>", views.add_item, name="additem"),
    path("order/", views.OrderView.as_view(), name="order"),
    path("removeitem/<slug>", views.remove_item, name="removeitem"),
    path("removesingleitem/<slug>", views.remove_single_item, name="removesingleitem"),
    path("payment/", views.PaymentView.as_view(), name="payment"),
    path("thanks/", views.ThanksView.as_view(), name="thanks"),
    path("search/", views.SearchView.as_view(), name="search"),
    path('toggle-favorite/<slug:slug>/', views.toggle_favorite, name='toggle-favorite'),
]
