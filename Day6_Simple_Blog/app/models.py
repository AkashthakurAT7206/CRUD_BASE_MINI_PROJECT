
from django.db import models  # import Django's model base classes and field types
from django.contrib.auth.models import User  # import the built-in User model provided by Django
from django.urls import reverse  # import reverse to build URLs from named routes
from django.db.models.signals import post_save  # import the post_save signal to run code after saving a model
from django.dispatch import receiver


class Category(models.Model):  # define a Category model to group blog posts
    name = models.CharField(max_length=100, unique=True)  # the category name, must be unique and limited to 100 chars
    description = models.TextField(blank=True)  # optional longer description of the category
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp set once when the category is created

    class Meta:  # metadata for the model
        verbose_name_plural = "Categories"  # use "Categories" as the plural display name in admin and elsewhere

    def __str__(self):  # string representation of the category
        return self.name  # show the category name when converted to a string

    def get_absolute_url(self):  # helper to get the URL for a category detail page
        return reverse('category_detail', kwargs={'pk': self.pk})  # build URL using the category's primary key
        
        
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(max_length=500,blank=True)
    location = models.CharField(max_length=500,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    avatar = models.ImageField(upload_to='profile_images/',null=True,blank=True,help_text='upload profile picture')
    website = models.URLField(blank=True)
    def __str__(self):  
        return self.user.username  

    def get_absolute_url(self):  
        return reverse('profile_detail', kwargs={'pk': self.pk})  
    
    
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):  # string representation of the category
        return self.name 



class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200) # url - friendly identifier for the posts must be  unique
    content = models.TextField()
    featured_image =  models.ImageField(upload_to='blog_images/', blank=True, null=True, help_text="Upload blog featured image")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') 
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag,blank=True,related_name='posts')
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['-created_at']
        unique_together = ['slug','author']
        
    def get_absolute_url(self):  
        return reverse('blog_detail', kwargs={'slug': self.slug})  
        
    def __str__(self):
        return self.title


class Comment(models.Model):  
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')  
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  
    content = models.TextField(max_length=1000) 
    created_at = models.DateTimeField(auto_now_add=True)  
    is_approved = models.BooleanField(default=True)  
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  

    class Meta: 
        ordering = ['created_at']  

    def __str__(self):  
        return f'Comment by {self.author.username} on {self.blog.title}' 
    
    
class BlogLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_blog')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['blog', 'user']
    
    def __str__(self):
        return f'Liked by {self.user.username} on {self.blog.title}'  

    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):  
        instance.profile.save()

        
