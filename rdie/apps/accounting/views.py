import decimal

from django.core.serializers import serialize
from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect

from .forms import HistoryRecordForm
from .models import *
from django.http import HttpResponse, JsonResponse


# Create your views here.


def index(request):
    all_accounts = Account.objects.all()
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    currencies = Currency.objects.all()

    ie_types = []
    for t in Category.CATEGORY_TYPES:
        ie_types.append(t[0])

    year = timezone.now().year
    month = timezone.now().month
    month_amount_expense = HistoryRecord.objects.filter(time_of_occurrence__year=year, time_of_occurrence__month=month,
                                                        category__category_type='支出').aggregate(Sum('amount'))
    month_amount_income = HistoryRecord.objects.filter(time_of_occurrence__year=year, time_of_occurrence__month=month,
                                                       category__category_type='收入').aggregate(Sum('amount'))
    mounth_dif = month_amount_income.get('amount__sum', 0) - month_amount_expense.get('amount__sum', 0)
    datas = HistoryRecord.objects.filter(time_of_occurrence__year=year, time_of_occurrence__month=month)
    current_month_records = {}
    day_income_expense = {}
    for data in datas:
        current_month_records[data.time_of_occurrence.strftime('%Y-%m-%d')] = list(HistoryRecord.objects.filter(
            time_of_occurrence__date=data.time_of_occurrence))

        day_income_expense[data.time_of_occurrence.strftime('%Y-%m-%d')] = {**HistoryRecord.objects.filter(
            time_of_occurrence__date=data.time_of_occurrence, category__category_type='支出').aggregate(
            expense=Sum('amount')), **HistoryRecord.objects.filter(
            time_of_occurrence__date=data.time_of_occurrence, category__category_type='收入').aggregate(
            income=Sum('amount'))}

    print(day_income_expense)
    context = {
        'month_amount_expense': month_amount_expense,
        'month_amount_income': month_amount_income,
        'mounth_dif': mounth_dif,
        'accounts': all_accounts,
        'categories': categories,
        'sub_categories': sub_categories,
        'currencies': currencies,
        'ie_types': ie_types,
        'current_month_records': current_month_records,
        'day_income_expense': day_income_expense
    }
    return render(request, 'accounting/index.html', context)


def retrieve_category(request):
    ie_type = request.POST.get('ie_type')
    serialized_data = serialize('json', Category.objects.filter(category_type=ie_type))
    return HttpResponse(serialized_data)


def record_income_expense(request):
    sub_category = request.POST.get('sub_category')
    time_now = timezone.now()
    if sub_category == "select value":
        try:
            account = request.POST.get('account')
            category = request.POST.get('category')
            currency = request.POST.get('currency')
            amount = request.POST.get('amount')
            comment = request.POST.get('comment')
            time_occur = request.POST.get('time_of_occurrence')
            history_record = HistoryRecord(account_id=account,
                                           category_id=category,
                                           currency_id=currency,
                                           amount=amount,
                                           comment=comment,
                                           time_of_occurrence=time_occur,
                                           created_date=time_now,
                                           updated_date=time_now
                                           )
            history_record.save()
        except Exception as e:
            print("not valid in request with error: %s" % str(e))
    else:
        form = HistoryRecordForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            category = form.cleaned_data['category']
            sub_category = form.cleaned_data['sub_category']
            currency = form.cleaned_data['currency']
            amount = form.cleaned_data['amount']
            comment = form.cleaned_data['comment']
            time_occur = form.cleaned_data['time_of_occurrence']
            history_record = HistoryRecord(account=account,
                                           category=category,
                                           sub_category=sub_category,
                                           currency=currency,
                                           amount=amount,
                                           comment=comment,
                                           time_of_occurrence=time_occur,
                                           created_date=time_now,
                                           updated_date=time_now
                                           )
            history_record.save()

            # 更新银行卡明细
            current_ie_type = category.category_type
            if current_ie_type == "支出":
                account.amount -= decimal.Decimal(amount)
            elif current_ie_type == "收入":
                account.amount += decimal.Decimal(amount)
            account.save()

        else:
            print("not valid in form")
    return redirect(index)
