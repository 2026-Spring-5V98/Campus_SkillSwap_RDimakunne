from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from MainApp.models import Skill


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


class Command(BaseCommand):
    help = 'Seeds the database with sample users and skill listings'

    def handle(self, *args, **kwargs):
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

        self.stdout.write('Seeding skills...')
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

        self.stdout.write(self.style.SUCCESS('Done! Database seeded successfully.'))
