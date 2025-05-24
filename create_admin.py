import os
import django

# 環境変数でDjangoの設定ファイルを指定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Djangoを初期化
django.setup()

# カスタムユーザーモデルの取得
from django.contrib.auth import get_user_model

User = get_user_model()

# 存在しない場合だけスーパーユーザーを作成
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "password")