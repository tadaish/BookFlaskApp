var number_input = document.getElementById('quantity')

var quantity = parseInt(number_input.value)


number_input.addEventListener('input', (e) => {
    var input_value = e.target.value
    quantity = parseInt(input_value)
})

function addToCart(id, title, price, image) {
    fetch("/api/carts", {
       method: "post",
       body: JSON.stringify({
            "id": id,
            "title": title,
            "price": price,
            'quantity': quantity,
            'image': image
       }),
       headers: {
            "Content-Type": "application/json"
       }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName("cart-counter");
        for (let e of d)
            e.innerText = data.total_quantity;
    })
}


function updateCart(bookId, obj) {
    fetch(`/api/cart/${bookId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": parseInt(obj.value)
        }),
        headers: {
            "Content-Type": "application/json"
       }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName("cart-counter");
        for (let e of d)
            e.innerText = data.total_quantity;

        let d2 = document.getElementsByClassName("cart-amount");
        for (let e of d2)
            e.innerText = data.total_amount.toLocaleString("en");
    });
}

function deleteCart(bookId) {
    if (confirm("Bạn chắc chắn xóa sản phẩm khỏi giỏ?") === true) {
        fetch(`/api/cart/${bookId}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            let d = document.getElementsByClassName("cart-counter");
            for (let e of d)
                e.innerText = data.total_quantity;

            let d2 = document.getElementsByClassName("cart-amount");
            for (let e of d2)
                e.innerText = data.total_amount.toLocaleString("en");

            location.reload()
        });
    }
}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán?") === true) {
        fetch("/api/pay", {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.status === 200)
            {
                 const myModal = new bootstrap.Modal(document.getElementById("successModal")).show();
                 const modal = document.getElementById('successModal');
                 modal.addEventListener('hidden.bs.modal', event => {
                      location.href ='/';
                 })

            }

            else
                alert("Something wrong!");
        })
    }
}
