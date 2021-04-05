from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category


@login_required(login_url='/login')
def profile(request):
    return render(request, "tracker/profile.html")

def contact_us(request):
    return render(request, "tracker/contact_us.html")

def about(request):
    return render(request, "tracker/about.html")


def find(ch):
    if ch == '':
        return 0
    else:
        return int(ch)

@login_required(login_url='/login')
def edit(request, data_id):
    data = Category.objects.get(current_user=request.user, id=data_id)
    if request.method == "POST":

        # date = data.date
        food = find(request.POST['food'])
        shopping = find(request.POST['shopping'])
        travel = find(request.POST['travel'])
        others = find(request.POST['others'])

        sum = food + travel + shopping + others
        if sum > 0:
            data.food = food
            data.shopping = shopping
            data.travel = travel
            data.others = others
            data.save()
            messages.info(request, 'expense edited succesfully')
            return redirect('/expense')
        else:
            messages.error(request, 'you did not filled any amount !!')
            return redirect('/edit')


    else:

        context = {'dat': data}
        return render(request, "tracker/edit.html", context)


def delete_it(request, data_id):
    data = Category.objects.get(current_user=request.user, id=data_id)
    data.delete()
    messages.info(request, 'expense deleted succesfully')
    return redirect('/expense')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'invalid credentials!!')
            return redirect('/login')
    else:
        return render(request, "tracker/login_page.html")


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password2 == password1:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username already exists!!')
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email already exists!!')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, "registered successfully")
                return redirect('/login')
        else:
            messages.error(request, 'password did not match!!')
            return redirect('/register')
    else:
        return render(request, "tracker/register_page.html")



@login_required(login_url='/login')
def home(request):
    if request.method=='POST' and request.POST['date'] is not '':

        date=request.POST['date']
        print("po0st")
        if Category.objects.filter(current_user=request.user,date=date).exists():
            data = Category.objects.get(current_user=request.user, date=date)
            food = data.food
            shopping = data.shopping
            travel = data.travel
            others = data.others

            total = food + shopping + travel + others
            # total=max(total,0.01)
            if total is not 0:
                fpr = round((food / total) * 100)
                spr = round((shopping / total) * 100)
                tpr = round((travel / total) * 100)
                opr = round((others / total) * 100)
            else:
                fpr = 0
                spr = 0
                tpr = 0
                opr = 0

            context = {'date': date, 'total': total, 'food': food, 'shopping': shopping, 'travel': travel,
                       'others': others, 'fpr': fpr,
                       'spr': spr, 'tpr': tpr, 'opr': opr}

            return render(request, "tracker/home.html", context)


        else:
            food = 0
            shopping = 0
            travel = 0
            others = 0

            total = food + shopping + travel + others
            # total=max(total,0.01)
            if total is not 0:
                fpr = round((food / total) * 100)
                spr = round((shopping / total) * 100)
                tpr = round((travel / total) * 100)
                opr = round((others / total) * 100)
            else:
                fpr = 0
                spr = 0
                tpr = 0
                opr = 0

            context = {'date': date, 'total': total, 'food': food, 'shopping': shopping, 'travel': travel,
                       'others': others, 'fpr': fpr,
                       'spr': spr, 'tpr': tpr, 'opr': opr}

            return render(request, "tracker/home.html", context)







    else:
        print("else po0st")
        data = Category.objects.filter(current_user=request.user)
        total = 0
        food = 0
        shopping = 0
        travel = 0
        others = 0

        for da in data:
            food += da.food
            shopping += da.shopping
            travel += da.travel
            others += da.others

        total = food + shopping + travel + others
        # total=max(total,0.01)
        if total is not 0:
            fpr = round((food / total) * 100)
            spr = round((shopping / total) * 100)
            tpr = round((travel / total) * 100)
            opr = round((others / total) * 100)
        else:
            fpr = 0
            spr = 0
            tpr = 0
            opr = 0

        context = {'total': total, 'food': food, 'shopping': shopping, 'travel': travel, 'others': others, 'fpr': fpr,
                   'spr': spr, 'tpr': tpr, 'opr': opr}
        return render(request, "tracker/home.html", context)





def about(request):
    return render(request, "tracker/about.html")


def support(request):
    return render(request, "tracker/contact_us.html")


def start(request):
    return render(request, 'tracker/start.html')


def hi(request):
    return render(request, 'tracker/hi.html')


def logout_page(request):
    auth.logout(request)
    return redirect('/login')


def expense(request):

    data = Category.objects.filter(current_user=request.user)
    data=data.order_by('date')
    context={'dat':data}

    return render(request, 'tracker/expense.html', context)


def add_expense(request):
    if request.method == "POST":
        current_user = request.user
        date = request.POST['date']
        food = find(request.POST['food'])
        shopping = find(request.POST['shopping'])
        travel = find(request.POST['travel'])
        others = find(request.POST['others'])

        sum = food + travel + shopping + others

        if date != "":
            if sum > 0:
                if Category.objects.filter(date=date, current_user=current_user).exists():
                    data = Category.objects.get(date=date, current_user=current_user)
                    data.food += food
                    data.shopping += shopping
                    data.travel += travel
                    data.others += others
                    data.save()
                    messages.info(request, 'expense added succesfully')
                    return redirect('/add_expense')
                else:
                    data = Category(date=date, food=food, shopping=shopping, travel=travel,
                                    others=others, current_user=current_user)
                    data.save()
                    messages.info(request, 'expense added succesfully')
                    return redirect('/add_expense')


            else:
                messages.error(request, 'you did not filled any amount !!')
                return redirect('/add_expense')
        else:
            messages.error(request, 'Unfortunately!! you missed the date ')
            return redirect('/add_expense')


    else:
        return render(request, "tracker/add_expense.html")
