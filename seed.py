"""Reset the database and fill it with demo data for presentations and marking.

Run from the folder containing main.py:
    venv\\Scripts\\python seed.py

WARNING: this deletes everything currently in instance/beyblade.sqlite.
"""
from datetime import datetime, timedelta
from decimal import Decimal
from werkzeug.security import generate_password_hash

from beyblade import create_app, db
from beyblade.models import User, Tournament, Booking, Comment

# Every demo account shares this password (listed in the README)
DEMO_PASSWORD = 'Blader2026!'

USERS = [
    # key, first name, last name, email, mobile, street address
    ('sam', 'Sam', 'Nguyen', 'sam.nguyen@example.com', '0412 345 678', '12 Albert St, Brisbane City QLD 4000'),
    ('priya', 'Priya', 'Sharma', 'priya.sharma@example.com', '0423 456 789', '48 Boundary St, West End QLD 4101'),
    ('liam', 'Liam', "O'Connor", 'liam.oconnor@example.com', '0434 567 890', '7 Oxford St, Paddington NSW 2021'),
    ('mia', 'Mia', 'Thompson', 'mia.thompson@example.com', '0445 678 901', '210 Lygon St, Carlton VIC 3053'),
    ('jordan', 'Jordan', 'Lee', 'jordan.lee@example.com', '0456 789 012', '33 Beaufort St, Northbridge WA 6003'),
    ('demo', 'Demo', 'Blader', 'demo@example.com', '0400 000 000', '1 George St, Brisbane City QLD 4000'),
]

# capacity = slots still available; seeded bookings below are subtracted from total_slots
TOURNAMENTS = [
    dict(key='brisbane_open', host='sam', title='Brisbane X-Burst Open',
         category='deck3v3', image='event-deck3v3.jpg', status='open',
         start=datetime(2026, 11, 21, 10, 0), hours=6,
         venue='Brisbane Square Library, 266 George St, Brisbane City QLD 4000',
         description=('Our flagship 3v3 Deck tournament. Register three unique Beyblade X combos - '
                      'no part duplicates across your deck. Swiss rounds in the morning, top 16 '
                      'single elimination after lunch. Prize support for the top 8 and a best-'
                      'custom-launcher award. Deck check closes at 9:45am sharp.'),
         match_points=4, gear='Official Takara Tomy & Hasbro Legal', stadium='Xtreme Stadium (BX-10)',
         total_slots=64, price='20.00', ack='enhanced',
         ack_text=('We acknowledge the Turrbal and Yuggera peoples, the Traditional Custodians of the land '
                   'on which this tournament is held, and pay our respects to Elders past and present.')),
    dict(key='westend_swiss', host='priya', title='West End Friday Night Swiss',
         category='swiss1v1', image='event-swiss.jpg', status='open',
         start=datetime(2026, 11, 13, 18, 30), hours=3,
         venue='The Board Room Game Cafe, 48 Boundary St, West End QLD 4101',
         description=('Weekly 1v1 Swiss night. Five rounds, first to 4 points, best combo wins. '
                      'Perfect for practising before the Brisbane Open. Loaner Beys available '
                      'for new bladers - just ask at the counter.'),
         match_points=4, gear='Official Takara Tomy & Hasbro Legal', stadium='Xtreme Stadium (BX-10)',
         total_slots=24, price='8.00', ack='generic', ack_text=None),
    dict(key='sydney_limited', host='liam', title='Sydney Limited Format Clash',
         category='limited', image='spin.jpg', status='open',
         start=datetime(2026, 12, 5, 11, 0), hours=5,
         venue='Paddington Town Hall, 249 Oxford St, Paddington NSW 2021',
         description=('Limited format: only Basic Line (BX) blades, ratchets and bits allowed - '
                      'no Unique Line or Custom Line parts. A great equaliser for newer players. '
                      'Full banned list posted in the comments.'),
         match_points=4, gear='BX parts only', stadium='Xtreme Stadium (BX-10)',
         total_slots=32, price='15.00', ack='enhanced',
         ack_text=('We acknowledge the Gadigal people of the Eora Nation, the Traditional Custodians of the '
                   'land where we gather, and pay our respects to Elders past and present.')),
    dict(key='melbourne_freeplay', host='mia', title='Melbourne Casual Spin Meetup',
         category='freeplay', image='event-freeplay.jpg', status='open',
         start=datetime(2026, 11, 28, 13, 0), hours=4,
         venue='Carlton Library, 667 Rathdowne St, Carlton North VIC 3054',
         description=('Relaxed free-play afternoon - no brackets, no pressure. Bring your collection, '
                      'trade parts, test combos and meet the Melbourne community. Families welcome.'),
         match_points=3, gear='Anything goes', stadium='Xtreme Stadium (BX-10)',
         total_slots=40, price='0.00', ack='generic', ack_text=None),
    dict(key='perth_championship', host='jordan', title='Perth Summer Championship',
         category='deck3v3', image='groups.jpg', status='sold_out',
         start=datetime(2027, 1, 16, 9, 30), hours=8,
         venue='Northbridge Community Hall, 33 Beaufort St, Northbridge WA 6003',
         description=('The biggest Beyblade X event in WA this summer. 3v3 Deck, Swiss into top 32 cut. '
                      'Registration has filled - follow the comments for waitlist updates.'),
         match_points=4, gear='Official Takara Tomy & Hasbro Legal', stadium='Xtreme Stadium (BX-10)',
         total_slots=4, price='25.00', ack='enhanced',
         ack_text=('We acknowledge the Whadjuk people of the Noongar Nation, the Traditional Custodians of '
                   'this land, and pay our respects to Elders past and present.')),
    dict(key='goldcoast_cancelled', host='sam', title='Gold Coast Beach Battle',
         category='swiss1v1', image='event-details-hero.jpg', status='cancelled',
         start=datetime(2026, 12, 12, 10, 0), hours=5,
         venue='Surfers Paradise Community Centre, Surfers Paradise QLD 4217',
         description=('1v1 Swiss by the beach. Cancelled due to a venue booking clash - all '
                      'registrations will be refunded in full.'),
         match_points=4, gear='Official Takara Tomy & Hasbro Legal', stadium='Xtreme Stadium (BX-10)',
         total_slots=32, price='12.00', ack='none', ack_text=None),
    dict(key='brisbane_spring', host='priya', title='Brisbane Spring Qualifier',
         category='swiss1v1', image='event-swiss.jpg', status='inactive',
         start=datetime(2026, 9, 19, 10, 0), hours=6,
         venue='Brisbane Square Library, 266 George St, Brisbane City QLD 4000',
         description=('Spring qualifier for the Brisbane X-Burst Open. Top 4 earned a seeded spot. '
                      'Thanks to everyone who came - results are posted in the comments.'),
         match_points=4, gear='Official Takara Tomy & Hasbro Legal', stadium='Xtreme Stadium (BX-10)',
         total_slots=32, price='10.00', ack='generic', ack_text=None),
    dict(key='canberra_cup', host='liam', title='Canberra Capital Cup',
         category='limited', image='spin.jpg', status='open',
         start=datetime(2027, 2, 6, 10, 0), hours=6,
         venue='Gungahlin Library, 1 Gungahlin Pl, Gungahlin ACT 2912',
         description=('Limited format cup for the Canberra region. Basic Line parts only. '
                      'Lunch break at 12:30 with food trucks on site.'),
         match_points=4, gear='BX parts only', stadium='Xtreme Stadium (BX-10)',
         total_slots=32, price='15.00', ack='enhanced',
         ack_text=('We acknowledge the Ngunnawal people, the Traditional Custodians of the land on which this '
                   'event takes place, and pay our respects to Elders past and present.')),
]

BOOKINGS = [
    # order ref, user, tournament, quantity, status, booked on
    ('XB-10421', 'demo', 'brisbane_open', 1, 'confirmed', datetime(2026, 10, 2, 19, 12)),
    ('XB-10587', 'demo', 'westend_swiss', 2, 'confirmed', datetime(2026, 10, 9, 12, 40)),
    ('XB-09833', 'demo', 'brisbane_spring', 1, 'attended', datetime(2026, 9, 1, 8, 5)),
    ('XB-11204', 'demo', 'goldcoast_cancelled', 1, 'cancelled', datetime(2026, 10, 11, 16, 30)),
    ('XB-10699', 'priya', 'brisbane_open', 1, 'confirmed', datetime(2026, 10, 3, 9, 20)),
    ('XB-10702', 'liam', 'brisbane_open', 3, 'confirmed', datetime(2026, 10, 4, 21, 2)),
    ('XB-10815', 'mia', 'sydney_limited', 1, 'confirmed', datetime(2026, 10, 12, 10, 45)),
    ('XB-10930', 'jordan', 'melbourne_freeplay', 2, 'confirmed', datetime(2026, 10, 14, 18, 0)),
    ('XB-11050', 'sam', 'perth_championship', 2, 'confirmed', datetime(2026, 10, 15, 7, 55)),
    ('XB-11051', 'mia', 'perth_championship', 2, 'confirmed', datetime(2026, 10, 15, 8, 10)),
    ('XB-09810', 'sam', 'brisbane_spring', 1, 'attended', datetime(2026, 8, 28, 13, 30)),
]

COMMENTS = [
    # tournament, user, body, posted on
    ('brisbane_open', 'priya', 'Are Hasbro and Takara Tomy versions of the same blade both allowed in one deck?',
     datetime(2026, 10, 5, 14, 2)),
    ('brisbane_open', 'sam', 'Yes - both are legal, but they still count as the same blade for deck rules.',
     datetime(2026, 10, 5, 15, 30)),
    ('brisbane_open', 'liam', 'Driving up from Sydney for this one. Is there parking nearby?',
     datetime(2026, 10, 8, 9, 15)),
    ('brisbane_open', 'sam', 'King George Square car park is a 2 minute walk. Early bird rates before 9:30am.',
     datetime(2026, 10, 8, 11, 0)),
    ('westend_swiss', 'demo', 'First time coming along - is it beginner friendly?',
     datetime(2026, 10, 10, 17, 45)),
    ('westend_swiss', 'priya', 'Absolutely! We pair new bladers together for the first round and have loaner Beys.',
     datetime(2026, 10, 10, 19, 5)),
    ('sydney_limited', 'mia', 'Is the Basic Line ratchet 3-60 allowed?',
     datetime(2026, 10, 13, 8, 30)),
    ('sydney_limited', 'liam', 'Yes, any BX ratchet is fine. Only UX and CX parts are banned for this event.',
     datetime(2026, 10, 13, 12, 10)),
    ('perth_championship', 'jordan', 'We are full! Comment here if you want a waitlist spot.',
     datetime(2026, 10, 16, 10, 0)),
    ('perth_championship', 'demo', 'Waitlist please - happy to drive from Fremantle.',
     datetime(2026, 10, 16, 13, 20)),
    ('goldcoast_cancelled', 'sam', 'Sorry everyone - venue double-booked us. Refunds are being processed.',
     datetime(2026, 10, 18, 9, 0)),
    ('brisbane_spring', 'priya', 'Congrats to our top 4! Seeded spots for the Brisbane Open have been emailed.',
     datetime(2026, 9, 20, 10, 0)),
    ('melbourne_freeplay', 'jordan', 'Bringing my whole collection for trades - looking for a spare Wizard Rod.',
     datetime(2026, 10, 17, 20, 40)),
]


def seed():
    app = create_app()
    with app.app_context():
        # Start from empty tables so the script can be run again safely
        db.drop_all()
        db.create_all()

        password_hash = generate_password_hash(DEMO_PASSWORD)
        users = {}
        for key, first, last, email, mobile, address in USERS:
            users[key] = User(first_name=first, last_name=last, email=email, mobile=mobile,
                              street_address=address, password_hash=password_hash,
                              created_at=datetime(2026, 8, 15, 12, 0))
        db.session.add_all(users.values())

        # Slots already taken by the seeded bookings (cancelled bookings free their slots)
        taken = {}
        for _, _, t_key, qty, status, _ in BOOKINGS:
            if status != 'cancelled':
                taken[t_key] = taken.get(t_key, 0) + qty

        tournaments = {}
        for t in TOURNAMENTS:
            tournaments[t['key']] = Tournament(
                title=t['title'], category=t['category'], image=t['image'], status=t['status'],
                start_time=t['start'], end_time=t['start'] + timedelta(hours=t['hours']),
                venue=t['venue'], description=t['description'],
                match_points=t['match_points'], gear_legality=t['gear'], stadium_type=t['stadium'],
                capacity=t['total_slots'] - taken.get(t['key'], 0), price=Decimal(t['price']),
                ack_statement=t['ack'], custom_ack_text=t['ack_text'],
                host=users[t['host']], created_at=datetime(2026, 9, 25, 9, 0))
        db.session.add_all(tournaments.values())

        for ref, u_key, t_key, qty, status, booked_on in BOOKINGS:
            tournament = tournaments[t_key]
            db.session.add(Booking(order_ref=ref, user=users[u_key], tournament=tournament,
                                   quantity=qty, total_paid=tournament.price * qty,
                                   status=status, created_at=booked_on))

        for t_key, u_key, body, posted_on in COMMENTS:
            tournament = tournaments[t_key]
            db.session.add(Comment(tournament=tournament, user=users[u_key], body=body,
                                   is_host_reply=(tournament.host is users[u_key]),
                                   created_at=posted_on))

        db.session.commit()
        print(f'Seeded {len(USERS)} users, {len(TOURNAMENTS)} tournaments, '
              f'{len(BOOKINGS)} bookings and {len(COMMENTS)} comments.')
        print(f'Log in with any demo account, e.g. demo@example.com / {DEMO_PASSWORD}')


if __name__ == '__main__':
    seed()
