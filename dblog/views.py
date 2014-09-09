from django.shortcuts import render_to_response, get_object_or_404
from simpleblog.dblog.models import Blog, Mood
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext 
from django.contrib import auth
import datetime

def index(request):
      """Generate the context for the main summary page"""
      now = datetime.datetime.now()
      latest_blog_list = Blog.objects.all().order_by('-post_date')[:2]
      latest_mood_list = Mood.objects.all().order_by('-post_date')[:1]
      return render_to_response('index.html', {'latest_blog_list': latest_blog_list, 
                                               'latest_mood_list': latest_mood_list, 
                                               'current_time': now})

def about(request):
      return render_to_response('about.html', {})

def bloglist(request):
      blog_list = Blog.objects.all().order_by('-post_date')
      return render_to_response('bloglist.html', {'blog_list': blog_list})

def moodlist(request):
      mood_list = Mood.objects.all().order_by('-post_date')
      return render_to_response('moodlist.html', {'mood_list': mood_list})

#%Blogs, comments 
def readBlog(request, blog_id):
      """Generate the context for the page that displayss a 
        single blog entry"""
      blog = get_object_or_404(Blog, pk=blog_id)
      return render_to_response('readBlog.html', {'blog': blog})

def comment(request, blog_id):
      """Generate the context for the page that displays the 
      comments for a particular blog entry"""
      blog = get_object_or_404(Blog, pk=blog_id)
      return render_to_response('comment.html', 
                              {'comments': blog.comment_set.all(), 'blog': blog})

def writeBlog(request):
      """No context for thispage. Just render the template"""
      return render_to_response('blogEntry.html')

def postEntry(request):
      """Accepts the HTTP POST data of a new blog entry and updates the database """
      if not(request.user.has_perm("dblog.may_create_blogs")):
          return render_to_response("blogPD.html")
      b = Blog()
      b.title = request.POST['title']
      b.reply_to = request.POST['reply_to']
      b.content = request.POST['content']
      b.post_date = datetime.datetime.now()
      b.save()
      return HttpResponseRedirect('/blog/%s/' % b.id)

def addComment(request, blog_id):
    """Generate the context for the form in which niw comments are entered"""
    blog = get_object_or_404(Blog, pk=blog_id)
    return render_to_response('addComment.html', {'blog': blog})

def postComment(request, blog_id):
    """Accepts the HTTP POST data of a new blog comment
       and updates the database accordingly"""
    blog = get_object_or_404(Blog, pk=blog_id)
    comment = blog.comment_set.create(content=request.POST['content'], 
                                      rating=request.POST['rating'],
                                      commenter=request.POST['commenter'])
                                      #post_date= datetime.datetime.now()
    comment.save()
    return HttpResponseRedirect('/blog/%s/comment/' % blog.id)


def viewProfile(request):
    return render_to_response('registration/user_profile.html', {}, 
                              RequestContext(request))

def newUser(request):
    """Create a new user with comment-only permission"""
    if request.POST:
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            if (len(username) == 0 or
                len(password) == 0 or
                len(email) == 0 or
                len(firstname) == 0 or
                len(lastname) == 0):
                return render_to_response('newUser.html', {'username': username,
                                                           'email': email,
                                                           'firstname': firstname,
                                                           'lastname': lastname,
                                                           'msg': 'All fields are required. Please resubmit.'})
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            #Log the user in here
            #This should be successful because we just created the user 
            #with that password
            newuser = authenticate(username=username, password=password)
            return HttpResponseRedirect('/accounts/profile/')
       
        except:
            import sys, traceback
            traceback.print_exc()
            print sys.exc_info()

            #If the username is already in use, a constraint error is thrown.
            #The type of exception thrown depends on the database backend in use
            #so here we assume that any exception is a 
            #"username already in use" error
            return render_to_response('newUser.html', 
                                      {'email': email,
                                       'firstname': firstname,
                                       'lastname': lastname,
                                       'msg': "Username  '%s' is in use. Please choose another." % username})
    else:
        return render_to_response('newUser.html', {})
