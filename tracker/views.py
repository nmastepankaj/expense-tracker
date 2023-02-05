"""Define all the views here."""
from calendar import month
from datetime import datetime
from django.http import QueryDict, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Expense
from .forms import *
from .decorators import unauthenticated_user

# Create your views here.
# region Authentication
@unauthenticated_user
def register_view(request):
    register_form: RegisterForm = RegisterForm()

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user: User = register_form.save()
            username: str = user.username

            messages.info(request, f"User {username} was created successfully!")

            return redirect("login")

    context = {"register_form": register_form}
    return render(request, "tracker/auth_register.html", context)


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        _username: str = request.POST.get("username")
        _password: str = request.POST.get("password")

        user: User = authenticate(request.POST, username=_username, password=_password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username or password is incorrect.")

    context = {}
    return render(request, "tracker/auth_login.html", context)


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")


# endregion

# region Main views
@login_required(login_url="login")
def dashboard(request):
    """The view of the main page."""
    expenses = Expense.objects.filter(owner=request.user)
    expenses = expenses.order_by("-transaction_date")

    # Expenses this year
    total_expenses = expenses.filter(
        cost__lt = 0
    )
    total_expense = sum(expense.cost for expense in total_expenses)

    total_money_ceditted = expenses.filter(
        cost__gt = 0
    )
    total_money_cedits = sum(expense.cost for expense in total_money_ceditted)
    # Expenses this month
    




    total_money_left = sum(expense.cost for expense in expenses)

    expense_short_form: ExpenseShortForm = ExpenseShortForm()
    add_money_short_form: AddMoneyShortForm = AddMoneyShortForm()

    # Quick expense addition
    if request.method == "POST":
        expense_short_form = ExpenseShortForm(request.POST)
        if expense_short_form.is_valid():
            expense: Expense = expense_short_form.save()
            expense.owner = request.user
            expense.cost = -expense.cost
            expense.save()
        return redirect("/")

    context = {
        "expenses": expenses,
        "expense_short_form": expense_short_form,
        "total_expense": total_expense,
        "total_money_credits": total_money_cedits,
        "money_left" : total_money_left,
        "add_money_short_form":add_money_short_form
    }
    return render(request, "tracker/dashboard.html", context)

@login_required(login_url="login")
def add_money(request):
    """The view of the main page."""
    if request.method == "POST":
        add_money_short_form = AddMoneyShortForm(request.POST)
        if add_money_short_form.is_valid():
            expense: Expense = add_money_short_form.save()
            expense.owner = request.user
            expense.save()
        return redirect("/")

    return redirect("/")


@login_required(login_url="login")
def add_expense_full_form(request):
    """A view for a full expense form, where the user can
    enter all the editable fields.
    """
    expense_full_form: ExpenseFullForm = ExpenseFullForm()

    if request.method == "POST":
        expense_full_form = ExpenseFullForm(request.POST)
        if expense_full_form.is_valid():
            expense: Expense = expense_full_form.save()
            expense.owner = request.user
            expense.save()
        return redirect("/")

    context = {
        "expense_full_form": expense_full_form,
    }
    return render(request, "tracker/add_expense_full_form.html", context)


@login_required(login_url="login")
def expense_info(request, expense_id: int):
    """A view of an expense page. Here, the user can see and edit the information of
    the inspected expense.
    """
    expense: Expense = Expense.objects.get(id=expense_id)
    expense_full_form: ExpenseFullForm = ExpenseFullForm(instance=expense)

    # Update the expense
    if request.method == "POST":
        expense: Expense = ExpenseFullForm(request.POST, instance=expense)
        if expense.is_valid():
            expense.save()
        return redirect("/")

    context = {
        "expense": expense,
        "expense_full_form": expense_full_form,
    }
    return render(request, "tracker/expense_info.html", context)


# endregion


@login_required(login_url="login")
def expense_delete(request, expense_id: int):
    """A view of an expense deletion confirmation page."""
    expense: Expense = Expense.objects.get(id=expense_id)

    # Remove the expense
    if request.method == "POST":
        expense.delete()
        return redirect("/")

    context = {
        "expense": expense,
    }
    return render(request, "tracker/expense_delete.html", context)
