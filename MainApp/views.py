from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Skill, Review, Appointment, Notification
from .forms import RegisterForm, SkillForm, ReviewForm, AppointmentForm


# --- Temporary password reset (remove after use) ---

def reset_password(request, username):
    from django.contrib.auth.models import User
    from django.http import HttpResponse
    try:
        u = User.objects.get(username=username)
        u.set_password('newpass123')
        u.is_staff = True
        u.is_superuser = True
        u.save()
        return HttpResponse(f'Password for {username} reset to: newpass123')
    except User.DoesNotExist:
        return HttpResponse('User not found')


# --- Landing Page ---

def landing(request):
    if request.user.is_authenticated:
        return redirect('skill-list')
    category_counts = {}
    for value, label in Skill.CATEGORY_CHOICES:
        category_counts[value] = {
            'label': label,
            'count': Skill.objects.filter(category=value).count(),
        }
    return render(request, 'mainapp/landing.html', {'category_counts': category_counts})


# --- Auth Views ---

def register(request):
    """Handles new user sign-up. Logs the user in immediately after registering."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Skip the login page — log them straight in
            messages.success(request, f'Welcome to Campus SkillSwap, {user.username}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'mainapp/register.html', {'form': form})


# --- Skill Views ---

class SkillListView(LoginRequiredMixin, ListView):
    """Shows all skill posts. Supports optional category filtering via ?category=tech in the URL."""
    model = Skill
    template_name = 'mainapp/skill_list.html'
    context_object_name = 'skills'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass choices to the template so the filter dropdown can build itself
        context['categories'] = Skill.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class SkillDetailView(LoginRequiredMixin, DetailView):
    """Shows a single skill post in full detail."""
    model = Skill
    template_name = 'mainapp/skill_detail.html'
    context_object_name = 'skill'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill = self.get_object()
        if self.request.user != skill.owner:
            context['appointment_form'] = AppointmentForm()
        return context


class SkillCreateView(LoginRequiredMixin, CreateView):
    """
    LoginRequiredMixin redirects unauthenticated users to the login page automatically.
    ⚠️ Without this mixin, anyone could POST to this URL and create skill posts.
    """
    model = Skill
    form_class = SkillForm
    template_name = 'mainapp/skill_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # Attach the logged-in user as the owner before saving
        form.instance.owner = self.request.user
        messages.success(self.request, 'Your skill post has been created!')
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    UserPassesTestMixin runs test_func() before allowing access.
    If it returns False, the user gets a 403 Forbidden response.
    """
    model = Skill
    form_class = SkillForm
    template_name = 'mainapp/skill_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        # Only the owner of this skill post can edit it
        return self.get_object().owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Skill post updated successfully!')
        return super().form_valid(form)


class SkillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Shows a confirmation page, then deletes the skill on POST."""
    model = Skill
    template_name = 'mainapp/skill_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.get_object().owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Skill post deleted.')
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, ListView):
    """Shows only the currently logged-in user's own skill posts."""
    model = Skill
    template_name = 'mainapp/dashboard.html'
    context_object_name = 'skills'

    def get_queryset(self):
        return Skill.objects.filter(owner=self.request.user)


# --- Profile & Reviews ---

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    skills = Skill.objects.filter(owner=profile_user)
    reviews = Review.objects.filter(reviewee=profile_user).select_related('reviewer')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    already_reviewed = Review.objects.filter(reviewer=request.user, reviewee=profile_user).exists()
    is_own_profile = request.user == profile_user

    if request.method == 'POST' and not is_own_profile and not already_reviewed:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewee = profile_user
            review.save()
            messages.success(request, f'Your review for {profile_user.username} has been posted!')
            return redirect('user-profile', username=username)
    else:
        form = ReviewForm()

    return render(request, 'mainapp/user_profile.html', {
        'profile_user': profile_user,
        'skills': skills,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
        'already_reviewed': already_reviewed,
        'is_own_profile': is_own_profile,
    })


# --- Appointments ---

@login_required
def book_appointment(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if skill.owner == request.user:
        messages.error(request, "You can't book your own skill.")
        return redirect('skill-detail', pk=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.requester = request.user
            appointment.skill = skill
            appointment.save()
            messages.success(request, f'Appointment request sent to {skill.owner.username}!')
            return redirect('appointments')
    else:
        form = AppointmentForm()

    return render(request, 'mainapp/book_appointment.html', {'skill': skill, 'form': form})


@login_required
def appointments(request):
    received = Appointment.objects.filter(skill__owner=request.user).select_related('requester', 'skill')
    sent = Appointment.objects.filter(requester=request.user).select_related('skill__owner', 'skill')
    return render(request, 'mainapp/appointments.html', {'received': received, 'sent': sent})


@login_required
def appointment_action(request, pk, action):
    if request.method != 'POST':
        return redirect('appointments')

    appointment = get_object_or_404(Appointment, pk=pk)
    is_owner = appointment.skill.owner == request.user
    is_requester = appointment.requester == request.user
    skill_title = appointment.skill.title
    owner_name = appointment.skill.owner.username

    if action == 'confirm' and is_owner and appointment.status == 'pending':
        appointment.status = 'confirmed'
        messages.success(request, 'Appointment confirmed.')
        Notification.objects.create(
            recipient=appointment.requester,
            message=f'Your appointment for "{skill_title}" with {owner_name} on {appointment.date} at {appointment.time.strftime("%I:%M %p")} has been confirmed.'
        )
    elif action == 'decline' and is_owner and appointment.status == 'pending':
        appointment.status = 'declined'
        messages.success(request, 'Appointment declined.')
        Notification.objects.create(
            recipient=appointment.requester,
            message=f'Your appointment request for "{skill_title}" with {owner_name} on {appointment.date} was rejected.'
        )
    elif action == 'cancel' and is_owner and appointment.status in ('pending', 'confirmed'):
        appointment.status = 'cancelled'
        messages.success(request, 'Appointment cancelled.')
        Notification.objects.create(
            recipient=appointment.requester,
            message=f'Your appointment for "{skill_title}" with {owner_name} on {appointment.date} has been cancelled by the skill owner.'
        )
    elif action == 'cancel' and is_requester and appointment.status in ('pending', 'confirmed'):
        appointment.status = 'cancelled'
        messages.success(request, 'Appointment cancelled.')
        Notification.objects.create(
            recipient=appointment.skill.owner,
            message=f'{appointment.requester.username} cancelled their appointment for "{skill_title}" on {appointment.date}.'
        )
    else:
        messages.error(request, 'Action not allowed.')
        return redirect('appointments')

    appointment.save()
    return redirect('appointments')


@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(recipient=request.user)
    user_notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'mainapp/notifications.html', {'notifications': user_notifications})
