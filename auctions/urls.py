from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("<int:listing_id>", views.auction, name="auction"),
    path("<int:listing_id>/finish", views.finish, name="finish"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/addwatchlist", views.addwatchlist, name="addwatchlist"),
    path("<int:listing_id>/delwatchlist", views.delete_watchlist, name="delete_watchlist"),
    path("categories/<str:listing_category>", views.categorie, name="categories"),
    path("<int:listing_id>/comment", views.makecomment, name="makecomment"),
    path("winned", views.winned, name="winned"),
    path("<int:listing_id>/finished", views.finishauc, name="finishauc")
]
