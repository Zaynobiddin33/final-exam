from django.urls import path

from . import views

urlpatterns = [
    #auth
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    #category CRUD
    path('category-list', views.category_list),
    path('category-create', views.category_create),
    path('category-update/<int:id>', views.category_update),
    path('category-delete/<int:id>', views.category_delete),
    #product CRUD
    path('product-list', views.product_list),
    path('product-create', views.product_create),
    path('product-detail/<int:id>', views.product_detail),
    path('product-update/<int:id>', views.product_update),
    path('product-delete/<int:id>', views.product_delete),
    #product_image CRUD
    path('image-create/<int:id>', views.image_create),
    path('image-update/<int:id>', views.image_update),
    path('image-delete/<int:id>', views.image_delete),
    #Cart
    path('cart-create', views.cart_create),
    path('my-cart', views.my_cart_detail),
    path('cart-delete/<int:id>', views.cart_delete),
    #Cart Product
    path('add-to-cart/<int:id>', views.add_to_cart), #create
    path('delete-from-cart/<int:id>', views.delete_from_cart), # request.data.get(quantity) 'all' bo'lganda yoki qiymati product.quantity'dan katta bo'lsa o'chiradi, aks holda qiymatini kamaytiradi. request.data.get(quantity) berilamsa quantity'dan 1 ayiradi
    path('cart-product-detail/<int:id>', views.cart_product_detail), #create
    #order
    path('order-create', views.order_create),
    path('order-detail', views.order_detail),
    path('order-status-update/<int:id>', views.order_status_update),
    path('cancel-order/<int:id>', views.cancel_order)
    
    

]