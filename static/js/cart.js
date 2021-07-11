var updateBtns = document.getElementsByClassName("update-cart")

for(var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId', productId, 'action', action )

        console.log("USER: ", user)
        if (user == 'AnonymousUser'){
            addCookiItem(productId, action)
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookiItem(productId, action){
    console.log("User is not authenticated")

    if(action == "add"){
        if(cart[productId] == undefined){
            cart[productId] = {"quantity":1}
        }else{
            cart[productId]["quantity"] +=1
        }
    }
    if(action == "remove"){
        cart[productId]["quantity"] -=1

        //when the quantity becomes 0 remove the item from the cart.
        if(cart[productId]["quantity"]<=0){
            delete cart[productId]
        }
    }
    console.log("Cart:", cart)
    document.cookie = "cart="+JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}


function updateUserOrder(productId, action){
    console.log("user is logged in, sending data...")
    var url = 'update-item'

    fetch(url, {
        method:'POST',
        headers:{
            'content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId':productId, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}