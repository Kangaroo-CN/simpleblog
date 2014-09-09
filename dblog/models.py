
"""Django model classes for a simple Blog site"""

from django.db import models

class Blog(models.Model):
    """The class representing an entry in the blog"""

    """The title or subject of the blog entry"""
    title = models.CharField(max_length=128)

    """The date that the post was created"""
    post_date = models.DateTimeField('date posted')
    
    """The email address of the posting author"""
    reply_to = models.EmailField()

    """The actual text content of the posting"""
    content = models.TextField()

    
    def rating(self):
        """Compute the average rating based on the comments received"""
        comments = self.comment_set.all()

        #Don't divide by zero
        if len(comments) == 0:
            return "(unrated)"

        sum = 0.0
        for c in comments:
            sum = sum + c.rating
        average = float(sum)/len(comments)
        return "%.2f" % average

    """The possible ratings for each blog entry"""
    RATING_CHOICES = (
            (1, '1point'),
            (2, '2points'),
            (3, '3points'),
            (4, '4points'),
            (5, '5points'),
            )
    """Empty class enables the Django admin web interface"""
    class Admin:
        pass

    """This custom permission is requred to create a new Blog entry"""
    class Meta:
        permissions = (
            ("may_create_blogs", "May Create Blogs"),
      )


    """String representation is used by the Django admin interface."""
    def __unicode__(self):
        return "Blog(title = '%s')" % (self.title)


class Comment(models.Model):
    commenter = models.TextField(max_length=20)
    in_reference_to = models.ForeignKey(Blog)
    content = models.TextField(max_length=256)
    rating = models.IntegerField(choices=Blog.RATING_CHOICES)
    #post_date = models.DateTimeField('date posted')


    def ratingText(self):

        """Return this comment's rating as a text string rather than an integer"""
        return Blog.RATING_CHOICES[self.rating-1][1]

    """Empty class enables the Django admin web interface"""
    class Admin:
        pass

    def __unicode__(self):
        """String representation is used by the Django admin interface"""
        return "Comment(commenter = '%s', content = '%s', rating = %s)" % (self.commenter, self.content, str(self.rating))


class  Mood(models.Model):
    post_date = models.DateTimeField('date')
    content = models.TextField(max_length=80)
    
    class Admin:
        pass
    
    def __unicode__(self):
        """String representation is used by the Django admin interface"""
        return "Mood(Content: %s)" % self.content
