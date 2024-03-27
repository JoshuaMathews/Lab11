from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

def place_list(request):
    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)
        place = form.save() # creating the model object from form data

        if form.is_valid(): # making sure all of the user supplied data is valid
            place.save() # save to database
            return redirect('place_list')
            # redirect to home page which is an easy way of just allowing a user to
            # 1. See their changes
            # 2. Enable them to send more easily


    places = Place.objects.filter(visited=False).order_by('name') # get where we HAVE NOT visited and then order by name.
    new_place_form = NewPlaceForm() # new model object

    return render(request, 'travel_wishlist/wishlist.html', {'places' : places, 'new_place_form' : new_place_form})
    # Feed it path to wishlist, feed it the user's places, and a finally a form so everything can be combined and displayed.

def about(request):
    author = 'Josh Mathews'
    about = 'A website to create a list of places to visit'

    return render(request, 'travel_wishlist/about.html', {'author': author, 'about' : about}) # feed variables into django so it can display data in the about page.

def places_visited(request):
    visited = Place.objects.filter(visited=True) # grab all of the objects that ARE visited.
    return render(request, 'travel_wishlist/visited.html', {"visited": visited})

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk) # get single object from DB by primary key
        place = get_object_or_404(Place, pk=place_pk) # try to get a single object from DB and if that fails, 404 them.

        place.visited = True # set visited directly to true
        place.save() # save to DB and we're done

    return redirect('place_list') # go back to the same page to reflect new data changes.