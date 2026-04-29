from flask import Blueprint, render_template, redirect, url_for, request, flash
from .forms import TicketForm

main_bp = Blueprint('main', __name__)


# ── Dummy data ──
temp_event = {
    'id': 1,
    'title': 'The Static Echo — Live at Black Bear Lodge',
    'venue': 'Black Bear Lodge, Fortitude Valley',
    'address': '1/322 Brunswick St, Fortitude Valley QLD 4006',
    'date': 'Sat 19 Apr 2025',
    'time': '8:00 PM — 11:30 PM',
    'price': 18.00,
    'tickets_available': 42,
    'status': 'Open',
    'category': 'Indie Rock',
    'description': 'The Static Echo return to Black Bear Lodge for a night of raw, reverb-drenched indie rock.',
    'acknowledgement_type': 'enhanced'
}

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/events')
def events():
    return render_template('events.html')

@main_bp.route('/event/<int:id>', methods=['GET', 'POST'])
def event_detail(id):
    form = TicketForm()
    event = temp_event

    if form.validate_on_submit():
        quantity = form.quantity.data

        if quantity > event['tickets_available']:
            flash(f'Sorry, only {event["tickets_available"]} tickets are available.')
            return redirect(url_for('main.event-details', id=id))

        event['tickets_available'] -= quantity

        if event['tickets_available'] == 0:
            event['status'] = 'Sold Out'

        flash('Tickets booked successfully!')
        return redirect(url_for('main.order_confirmation', quantity=quantity))

    dummy_comments = [
        {'author': 'Jordan Lee', 'date': '14 Apr 2025', 'text': 'Saw these guys last year — absolute standouts!'},
        {'author': 'Samira K.', 'date': '15 Apr 2025', 'text': 'Is this all ages? Bringing my younger sister.'},
    ]

    return render_template('event-details.html', event=event, form=form, comments=dummy_comments)

@main_bp.route('/order-confirmation')
def order_confirmation():
    quantity = request.args.get('quantity', 1, type=int)
    return render_template('order-confirmation.html', quantity=quantity, event=temp_event)

@main_bp.route('/create-event', methods=['GET', 'POST'])
def create_event():
    return render_template('create-event.html')

@main_bp.route('/event/<int:id>/edit', methods=['GET', 'POST'])
def edit_event(id):
    return render_template('edit-event.html')

@main_bp.route('/booking-history')
def booking_history():
    return render_template('booking-history.html')

