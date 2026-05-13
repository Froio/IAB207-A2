from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .forms import TicketForm
from .models import Event, Order
from . import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/events')
def events():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'soonest')

    all_events = db.session.scalars(db.select(Event)).all()
    filtered_events = list(all_events)

    if category != 'all':
        filtered_events = [e for e in filtered_events if e.category == category]

    if search:
        search_lower = search.lower()
        filtered_events = [e for e in filtered_events if
            search_lower in e.title.lower() or
            search_lower in e.venue.lower() or
            search_lower in e.description.lower() or
            search_lower in e.category.lower()]

    def normalise_sort_text(value):
        value = value.strip().lower()
        for prefix in ('the ', 'a ', 'an '):
            if value.startswith(prefix):
                return value[len(prefix):].strip()
        return value

    if sort == 'price-asc':
        filtered_events = [e for e in filtered_events if e.status not in ('Cancelled', 'Inactive')]
        filtered_events = sorted(filtered_events, key=lambda e: e.price)
    elif sort == 'price-desc':
        filtered_events = [e for e in filtered_events if e.status not in ('Cancelled', 'Inactive')]
        filtered_events = sorted(filtered_events, key=lambda e: e.price, reverse=True)
    elif sort == 'title-asc':
        filtered_events = sorted(filtered_events, key=lambda e: normalise_sort_text(e.title))
    elif sort == 'title-desc':
        filtered_events = sorted(filtered_events, key=lambda e: normalise_sort_text(e.title), reverse=True)
    elif sort == 'venue-asc':
        filtered_events = sorted(filtered_events, key=lambda e: normalise_sort_text(e.venue))
    elif sort == 'venue-desc':
        filtered_events = sorted(filtered_events, key=lambda e: normalise_sort_text(e.venue), reverse=True)
    else:
        filtered_events = sorted(filtered_events, key=lambda e: e.start_date)

    return render_template('events.html', events=filtered_events, current_category=category, current_search=search, current_sort=sort)

@main_bp.route('/event/<int:id>', methods=['GET', 'POST'])
def event_detail(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))

    if event is None:
        flash('Event not found.')
        return redirect(url_for('main.events'))

    form = TicketForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.path))

        quantity = form.quantity.data

        if quantity > event.tickets_available:
            flash(f'Sorry, only {event.tickets_available} tickets are available.')
            return redirect(url_for('main.event_detail', id=id))

        # Create order
        order = Order(
            quantity=quantity,
            total_price=round(event.price * quantity + 1.50, 2),
            booking_fee=1.50,
            order_date=datetime.utcnow(),
            user_id=current_user.id,
            event_id=event.id
        )
        db.session.add(order)

        # Update ticket count
        event.tickets_available -= quantity
        if event.tickets_available == 0:
            event.status = 'Sold Out'

        db.session.commit()

        return redirect(url_for('main.order_confirmation', order_id=order.id))

    comments = event.comments

    return render_template('event-details.html', event=event, form=form, comments=comments)

@main_bp.route('/order-confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = db.session.scalar(db.select(Order).where(Order.id == order_id))
    if order is None:
        flash('Order not found.')
        return redirect(url_for('main.events'))
    return render_template('order-confirmation.html', order=order, event=order.event)

@main_bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    return render_template('create-event.html')

@main_bp.route('/event/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    return render_template('edit-event.html')

@main_bp.route('/booking-history')
@login_required
def booking_history():
    orders = db.session.scalars(
        db.select(Order)
        .where(Order.user_id == current_user.id)
        .order_by(Order.order_date.desc())
    ).all()
    return render_template('booking-history.html', orders=orders)


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')