from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from notes.forms import * 
from django.views.generic.list import ListView
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'notes/login.html')

def register(request):
    if request.method == 'POST':
        a=request.POST.get('name')
        b=request.POST.get('username')
        c=request.POST.get('email')
        d=request.POST.get('password')
        e=request.POST.get('confirmpassword')
        if d==e:
            if Customer.objects.filter(username=b).exists():
                messages.info(request,"username already exists")
                return redirect("notes/register.html")
            elif Customer.objects.filter(email=c).exists():
                messages.info(request,"email already exists")
                return redirect("notes/register.html")
            else:
                user = Customer.objects.create(name=a,username=b,email=c,password=d)
                user.save()
                return redirect("http://127.0.0.1:8000/login")
        else:
            messages.info(request,"passwords do not match")
            return render(request,"notes/register.html")
    else:
        return render(request,"notes/register.html")


def login(request):
    if request.method == 'POST':
        u=request.POST.get('username')
        p=request.POST.get('password')
        log1 = Customer.objects.filter(username=u,password=p)
        if log1.filter(username=u, password=p).exists():
            for i in log1:
                x = i.username
                y = i.status
                request.session['username'] = u
                request.session['password'] = p
                if y == 'A':
                    return render(request, "notes/admin1.html")
                else:   
                    messages.success(request, f'Welcome "{u}" !')
                    return render(request, "notes/user.html")
        else:
            return render(request, "notes/login.html")
    else:
        return render(request, "notes/login.html")
        
def user(request):
    return render(request,"notes/user.html") 
        
    
#crud of file
@login_required
def upload(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            c=request.session["username"]
            cus=Customer.objects.get(username=c) 
            post.username = cus
            post.save()
            messages.success(request, f'Your document "{form.cleaned_data["title"]}" was uploaded successfully!')
            return redirect("uploaddash")
    else:
        form = PostForm()
    return render(request, 'notes/upload.html', {'form': form})

@login_required
def pdfedit(request, pk):
    c=request.session.get("username")
    cus = get_object_or_404(Customer, username=c)
    pdf = get_object_or_404(Post, pk=pk)
    if cus != pdf.username:  # check if the user owns the document
        messages.error(request, "You don't have permission to edit this document.")
        return redirect('uploaddash')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=pdf)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your document "{form.cleaned_data["title"]}" was updated successfully!')
            return redirect('uploaddash')
    else:
        form = PostForm(instance=pdf)
    return render(request, 'notes/pdfedit.html', {'form': form, 'pdf': pdf})

@login_required
def delete(request, pk):
    c=request.session.get("username")
    cus = get_object_or_404(Customer, username=c)
    pdf = get_object_or_404(Post, pk=pk)
    if cus == pdf.username:  # check if the user owns the document
        pdf.delete()
        messages.success(request, "PDF file deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this document.")
    return redirect('uploaddash')

def uploaddash(request):
    c=request.session["username"]
    cus=Customer.objects.get(username=c)
    details = Post.objects.filter(username=cus)
    return render(request,'notes/uploaddash.html', {'details': details})
def logouts(request):
    logout(request)
    return redirect('login')

def editprofile(request):
    # Get the current user object
    username = request.session.get('username')
    user = Customer.objects.get(username=username)

    if request.method == 'POST':
        # Update the user object with new data from the form
        user.name = request.POST.get('name', user.name)
        user.email = request.POST.get('email', user.email)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user.password = password
            user.confirmpassword = confirm_password
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('profilee')
        user.save()
        messages.success(request, "Profile updated successfully.")
        return render(request,"notes/user.html")
    else:
        # Render the edit profile form with the current user data
        context = {'user': user}
        return render(request, 'notes/profileedit.html', context)        
def profilee(request):
    return render(request,'notes/profileedit.html')

#notifications views
def notifications(request):
    notifications = Notification.objects.all().order_by('-timestamp')
    return render(request, 'notes/notification.html', {'notifications': notifications})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'notes/post_detail.html', {'post': post})   

#search
def search(request):
    query = request.GET.get('query')
    results = []
    if query:
        results = Post.objects.filter(title__icontains=query)
    return render(request, 'notes/search.html', {'results': results})
#favorites
@login_required
def add_to_favorites(request, post_id):
    c=request.session.get("username")
    cus = get_object_or_404(Customer, username=c)
    post = get_object_or_404(Post, id=post_id)
    favorite, created = Favorite.objects.get_or_create(username=cus, post=post)
    if created:
        messages.success(request, 'Post added to favorites.')
        return render(request,'notes/popup.html')
    else:
        messages.warning(request, 'Post is already in favorites.')
        return render(request,'notes/popup1.html')
    print("errorr3")    
    return redirect(request.META.get('HTTP_REFERER'))
    
@login_required
def favorites(request):
    c=request.session["username"]
    cus=Customer.objects.get(username=c)
    favorites = Favorite.objects.filter(username=cus)
    return render(request, 'notes/favorites.html', {'favorites': favorites})

#courses crud
def upload_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            return render(request,'courses/courselist.html')
    else:
        form = CourseForm()
    return render(request, 'courses/courseupload.html', {'form': form})

def edit_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('courses/coursedetail', slug=course.slug)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/editcourse.html', {'form': form})

def delete_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        course.delete()
        return redirect('home')
    return render(request, 'delete_course.html', {'course': course})

def course_list(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses/courselist.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {'course': course}
    return render(request, 'courses/coursedetail.html', context)

def coursedash(request):
    return render(request,'courses/coursedashboard.html')

#videos crud
def upload_video(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()
            return redirect('courses/coursedetail.html', slug=course.slug)
    else:
        form = VideoForm()
    return render(request, 'videos/uploadvideo.html', {'form': form, 'course': course})

def edit_video(request, slug, serial_number):
    course = get_object_or_404(Course, slug=slug)
    video = get_object_or_404(Video, course=course, serial_number=serial_number)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('courses/coursedetail.html', slug=course.slug)
    else:
        form = VideoForm(instance=video)
    return render(request, 'videos/editvideo.html', {'form': form, 'course': course, 'video': video})

def delete_video(request, slug, serial_number):
    course = get_object_or_404(Course, slug=slug)
    video = get_object_or_404(Video, course=course, serial_number=serial_number)
    if request.method == 'POST':
        video.delete()
        return redirect('courses/coursedetail.html', slug=course.slug)
    return render(request, 'videos/deletevideo.html', {'course': course, 'video': video})

#tags,learnings
def add_tag(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.course = course
            tag.save()
            return redirect('courses/coursedetail.html', slug=course.slug)
    else:
        form = TagForm()
    return render(request, 'courses/addtag.html', {'form': form, 'course': course})

def add_prerequisite(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = PrerequisiteForm(request.POST)
        if form.is_valid():
            prerequisite = form.save(commit=False)
            prerequisite.course = course
            prerequisite.save()
            return redirect('courses/coursedetail.html', slug=course.slug)
    else:
        form = PrerequisiteForm()
    return render(request, 'courses/addprerequisite.html', {'form': form, 'course': course})

def add_learning(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = LearningForm(request.POST)
        if form.is_valid():
            learning = form.save(commit=False)
            learning.course = course
            learning.save()
            return redirect('courses/coursedetail.html', slug=course.slug)
    else:
        form = LearningForm()
    return render(request, 'courses/addlearning.html', {'form': form, 'course': course})

def delete_tag(request, slug, tag_id):
    course = get_object_or_404(Course, slug=slug)
    tag = get_object_or_404(Tag, id=tag_id, course=course)
    if request.method == 'POST':
        tag.delete()
        return redirect('courses/coursedetail.html', slug=course.slug)
    return render(request, 'courses/deletetag.html', {'course': course, 'tag': tag})

def delete_prerequisite(request, slug, prereq_id):
    course = get_object_or_404(Course, slug=slug)
    prerequisite = get_object_or_404(Prerequisite, id=prereq_id, course=course)
    if request.method == 'POST':
        prerequisite.delete()
        return redirect('courses/coursedetail.html', slug=course.slug)
    return render(request, 'courses/deleteprerequisite.html', {'course': course, 'prerequisite': prerequisite})

def delete_learning(request, slug, learning_id):
    course = get_object_or_404(Course, slug=slug)
    learning = get_object_or_404(Learning, id=learning_id, course=course)
    if request.method == 'POST':
        learning.delete()
        return redirect('courses/coursedetail', slug=course.slug)
    return render(request, 'courses/deletelearning.html', {'course': course, 'learning': learning})

def learning_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    learning_objects = Learning.objects.filter(course=course)
    return render(request, 'courses/learningdisplay.html', {'course': course, 'learning_objects': learning_objects})

def tags_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    tags = Tag.objects.filter(course=course)
    return render(request, 'courses/tagsdisplay.html', {'course': course, 'tags': tags})

def videos_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = Video.objects.filter(course=course)
    return render(request, 'videos/videosdisplay.html', {'course': course, 'videos': videos})

def prerequisites_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    prerequisites = Prerequisite.objects.filter(course=course)
    return render(request, 'courses/prerequisitesdisplay.html', {'course': course, 'prerequisites': prerequisites})
