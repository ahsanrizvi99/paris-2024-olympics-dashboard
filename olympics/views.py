import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from .models import Athlete, Event, Medal
from .forms import CustomUserCreationForm

@login_required
def home(request):
    top_athletes = Athlete.objects.all()[:5]
    top_events = Event.objects.all()[:5]
    top_medalists = Medal.objects.select_related('athlete', 'event').all()[:5]

    context = {
        'total_athletes': Athlete.objects.count(),
        'total_events': Event.objects.count(),
        'total_medals': Medal.objects.count(),
        'top_athletes': top_athletes,
        'top_events': top_events,
        'top_medalists': top_medalists,
    }
    return render(request, 'home.html', context)

from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def athletes_list(request):
    query = request.GET.get('q', '')
    sport_filter = request.GET.get('sport', '')

    # Base QuerySet for all athletes
    athletes = Athlete.objects.all()

    # Apply search filter (by name or country)
    if query:
        athletes = athletes.filter(Q(name__icontains=query) | Q(country__icontains=query))

    # Apply sport filter
    if sport_filter:
        athletes = athletes.filter(sport__icontains=sport_filter)

    # List of distinct sports for filtering options
    sports = Athlete.objects.values_list('sport', flat=True).distinct()

    # Count athletes per sport
    athletes_by_sport = (
        athletes.values('sport')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    context = {
        'athletes': athletes,
        'sports': sports,
        'query': query,
        'sport_filter': sport_filter,
        'athletes_by_sport': athletes_by_sport,
    }
    return render(request, 'athletes.html', context)

@login_required
def events_list(request):
    query = request.GET.get('q', '')  # Get the search query
    sport_filter = request.GET.get('sport_code', '')  # Get the sport code filter

    # Base query for events
    events = Event.objects.all()

    # Apply search functionality
    if query:
        events = events.filter(
            Q(name__icontains=query) | Q(sport__icontains=query)
        )

    # Apply sport code filter
    if sport_filter:
        events = events.filter(sport_code__icontains=sport_filter)

    # Populate distinct sport codes for dropdown
    sport_codes = Event.objects.values_list('sport_code', flat=True).distinct()

    return render(request, 'events.html', {
        'events': events,
        'sport_codes': sport_codes,
        'query': query,
        'sport_filter': sport_filter,
    })

@login_required
def medals_list(request):
    # Fetch medal types dynamically
    medal_types = Medal.objects.values_list('medal_type', flat=True).distinct()

    # Get filter values
    medal_filter = request.GET.get('medal_type')
    athlete_query = request.GET.get('athlete_name')
    country_query = request.GET.get('country')

    # Base queryset
    medals = Medal.objects.select_related('athlete', 'event')

    # Filter by medal type
    if medal_filter:
        medals = medals.filter(medal_type=medal_filter)

    # Search by athlete name
    if athlete_query:
        medals = medals.filter(athlete__name__icontains=athlete_query)

    # Search by country
    if country_query:
        medals = medals.filter(country__icontains=country_query)

    context = {
        'medals': medals,
        'medal_types': medal_types,
        'medal_filter': medal_filter,
        'athlete_query': athlete_query,
        'country_query': country_query,
    }
    return render(request, 'medals.html', context)
   
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.db.models import Count
from .models import Athlete, Event, Medal
import io
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend
  
@login_required   
def athletes_by_country_graph(request):
    # Get the top 10 countries by the number of athletes
    data = Athlete.objects.values('country').annotate(count=Count('id')).order_by('-count')[:10]
    countries = [item['country'] for item in data]
    counts = [item['count'] for item in data]
 
    # Create the bar chart with countries on the x-axis
    plt.figure(figsize=(10, 6))
    plt.bar(countries, counts, color='gold')
    plt.xlabel('Country')
    plt.ylabel('Number of Athletes')
    plt.title('Top 10 Countries by Number of Athletes')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.tight_layout()

    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Return the image as HTTP response
    return HttpResponse(buf, content_type='image/png')

@login_required
def athletes_visualization(request):
    data = Athlete.objects.values('country').annotate(count=Count('id')).order_by('-count')
    countries = [item['country'] for item in data]
    counts = [item['count'] for item in data]

    plt.figure(figsize=(10, 6))
    plt.bar(countries, counts, color='gold')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Country')
    plt.ylabel('Number of Athletes')
    plt.title('Number of Athletes by Country')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return HttpResponse(buf, content_type='image/png')

# View for Events Visualization

@login_required
def events_visualization(request):
    # Get the top 10 sports by the number of events
    data = Event.objects.values('sport').annotate(count=Count('id')).order_by('-count')[:10]
    sports = [item['sport'] for item in data]
    counts = [item['count'] for item in data]

    # Create the pie chart
    plt.figure(figsize=(10, 6))
    wedges, _, autotexts = plt.pie(
        counts,
        labels=None,  # Don't label the pie directly
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.tab20.colors[:len(counts)]  # Use consistent color palette
    )
  
    # Add legend on the top right
    plt.legend(
        wedges, sports,
        title="Sports",
        loc="upper right",
        bbox_to_anchor=(1.3, 1),  # Adjust position of legend
        frameon=False  # Optional: remove legend box border
    )

    # Add title
    plt.title('Percentage of Events by Sport (Top 10)')
    plt.tight_layout()

    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Return the image as HTTP response
    return HttpResponse(buf, content_type='image/png')

@login_required
def medals_visualization(request):
    data = Medal.objects.values('country').annotate(count=Count('id')).order_by('-count')
    countries = [item['country'] for item in data]
    counts = [item['count'] for item in data]

    plt.figure(figsize=(10, 6))
    plt.bar(countries, counts, color='gold')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Country')
    plt.ylabel('Number of Medals')
    plt.title('Number of Medals by Country')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return HttpResponse(buf, content_type='image/png')


@login_required
def export_athletes_csv(request):
    # Get filters from GET parameters
    query = request.GET.get('q', '')
    sport_filter = request.GET.get('sport', '')

    # Base queryset
    athletes = Athlete.objects.all()

    # Apply filters
    if query:
        athletes = athletes.filter(Q(name__icontains=query) | Q(country__icontains=query))
    if sport_filter:
        athletes = athletes.filter(sport__icontains=sport_filter)

    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_athletes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Country', 'Sport', 'Height', 'Weight'])  # Headers

    # Write data
    for athlete in athletes:
        writer.writerow([athlete.name, athlete.country, athlete.sport, athlete.height, athlete.weight])

    return response

@login_required
def export_athletes_pdf(request):
    # Get filters from GET parameters
    query = request.GET.get('q', '')
    sport_filter = request.GET.get('sport', '')

    # Base queryset
    athletes = Athlete.objects.all()

    # Apply filters
    if query:
        athletes = athletes.filter(Q(name__icontains=query) | Q(country__icontains=query))
    if sport_filter:
        athletes = athletes.filter(sport__icontains=sport_filter)

    # Define title, headings, and data for the template
    title = "Filtered Athletes List"
    headings = ["Name", "Country", "Sport", "Height", "Weight"]
    data = [[athlete.name, athlete.country, athlete.sport, athlete.height, athlete.weight] for athlete in athletes]

    # Render and generate PDF
    template = get_template('export_pdf.html')
    html = template.render({'title': title, 'headings': headings, 'data': data})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="filtered_athletes.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with generating your PDF.')
    return response

@login_required
def export_events_csv(request):
    # Get filters from GET parameters
    query = request.GET.get('q', '')
    sport_code_filter = request.GET.get('sport_code', '')

    # Base queryset
    events = Event.objects.all()

    # Apply filters
    if query:
        events = events.filter(Q(name__icontains=query) | Q(sport__icontains=query))
    if sport_code_filter:
        events = events.filter(sport_code__icontains=sport_code_filter)

    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_events.csv"'

    writer = csv.writer(response)
    writer.writerow(['Event Name', 'Sport', 'Sport Code'])  # Headers

    # Write data
    for event in events:
        writer.writerow([event.name, event.sport, event.sport_code])

    return response

@login_required
def export_events_pdf(request):
    # Get filters from GET parameters
    query = request.GET.get('q', '')
    sport_code_filter = request.GET.get('sport_code', '')

    # Base queryset
    events = Event.objects.all()

    # Apply filters
    if query:
        events = events.filter(Q(name__icontains=query) | Q(sport__icontains=query))
    if sport_code_filter:
        events = events.filter(sport_code__icontains=sport_code_filter)

    # Define title, headings, and data for the template
    title = "Filtered Events List"
    headings = ["Event Name", "Sport", "Sport Code"]
    data = [[event.name, event.sport, event.sport_code] for event in events]

    # Render and generate PDF
    template = get_template('export_pdf.html')
    html = template.render({'title': title, 'headings': headings, 'data': data})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="filtered_events.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with generating your PDF.')
    return response
@login_required
def export_medals_csv(request):
    # Get filters from GET parameters
    medal_filter = request.GET.get('medal_type', '')
    athlete_query = request.GET.get('athlete_name', '')
    country_query = request.GET.get('country', '')

    # Base queryset
    medals = Medal.objects.select_related('athlete', 'event').all()

    # Apply filters
    if medal_filter:
        medals = medals.filter(medal_type__icontains=medal_filter)
    if athlete_query:
        medals = medals.filter(athlete__name__icontains=athlete_query)
    if country_query:
        medals = medals.filter(country__icontains=country_query)

    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_medals.csv"'

    writer = csv.writer(response)
    writer.writerow(['Athlete', 'Country', 'Event', 'Medal Type'])  # Headers

    # Write data
    for medal in medals:
        writer.writerow([
            medal.athlete.name if medal.athlete else "N/A",
            medal.country,
            medal.event.name if medal.event else "N/A",
            medal.medal_type
        ])

    return response
@login_required
def export_medals_pdf(request):
    # Get filters from GET parameters
    medal_filter = request.GET.get('medal_type', '')
    athlete_query = request.GET.get('athlete_name', '')
    country_query = request.GET.get('country', '')

    # Base queryset
    medals = Medal.objects.select_related('athlete', 'event').all()

    # Apply filters
    if medal_filter:
        medals = medals.filter(medal_type__icontains=medal_filter)
    if athlete_query:
        medals = medals.filter(athlete__name__icontains=athlete_query)
    if country_query:
        medals = medals.filter(country__icontains=country_query)

    # Define title, headings, and data for the template
    title = "Filtered Medals List"
    headings = ["Athlete", "Country", "Event", "Medal Type"]
    data = [[
        medal.athlete.name if medal.athlete else "N/A",
        medal.country,
        medal.event.name if medal.event else "N/A",
        medal.medal_type
    ] for medal in medals]

    # Render and generate PDF
    template = get_template('export_pdf.html')
    html = template.render({'title': title, 'headings': headings, 'data': data})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="filtered_medals.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with generating your PDF.')
    return response
