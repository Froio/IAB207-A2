from flask import Blueprint, render_template, redirect, url_for, request, flash
from .forms import TicketForm

main_bp = Blueprint('main', __name__)


# ── Dummy data ──
temp_events = [
    {
        'id': 1,
        'title': 'The Static Echo — Live at Black Bear Lodge',
        'venue': 'Black Bear Lodge, Fortitude Valley',
        'address': '1/322 Brunswick St, Fortitude Valley QLD 4006',
        'date': 'Sat 19 Apr 2026',
        'time': '8:00 PM — 11:30 PM',
        'price': 18.00,
        'tickets_available': 42,
        'status': 'Open',
        'category': 'Indie Rock',
        'description': 'The Static Echo return to Black Bear Lodge for a night of raw, reverb-drenched indie rock.',
        'acknowledgement_type': 'enhanced',
        'image': 'img/indie_concert.jpg'
    },
    {
        'id': 2,
        'title': 'River Hollow Acoustic Session',
        'venue': 'Black Bear Lodge, Fortitude Valley',
        'address': '1/322 Brunswick St, Fortitude Valley QLD 4006',
        'date': 'Fri 25 Apr 2026',
        'time': '7:30 PM — 10:00 PM',
        'price': 12.00,
        'tickets_available': 18,
        'status': 'Open',
        'category': 'Folk',
        'description': 'River Hollow bring their stripped back acoustic sound to Black Bear Lodge for an intimate evening.',
        'acknowledgement_type': 'generic',
        'image': 'img/folk.webp'
    },
    {
        'id': 3,
        'title': 'Purple Haze — The Night Room',
        'venue': 'The Brightside, Fortitude Valley',
        'address': '27 Warner St, Fortitude Valley QLD 4006',
        'date': 'Sat 26 Apr 2026',
        'time': '9:00 PM — 12:00 AM',
        'price': 22.00,
        'tickets_available': 0,
        'status': 'Sold Out',
        'category': 'Shoegaze',
        'description': 'Purple Haze sell out The Brightside for a night of dreamy, effects-laden shoegaze.',
        'acknowledgement_type': 'none',
        'image': 'img/shoegaze.jpg'
    },
    {
        'id': 4,
        'title': 'Moonbeam Collective',
        'venue': 'The Tivoli, Fortitude Valley',
        'address': '52 Costin St, Fortitude Valley QLD 4006',
        'date': 'Thu 1 May 2026',
        'time': '8:30 PM — 11:00 PM',
        'price': 20.00,
        'tickets_available': 60,
        'status': 'Open',
        'category': 'Dream Pop',
        'description': 'Moonbeam Collective bring their ethereal dream pop sound to The Tivoli.',
        'acknowledgement_type': 'generic',
        'image': 'img/alt_concert.jpg'
    },
    {
        'id': 5,
        'title': 'Wire & Static — Fortitude Valley',
        'venue': 'The Zoo, Fortitude Valley',
        'address': '711 Ann St, Fortitude Valley QLD 4006',
        'date': 'Sat 3 May 2026',
        'time': '9:00 PM — 12:00 AM',
        'price': 15.00,
        'tickets_available': 0,
        'status': 'Cancelled',
        'category': 'Post-Punk',
        'description': 'Wire & Static bring their post-punk sound to The Zoo.',
        'acknowledgement_type': 'none',
        'image': 'img/WirenStatic.jpeg'
    },
    {
        'id': 6,
        'title': 'Sunday Tape Session',
        'venue': "Lefty's Music Hall, Brisbane CBD",
        'address': '15 Caxton St, Brisbane QLD 4000',
        'date': 'Sun 4 May 2026',
        'time': '3:00 PM — 6:00 PM',
        'price': 0.00,
        'tickets_available': 30,
        'status': 'Open',
        'category': 'Lo-Fi',
        'description': 'A relaxed Sunday afternoon of lo-fi beats and good vibes.',
        'acknowledgement_type': 'generic',
        'image': 'img/Swingamajig.webp'
    },
    {
        'id': 7,
        'title': 'Dustbowl Riders',
        'venue': 'The Joynt, West End',
        'address': '193 Boundary St, West End QLD 4101',
        'date': 'Sat 15 Mar 2026',
        'time': '8:00 PM — 11:00 PM',
        'price': 10.00,
        'tickets_available': 0,
        'status': 'Inactive',
        'category': 'Alt Country',
        'description': 'Dustbowl Riders bring their alt country sound to The Joynt.',
        'acknowledgement_type': 'none',
        'image': 'img/country.avif'
    },
    {
        'id': 8,
        'title': 'Glass Houses',
        'venue': 'The Foundry, Fortitude Valley',
        'address': '17 Doggett St, Fortitude Valley QLD 4006',
        'date': 'Fri 9 May 2026',
        'time': '10:00 PM — 1:00 AM',
        'price': 15.00,
        'tickets_available': 15,
        'status': 'Open',
        'category': 'Indie Rock',
        'description': 'Glass Houses close out the week with a late set at The Foundry.',
        'acknowledgement_type': 'none',
        'image': 'img/indie_rock.jpg'
    },
]



@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/events')
def events():
    return render_template('events.html', events=temp_events)

@main_bp.route('/event/<int:id>', methods=['GET', 'POST'])
def event_detail(id):
    form = TicketForm()
    event = next((e for e in temp_events if e['id'] == id), None)

    if event is None:
        flash('Event not found.')
        return redirect(url_for('main.events'))

    if form.validate_on_submit():
        quantity = form.quantity.data

        if quantity > event['tickets_available']:
            flash(f'Sorry, only {event["tickets_available"]} tickets are available.')
            return redirect(url_for('main.event_detail', id=id))

        event['tickets_available'] -= quantity

        if event['tickets_available'] == 0:
            event['status'] = 'Sold Out'

        return redirect(url_for('main.order_confirmation', quantity=quantity, event_id=id))

    dummy_comments = [
        {'author': 'Jordan Lee', 'date': '14 Apr 2025', 'text': 'Saw these guys last year — absolute standouts!'},
        {'author': 'Samira K.', 'date': '15 Apr 2025', 'text': 'Is this all ages? Bringing my younger sister.'},
    ]

    return render_template('event-details.html', event=event, form=form, comments=dummy_comments)

@main_bp.route('/order-confirmation')
def order_confirmation():
    quantity = request.args.get('quantity', 1, type=int)
    event_id = request.args.get('event_id', 1, type=int)
    event = next((e for e in temp_events if e['id'] == event_id), None)
    return render_template('order-confirmation.html', quantity=quantity, event=event)

@main_bp.route('/create-event', methods=['GET', 'POST'])
def create_event():
    return render_template('create-event.html')

@main_bp.route('/event/<int:id>/edit', methods=['GET', 'POST'])
def edit_event(id):
    return render_template('edit-event.html')

@main_bp.route('/booking-history')
def booking_history():
    return render_template('booking-history.html')

