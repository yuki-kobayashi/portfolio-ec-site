from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import JsonResponse
from accounts.models import CustomUser
from .serializers import PaymentSerializer
from .models import Item, OrderItem, Order, Payment, CarouselTitle, Favorite


class IndexView(View):
    def get(self, request, *args, **kwargs):
        # 商品一覧用のデータ
        item_data = list(Item.objects.all())
        # カルーセル表示用のデータ
        carousel_data = Item.objects.filter(category="お菓子")
        carousel_title = CarouselTitle.objects.first()
        # 検索フォーム用のデータ
        categories = Item.objects.values("category").distinct()
        
        # お気に入り商品のデータ
        favorite_items = []
        if request.user.is_authenticated:
            favorite_items = Favorite.objects.filter(user=request.user).values_list("item__id", flat=True)
        # 各アイテムに is_favorited 属性を追加
        for item in item_data:
            item.is_favorited = item.id in favorite_items
            item.price_type = type(item.price).__name__

        context = {
            "item_data": item_data,

            "carousel_data": carousel_data,
            "carousel_title": carousel_title,
            "categories": categories,
            "favorite_items": favorite_items,
        }
        return render(request, "app/index.html", context)


class ItemDetailView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.get(slug=self.kwargs["slug"])
        is_favorited = False
        if request.user.is_authenticated:
            is_favorited = Favorite.objects.filter(user=request.user, item=item_data).exists()

        item_data.is_favorited = is_favorited

        context = {
            "item_data": item_data
        }
        return render(request, "app/product.html", context)


@login_required  # ログインしている時のみコール
def add_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # 注文データが存在している場合はデータ取得、存在していなければ作成
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False
    )
    order = Order.objects.filter(user=request.user, ordered=False)

    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)

    return redirect("order")


class OrderView(LoginRequiredMixin, View):
    # 注文データが存在しない場合、app/order.htmlにリダイレクト
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {"order": order}
            return render(request, "app/order.html", context)
        except ObjectDoesNotExist:
            return render(request, "app/order.html")


@login_required
def remove_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(user=request.user, ordered=False)
    # 注文情報の存在チェック
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            # 最新の注文情報を取得
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            # 注文情報が存在していたら削除
            order_item.delete()
            return redirect("order")
    # 注文情報が無ければ商品ページにリダイレクト
    return redirect("product", slug=slug)


@login_required
def remove_single_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            # 個数を減らす商品が1つの場合は削除
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            return redirect("order")
    return redirect("product", slug=slug)


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user_data = CustomUser.objects.get(id=request.user.id)
        context = {"order": order, "user_data": user_data}
        return render(request, "app/payment.html", context)

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user_data = CustomUser.objects.get(id=request.user.id)
        order_items = order.items.all()
        amount = order.get_total()

        # 支払い処理
        payment = Payment(user=request.user)
        payment.stripe_charge_id = "test_stripe_charge_id"
        payment.amount = amount
        payment.save()

        # 注文確定処理
        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.ordered = True
        order.payment = payment
        order.save()

        # 注文確定メールの送信
        # ※Gmailを利用したメール送信の実装を試みたが、どうしてもセキュリティで弾かれてしまうため、
        # Djangoのコンソールメールバックエンドを用い、メールの内容を確認するに留める。
        # (恐らくメール送信を許可するためのアプリパスワードの設定が上手くいっていない。)
        subject = "ご注文が確定しました"
        message = (
            f"{user_data.first_name} {user_data.last_name} 様\n\n"
            "この度はご注文いただきありがとうございます。\n"
            "以下の内容で注文が確定しました。\n\n"
            "【注文内容】\n"
        )
        for item in order_items:
            message += f"- {item.item.title}：{item.item.price}円\n"

        message += f"\n合計金額: {amount}円\n\n"
        message += "またのご利用をお待ちしております。\n"
        message += "ECサイト運営チーム"

        send_mail(
            subject,
            message,
            from_email="no-reply@example.com",
            recipient_list=["user@example.com"],
            fail_silently=False,
        )

        return redirect("thanks")


class ThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "app/thanks.html")


class SearchView(View):
    def get(self, request, *args, **kwargs):
        category = request.GET.get("category", "")
        min_price = request.GET.get("min_price", "")
        max_price = request.GET.get("max_price", "")
        keyword = request.GET.get("keyword", "")
        only_favorites = request.GET.get("only_favorites", "")

        # 商品をフィルタリング
        search_item_data = Item.objects.all()

        if category:
            search_item_data = search_item_data.filter(category=category)

        if min_price:
            search_item_data = search_item_data.filter(price__gte=min_price)

        if max_price:
            search_item_data = search_item_data.filter(price__lte=max_price)

        if keyword:
            search_item_data = search_item_data.filter(title__icontains=keyword)
        
        if only_favorites == "on" and request.user.is_authenticated:
            favorite_item_ids = Favorite.objects.filter(user=request.user).values_list("item_id", flat=True)
            search_item_data = search_item_data.filter(id__in=favorite_item_ids)

        context = {
            "search_item_data": search_item_data,
            "categories": Item.objects.values("category").distinct(),
        }
        return render(request, "app/search.html", context)


# お気に入りボタン処理
@login_required
def toggle_favorite(request, slug):
    item = get_object_or_404(Item, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)

    if not created:
        # すでにお気に入りに登録されていたら削除
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True

    return JsonResponse({'is_favorited': is_favorited})
