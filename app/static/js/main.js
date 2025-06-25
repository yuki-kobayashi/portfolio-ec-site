document.addEventListener('DOMContentLoaded', function() {
    var productDetailButtons = document.querySelectorAll('.product-detail-button');
    // 各商品のボタン要素を取得
    productDetailButtons.forEach(function(button) {
        // 商品詳細ボタンクリックで発火
        button.addEventListener('click', function(event) {
            // モーダル用のデータを取得
            var title = button.getAttribute('data-title');
            var category = button.getAttribute('data-category');
            var price = button.getAttribute('data-price');
            var description = button.getAttribute('data-description');
            var image = button.getAttribute('data-image');
            // モーダルの要素を取得
            var modalTitle = document.querySelector('#modalTitle');
            var modalCategory = document.querySelector('#modalCategory');
            var modalPrice = document.querySelector('#modalPrice');
            var modalDescription = document.querySelector('#modalDescription');
            var modalImage = document.querySelector('#modalImage');
            // モーダルにデータをセット
            modalTitle.textContent = title;
            modalCategory.textContent = category;
            modalPrice.textContent = price;
            modalDescription.textContent = description;
            modalImage.src = image;
        });
    });

    // 画像モーダル表示
    $(document).ready(function() {
        // 画像クリックで発火
        $('#productImage').on('click', function() {
            // クリックした画像のURLを取得
            var imageUrl = $(this).data('image');
            // モーダルに画像をセット
            $('#expandedImage').attr('src', imageUrl);
        });
    });

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

    // パスワード表示・非表示の切り替え
    const passwordToggles = document.querySelectorAll('.password-toggle');
    // パスワード入力欄が二つあるためループを入れる
    passwordToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            const icon = toggle.querySelector('i');
            const inputId = toggle.getAttribute('data-target');
            const input = document.getElementById(inputId);
            if (input) {
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    input.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        });
    });

    // CSRFトークン取得
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});