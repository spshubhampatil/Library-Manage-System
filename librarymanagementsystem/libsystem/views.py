from .models import *
from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):   
    books=Book.objects.all()
    books_count=Book.objects.all().count()
    users_count=SiteUser.objects.filter(is_admin=False).count()
    return render(request, 'index.html',{'books':books,'books_count':books_count,'users_count':users_count})
       


class SignupView(View):
    def get(self, request):
        return render(request,'signup.html')
        
    def post(self, request):
        thank=False
        try:
            first_name=request.POST.get('fname')
            last_name=request.POST.get('lname')
            email=request.POST.get('email')
            usertype=request.POST.get('usertype')
            password=request.POST.get('password')
            repassword=request.POST.get('repassword')   

            print(usertype)         

            if len(password)<6:
                return render(request,'signup.html',{'messaged':"Password must be greatar than 6 digit..."})

            if password != repassword:               
                return render(request,'signup.html',{'messaged':"Password must be same..."})
            
              
            password=make_password(password)
            if usertype=='student':
                siteuser=SiteUser(
                    name=first_name+" "+last_name,
                    profile_name=first_name+" "+last_name,               
                    email=email,
                    password=password
                )
                
            else:
                siteuser=SiteUser(
                    name=first_name+" "+last_name,
                    profile_name=first_name+" "+last_name,               
                    email=email,
                    password=password,
                    is_admin=True
                )
            
            siteuser.save() 
                                 
            thank=True   
            return render(request,'login.html',{'thank':thank})

        except:
            return render(request,'signup.html',{'messaged':"User already existed..."})


class LoginView(View):
    return_url = None

    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email,password)

        try:
            user = SiteUser.objects.get(email=email)
            print(user)

            if user.is_active == True:                
                user = authenticate(request, username=email, password=password)

                print(user)
                if user is not None:
                    login(request, user)
                    return redirect('/')

                else:
                    return render(request,
                                  'login.html',
                                  {'messaged': "Invalide Credentials!!!"})
            else:
                return render(
                    request, 'login.html', {
                        'messaged':
                        "Invalide Credentials!!!!!!"
                    })
        except:
            return render(request, 'login.html',
                          {'messaged': "Invalide Credentials!!!"})


def Signout(request):
    request.session.clear()
    return redirect('library_system:login')

class BooksView(View):
    def get(self, request):   
                
            books=Book.objects.all()                

            return render(request,'books.html',{'books':books})


class AddBookView(View):
    def get(self, request):
        return render(request,'add-book.html')
        
    def post(self, request):
        
        try:
            title=request.POST.get('title')
            author=request.POST.get('author')
            summary=request.POST.get('summary')
            isbn=request.POST.get('isbn')
            total_copies=request.POST.get('total_copies')
            available_copies=request.POST.get('available_copies')                       
            pic=request.FILES.get('pic')                       

            book=Book(
                title=title,
                author=author,
                summary=summary,
                isbn=isbn,
                total_copies=total_copies,
                available_copies=available_copies,
                pic=pic                
            )  
            book.save()            
           
            return redirect('/books')

        except:
            return render(request,'add-book.html',{'messaged':"Something wend wrong..."})


class UpdateBookView(View):
    def get(self, request,book_id):
        book=Book.objects.get(id=book_id)
        return render(request,'update-book.html',{'book':book})
        
    def post(self, request,book_id):
        
        try:
            title=request.POST.get('title')
            author=request.POST.get('author')
            summary=request.POST.get('summary')
            isbn=request.POST.get('isbn')
            total_copies=request.POST.get('total_copies')
            available_copies=request.POST.get('available_copies')                       
            pic=request.FILES.get('pic')   

            book=Book.objects.get(id=book_id) 

            book.title=title
            book.author=author
            book.summary=summary
            book.isbn=isbn
            book.total_copies=total_copies
            book.available_copies=available_copies
            if pic:
                book.pic=pic
             
            book.save()            
           
            return redirect('/books')

        except:
            return render(request,'update-book.html',{'messaged':"Something wend wrong..."})


class DeleteBookView(View):
    def get(self, request,book_id):
        book=Book.objects.get(id=book_id)
        book.delete()
        return redirect('/books')


class ProfileView(View):
    def get(self, request):
        user=SiteUser.objects.get(id=request.user.id)   

        data={'user':user}
        return render(request,'profile.html',data)


class UpdateProfileView(View):
    def get(self, request):
        user=SiteUser.objects.get(id=request.user.id)
        return render(request,'updateprofile.html',{'user':user})
        
    def post(self, request):
        
        try:
            name=request.POST.get('name')            
            email=request.POST.get('email')           

            user=SiteUser.objects.get(id=request.user.id)

            user.name=name
            user.profile_name=name
            
            user.email=email            
                            
            user.save()            
           
            return redirect('/profile')

        except:
            return render(request,'updateprofile.html',{'messaged':"Something wend wrong..."})


class ChangePasswordView(View):
    def get(self, request):
        user=SiteUser.objects.get(id=request.user.id)
        return render(request,'changepassword.html',{'user':user})
        
    def post(self, request):
        
        try:
            opassword=request.POST.get('opassword')
            password=request.POST.get('password')
            repassword=request.POST.get('repassword')    
            
            user=SiteUser.objects.get(id=request.user.id)
            
            chack=check_password(password=opassword, encoded=user.password)
            if chack:                
                if len(password)<6:
                    return render(request,'changepassword.html',{'messaged':"Password must be greatar than 6 digit..."})

                if password != repassword:               
                    return render(request,'changepassword.html',{'messaged':"Password must be same..."})

                password=make_password(password)
                user.password=password
                user.save()                        
           
                return redirect('/')

            return render(request,'changepassword.html',{'messaged':"Please enter correct password..."})
        except:
            return render(request,'changepassword.html',{'messaged':"Something wend wrong..."})

class UsersView(View):
    def get(self, request):   
                
            users=SiteUser.objects.filter(is_admin=False)                

            return render(request,'users.html',{'users':users})


class UpdateUserView(View):
    def get(self, request,user_id):
        user=SiteUser.objects.get(id=user_id)
        return render(request,'update-user.html',{'user':user})
        
    def post(self, request,user_id):
        
        try:
            name=request.POST.get('name')
            
            email=request.POST.get('email')
            
            user=SiteUser.objects.get(id=user_id)                            
            
            user.profile_name=name
            user.name=name            
            user.email=email
            user.save()
           
            return redirect('/users')

        except:
            return render(request,'update-user.html',{'messaged':"Something wend wrong..."})


class DeleteUserView(View):
    def get(self, request,user_id):
        user=SiteUser.objects.get(id=user_id)
        user.delete()
        return redirect('/users')

import csv, io
from django.contrib import messages
def profile_upload(request):

    try:
        # declaring template
        template = "book_upload.html"
        data = Book.objects.all()
        # prompt is a context variable that can have different values      depending on their context
        prompt = {
            'order': 'Order of the CSV should be title, author, summary, isbn, total_copies, available_copies',
            'profiles': data    
                  }
        # GET request returns the value of the data with the specified key.
        if request.method == "GET":
            return render(request, template, prompt)
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Book.objects.update_or_create(
                title=column[0],
                author=column[1],
                summary=column[2],
                isbn=column[3],
                total_copies=column[4],
                available_copies=column[5]
            )
        successm=messages.success(request, 'Data Saved Successfully!!!')    
        context = {'successm':successm}
        return render(request, template, context)
    except:
        return render(request,'book_upload.html',{'messaged':"Something wend wrong..."})