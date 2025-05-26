# ECサイトポートフォリオ

Django + BootstrapによるシンプルなECサイトです。ユーザー登録・商品閲覧・お気に入り機能・商品詳細モーダルなど、基本的な機能を備えています。

サイトURL：https://portfolio-ec-site.onrender.com/

---

## 📝 開発の背景

以前より機械学習(AI開発)分野に興味を持っており、そういった分野の開発にはどういった言語が適しているのだろうか？
と疑問に思い調べる中で、AIプログラミングには下記条件を満たしているPythonが適していることを知りました。
- 開発のしやすさ
- 十分な計算速度
- 安全性
- サービスにあった場所で動く事

そして、私自身扱えるバックエンド言語はPHPしかなかったため、機械学習分野に携わる可能性を考えたことや、自身のスキルを広げるためにも、
Pythonを扱えるようになろうと決意しました。

また、私自身コロナ禍において、直接お店まで買い物に行くことに対して抵抗を感じていた時期があり、Amazonや楽天などのECサイトを利用する場面が増えましたが、その経験からECサイトは生活を快適にしてくれるものという印象を持つことができ、私も誰かの生活を快適・豊かにできるようなものを作ってみたいという思いから、Python + ECサイトでポートフォリオを作成することに決めました。

---

## 🎯 開発の目的

- Pythonを用いたWebサイトの開発経験を積む。
- Pythonのフレームワークの扱いに慣れておく。(Djangoを利用)
- スクラッチ開発によって、Djangoの基本的な構成、動作を知る。
- Python3エンジニア認定実践試験の資格を得た上で実践的なサイトを作成することで、実務ができるスキルが備わっているということを企業にアピールする。

---

## 🔧 使用技術・スペック

- 言語：Python 3.13.3
- フレームワーク：Django 5.2.1
- フロントエンド：HTML5 / CSS3 / Bootstrap 5.3.3 / JavaScript / jQuery
- デプロイ：Render
- 認証：django-allauth
- バージョン管理：GitHub

---

## 🖥 主な機能

| 機能              | 説明 |
|-------------------|------|
| ユーザー登録・ログイン・ログアウト | django-allauthを使った認証機能 |
| ユーザー情報表示 | 登録したユーザー情報の表示と編集 |
| 商品検索  | 商品名、カテゴリー、価格、お気に入りで表示商品をフィルター |
| 商品一覧表示      | モデルに登録した商品を一覧表示 |
| 商品詳細モーダル   | JavaScriptで商品情報をモーダル表示 |
| 商品画像の拡大   | 商品購入画面にて、商品の画像をクリックした際、Bootstrap5のJavaScriptで商品画像を拡大表示 |
| お気に入り機能     | AJAX + jQuery による非同期切り替え |
| ショッピングカート機能     | 商品の削除、購入個数の変更機能 |
| レスポンシブ対応   | Bootstrapによるスマホ対応 |

---

## 💡 開発で工夫した点（アピールポイント）

- **JavaScriptとjQueryを併用**し、モーダルや非同期更新をスムーズに実装
```javascript
// お気に入り切り替え
$(".favorite-button").on("click", function () {
    const $button = $(this);
    const slug = $button.data("slug");
    const isFavorited = $button.data("favorited") === true;
    // AJAXを用い、お気に入り切り替えを非同期で処理
    $.ajax({
        url: `/toggle-favorite/${slug}/`,
        type: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        contentType: "application/json",
        data: JSON.stringify({ favorited: !isFavorited }),
        success: function (response) {
            if (response.is_favorited) {
                $button.html("❤️ お気に入り済み")
                        .removeClass("btn-outline-danger")
                        .addClass("btn-danger")
                        .data("favorited", true);
            } else {
                $button.html("🤍 お気に入り")
                        .removeClass("btn-danger")
                        .addClass("btn-outline-danger")
                        .data("favorited", false);
            }
        },
        error: function () {
            console.error("お気に入りの切り替えに失敗しました");
        }
    });
});
```


- **バリデーションの強化**：パスワードに対して正規表現を使い、セキュリティを意識
- **エラー時のユーザー体験向上**：フォームエラーを分かりやすく表示
- **Djangoのベストプラクティス**に基づいたフォルダ構成とクラスベースビュー
- **本番環境でのJavaScript不具合に対応**：ローカルとRender環境の違いに対応
- **メール送信について**：ローカルとRender環境の違いに対応

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