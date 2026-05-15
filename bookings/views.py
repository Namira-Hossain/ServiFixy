from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, Rating, Discount
from accounts.models import UserProfile, WorkerProfile
from services.models import Service

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    customer_profile = UserProfile.objects.get(user=request.user)

    # check if first booking for discount
    is_first = not Booking.objects.filter(customer=customer_profile).exists()
    total_price = service.price
    final_price = round(total_price * 0.9, 2) if is_first else total_price

    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        booking = Booking.objects.create(
            customer=customer_profile,
            worker=service.worker,
            service=service,
            date=date,
            time=time,
            total_price=total_price,
            final_price=final_price,
        )
        # create discount record if first booking
        if is_first:
            Discount.objects.create(
                customer=customer_profile,
                is_first_booking=True,
                discount_percent=10,
            )
        return redirect('booking_history')

    return render(request, 'bookings/book_service.html', {
        'service': service,
        'total_price': total_price,
        'final_price': final_price,
        'is_first': is_first,
    })

@login_required
def booking_history(request):
    customer_profile = UserProfile.objects.get(user=request.user)
    bookings = Booking.objects.filter(customer=customer_profile).order_by('-id')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})

@login_required
def booking_requests(request):
    worker_profile = WorkerProfile.objects.get(user=request.user)
    bookings = Booking.objects.filter(worker=worker_profile).order_by('-id')
    return render(request, 'bookings/booking_requests.html', {'bookings': bookings})

@login_required
def leave_rating(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    reviewer_profile = UserProfile.objects.get(user=request.user)

    # check if already rated
    already_rated = Rating.objects.filter(
        booking=booking,
        reviewer=reviewer_profile
    ).exists()

    if already_rated:
        return redirect('booking_history')

    if request.method == 'POST':
        score = request.POST['score']
        comment = request.POST['comment']

        # two-way: identify who is the receiver
        if reviewer_profile == booking.customer:
            receiver_profile = booking.worker.user.userprofile
        else:
            receiver_profile = booking.customer

        Rating.objects.create(
            booking=booking,
            reviewer=reviewer_profile,
            receiver=receiver_profile,
            score=score,
            comment=comment,
        )
        return redirect('booking_history')

    return render(request, 'bookings/rating.html', {'booking': booking})