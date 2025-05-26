# ECサイトポートフォリオ

Django + Bootstrap によるシンプルな EC サイトです。ユーザー登録・商品閲覧・お気に入り機能・商品詳細モーダルなど、基本的な機能を備えています。

---

## 🔧 使用技術

- フレームワーク：Django 4.x
- フロントエンド：HTML / CSS (Bootstrap) / JavaScript / jQuery
- デプロイ：Render
- 認証：django-allauth

---

## 🖥 主な機能

| 機能              | 説明 |
|-------------------|------|
| ユーザー登録・ログイン | `django-allauth` を使った認証機能 |
| 商品一覧表示      | モデルに登録した商品を一覧表示 |
| 商品詳細モーダル   | JavaScriptで商品情報をモーダル表示 |
| お気に入り機能     | AJAX + jQuery による非同期切り替え |
| レスポンシブ対応   | Bootstrap によるスマホ対応 |

---

## 💡 開発で工夫した点（アピールポイント）

- **JavaScriptとjQueryを併用**し、モーダルや非同期更新をスムーズに実装
- **バリデーションの強化**：パスワードに対して正規表現を使い、セキュリティを意識
- **エラー時のユーザー体験向上**：フォームエラーを分かりやすく表示
- **Djangoのベストプラクティス**に基づいたフォルダ構成とクラスベースビュー
- **本番環境でのJavaScript不具合に対応**：ローカルとRender環境の違いに対応

---

## 🚀 デプロイ先（Render）

🔗 https://your-ec-site.onrender.com  
※デモ用アカウント：`demo@example.com` / `demopassword`

---

## 📸 画面イメージ

※ 必要に応じて画像を貼ると好印象です（`img/ss1.png` など）

---

## 📁 セットアップ方法（開発環境）

```bash
# 仮想環境を作成
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# ライブラリをインストール
pip install -r requirements.txt

# マイグレーションと起動
python manage.py migrate
python manage.py runserver