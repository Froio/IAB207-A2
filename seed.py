from website import create_app, db
from website.models import User, Event
from flask_bcrypt import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create a test user
    user = User(
        firstname='Shrey',
        surname='Kulkarni',
        email='shrey@email.com',
        password_hash=generate_password_hash('qwerty123').decode('utf-8'),
        contact_number='0402857051',
        street_address='123 Example St, Brisbane QLD 4000'
    )
    db.session.add(user)
    db.session.commit()

    # Create test events
    events = [
        Event(
            title='The Static Echo — Live at Black Bear Lodge',
            description='The Static Echo return to Black Bear Lodge for a night of raw, reverb-drenched indie rock.',
            artist_name='The Static Echo',
            venue='Black Bear Lodge, Fortitude Valley',
            address='1/322 Brunswick St, Fortitude Valley QLD 4006',
            start_date=datetime(2026, 4, 19, 20, 0),
            end_date=datetime(2026, 4, 19, 23, 30),
            tickets_available=42,
            image='img/indie_concert.jpg',
            status='Open',
            category='Indie Rock',
            acknowledgement_type='enhanced',
            price=18.00,
            user_id=1
        ),
        Event(
            title='River Hollow Acoustic Session',
            description='River Hollow bring their stripped back acoustic sound to Black Bear Lodge for an intimate evening.',
            artist_name='River Hollow',
            venue='Black Bear Lodge, Fortitude Valley',
            address='1/322 Brunswick St, Fortitude Valley QLD 4006',
            start_date=datetime(2026, 4, 25, 19, 30),
            end_date=datetime(2026, 4, 25, 22, 0),
            tickets_available=18,
            image='img/folk.webp',
            status='Open',
            category='Folk',
            acknowledgement_type='generic',
            price=12.00,
            user_id=1
        ),
        Event(
            title='Purple Haze — The Night Room',
            description='Purple Haze sell out The Brightside for a night of dreamy, effects-laden shoegaze.',
            artist_name='Purple Haze',
            venue='The Brightside, Fortitude Valley',
            address='27 Warner St, Fortitude Valley QLD 4006',
            start_date=datetime(2026, 4, 26, 21, 0),
            end_date=datetime(2026, 4, 27, 0, 0),
            tickets_available=0,
            image='img/shoegaze.jpg',
            status='Sold Out',
            category='Shoegaze',
            acknowledgement_type='none',
            price=22.00,
            user_id=1
        ),
        Event(
            title='Moonbeam Collective',
            description='Moonbeam Collective bring their ethereal dream pop sound to The Tivoli.',
            artist_name='Moonbeam Collective',
            venue='The Tivoli, Fortitude Valley',
            address='52 Costin St, Fortitude Valley QLD 4006',
            start_date=datetime(2026, 5, 1, 20, 30),
            end_date=datetime(2026, 5, 1, 23, 0),
            tickets_available=60,
            image='img/alt_concert.jpg',
            status='Open',
            category='Dream Pop',
            acknowledgement_type='generic',
            price=20.00,
            user_id=1
        ),
        Event(
            title='Wire & Static — Fortitude Valley',
            description='Wire & Static bring their post-punk sound to The Zoo.',
            artist_name='Wire & Static',
            venue='The Zoo, Fortitude Valley',
            address='711 Ann St, Fortitude Valley QLD 4006',
            start_date=datetime(2026, 5, 3, 21, 0),
            end_date=datetime(2026, 5, 4, 0, 0),
            tickets_available=0,
            image='img/WirenStatic.jpeg',
            status='Cancelled',
            category='Post-Punk',
            acknowledgement_type='none',
            price=15.00,
            user_id=1
        ),
        Event(
            title='Sunday Tape Session',
            description='A relaxed Sunday afternoon of lo-fi beats and good vibes.',
            artist_name='Various Artists',
            venue="Lefty's Music Hall, Brisbane CBD",
            address='15 Caxton St, Brisbane QLD 4000',
            start_date=datetime(2026, 5, 4, 15, 0),
            end_date=datetime(2026, 5, 4, 18, 0),
            tickets_available=30,
            image='img/Swingamajig.webp',
            status='Open',
            category='Lo-Fi',
            acknowledgement_type='generic',
            price=0.00,
            user_id=1
        ),
        Event(
            title='Dustbowl Riders',
            description='Dustbowl Riders bring their alt country sound to The Joynt.',
            artist_name='Dustbowl Riders',
            venue='The Joynt, West End',
            address='193 Boundary St, West End QLD 4101',
            start_date=datetime(2026, 3, 15, 20, 0),
            end_date=datetime(2026, 3, 15, 23, 0),
            tickets_available=0,
            image='img/country.avif',
            status='Inactive',
            category='Alt Country',
            acknowledgement_type='none',
            price=10.00,
            user_id=1
        ),
        Event(
            title='Glass Houses',
            description='Glass Houses close out the week with a late set at The Foundry.',
            artist_name='Glass Houses',
            venue='The Foundry, Fortitude Valley',
            address='17 Doggett St, Fortitude Valley QLD 4006',
            start_date=datetime(2026, 5, 9, 22, 0),
            end_date=datetime(2026, 5, 10, 1, 0),
            tickets_available=15,
            image='img/indie_rock.jpg',
            status='Open',
            category='Indie Rock',
            acknowledgement_type='none',
            price=15.00,
            user_id=1
        ),
    ]

    db.session.add_all(events)
    db.session.commit()
    print('Database seeded')