import calendar
import datetime
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
    month_expense = HistoryRecord.objects.filter(time_of_occurrence__year=year, time_of_occurrence__month=month,
                                                        category__category_type='支出').aggregate(Sum('amount'))
    month_income = HistoryRecord.objects.filter(time_of_occurrence__year=year, time_of_occurrence__month=month,
                                                       category__category_type='收入').aggregate(Sum('amount'))

    month_amount_expense = month_expense['amount__sum'] if month_expense['amount__sum'] else 0
    month_amount_income = month_income['amount__sum'] if month_income['amount__sum'] else 0
    mounth_dif = month_amount_income - month_amount_expense

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
    print(ie_type)
    serialized_data = serialize('json', Category.objects.filter(category_type=ie_type))
    print(serialized_data)
    return HttpResponse(serialized_data)


def retrieve_sub_category(request):
    category_id = request.POST.get('category_id')
    print(category_id)
    serialized_data = serialize('json', SubCategory.objects.filter(parent_id=category_id))
    print(serialized_data)
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


def retrieve_current_month_income_expense(request):
    if request.user.is_authenticated:
        post_year = request.POST.get('year')
        post_month = request.POST.get('month')
        if post_year and post_month:
            year = int(post_year)
            month = int(post_month)
        else:
            today = datetime.date.today()
            year = today.year
            month = today.month
        month_has_days = calendar.monthrange(year, month)[1]
        days = [datetime.date(year, month, day).strftime("%Y-%m-%d") for day in range(1, month_has_days + 1)]
        days_income = []
        days_expense = []
        category_names = []
        month_category_income = {}
        month_category_expense = {}
        month_total_income = 0
        month_total_expense = 0
        month_history_records = HistoryRecord.objects.filter(time_of_occurrence__year=year,
                                                             time_of_occurrence__month=month).order_by(
            "time_of_occurrence")
        for day in days:
            day_history_records = month_history_records.filter(time_of_occurrence__day=int(day.split("-")[-1]))
            day_income = 0
            day_expense = 0
            for hr in day_history_records:
                hr_category = hr.category
                if hr_category.category_type == "支出":
                    day_expense += hr.amount
                    month_total_expense += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        month_category_expense[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        month_category_expense[hr_category.name]["value"] += hr.amount
                elif hr_category.category_type == "收入":
                    day_income += hr.amount
                    month_total_income += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        month_category_income[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        month_category_income[hr_category.name]["value"] += hr.amount
            days_income.append(day_income)
            days_expense.append(day_expense)
        return JsonResponse({"days": days,
                             "days_income": days_income,
                             "days_expense": days_expense,
                             "month_total_income": month_total_income,
                             "month_total_expense": month_total_expense,
                             "month_category_names": category_names,
                             "month_category_income": list(month_category_income.values()),
                             "month_category_expense": list(month_category_expense.values())})
    else:
        return JsonResponse({"error": "unauthenticated"})
