from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date, datetime
from django.forms import ModelForm
# Create your models here.

# Create your models here.

def upload_location(instance, filename):
    return "%s" %( filename)

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    email = models.EmailField( blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=50, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    description =  models.CharField(max_length=20, blank=True)


class profileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email', 'phone', 'address', 'zip', 'city', 'country', 'description')

class Illustration(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='', width_field=0, height_field=0)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Overview_img(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='', width_field=0, height_field=0)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, help_text="Enter a brief description of the pattern", null=True)
    illustration = models.ManyToManyField(Illustration, help_text="Select a genre for this pattern")
    overview_img = models.ManyToManyField(Overview_img, help_text="Select a genre for this pattern")



class Pricelist(models.Model):
    price_group = models.CharField(max_length=200, help_text="Enter a price group")
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    product = models.ManyToManyField(Product)
    date = models.DateTimeField(default=datetime.now())

class Genre(models.Model):
    """
    Model representing a pattern genre (e.g. Basic, variation of Basic, product).
    """
    name = models.CharField(max_length=200, help_text="Enter a pattern genre (e.g.  Basic, variation of Basic, product etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Pattern(models.Model):
    """
    Model representing a pattern sheet (but not a specific copy of a pattern).
    """
    title = models.CharField(max_length=200)

    summary = models.TextField(max_length=2000, help_text="Enter a brief description of the pattern")
    illustration = models.ManyToManyField(Illustration, help_text="Select a genre for this pattern")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this pattern")
    # ManyToManyField used because genre can contain many patterns. pattern can cover many genres.
    # Genre class has already been defined so we can specify the object above.

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('pattern-detail', args=[str(self.id)])

    def display_genre(self):
            """
            Creates a string for the Genre. This is required to display genre in Admin.
            """
            return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'


class Purchases(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price = models.ManyToManyField(Pricelist)
    date = models.DateTimeField(default=datetime.now())

class Measure_help(models.Model):
    sprog = models.CharField(max_length=10, unique=True)
    ucc = models.ImageField(upload_to='',  width_field=0, height_field=0, blank=True)
    bc = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    bd = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)

    wc = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    hc1 = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    hc2 = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.sprog

    hh2 = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ubw = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    bl = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    bh = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    shl = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    shh = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    sih = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    shw = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)

    out_ls = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    in_ls = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    kc = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    br = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    fc = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    _1_6 = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    _1_3 = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    diff = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    _1_10 = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    kh = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)

    in_sl = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    bic = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    wrc = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    hac = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ch_a = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ahw_a = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ch_b = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ahw_b = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ch_c = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ahw_c = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ch_d = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ahw_d = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ch_e = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ahw_e = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ch_f = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)
    ahw_f = models.ImageField(upload_to='', width_field=0, height_field=0, blank=True)



class Persons(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField("Client", max_length=50)
    email = models.EmailField( blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=50, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=20, blank=True)

    img = models.ManyToManyField(Measure_help, help_text='Help')
    #person_id = models.ForeignKey(Persons, on_delete=models.CASCADE)
    ucc = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    bc = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    bd = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    wc = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    hc1 = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    hh1 = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    hc2 = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    hh2 = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ubw = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    bl = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    bh = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    shl = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    shh = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    sih = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    shw = models.DecimalField(default=0,max_digits=6, decimal_places=1)

    out_ls = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    in_ls = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    kc = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    br = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    fc = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    _1_6 = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    _1_3 = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    diff = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    _1_10 = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    kh = models.DecimalField(default=0,max_digits=6, decimal_places=1)

    in_sl = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    bic = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    wrc = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    hac = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ch_a = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ahw_a = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ch_b = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ahw_b = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ch_c = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ahw_c = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ch_d = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ahw_d = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ch_e = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ahw_e = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ch_f = models.DecimalField(default=0,max_digits=6, decimal_places=1)
    ahw_f = models.DecimalField(default=0,max_digits=6, decimal_places=1)
