from django import template

from app_Transactions.models import Wallet

register = template.Library()


@register.simple_tag
def wallet_amount(user):
    try:
        user_wallet = Wallet.objects.get(user=user)
        return user_wallet.amount
    except Wallet.DoesNotExist:
        return 0


@register.simple_tag
def wallet_amount_status(user):
    try:
        user_wallet = Wallet.objects.get(user=user)
        return "success" if user_wallet.amount > 0 else "danger" if user_wallet.amount < 0 else "white"
    except Wallet.DoesNotExist:
        return "white"
