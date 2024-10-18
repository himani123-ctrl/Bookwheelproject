import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Author, Story, Enquiry, Payment,Category
from .forms import StoryForm

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def author_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        author = Author.objects.create(user=user)
        messages.success(request, 'Registration successful! Proceed to payment.')
        return redirect('payment_view')  # Redirect to payment
    return render(request, 'author_registration.html')

def author_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('author_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'author_login.html')
def author_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('author_login')

    author = Author.objects.get(user=request.user)
    stories = Story.objects.filter(author=author)
    categories = Category.objects.all()  # Fetch all categories

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image')
        category_id = request.POST.get('category')

        if category_id:
            category = Category.objects.get(id=category_id)
            Story.objects.create(
                title=title,
                author=author,
                description=description,
                image=image,
                category=category
            )
            messages.success(request, 'Story added successfully!')
            return redirect('author_dashboard')
        else:
            messages.error(request, 'Please select a category.')

    return render(request, 'author_dashboard.html', {
        'stories': stories,
        'categories': categories  # Pass categories to the template
    })


def enquiry_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Enquiry.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Enquiry submitted!')
        return redirect('author_login')
    return render(request, 'enquiry_form.html')

def payment_view(request):
    if request.method == 'POST':
        amount = 5000  # Amount in cents ($50.00)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Payment for registration',
                source=request.POST['stripeToken']
            )
            # Save payment information
            author = Author.objects.get(user=request.user)
            Payment.objects.create(author=author, amount=50.00)
            messages.success(request, 'Payment successful!')
            return redirect('author_dashboard')
        except stripe.error.StripeError as e:
            messages.error(request, str(e))

    return render(request, 'payment.html', {
        'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY
    })

def story_list(request):
    stories = Story.objects.all()
    return render(request, 'story_list.html', {'stories': stories})


def rate_story(request, story_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        story = Story.objects.get(id=story_id)

        # Update rating logic
        total_rating = story.rating * story.rating_count
        total_rating += float(rating)
        story.rating_count += 1
        story.rating = total_rating / story.rating_count
        story.save()
        
        messages.success(request, 'Thank you for rating the story!')
        return redirect('story_detail', story_id=story.id) 
    
def story_detail(request, story_id):
    story = Story.objects.get(id=story_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        total_rating = story.rating * story.rating_count
        total_rating += float(rating)
        story.rating_count += 1
        story.rating = total_rating / story.rating_count
        story.save()
        messages.success(request, 'Thank you for rating the story!')
        return redirect('story_detail', story_id=story.id)

    return render(request, 'story_detail.html', {'story': story})
