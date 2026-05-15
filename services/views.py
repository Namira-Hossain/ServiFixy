from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service, Category
from .forms import ServiceForm
from accounts.models import WorkerProfile

def service_list(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    # recommendation — top 3 workers by rating then completed jobs
    recommended = WorkerProfile.objects.order_by(
        '-rating', '-completed_jobs'
    )[:3]
    return render(request, 'services/service_list.html', {
        'services': services,
        'categories': categories,
        'recommended': recommended,
    })

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/service_detail.html', {
        'service': service
    })

def search_view(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    female_only = request.GET.get('female_only', '')
    sort = request.GET.get('sort', '')

    if query:
        services = services.filter(title__icontains=query)
    if category:
        services = services.filter(category__name=category)
    if female_only:
        services = services.filter(
            worker__user__userprofile__is_female=True
        )
    # price comparison
    if sort == 'price_low':
        services = services.order_by('price')
    elif sort == 'price_high':
        services = services.order_by('-price')
    elif sort == 'rating':
        services = services.order_by('-worker__rating')

    return render(request, 'services/search.html', {
        'services': services,
        'categories': categories,
        'query': query,
    })

@login_required
def create_service(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.worker = WorkerProfile.objects.get(user=request.user)
            service.save()
            return redirect('service_list')
    return render(request, 'services/create_service.html', {'form': form})

@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(instance=service)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_detail', pk=pk)
    return render(request, 'services/edit_service.html', {
        'form': form,
        'service': service,
    })

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'services/delete_service.html', {
        'service': service
    })