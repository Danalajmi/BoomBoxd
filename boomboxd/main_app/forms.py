from django.forms import ModelForm
from .models import *

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating', 'date', 'fav', 'mention', 'least', 'album' ]
