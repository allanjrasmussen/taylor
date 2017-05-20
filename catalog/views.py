
from django.forms import modelformset_factory, ModelForm
from django.utils.translation import ugettext as _
from django.shortcuts import render
from .models import Pattern, Genre, Illustration, Profile, Persons, Measure_help
from django.http import HttpResponse
from django.views import generic
from django.forms import ModelChoiceField, ModelForm
import datetime
from django.core.mail import send_mail
from django import forms
import re
from django.template import Template
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from decimal import Decimal
from django.templatetags.static import static

# Create your views here.



def index(request):
    return render(request, 'index.html')

def navgoco(request):
    return render(request, 'navgoco.html')
    
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

def adduser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return HttpResponse('index.html')
    else:
        form = UserForm()
    return render(request, 'catalog/registration/adduser.html', {'form': form})

def profile(request):
    profileFormSet = modelformset_factory(Profile, fields=('name', 'email', 'phone', 'address', 'zip', 'city', 'country', 'description'))
    if request.method == "POST":
        formset = profileFormSet(
            request.POST, request.FILES,
            queryset=Profile.objects.filter(name__startswith='0'),
        )
        if formset.is_valid():
            formset.save()
            return render(request, 'catalog/registration/profile.html')
    else:
        formset = profileFormSet(queryset=Profile.objects.filter(name__startswith='0'))
    return render(request, 'catalog/registration/profile.html', {'formset': formset,})

class personForm(ModelForm):
    class Meta:
        model = Persons
        fields = ['user', 'name', 'email','phone', 'address', 'zip', 'city']

def person(request):
    if request.method == 'POST':
        form = personForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return render(request, 'catalog/clients/clients.html')
    else:

        form = personForm( initial={'user':request.user} )
        form.fields['user'].widget = forms.HiddenInput()
    return render(request, 'catalog/person/person.html', {'form': form})



def measurements(request):
    #user_id = request.user.id
    personFormSet = modelformset_factory(Persons,
            fields=('ucc', 'bc', 'bd', 'wc', 'hc1', 'hh1','hc2' ,'hh2','ubw','bl','bh','shl','shh','sih','shw',
            'out_ls','in_ls','kc','br','fc','_1_6','_1_3','diff','_1_10','kh',
            'in_sl','bic','wrc','hac','ch_a','ahw_a','ch_b','ahw_b','ch_c','ahw_c','ch_d','ahw_d','ch_e','ahw_e','ch_f','ahw_f','name',))
    if request.method == "POST":
        formset = personFormSet(
            request.POST, request.FILES,
            #queryset=persons.objects.filter(name__startswith='O'),
            queryset=Persons.objects.filter(name__startswith='0'),
        )
        if formset.is_valid():
            formset.save()
            # Do something.
    else:
        #formset = personFormSet(queryset=persons.objects.filter(name__startswith='O'))
        formset = personFormSet(queryset=Persons.objects.filter(name__startswith='0'))
    return render(request, 'catalog/measurements/measurements.html', {'formset': formset})

def clients(request):
    queryset = Persons.objects.filter(user = request.user)

    context= {
                'queryset': queryset,
            }
    return render(request,'catalog/clients/clients.html', context)

class ClientDetailView( generic.DetailView):
    model = Persons

def klient_gemt(request):
    help = Measure_help.objects.filter(sprog='en')
    form = request.POST
    ucck=form['ucc'].replace(',','.')
    bck=form['bc'].replace(',','.')
    bdk=form['bd'].replace(',','.')
    wck=form['wc'].replace(',','.')
    hc1k=form['hc1'].replace(',','.')
    pk = form['pk']
    q=Persons(user_id=User.id, id=pk,
    ucc=ucck,
    bc=bck,
    bd=bdk,
    wc=wck,
    hc1=hc1k )
    navn=q.name


    q.save(update_fields=['ucc', 'bc','bd', 'wc','hc1'])

    context={
        'ucc': ucck,
        'bc': bck,
        'bd': bdk,
        'wc': wck,
        'hc1': hc1k,
        'pk': pk,
        'navn': navn,
        'help': help,
    }
    return render(request,'catalog/klient_gemt.html',context)

def purchases(request):
    queryset = Persons.objects.filter(user = request.user)

    context= {
                'queryset': queryset,

            }
    return render(request,'catalog/purchases/purchases.html', context)



def about(request):
    queryset = Pattern.objects.filter(title = 'About')
    width = '50%'
    about = '''CUT UP STUDIO I/S
Cort Adelers Gade 7, kld.
1053 Copenhagen
Denmark
CVR-nr.: 37639788'''
    context= {
                'queryset': queryset,
                'width': width,
                'about': about
            }
    return render(request,'catalog/includes/dropdown05/about.html', context)








def drop01_view_all(request):
    queryset = Pattern.objects.filter(title = 'Basic view all')
    width = '30%'
    context= {
                'queryset': queryset,
                'width': width
            }
    return render(request,'catalog/includes/dropdown01/view_all.html', context)

def drop01_dress_block(request):
    title='Basic Dress Block';
    queryset = Pattern.objects.filter(title = 'Basic Dress Block')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/DRESS BLOCK/Kjolegrundform_for_01.png',
    'produkt_bibliotek/BASIC_BLOCKS/DRESS BLOCK/Kjolegrundform_bag_02.png',
    'produkt_bibliotek/BASIC_BLOCKS/DRESS BLOCK/Kjolegrundform_03.png')
    antal=3

    oversigt='produkt_bibliotek/BASIC_BLOCKS/DRESS BLOCK/kjole-oversigt.png'
    url='produkt_bibliotek/BASIC_BLOCKS/DRESS SLEEVE/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic dress block. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it. You can download the compendium as a PDF-file from your account as soon as you are checked out. 

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes:  • Instruction on the basic dress block  • Step-by-step guide to instruction  • Guide to alignment (bust dart)  • Pattern overview
 PAGES
DETAILS
Language: English  Published:
 Edition: 1
 Binding: PDF
    '''

    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)

def drop01_dress_sleeve(request):
    title='Basic Dress Sleeve'
    queryset = Pattern.objects.filter(title = 'Basic Dress Sleeve')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/DRESS SLEEVE /Basis-kjoleaerme_01.png',
    'produkt_bibliotek/BASIC_BLOCKS/DRESS SLEEVE /Basis-kjoleaerme02.png',)
    antal=2

    oversigt='produkt_bibliotek/BASIC_BLOCKS/DRESS SLEEVE /kjoleæaerme-oversigt.png'
    url='produkt_bibliotek/BASIC_BLOCKS/DRESS SLEEVE/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic dress sleeve for our basic dress block. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it.
The instruction is developed for our basic dress block, but with a few adjustments you can also use it for your other basic dress blocks. You can download the compendium as a PDF-file from your account as soon as you are checked out. 

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes: 
• Instructions for fitting the basic dress block, armhole width and cap height  • Instruction on the basic dress sleeve block  • Step-by-step guide to instruction  • Pattern overview  PAGES  DETAILS Language: English  Published: Edition: 1 Binding: PDF

To create this dress sleeve you will need the following instructions:

(Her skal der linkes til kjolegrundformen i form af et lille billede som vist I layout til produktside)
    '''

    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)

def drop01_shirt_sweatshirt(request):
    title='BASIC SHIRT/SWEARSHIRT BLOCK'
    queryset = Pattern.objects.filter(title = 'Basic shirt_sweatshirt')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/Skjorte-sweatshirtgrundform_01.png',
    'produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/Skjorte-sweatshirtgrundform_02.png',
    'produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/Skjorte-sweatshirtgrundform_03.png',
    'produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/Skjorte-sweatshirtgrundform_04.png')
    antal=4
    oversigt='produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/skjorte-sweatshirt-oversigt.png'
    url='produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic shirt and sweatshirt block. Each block has the same starting point; it’s only the length and neckline, which is different form each other and therefore are both the basic blocks gathered in one compendium. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it.
You can download the compendium as a PDF-file from your account as soon as you are checked out. 

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes: 
 • Instruction on the basic shirt/sweatshirt block 
 • Step-by-step guide to instruction 
 • Pattern overview - shirt  
• Pattern overview - sweatshirt

PAGES

DETAILS
Language: English 
 Published: 
Edition: 1 
Binding: PDF
    '''

    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)

def drop01_dress_sleeve(request):
    title='Basic Dress Sleeve'
    queryset = Pattern.objects.filter(title = 'Basic Dress Sleeve')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/DRESS SLEEVE /Basis-kjoleaerme_01.png',
    'produkt_bibliotek/BASIC_BLOCKS/DRESS SLEEVE /Basis-kjoleaerme02.png',)
    antal=2

    oversigt='produkt_bibliotek/BASIC_BLOCKS/DRESS SLEEVE /kjoleæaerme-oversigt.png'
    url='produkt_bibliotek/BASIC_BLOCKS/DRESS SLEEVE/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic dress sleeve for our basic dress block. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it.
The instruction is developed for our basic dress block, but with a few adjustments you can also use it for your other basic dress blocks. You can download the compendium as a PDF-file from your account as soon as you are checked out. 

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes: 
• Instructions for fitting the basic dress block, armhole width and cap height 
 • Instruction on the basic dress sleeve block  
• Step-by-step guide to instruction  
• Pattern overview  
PAGES  DETAILS
 Language: English 
 Published: 
Edition: 1 
Binding: PDF

To create this dress sleeve you will need the following instructions:

(Her skal der linkes til kjolegrundformen i form af et lille billede som vist I layout til produktside)
    '''

    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)

def drop01_shirt_sleeve(request):
    title='BASIC SHIRT SLEEVE'
    queryset = Pattern.objects.filter(title = 'BASIC SHIRT SLEEVE')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/SHIRT SLEEVE/Basis-skjorteærme_01.png',
    'produkt_bibliotek/BASIC_BLOCKS/SHIRT SLEEVE/Basis-skjorteærme_02.png')
    antal=2
    oversigt='produkt_bibliotek/BASIC_BLOCKS/SHIRT SLEEVE/skjorteærme-oversigt.png'
    url='produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic shirt sleeve for our basic shirt block. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it.
The instruction is developed for our basic shirt block and to achieve the best result, we recommend you to use this sleeve instruction in connection with the instruction on our basic shirt block. Though, with a few adjustments you can also use this instruction for your other basic shirt blocks. You can download the compendium as a PDF-file from your account as soon as you are checked out.

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes:  
• Instruction on the basic shirt sleeve  
• Step-by-step guide to instruction  
• Pattern overview
 PAGES  DETAILS
Language: English  
Published:
 Edition: 1 
Binding: PDF

To create this shirt sleeve you will need the following instructions:

(Her skal der linkes til skjortegrundform, i form af et lille billede som vist I layout til produktside)
    '''

    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)

def drop01_sweatshirt_sleeve(request):
    title='BASIC SWEATSHIRT SLEEVE'
    queryset = Pattern.objects.filter(title = 'BASIC SWEATSHIRT SLEEVE')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/SWEATSHIRT SLEEVE /Basis-sweatshirtærme_01.png',
    'produkt_bibliotek/BASIC_BLOCKS/SWEATSHIRT SLEEVE /Basis-sweatshirtærme_02.png')
    antal=2
    oversigt='produkt_bibliotek/BASIC_BLOCKS/SWEATSHIRT SLEEVE /sweatshirtærme.png'
    url='produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic sweatshirt sleeve. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it.
The instruction is developed for our basic sweatshirt block and to achieve the best results, we recommend you to use this sleeve instruction in connection with the instruction on our basic sweatshirt block. Though, with a few adjustments you can also use this instruction for your other basic sweatshirt blocks. You can download the compendium as a PDF-file from your account as soon as you are checked out. 

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes:  
• Instruction on the basic sweatshirt sleeve 
 • Step-by-step guide to instruction  
• Pattern overview
 PAGES  DETAILS
Language: English  
Published:
 Edition: 1 
Binding: PDF

To create this sweatshirt sleeve you will need the following instructions:

(Her skal der linkes til skjorte/sweatshirtgrundform, i form af et lille billede som vist I layout til produktside)

    '''

    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)

def drop01_skirt_block(request):
    title='BASIC SKIRT BLOCK'
    queryset = Pattern.objects.filter(title = 'BASIC SKIRT BLOCK')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/SKIRT BLOCK/Nederdelsgrundform_01.png',
    'produkt_bibliotek/BASIC_BLOCKS/SKIRT BLOCK/Nederdelsgrundform_02.png',
    'produkt_bibliotek/BASIC_BLOCKS/SKIRT BLOCK/Nederdelsgrundform_03.png' )
    antal=3
    oversigt='produkt_bibliotek/BASIC_BLOCKS/SKIRT BLOCK/nederdel-oversigt.png'
    url='produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic skirt block. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it.
You can download the compendium as a PDF-file from your account as soon as you are checked out. 

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes: 
 • Instruction on the basic skirt block  
• Step-by-step guide to instruction  
• Guide to waist darts and hip curves  
• Pattern overview

PAGES

DETAILS
Language: English  
Published:
 Edition: 1 
Binding: PDF
    '''

    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)

def drop01_trouser_block(request):
    title='BASIC TROUSER BLOCK'
    queryset = Pattern.objects.filter(title = 'BASIC TROUSER BLOCK')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/TROUSER BLOCK/Buksegrundform_01.png',
    'produkt_bibliotek/BASIC_BLOCKS/TROUSER BLOCK/Buksegrundform_02.png',
    'produkt_bibliotek/BASIC_BLOCKS/TROUSER BLOCK/Buksegrundform_03.png' )
    antal=3
    oversigt='produkt_bibliotek/BASIC_BLOCKS/TROUSER BLOCK/bukse-oversigt.png'
    url='produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic trouser block. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it.
You can download the compendium as a PDF-file from your account as soon as you are checked out. 

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes:  
• Instruction on the basic trouser block 
 • Step-by-step guide to instruction  
• Guide to waist dart  
• Pattern overview

PAGES

DETAILS
Language: English  
Published:
 Edition: 1 
Binding: PDF
'''

    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)

def drop01_coat_block(request):
    title='BASIC COAT BLOCK'
    queryset = Pattern.objects.filter(title = 'BASIC COAT BLOCK')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/COAT BLOCK/Frakkegrundform_01.png',
    'produkt_bibliotek/BASIC_BLOCKS/COAT BLOCK/Frakkegrundform_02.png',
    'produkt_bibliotek/BASIC_BLOCKS/COAT BLOCK/Frakkegrundform_03.png' )
    antal=3
    oversigt='produkt_bibliotek/BASIC_BLOCKS/COAT BLOCK/frakke-oversigt.png'
    url='produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic coat block. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it. You can download the compendium as a PDF-file from your account as soon as you are checked out. 

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes: 
• Instruction on the basic coat block  
• Step-by-step guide to instruction  
• Guide to alignment (bust dart)  
• Pattern overview

PAGES DETAILS 
Language: English  
Published: 
Edition: 1 
Binding: PDF

'''

    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)

def drop01_jacket_block(request):
    title='BASIC JACKET BLOCK'
    queryset = Pattern.objects.filter(title = 'BASIC JACKET BLOCK')
    width = '50%'
    images=('produkt_bibliotek/BASIC_BLOCKS/JACKET BLOCK /jakke-oversigt.png',
    'produkt_bibliotek/BASIC_BLOCKS/COAT BLOCK/Frakkegrundform_02.png',
    'produkt_bibliotek/BASIC_BLOCKS/COAT BLOCK/Frakkegrundform_03.png' )
    antal=3
    oversigt='produkt_bibliotek/BASIC_BLOCKS/JACKET BLOCK /jakke-oversigt.png'
    url='produkt_bibliotek/BASIC_BLOCKS/SHIRT-SWEATSHIRT BLOCK/summary.txt'
    price= '€15'
    summary='''
DESCRIPTION
This is an instruction on how to draft a basic jacket block. The instruction contains a quarter–scale illustration, showing all the stages of the construction and is divided into two parts: a complete instruction and a step-by-step guide to the instruction. Whether you are new to the profession, or have experience in cutting, you can use it.
You can download the compendium as a PDF-file from your account as soon as you are checked out. 

Create an account with your own personal measurements or a customer record and get the measurements directly into your instructions.

This compendium includes: 
• Instruction on the basic jacket block  
• Step-by-step guide to instruction  
• Guide to alignment (bust dart)  
• Pattern overview

PAGES DETAILS
Language: English  
Published: 
Edition: 1 
Binding: PDF
'''
    context= {
                'title': title,
                'queryset': queryset,
                'width': width,
                'images': images,
                'antal': antal,
                'oversigt': oversigt,
                'summary': summary,
                'url': url,
                'price': price,
            }
    return render(request,'catalog/includes/dropdown01/view_1v02.html', context)










def drop05_how2_meas(request):
    queryset = Pattern.objects.filter(title = 'Måltagning')
    width = '30%'
    context= {
                'queryset': queryset,
                'width': width
            }
    return render(request,'catalog/includes/dropdown01/view_all.html', context)
