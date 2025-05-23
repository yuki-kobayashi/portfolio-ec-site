from django import template
from app.models import Order

register = template.Library()


@register.filter
def itemCount(user):
    # ユーザー判定
    if user.is_authenticated:
        order = Order.objects.filter(user=user, ordered=False)
        if order.exists():
            return order[0].items.count()  # 注文があれば注文数をカウント
        return 0
