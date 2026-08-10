document.addEventListener("DOMContentLoaded", function () {
    var stripe = Stripe(window.STRIPE_PUBLISHABLE_KEY);
    var button = document.getElementById("buy-button");
    if (!button) {return;}
    button.addEventListener("click", function () {
        var itemId = button.dataset.itemId;
        fetch("/buy/" + itemId + "/").then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data.session_id) {
                    return stripe.redirectToCheckout({ sessionId: data.session_id });
                }
            })
            .catch(function (error) {
                console.error("Something failed:", error);
            });
});
});
