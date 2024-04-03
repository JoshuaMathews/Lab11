from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

@login_required
def place_list(request):
    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) # creating the model object from form data
        place.user = request.user

        if form.is_valid(): # making sure all of the user supplied data is valid
            place.save() # save to database
            return redirect('place_list')
            # redirect to home page which is an easy way of just allowing a user to
            # 1. See their changes
            # 2. Enable them to send more easily


    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name') # get where we HAVE NOT visited and then order by name.
    new_place_form = NewPlaceForm() # new model object

    return render(request, 'travel_wishlist/wishlist.html', {'places' : places, 'new_place_form' : new_place_form})
    # Feed it path to wishlist, feed it the user's places, and a finally a form so everything can be combined and displayed.

@login_required
def about(request):
    author = 'Josh Mathews'
    about = 'A website to create a list of places to visit'

    return render(request, 'travel_wishlist/about.html', {'author': author, 'about' : about}) # feed variables into django so it can display data in the about page.

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True) # grab all of the objects that ARE visited.
    return render(request, 'travel_wishlist/visited.html', {"visited": visited})

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk) # get single object from DB by primary key
        place = get_object_or_404(Place, pk=place_pk) # try to get a single object from DB and if that fails, 404 them.

        print(f"VISITED {place.user} {request.user} {place.user == request.user}")

        if place.user == request.user:
            place.visited = True  # set visited directly to true
            place.save()  # save to DB and we're done
        else:
            return HttpResponseForbidden()

    return redirect('place_list') # go back to the same page to reflect new data changes.

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)  # try to get a single object from DB and if that fails, 404 them.

    #print(f"DELETE {place.user} {request.user} {place.user == request.user}")

    if place.user == request.user: # Check if the place's owner is the same person making the request.
        place.delete() # Delete
        return redirect('place_list') # Go back and show new data
    else:
        return HttpResponseForbidden() # owner isn't correct and deny them outright.

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    if place.user != request.user:
        return HttpResponseForbidden()  # owner isn't correct and deny them outright.

    if request.method == "POST": # POST request so we're updating information
        form = TripReviewForm(request.POST, request.FILES, instance=place)

        if form.is_valid():
            form.save()
            messages.info(request, 'Trip Information Updated')
        else:
            messages.error(request, form.errors) # if not valid then return the errors

        return redirect('place_details', place_pk=place_pk) # redirect after.
    else:
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})