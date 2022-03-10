from ast import arg
from queue import Empty
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, auction_listings, bids, comments
from .forms import createlisting, newoffer, newcomment

categories = ["Electronic", "Furniture", "Books", "Clothes", "Videogames", "Miscellaneous"]

def index(request):
    active_listings = auction_listings.objects.exclude(finished = True).all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        form = createlisting(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Product']
            description = form.cleaned_data['Description']
            price = form.cleaned_data['Price']
            image = form.cleaned_data['Image']
            category = form.cleaned_data['Category']

            auction = auction_listings()
            auction.product = name
            auction.description = description
            auction.image = image
            auction.seller = request.user
            auction.startingbid = price
            auction.category = category
            auction.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = createlisting()
        return render(request, "auctions/listing.html", {
            "form": form
        })


def auction(request, listing_id):
    auction = auction_listings.objects.get(pk = listing_id)
    bid = bids()
    bid.listing = auction
    if request.user not in auction.watchers.all():
        watcher = False
    else:
        watcher = True
    if request.method == "POST":
        form = newoffer(request.POST)
        if form.is_valid():
            offer = form.cleaned_data['offer']
            if valid(offer,auction):
                auction.currentbid = offer
                auction.save()
                bid = bids()
                bid.listing = auction
                bid.offer = offer
                bid.buyer = request.user
                bid.save()
                return HttpResponseRedirect(reverse("auction", args=[listing_id]))
            else:
                return render(request, "auctions/auction.html", {
                    "auction": auction,
                    "form": newoffer(),
                    "error": True,
                    "user": request.user,
                    "watcher": watcher,
                    "commentform": newcomment(),
                    "commentbox": auction.get_comments.all()
                })
                
    else:
        try:
             bid = bids.objects.get(listing = auction)
        except bid.DoesNotExist:
            return render(request, "auctions/auction.html", {
                "auction": auction,
                "form": newoffer(),
                "user": request.user,
                "buyer": None,
                "watcher": watcher,
                "commentform": newcomment(),
                "commentbox": auction.get_comments.all()
            })
        buyer = bids.objects.filter(listing = auction).last().buyer
        return render(request, "auctions/auction.html", {
                "auction": auction,
                "form": newoffer(),
                "user": request.user,
                "buyer": buyer,
                "watcher": watcher,
                "commentform": newcomment(),
                "commentbox": auction.get_comments.all()
            })


def valid(offer, auction):
    if offer > auction.startingbid and offer > auction.currentbid:
        return True
    else:
        return False    


@login_required
def makecomment(request, listing_id):
    auction = auction_listings.objects.get(pk=listing_id)
    if request.method == "POST":
        form = newcomment(request.POST)
        if form.is_valid():
            commentary = form.cleaned_data['comment']
            addcomment = comments()
            addcomment.listing = auction
            addcomment.comment = commentary
            addcomment.writer = request.user
            addcomment.save()
        return HttpResponseRedirect(reverse("auction", args=[listing_id]))


def addwatchlist(request, listing_id):
    listing = auction_listings.objects.get(pk=listing_id)
    if request.user not in listing.watchers.all():
        listing.watchers.add(request.user)
        watcher = True
    else:
        watcher = True    
        return render(request, "auctions/auction.html", {
            "auction": listing,
            "form": newoffer(),
            "Already": True,
            "user": request.user,
            "watcher": watcher,
            "commentform": newcomment(),
            "commentbox": auction.get_comments.all()
        })
    return HttpResponseRedirect(reverse("auction", args=[listing_id]))


def watchlist(request):
    listings = auction_listings.objects.filter(watchers= request.user, finished = False)
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })


def delete_watchlist(request, listing_id):
    listing = auction_listings.objects.get(pk=listing_id)
    if request.user in listing.watchers.all():
        listing.watchers.remove(request.user)
    return HttpResponseRedirect(reverse("auction", args=[listing_id]))


def winned(request):
    listings = auction_listings.objects.filter(buyer = request.user)
    return render(request, "auctions/winned.html",{
        "listings": listings
    })

def finishauc(request, listing_id):
    listing = auction_listings.objects.get(pk=listing_id)
    return render(request,"auctions/finishauc.html",{
        "auction": listing
    })
       

@login_required
def finish(request, listing_id):
    auction = auction_listings.objects.get(pk = listing_id)
    bid = bids()
    try:
        bid = bids.objects.get(listing = auction)
    except bid.DoesNotExist:
        auction.finished = True
        auction.save()
        return HttpResponseRedirect(reverse("index"))
    auction.finished = True
    auction.buyer = bids.objects.filter(listing = auction).last().buyer
    auction.save()
    return HttpResponseRedirect(reverse("index"))
    


def categorie(request, listing_category):
    auction = auction_listings.objects.filter(category = listing_category, finsihed = False)
    return render(request, "auctions/categories.html", {
        "listings": auction,
        "category": listing_category
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
