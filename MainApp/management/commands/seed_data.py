import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from MainApp.models import Skill, Appointment, Review, Notification


USERS = [
    {'username': 'alice_dev', 'email': 'alice@campus.edu', 'first_name': 'Alice', 'last_name': 'Mensah'},
    {'username': 'brian_arts', 'email': 'brian@campus.edu', 'first_name': 'Brian', 'last_name': 'Osei'},
    {'username': 'chloe_music', 'email': 'chloe@campus.edu', 'first_name': 'Chloe', 'last_name': 'Adu'},
    {'username': 'david_lang', 'email': 'david@campus.edu', 'first_name': 'David', 'last_name': 'Asante'},
    {'username': 'eva_math', 'email': 'eva@campus.edu', 'first_name': 'Eva', 'last_name': 'Boateng'},
]

SKILLS = [
    {
        'owner_username': 'alice_dev',
        'title': 'Python Programming for Beginners',
        'description': 'I will teach you Python from scratch — variables, loops, functions, and small projects. Great for students with zero coding experience.',
        'category': 'tech',
        'price': None,
        'is_free': True,
        'contact_preference': 'whatsapp',
        'availability_status': 'available',
    },
    {
        'owner_username': 'alice_dev',
        'title': 'Web Development with Django',
        'description': 'Learn how to build full-stack web apps using Django. Covers models, views, templates, and deploying to the web.',
        'category': 'tech',
        'price': 30.00,
        'is_free': False,
        'contact_preference': 'email',
        'availability_status': 'available',
    },
    {
        'owner_username': 'brian_arts',
        'title': 'Logo & Brand Identity Design',
        'description': 'I design clean, professional logos and brand kits using Canva and Illustrator. Ideal for student projects, clubs, or small businesses.',
        'category': 'design',
        'price': 20.00,
        'is_free': False,
        'contact_preference': 'instagram',
        'availability_status': 'available',
    },
    {
        'owner_username': 'brian_arts',
        'title': 'Poster & Flyer Design',
        'description': 'Need a flyer for your event? I create eye-catching posters and social media graphics fast.',
        'category': 'design',
        'price': 10.00,
        'is_free': False,
        'contact_preference': 'whatsapp',
        'availability_status': 'busy',
    },
    {
        'owner_username': 'chloe_music',
        'title': 'Guitar Lessons (Beginner)',
        'description': 'Learn basic chords, strumming patterns, and your first songs on acoustic guitar. Sessions are 45 minutes each.',
        'category': 'music',
        'price': 15.00,
        'is_free': False,
        'contact_preference': 'in_person',
        'availability_status': 'available',
    },
    {
        'owner_username': 'chloe_music',
        'title': 'Music Theory Tutoring',
        'description': 'Struggling with music theory for your course? I can help with notes, scales, chords, rhythm, and ear training.',
        'category': 'music',
        'price': None,
        'is_free': True,
        'contact_preference': 'whatsapp',
        'availability_status': 'available',
    },
    {
        'owner_username': 'david_lang',
        'title': 'French Conversation Practice',
        'description': 'Practice spoken French with a near-native speaker. Focus on pronunciation, daily vocabulary, and confidence building.',
        'category': 'language',
        'price': None,
        'is_free': True,
        'contact_preference': 'in_person',
        'availability_status': 'available',
    },
    {
        'owner_username': 'david_lang',
        'title': 'Twi Language Lessons',
        'description': 'Learn Akan Twi — greetings, common phrases, and basic conversation. Perfect for international students on campus.',
        'category': 'language',
        'price': 10.00,
        'is_free': False,
        'contact_preference': 'whatsapp',
        'availability_status': 'available',
    },
    {
        'owner_username': 'eva_math',
        'title': 'Calculus Tutoring',
        'description': 'I tutor Calculus 1 and 2 — limits, derivatives, integrals, and series. I break things down simply with practice problems.',
        'category': 'math',
        'price': 25.00,
        'is_free': False,
        'contact_preference': 'in_person',
        'availability_status': 'available',
    },
    {
        'owner_username': 'eva_math',
        'title': 'Statistics & Data Analysis Help',
        'description': 'Need help with stats assignments or understanding SPSS/Excel analysis? I cover descriptive stats, hypothesis testing, and regression.',
        'category': 'math',
        'price': 20.00,
        'is_free': False,
        'contact_preference': 'email',
        'availability_status': 'available',
    },
    {
        'owner_username': 'alice_dev',
        'title': 'CV & Cover Letter Writing',
        'description': 'I will help you write a clean, professional CV and a tailored cover letter for internships and entry-level jobs.',
        'category': 'writing',
        'price': None,
        'is_free': True,
        'contact_preference': 'email',
        'availability_status': 'available',
    },
    {
        'owner_username': 'brian_arts',
        'title': 'Essay Proofreading & Editing',
        'description': 'I proofread and edit academic essays for grammar, clarity, and structure. Turnaround within 24 hours.',
        'category': 'writing',
        'price': 5.00,
        'is_free': False,
        'contact_preference': 'whatsapp',
        'availability_status': 'available',
    },
    {
        'owner_username': 'david_lang',
        'title': 'Photography for Events',
        'description': 'I shoot campus events, portraits, and group photos. Edited photos delivered within 3 days.',
        'category': 'other',
        'price': 50.00,
        'is_free': False,
        'contact_preference': 'instagram',
        'availability_status': 'available',
    },
    {
        'owner_username': 'chloe_music',
        'title': 'Video Editing (Reels & Shorts)',
        'description': 'I edit short-form videos for Instagram Reels, TikTok, and YouTube Shorts. Fast delivery with captions and transitions.',
        'category': 'other',
        'price': 15.00,
        'is_free': False,
        'contact_preference': 'instagram',
        'availability_status': 'busy',
    },
    {
        'owner_username': 'eva_math',
        'title': 'Excel & Google Sheets Training',
        'description': 'Learn formulas, pivot tables, charts, and data cleaning in Excel or Google Sheets. Useful for projects and internships.',
        'category': 'tech',
        'price': None,
        'is_free': True,
        'contact_preference': 'email',
        'availability_status': 'unavailable',
    },
]

# (requester_username, skill_title, date, time, message, status)
APPOINTMENTS = [
    ('brian_arts', 'Python Programming for Beginners', '2026-05-02', '10:00', 'Hi Alice! I want to start learning Python. Is morning okay?', 'confirmed'),
    ('chloe_music', 'Web Development with Django', '2026-05-05', '14:00', 'I want to build a portfolio site. Can we start next week?', 'pending'),
    ('eva_math', 'Logo & Brand Identity Design', '2026-05-03', '11:00', 'Need a logo for my math tutoring service. Is $20 the final price?', 'confirmed'),
    ('alice_dev', 'Guitar Lessons (Beginner)', '2026-05-07', '09:00', 'Always wanted to learn guitar. Available on Saturday mornings.', 'confirmed'),
    ('david_lang', 'Calculus Tutoring', '2026-05-04', '16:00', 'Struggling with integration by parts. Can we meet Wednesday?', 'confirmed'),
    ('brian_arts', 'French Conversation Practice', '2026-05-06', '13:00', 'Je veux pratiquer mon français! Available Tuesday afternoons.', 'pending'),
    ('chloe_music', 'CV & Cover Letter Writing', '2026-05-08', '15:00', 'Applying for internships and need help with my CV urgently.', 'confirmed'),
    ('eva_math', 'Guitar Lessons (Beginner)', '2026-05-10', '10:00', 'Can we do a trial session first before committing?', 'declined'),
    ('alice_dev', 'Statistics & Data Analysis Help', '2026-05-09', '11:00', 'I have an assignment due Friday. Can we meet before then?', 'cancelled'),
    ('david_lang', 'Poster & Flyer Design', '2026-05-11', '14:00', 'Need a flyer for a campus event happening next weekend.', 'confirmed'),
]

# (reviewer_username, reviewee_username, rating, comment)
REVIEWS = [
    ('brian_arts', 'alice_dev', 5, 'Alice explained Python so clearly! I built my first script after just two sessions. Highly recommend.'),
    ('eva_math', 'brian_arts', 4, 'Brian did a great job on my logo. Clean design, fast delivery. Would use again.'),
    ('alice_dev', 'chloe_music', 5, 'Chloe is an amazing teacher. Patient and fun. I can already play two songs after 3 lessons!'),
    ('david_lang', 'eva_math', 5, 'Eva broke down calculus in a way no lecturer ever did. Passed my exam because of her!'),
    ('chloe_music', 'david_lang', 4, 'David is so passionate about languages. My French accent has improved a lot. Merci!'),
    ('eva_math', 'alice_dev', 5, 'Alice helped me write the best CV I have ever had. Got two interview callbacks the same week!'),
    ('alice_dev', 'eva_math', 4, 'Really helpful stats session. Eva knows her stuff and explains things with real examples.'),
]


class Command(BaseCommand):
    help = 'Seeds the database with sample users, skills, appointments, and reviews'

    def handle(self, *args, **kwargs):
        # --- Users ---
        self.stdout.write('Seeding users...')
        user_map = {}
        for data in USERS:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                user.set_password('pass1234')
                user.save()
                self.stdout.write(f'  Created user: {user.username}')
            else:
                self.stdout.write(f'  Skipped (exists): {user.username}')
            user_map[data['username']] = user

        # --- Skills ---
        self.stdout.write('Seeding skills...')
        skill_map = {}
        for data in SKILLS:
            owner = user_map[data['owner_username']]
            skill, created = Skill.objects.get_or_create(
                owner=owner,
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'category': data['category'],
                    'price': data['price'],
                    'is_free': data['is_free'],
                    'contact_preference': data['contact_preference'],
                    'availability_status': data['availability_status'],
                }
            )
            if created:
                self.stdout.write(f'  Created skill: {skill.title}')
            else:
                self.stdout.write(f'  Skipped (exists): {skill.title}')
            skill_map[data['title']] = skill

        # --- Appointments ---
        self.stdout.write('Seeding appointments...')
        for data in APPOINTMENTS:
            requester = user_map[data[0]]
            skill = skill_map.get(data[1])
            if not skill:
                self.stdout.write(f'  Skipped appointment — skill not found: {data[1]}')
                continue
            if skill.owner == requester:
                continue
            exists = Appointment.objects.filter(requester=requester, skill=skill).exists()
            if not exists:
                appt = Appointment.objects.create(
                    requester=requester,
                    skill=skill,
                    date=datetime.date.fromisoformat(data[2]),
                    time=datetime.time.fromisoformat(data[3]),
                    message=data[4],
                    status=data[5],
                )
                self.stdout.write(f'  Created appointment: {requester.username} → {skill.title} [{appt.status}]')
            else:
                self.stdout.write(f'  Skipped (exists): {requester.username} → {skill.title}')

        # --- Reviews ---
        self.stdout.write('Seeding reviews...')
        for reviewer_name, reviewee_name, rating, comment in REVIEWS:
            reviewer = user_map[reviewer_name]
            reviewee = user_map[reviewee_name]
            exists = Review.objects.filter(reviewer=reviewer, reviewee=reviewee).exists()
            if not exists:
                Review.objects.create(
                    reviewer=reviewer,
                    reviewee=reviewee,
                    rating=rating,
                    comment=comment,
                )
                self.stdout.write(f'  Created review: {reviewer_name} → {reviewee_name} ({rating}★)')
            else:
                self.stdout.write(f'  Skipped (exists): {reviewer_name} → {reviewee_name}')

        self.stdout.write(self.style.SUCCESS('Done! Database seeded successfully.'))
