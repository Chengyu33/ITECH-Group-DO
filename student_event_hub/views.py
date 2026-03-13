from django.shortcuts import render
from django.http import JsonResponse

# Mock data
MOCK_EVENTS = [
    {
        'id': 1,
        'title': 'Campus Music Festival',
        'date_time': 'February 2 19:00',
        'location': 'Main Gate',
        'category': 'Entertainment',
        'description': 'Craving the stage? Love being live? Join this wild party! From indie bands to pop hits, tonight we dance just for the pure love of music.',
        'image': 'https://th.bing.com/th/id/OIP.Q1UImiWqNyOj2V93wdIO6gHaEv?w=307&h=196&c=7&r=0&o=7&pid=1.7&rm=3'
    },
    {
        'id': 2,
        'title': 'Freshmen Campus Tour Activity',
        'date_time': 'September 20 08:00',
        'location': 'James McCune Smith learning hub 438AB',
        'category': 'Academic',
        'description': 'The first step of the new semester starts with making new friends! A walking-and-talking campus exploration journey helps you get familiar with the environment while quickly integrating into the brand-new university circle.',
        'image': 'https://th.bing.com/th/id/OIP.NUmbQCq7CqftJ3YR-fal5AHaEw?w=265&h=180&c=7&r=0&o=7&pid=1.7&rm=3'
    },
    {
        'id': 3,
        'title': 'Introduction to Python Data Analysis Lecture',
        'date_time': 'May 1 18:30',
        'location': 'Boyd Orr Building:1028 Lab',
        'category': 'Academic',
        'description': 'Friendly for beginners! Hand-in-hand guidance on how to use Python to process and analyze daily data. Limited spots, first come first served.',
        'image': 'https://cfmnsugzia.cloudimg.io/www.gla.ac.uk/media/Media_1188733_smxx.png?width=1400&force_format=webp'
    }
]

# Main page
def event_list(request):
    context = {
        'events': MOCK_EVENTS
    }
    return render(request, 'Events.html', context)

# AJAX Search API
def search_events(request):
    query = request.GET.get('q', '').lower()

    if query:
        filtered_events = [
            event for event in MOCK_EVENTS
            if query in event['title'].lower() or query in event['category'].lower()
        ]
    else:
        filtered_events = MOCK_EVENTS

    return JsonResponse({'events': filtered_events})