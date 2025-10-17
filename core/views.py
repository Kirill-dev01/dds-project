# from django.http import JsonResponse
# from .models import Transaction, Category, SubCategory
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Transaction
# from .forms import TransactionForm


# def transaction_list(request):
#     transactions = Transaction.objects.all()
#     context = {
#         'transactions': transactions
#     }
#     return render(request, 'core/transaction_list.html', context)


# def transaction_create(request):
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('transaction_list')
#     else:
#         form = TransactionForm()

#     context = {
#         'form': form
#     }
#     return render(request, 'core/transaction_form.html', context)


# def transaction_update(request, pk):
#     transaction = get_object_or_404(Transaction, pk=pk)
#     if request.method == 'POST':
#         form = TransactionForm(request.POST, instance=transaction)
#         if form.is_valid():
#             form.save()
#             return redirect('transaction_list')
#     else:
#         form = TransactionForm(instance=transaction)

#     context = {
#         'form': form
#     }
#     return render(request, 'core/transaction_form.html', context)


# def transaction_delete(request, pk):
#     transaction = get_object_or_404(Transaction, pk=pk)
#     if request.method == 'POST':
#         transaction.delete()
#         return redirect('transaction_list')

#     context = {
#         'transaction': transaction
#     }
#     return render(request, 'core/transaction_confirm_delete.html', context)

# # NEW VIEW 1: Load categories based on a type_id


# def load_categories(request):
#     type_id = request.GET.get('type_id')
#     categories = Category.objects.filter(type_id=type_id).order_by('name')
#     # We return the data in a format that's easy for JavaScript to use
#     return JsonResponse(list(categories.values('id', 'name')), safe=False)

# # NEW VIEW 2: Load subcategories based on a category_id


# def load_subcategories(request):
#     category_id = request.GET.get('category_id')
#     subcategories = SubCategory.objects.filter(
#         category_id=category_id).order_by('name')
#     return JsonResponse(list(subcategories.values('id', 'name')), safe=False)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Transaction, Status, Type, Category, SubCategory
from .forms import TransactionForm


def transaction_list(request):
    transactions = Transaction.objects.select_related(
        'status', 'type', 'category', 'subcategory').all()

    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()

    # --- THIS IS THE NEW SIMPLER LOGIC ---

    # We will just pass the raw request.GET object to the template
    # and let the template handle the logic.

    if request.GET.get('status'):
        transactions = transactions.filter(status_id=request.GET.get('status'))

    if request.GET.get('type'):
        transactions = transactions.filter(type_id=request.GET.get('type'))

    if request.GET.get('category'):
        transactions = transactions.filter(
            category_id=request.GET.get('category'))

    if request.GET.get('date_from'):
        transactions = transactions.filter(
            created_date__gte=request.GET.get('date_from'))

    if request.GET.get('date_to'):
        transactions = transactions.filter(
            created_date__lte=request.GET.get('date_to'))

    context = {
        'transactions': transactions,
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'filters': request.GET  # We pass the raw request.GET data
    }
    return render(request, 'core/transaction_list.html', context)

# --- THE REST OF OUR VIEWS ARE UNCHANGED ---


def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    context = {
        'form': form
    }
    return render(request, 'core/transaction_form.html', context)


def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    context = {
        'form': form
    }
    return render(request, 'core/transaction_form.html', context)


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    context = {
        'transaction': transaction
    }
    return render(request, 'core/transaction_confirm_delete.html', context)


# --- OUR AJAX VIEWS ARE ALSO UNCHANGED ---

def load_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).order_by('name')
    return JsonResponse(list(categories.values('id', 'name')), safe=False)


def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(
        category_id=category_id).order_by('name')
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)
