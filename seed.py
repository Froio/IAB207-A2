from datetime import datetime, date, time

from website import create_app, db, bcrypt
from website.models import User, Event


SEED_EVENTS = [
    {
        'title': 'The Static Echo \u2014 Live at Black Bear Lodge',
        'category': 'Indie Rock',
        'description': 'The Static Echo return to Black Bear Lodge for a night of raw, reverb-drenched indie rock.',
        'image': 'img/indie_concert.jpg',
        'headliner': 'The Static Echo',
        'support_acts': 'Pale Grey Horses, Foxfield',
        'venue': 'Black Bear Lodge, Fortitude Valley',
        'address': '1/322 Brunswick St, Fortitude Valley QLD 4006',
        'event_date': date(2026, 12, 19),
        'start_time': time(20, 0),
        'end_time': time(23, 30),
        'capacity': 60,
        'tickets_available': 42,
        'price': 18.00,
        'acknowledgement_type': 'enhanced',
        'acknowledgement_region': 'Brisbane CBD',
        'status': 'Open',
    },
    {
        'title': 'River Hollow Acoustic Session',
        'category': 'Folk',
        'description': 'River Hollow bring their stripped back acoustic sound to Black Bear Lodge for an intimate evening.',
        'image': 'img/folk.webp',
        'headliner': 'River Hollow',
        'support_acts': None,
        'venue': 'Black Bear Lodge, Fortitude Valley',
        'address': '1/322 Brunswick St, Fortitude Valley QLD 4006',
        'event_date': date(2026, 12, 25),
        'start_time': time(19, 30),
        'end_time': time(22, 0),
        'capacity': 30,
        'tickets_available': 18,
        'price': 12.00,
        'acknowledgement_type': 'generic',
        'status': 'Open',
    },
    {
        'title': 'Purple Haze \u2014 The Night Room',
        'category': 'Shoegaze',
        'description': 'Purple Haze sell out The Brightside for a night of dreamy, effects-laden shoegaze.',
        'image': 'img/shoegaze.jpg',
        'headliner': 'Purple Haze',
        'support_acts': 'Velvet Drift',
        'venue': 'The Brightside, Fortitude Valley',
        'address': '27 Warner St, Fortitude Valley QLD 4006',
        'event_date': date(2026, 12, 26),
        'start_time': time(21, 0),
        'end_time': time(0, 0),
        'capacity': 80,
        'tickets_available': 0,
        'price': 22.00,
        'acknowledgement_type': 'none',
        'status': 'Sold Out',
    },
    {
        'title': 'Moonbeam Collective',
        'category': 'Dream Pop',
        'description': 'Moonbeam Collective bring their ethereal dream pop sound to The Tivoli.',
        'image': 'img/alt_concert.jpg',
        'headliner': 'Moonbeam Collective',
        'support_acts': None,
        'venue': 'The Tivoli, Fortitude Valley',
        'address': '52 Costin St, Fortitude Valley QLD 4006',
        'event_date': date(2026, 5, 1),
        'start_time': time(20, 30),
        'end_time': time(23, 0),
        'capacity': 100,
        'tickets_available': 60,
        'price': 20.00,
        'acknowledgement_type': 'generic',
        'status': 'Open',
    },
    {
        'title': 'Wire & Static \u2014 Fortitude Valley',
        'category': 'Post-Punk',
        'description': 'Wire & Static bring their post-punk sound to The Zoo.',
        'image': 'img/WirenStatic.jpeg',
        'headliner': 'Wire & Static',
        'support_acts': None,
        'venue': 'The Zoo, Fortitude Valley',
        'address': '711 Ann St, Fortitude Valley QLD 4006',
        'event_date': date(2026, 12, 3),
        'start_time': time(21, 0),
        'end_time': time(0, 0),
        'capacity': 70,
        'tickets_available': 0,
        'price': 15.00,
        'acknowledgement_type': 'none',
        'status': 'Cancelled',
    },
    {
        'title': 'Sunday Tape Session',
        'category': 'Lo-Fi',
        'description': 'A relaxed Sunday afternoon of lo-fi beats and good vibes.',
        'image': 'img/Swingamajig.webp',
        'headliner': 'Various Artists',
        'support_acts': None,
        'venue': "Lefty's Music Hall, Brisbane CBD",
        'address': '15 Caxton St, Brisbane QLD 4000',
        'event_date': date(2026, 12, 4),
        'start_time': time(15, 0),
        'end_time': time(18, 0),
        'capacity': 40,
        'tickets_available': 30,
        'price': 0.00,
        'acknowledgement_type': 'generic',
        'status': 'Open',
    },
    {
        'title': 'Dustbowl Riders',
        'category': 'Alt Country',
        'description': 'Dustbowl Riders bring their alt country sound to The Joynt.',
        'image': 'img/country.avif',
        'headliner': 'Dustbowl Riders',
        'support_acts': None,
        'venue': 'The Joynt, West End',
        'address': '193 Boundary St, West End QLD 4101',
        'event_date': date(2026, 12, 15),
        'start_time': time(20, 0),
        'end_time': time(23, 0),
        'capacity': 50,
        'tickets_available': 0,
        'price': 10.00,
        'acknowledgement_type': 'none',
        'status': 'Inactive',
    },
    {
        'title': 'Glass Houses',
        'category': 'Indie Rock',
        'description': 'Glass Houses close out the week with a late set at The Foundry.',
        'image': 'img/indie_rock.jpg',
        'headliner': 'Glass Houses',
        'support_acts': None,
        'venue': 'The Foundry, Fortitude Valley',
        'address': '17 Doggett St, Fortitude Valley QLD 4006',
        'event_date': date(2026, 12, 9),
        'start_time': time(22, 0),
        'end_time': time(1, 0),
        'capacity': 25,
        'tickets_available': 15,
        'price': 15.00,
        'acknowledgement_type': 'none',
        'status': 'Open',
    },
]


def seed():
    app = create_app()
    with app.app_context():
        # Skip if there are already events in the DB
        existing_count = db.session.scalar(db.select(db.func.count(Event.id)))
        if existing_count and existing_count > 0:
            print(f"Database already contains {existing_count} events \u2014 skipping seed.")
            return

        # Find or create the seed user
        admin_email = 'admin@indiezone.com'
        user = db.session.scalar(db.select(User).where(User.email == admin_email))
        if user is None:
            user = User(
                firstname='Admin',
                surname='User',
                email=admin_email,
                contact_number='0400000000',
                street_address='1 Test St, Brisbane QLD 4000',
                password_hash=bcrypt.generate_password_hash('password').decode('utf-8'),
                created_at=datetime.utcnow(),
            )
            db.session.add(user)
            db.session.commit()
            print(f"Created seed user: {admin_email} / password")
        else:
            print(f"Reusing existing user: {admin_email}")

        # Insert events
        for data in SEED_EVENTS:
            event = Event(creator_id=user.id, **data)
            db.session.add(event)

        db.session.commit()
        print(f"Seeded {len(SEED_EVENTS)} events.")


if __name__ == '__main__':
    seed()
