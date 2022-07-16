from django.utils import timezone

from celery import shared_task

from app_Bills.models import Bill
from app_Transactions.models import Transaction


def save_bill_in_transaction(objects):
    for obj in objects:
        Transaction.objects.create(user=obj.user, type="BIL", reference_id=obj.id, condition="ADT", amount=obj.amount, description=obj.description)


@shared_task
def bill_task():
    time_now = timezone.now().date()
    all_bill_yearly = Bill.objects.filter(receive_date__month=time_now.month, receive_date__day=time_now.day, type="YEA")
    save_bill_in_transaction(all_bill_yearly)

    all_bill_monthly = Bill.objects.filter(receive_date__day=time_now.day, type="MON")
    save_bill_in_transaction(all_bill_monthly)

    all_bill_weekly = Bill.objects.filter(receive_date__week_day=time_now.weekday() + 2, type="WEK")
    save_bill_in_transaction(all_bill_weekly)

    all_bill_daily = Bill.objects.filter(type="DAY")
    save_bill_in_transaction(all_bill_daily)
