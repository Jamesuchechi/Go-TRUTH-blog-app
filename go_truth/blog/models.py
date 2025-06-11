from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    CATEGORY_CHOICES =(
        ('health', 'Health'),
        ('entertainment','Entertainment'),
        ('sports', 'Sports'),
        ('education','Education'),
        ('business','Business'),
        ('travel', 'Travel'),
        ('food', 'Food'),
        ('fashion','Fashion'),
        ('lifestyle','Lifestyle'),
        ('gaming', 'Gaming'),
        ('news', 'News'),
    )
    name = models.CharField(max_length=100,choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True, help_text="A brief description of the category")
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=100, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name

class Tag(models.Model):
    TAG_CHOICES = (
        ('fitness', 'Fitness'),
        ('movies', 'Movies'),
        ('gadgets', 'Gadgets'),
        ('football', 'Football'),
        ('learning', 'Learning'),
        ('startup', 'Startup'),
        ('adventures', 'Adventures'),
        ('recipes', 'Recipes'),
        ('style', 'Style'),
        ('wellness', 'Wellness'),
        ('esports', 'Esports'),
        ('politics', 'Politics'),
    )
    name = models.CharField(max_length=50,choices=TAG_CHOICES, unique=True)
    description = models.TextField(blank=True,help_text="A brief description of the tag.")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now= True)
    slug = models.SlugField(max_length=50, unique=True)

    def _str_(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category,blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts',blank=True)
   # comments = models.ManyToManyField('Comment', related_name='related_posts',blank=True)

    def _str_(self):
        return self.title
    
    
    def comment_count(self):
        return self.comments.filter(is_hidden=False).count()
    
    
    def like_count(self):
        return self.likes.count()
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comment_image/',blank=True, null=True)
    video = models.URLField(max_length=200,blank=True,null=True,help_text="Add a video URL(e.g, youtube link)for the comment")
    likes = models.ManyToManyField(User,related_name='liked_comments',blank=True)
    is_hidden = models.BooleanField(default=False)

    def _str_(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta:
        unique_together = ('post', 'user')

    def _str_(self):
        return f"{self.user.username} likes {self.post.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    email = models.EmailField(max_length=255, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    contact = models.CharField(max_length=255, blank=True, help_text="Phone or email for contact")
    link = models.URLField(max_length=200, blank=True, help_text="Personal webpage or social link")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.jpg')
    date_modified = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100, blank=True)

    def _str_(self):
        return f"{self.user.username}'s Profile"