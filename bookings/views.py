from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, Rating, Discount
from .forms import BookingForm, RatingForm
from accounts.models import UserProfile, WorkerProfile
from services.models import Service

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    customer_profile = UserProfile.objects.get(user=request.user)

    # first booking discount check
    is_first = not Booking.objects.filter(
        customer=customer_profile
    ).exists()
    total_price = service.price
    final_price = round(float(total_price) * 0.9, 2) if is_first else total_price

    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = customer_profile
            booking.worker = service.worker
            booking.service = service
            booking.total_price = total_price
            booking.final_price = final_price
            booking.save()

            if is_first:
                Discount.objects.create(
                    customer=customer_profile,
                    is_first_booking=True,
                    discount_percent=10,
                )
            return redirect('booking_history')

    return render(request, 'bookings/book_service.html', {
        'form': form,
        'service': service,
        'total_price': total_price,
        'final_price': final_price,
        'is_first': is_first,
    })

@login_required
def booking_history(request):
    customer_profile = UserProfile.objects.get(user=request.user)
    bookings = Booking.objects.filter(
        customer=customer_profile
    ).order_by('-id')
    return render(request, 'bookings/booking_history.html', {
        'bookings': bookings
    })

@login_required
def booking_requests(request):
    worker_profile = WorkerProfile.objects.get(user=request.user)
    bookings = Booking.objects.filter(
        worker=worker_profile
    ).order_by('-id')
    return render(request, 'bookings/booking_requests.html', {
        'bookings': bookings
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        return redirect('booking_history')
    return render(request, 'bookings/cancel_booking.html', {
        'booking': booking
    })

@login_required
def leave_rating(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    reviewer_profile = UserProfile.objects.get(user=request.user)

    # prevent double rating
    already_rated = Rating.objects.filter(
        booking=booking,
        reviewer=reviewer_profile
    ).exists()
    if already_rated:
        return redirect('booking_history')

    form = RatingForm()
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.booking = booking
            rating.reviewer = reviewer_profile

            # two way rating
            if reviewer_profile == booking.customer:
                rating.receiver = booking.worker.user.userprofile
            else:
                rating.receiver = booking.customer

            rating.save()

            # auto update worker average rating
            worker = booking.worker
            all_ratings = Rating.objects.filter(
                receiver=booking.worker.user.userprofile
            )
            if all_ratings.exists():
                avg = sum([r.score for r in all_ratings]) / all_ratings.count()
                worker.rating = round(avg, 1)
                worker.save()

            return redirect('booking_history')

    return render(request, 'bookings/rating.html', {
        'form': form,
        'booking': booking,
    })