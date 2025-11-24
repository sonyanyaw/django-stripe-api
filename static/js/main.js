const buyButton = document.getElementById("buy-button");
if (buyButton) {
    buyButton.addEventListener("click", () => {
        console.log("buy button clicked")
        const itemId = buyButton.getAttribute('data-item-id');
        const publicKey = buyButton.getAttribute('data-public-key');
        
        const stripe = Stripe(publicKey);
        fetch(`/buy/${itemId}`)
            .then(res => res.json())
            .then(data => stripe.redirectToCheckout({ sessionId: data.id }))
            .catch(err => console.error(err));
    });
}

const buyOrderButton = document.getElementById("buy-order-button");
if (buyOrderButton) {
    buyOrderButton.addEventListener("click", () => {
        const orderId = buyOrderButton.getAttribute('data-order-id');
        const publicKey = buyOrderButton.getAttribute('data-public-key')

        const stripe = Stripe(publicKey);
        fetch(`/order/${orderId}/buy`)
            .then(res => res.json())
            .then(data => stripe.redirectToCheckout({ sessionId: data.id }))
            .catch(err => console.error(err));
    });
}

// const { actions } = await checkout.loadActions();
// const { total } = actions.getSession();

// // Display the formatted amounts in your UI
// // document.getElementById('order-total').textContent = total.total.amount;
// console.log(actions, total)