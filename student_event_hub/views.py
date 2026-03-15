from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from events.models import Event, Registration

# M2: Realistic Event List Rendering
def event_list(request):
    """
    Fetches all events from the database, ordered by their start time.
    Renders the main events listing page.
    """
    events = Event.objects.all().order_by('start_time')
    return render(request, 'Events.html', {'events': events})

# AJAX Search API
def search_events(request):
    """
    Handles AJAX-based search queries.
    Performs a fuzzy search on 'title' and 'category' fields using SQL LIKE equivalents.
    """
    query = request.GET.get('q', '').lower()

    if query:
        events = Event.objects.filter(title__icontains=query) | Event.objects.filter(category__icontains=query)
    else:
        events = Event.objects.all()

    # Convert QuerySet to a list of dictionaries for JSON serialization
    events_data = [
        {
            'id': e.id,
            'title': e.title,
            'date_time': e.start_time.strftime('%B %d %H:%M'),
            'location': e.location,
            'category': e.category,
            'description': e.description,
            'image': e.image
        } for e in events
    ]
    return JsonResponse({'events': events_data})

# Event Detail and Registration Logic
def event_detail(request, event_id):
    """
    Retrieves a specific event by its ID.
    Uses get_object_or_404 to ensure robust error handling.
    """
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events_details.html', {'event': event})
@login_required
def event_register(request, event_id):
    """
    Handles event registration for authenticated users.
    Implements @login_required decorator for access control.
    """
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Capture form data submitted by the user
        phone_number = request.POST.get('phone', '')
        user_remarks = request.POST.get('remarks', '')

        # 预留位：M5 防冲突算法

        # Store the registration record in the database
        Registration.objects.get_or_create(
            student=request.user,
            event=event,
            defaults={'phone': phone_number, 'remarks': user_remarks}
        )
        print(f"✅ Success: User {request.user.username} registered for {event.title}!")
        return redirect('my_tickets')

    return render(request, 'event_registration.html', {'event': event})

# Admin-only: Event Creation View
@login_required
def create_event(request):
    """
    Administrative view for editing events.
    Restricted to staff users via authorization checks.
    """
    if not request.user.is_staff:
        # Authorization check: redirect non-staff users to the home page
        return redirect('home')
    return render(request, 'create_event.html')

# My Tickets
@login_required
def my_tickets(request):
    # Retrieves and displays all event registrations for the currently logged-in student
    registrations = Registration.objects.filter(student=request.user).select_related('event')

    # Pass the registration QuerySet to the 'my_tickets.html' template
    return render(request, 'my_tickets.html', {'registrations': registrations})