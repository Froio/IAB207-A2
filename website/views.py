import os
from datetime import datetime
from flask import (
    Blueprint, render_template, redirect, url_for, request, flash, current_app
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import db
from .forms import TicketForm, CommentForm, EventForm
from .models import Event, Comment, Order


main_bp = Blueprint('main', __name__)


# ── helpers ─────────────────────────────────────────────────────────────

def _save_event_image(file_storage):
    """Save an uploaded image to static/img and return its relative path
    (e.g. 'img/myfile.jpg'). Returns None if no usable file was provided."""
    if not file_storage or not getattr(file_storage, 'filename', ''):
        return None
    filename = secure_filename(file_storage.filename)
    if not filename:
        return None
    # Make filename unique to avoid collisions
    stem, ext = os.path.splitext(filename)
    unique = f"{stem}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{ext}"
    dest_dir = os.path.join(current_app.root_path, 'static', 'img')
    os.makedirs(dest_dir, exist_ok=True)
    file_storage.save(os.path.join(dest_dir, unique))
    return f"img/{unique}"


# ── routes ──────────────────────────────────────────────────────────────

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/events')
def events():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'soonest')

    try:
        query = db.select(Event)

        if category != 'all':
            query = query.where(Event.category == category)

        if search:
            like = f"%{search}%"
            query = query.where(
                db.or_(
                    Event.title.ilike(like),
                    Event.venue.ilike(like),
                    Event.description.ilike(like),
                    Event.category.ilike(like),
                )
            )

        if sort == 'price-asc':
            query = query.where(~Event.status.in_(('Cancelled', 'Inactive')))
            query = query.order_by(Event.price.asc())
        elif sort == 'price-desc':
            query = query.where(~Event.status.in_(('Cancelled', 'Inactive')))
            query = query.order_by(Event.price.desc())
        elif sort == 'title-asc':
            query = query.order_by(Event.title.asc())
        elif sort == 'title-desc':
            query = query.order_by(Event.title.desc())
        elif sort == 'venue-asc':
            query = query.order_by(Event.venue.asc())
        elif sort == 'venue-desc':
            query = query.order_by(Event.venue.desc())
        else:
            query = query.order_by(Event.event_date.asc(), Event.start_time.asc())

        results = db.session.scalars(query).all()
    except Exception as e:
        current_app.logger.error(f'Events list error: {e}')
        flash('An error occurred while loading events.', 'danger')
        results = []

    return render_template('events.html',
        events=results,
        current_category=category,
        current_search=search,
        current_sort=sort)


@main_bp.route('/event/<int:id>', methods=['GET', 'POST'])
def event_detail(id):
    ticket_form = TicketForm()
    comment_form = CommentForm()

    try:
        event = db.session.scalar(db.select(Event).where(Event.id == id))
    except Exception as e:
        current_app.logger.error(f'Event detail load error: {e}')
        flash('An error occurred while loading the event.', 'danger')
        return redirect(url_for('main.events'))

    if event is None:
        flash('Event not found.', 'danger')
        return redirect(url_for('main.events'))

    # ── Comment submission ──
    if comment_form.submit_comment.data and comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please log in to post a comment.', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        try:
            comment = Comment(
                text=comment_form.text.data,
                user_id=current_user.id,
                event_id=event.id,
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment posted!', 'success')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Comment creation error: {e}')
            flash('An error occurred while posting your comment.', 'danger')
        return redirect(url_for('main.event_detail', id=id))

    # ── Ticket purchase ──
    if ticket_form.submit.data and ticket_form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.path))

        if event.status != 'Open':
            flash('Tickets are no longer available for this event.', 'warning')
            return redirect(url_for('main.event_detail', id=id))

        quantity = ticket_form.quantity.data
        if quantity > event.tickets_available:
            flash(f'Sorry, only {event.tickets_available} tickets are available.', 'warning')
            return redirect(url_for('main.event_detail', id=id))

        try:
            event.tickets_available -= quantity
            if event.tickets_available == 0:
                event.status = 'Sold Out'

            order = Order(
                quantity=quantity,
                total_price=event.price * quantity,
                user_id=current_user.id,
                event_id=event.id,
            )
            db.session.add(order)
            db.session.commit()
            flash('Tickets purchased successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Ticket purchase error: {e}')
            flash('An error occurred while processing your order.', 'danger')
            return redirect(url_for('main.event_detail', id=id))

        return redirect(url_for('main.order_confirmation',
            quantity=quantity, event_id=id, order_id=order.id))

    # ── Load comments (newest first) ──
    try:
        comments = db.session.scalars(
            db.select(Comment).where(Comment.event_id == id)
              .order_by(Comment.created_at.desc())
        ).all()
    except Exception as e:
        current_app.logger.error(f'Comment load error: {e}')
        flash('Could not load comments.', 'danger')
        comments = []

    return render_template('event-details.html',
        event=event,
        form=ticket_form,
        comment_form=comment_form,
        comments=comments)


@main_bp.route('/order-confirmation')
@login_required
def order_confirmation():
    quantity = request.args.get('quantity', 1, type=int)
    event_id = request.args.get('event_id', 0, type=int)
    order_id = request.args.get('order_id', 0, type=int)

    try:
        event = db.session.scalar(db.select(Event).where(Event.id == event_id))
    except Exception as e:
        current_app.logger.error(f'Order confirmation load error: {e}')
        flash('An error occurred while loading the confirmation.', 'danger')
        return redirect(url_for('main.events'))

    if event is None:
        flash('Event not found.', 'danger')
        return redirect(url_for('main.events'))

    return render_template('order-confirmation.html',
        quantity=quantity, event=event, order_id=order_id)


@main_bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        try:
            ## Acknowledgement of Country validation
            acknowledgement_type = form.acknowledgement_type.data
            acknowledgement_region = form.acknowledgement_region.data or None

            if acknowledgement_type == 'none':
                if form.is_indigenous.data == 'yes':
                    acknowledgement_type = 'welcome_to_country'
                else:
                    flash('If you are not Aboriginal or Torres Strait Islander, you must include an Acknowledgement of Country. Please select Generic or Enhanced.', 'warning')
                    return render_template('create-event.html', form=form)

            if acknowledgement_type == 'enhanced' and not acknowledgement_region:
                flash('Please select a region for the Enhanced Acknowledgement of Country.', 'warning')
                return render_template('create-event.html', form=form)

            image_path = None
            if form.image.data:
                try:
                    image_path = _save_event_image(form.image.data)
                except Exception as img_err:
                    current_app.logger.error(f'Image upload error: {img_err}')
                    flash('Image upload failed; event created without image.', 'warning')

            event = Event(
                title=form.title.data,
                category=form.category.data,
                description=form.description.data,
                image=image_path,
                headliner=form.headliner.data,
                support_acts=form.support_acts.data,
                venue=form.venue.data,
                address=form.address.data,
                event_date=form.event_date.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                capacity=form.capacity.data,
                tickets_available=form.capacity.data,
                price=form.price.data,
                acknowledgement_type=acknowledgement_type,
                acknowledgement_region=acknowledgement_region,
                status='Open',
                creator_id=current_user.id,
            )
            db.session.add(event)
            db.session.commit()
            flash('Event published successfully!', 'success')
            return redirect(url_for('main.event_detail', id=event.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Create event error: {e}')
            flash('An error occurred while creating the event.', 'danger')

    return render_template('create-event.html', form=form)


@main_bp.route('/event/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    try:
        event = db.session.scalar(db.select(Event).where(Event.id == id))
    except Exception as e:
        current_app.logger.error(f'Edit event load error: {e}')
        flash('An error occurred while loading the event.', 'danger')
        return redirect(url_for('main.events'))

    if event is None:
        flash('Event not found.', 'danger')
        return redirect(url_for('main.events'))

    if event.creator_id != current_user.id:
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('main.event_detail', id=id))

    form = EventForm(obj=event)

    if form.validate_on_submit():
        try:
            old_image = event.image
            old_capacity = event.capacity
            old_tickets_available = event.tickets_available

            new_image = None
            if form.image.data:
                try:
                    new_image = _save_event_image(form.image.data)
                except Exception as img_err:
                    current_app.logger.error(f'Image upload error: {img_err}')
                    flash('Image upload failed; existing image kept.', 'warning')

            # populate everything except image (we manage it ourselves)
            event.title = form.title.data
            event.category = form.category.data
            event.description = form.description.data
            event.headliner = form.headliner.data
            event.support_acts = form.support_acts.data
            event.venue = form.venue.data
            event.address = form.address.data
            event.event_date = form.event_date.data
            event.start_time = form.start_time.data
            event.end_time = form.end_time.data
            event.price = form.price.data
            event.acknowledgement_type = form.acknowledgement_type.data
            event.acknowledgement_region = form.acknowledgement_region.data or None

            # Capacity changes also adjust remaining tickets by the same delta
            tickets_sold = old_capacity - old_tickets_available
            event.capacity = form.capacity.data
            event.tickets_available = max(0, form.capacity.data - tickets_sold)

            event.image = new_image if new_image else old_image

            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('main.event_detail', id=event.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Edit event error: {e}')
            flash('An error occurred while updating the event.', 'danger')

    return render_template('edit-event.html', form=form, event=event)


@main_bp.route('/event/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_event(id):
    try:
        event = db.session.scalar(db.select(Event).where(Event.id == id))
    except Exception as e:
        current_app.logger.error(f'Cancel event load error: {e}')
        flash('An error occurred while loading the event.', 'danger')
        return redirect(url_for('main.events'))

    if event is None:
        flash('Event not found.', 'danger')
        return redirect(url_for('main.events'))

    if event.creator_id != current_user.id:
        flash('You do not have permission to cancel this event.', 'danger')
        return redirect(url_for('main.event_detail', id=id))

    try:
        event.status = 'Cancelled'
        db.session.commit()
        flash('Event has been cancelled.', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Cancel event error: {e}')
        flash('An error occurred while cancelling the event.', 'danger')

    return redirect(url_for('main.event_detail', id=id))


@main_bp.route('/booking-history')
@login_required
def booking_history():
    try:
        orders = db.session.scalars(
            db.select(Order).where(Order.user_id == current_user.id)
              .order_by(Order.created_at.desc())
        ).all()
    except Exception as e:
        current_app.logger.error(f'Booking history error: {e}')
        flash('Could not load your booking history.', 'danger')
        orders = []
    return render_template('booking-history.html', orders=orders)


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
