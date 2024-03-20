from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers

# Create your views here.

############################## AUTH ###################################

@api_view(["POST"])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username = username, password = password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user = user)
        info = {
            'token': token.key
        }
    else:
        info = {'fatal':'user not found'}
    return Response(info)


@api_view(['POST'])
def register(request):
    username = request.data['username']
    password = request.data['password']
    confirm_password = request.data['confirm_password']
    if models.User.objects.filter(username = username).first():
        return Response({'fatal':'username already exists'})
    elif password == confirm_password:
        user = models.User.objects.create_user(
            username = username,
            password = password
        )
        user_ser = serializers.UserSerializer(user)
        token, _ = Token.objects.get_or_create(user = user)
        data = {
            'token': token.key,
            'user': user_ser.data
        }
        return Response(data)
    else:
        return Response({'fatal':'check the password you wrote'})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'success' : 'logged out succesfully'})


################### CRUD CATEGORY ###################################

@api_view(['GET'])
def category_list(request):
    categories = models.Category.objects.all()
    category_ser = serializers.CategorySerializer(categories, many = True)
    return Response(category_ser.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def  category_create(request):
    name = request.data['name']
    models.Category.objects.create(
        name = name
    )
    return Response({'sucess': "created"})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_update(request, id):
    name = request.data['name']
    category = models.Category.objects.get(id = id)
    category.name = name
    category.save()
    category_ser = serializers.CategorySerializer(category)
    return Response({'success' : 'updated',
                     'updated_to' : category_ser.data})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_delete(request, id):
    category = models.Category.objects.get(id = id).delete()
    return Response({'success' : 'deleted'})


################### CRUD PRODUCT ###################################

@api_view(['GET'])
def product_list(request):
    products = models.Product.objects.filter(quantity__gt = 0)
    product_ser = serializers.ProductSerializerImage(products, many = True)
    return Response({'all products': product_ser.data})

@api_view(['GET'])
def product_detail(request, id):
    product = models.Product.objects.get(id = id)
    product_ser = serializers.ProductSerializerImage(product)
    return Response(product_ser.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_create(request):
    title = request.data['title']
    body = request.data['body']
    price = request.data['price']
    quantity = request.data['quantity']
    category_id = request.data['category_id']
    banner = request.FILES.get('banner')
    category = models.Category.objects.get(id = category_id)
    prod = models.Product.objects.create(
        title = title,
        body = body,
        price = price,
        quantity = quantity,
        banner = banner,
        category = category,
        author = request.user
    )
    product_ser = serializers.ProductSerializer(prod)
    return Response(product_ser.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_update(request, id):
    product = models.Product.objects.get(id = id)
    serializer = serializers.ProductSerializer(product, data=request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response({'updated':'success', 'product':serializer.data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_delete(request, id):
    product = models.Product.objects.get(id = id)
    if product.author == request.user:
        product.delete()
        return Response({'success':'deleted'})
    else:
        return Response({'fatal':'you dont have a permission to delete this product'})
    

######################### CRUD ProductImage ##############################################

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_create(request, id):
    product = models.Product.objects.get(id = id)
    if request.user == product.author:
        l = []
        images = request.data.getlist('image')
        for i in images:
            data = models.ProductImage.objects.create(
                image = i,
                product = product
            )
            data_ser = serializers.ProductImageSerializer(data)
            l.append(data_ser.data)
        return Response(l)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_update(request, id):
    image = models.ProductImage.objects.get(id = id)
    image.image = request.FILES['image']
    image.save()
    image_ser = serializers.ProductImageSerializer(image)
    return Response({'success':'edited','updated_image':image_ser.data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_update(request, id):
    image = models.ProductImage.objects.get(id = id)
    image.image = request.FILES['image']
    image.save()
    image_ser = serializers.ProductImageSerializer(image)
    return Response({'success':'edited','updated_image':image_ser.data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_delete(request, id):
    models.ProductImage.objects.get(id = id).delete()
    return Response({'success':'deleted'})

###################################### CRUD CART #######################################

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_create(request):
    user = request.user
    if not models.Cart.objects.filter(user = user, is_active = True).first():
        cart = models.Cart.objects.create(
            user = user,
            is_active = True
        )
        cart_ser = serializers.CartSerializer(cart)
        return Response({'success':'created', 'data':cart_ser.data})
    else:
        data = models.Cart.objects.get(user = user, is_active = True)
        serializer = serializers.CartSerializer(data)
        return Response({'fatal':'you already have active cart', 'data':serializer.data})
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_delete(request, id):
    models.Cart.objects.get(id = id, user = request.user).delete()
    return Response({'success':'deleted'})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_cart_detail(request):
    cart = models.Cart.objects.get(user = request.user, is_active = True)
    serializer = serializers.CartSerializerGet(cart)
    return Response(serializer.data)

################################## Cart Product ########################################

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request, id):
    if request.data.get('quantity'):
        quantity = int(request.data.get('quantity'))
    else:
        quantity = 1
    product = models.Product.objects.get(id = id)
    cart, _ = models.Cart.objects.get_or_create(user = request.user, is_active = True)
    cartproduct = models.CartProduct.objects.filter(cart = cart, product = product).first()
    if cartproduct:
        cartproduct.quantity += quantity
        cartproduct.save()
    else:
        cartproduct = models.CartProduct.objects.create(
            cart = cart,
            product = product,
            quantity = quantity
        )
    serializer = serializers.CartProductSerializer(cartproduct)
    return Response({'success':'created', 'data': serializer.data})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_from_cart(request, id):
    cart_product = models.CartProduct.objects.get(id = id)
    quantity = 1
    if request.data.get('quantity'):
        if request.data.get('quantity') == 'all':
            cart_product.delete()
            return Response({'success':'deleted'})
        
        elif int(request.data.get('quantity')) >= cart_product.quantity:
            cart_product.delete()
            return Response({'success':'deleted'})
        
        else:
            quantity = int(request.data.get('quantity'))

    elif quantity == cart_product.quantity:
        cart_product.delete()
        return Response({'success':'deleted'})

    cart_product.quantity -= quantity
    cart_product.save()
    serializer = serializers.CartProductSerializer(cart_product)
    return Response({'success': f'quantity reduced by {quantity}', 'cart_product' : serializer.data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_product_detail(request, id):
    cart_product = models.CartProduct.objects.get(id = id)
    serializer = serializers.CartProductSerializer(cart_product)
    return Response(serializer.data)


############################ ORDER ########################################

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_create(request):
    address = request.data['address']
    try:
        cart = models.Cart.objects.get(user = request.user, is_active = True)
    except:
        return Response({'fatal':'you dont have active carts'})
    cart.is_active = False
    cart.save()
    products = models.CartProduct.objects.filter(cart = cart)
    info = []
    for product in products:
        data = models.Order.objects.create(
            user = request.user,
            cart_product = product,
            address = address,
            status = 1
        )
        info.append(serializers.OrderSerializer(data).data)
    return Response({'success':'ordered', 'orders':info})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_detail(request):
    orders = models.Order.objects.filter(user = request.user)
    serializer = serializers.OrderSerializer(orders, many = True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_status_update(request, id):
    """the function is for changing status of the product and using the url of 
        this view function does this. Sending the good is done by owner of the product,
        and recieving or returning is done by order user 
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Bu funksiya order'ning statusini o'zgartirish uchun ishlatiladi va url dan foydalanishni o'zi shu ishni
        bajaradi. Maxsulot sotuvchisi ushbu urldan status = 1 bo'lganda foydalansa status 2ga ya'ni 'jo'natilidi'ga o'zgaradi. Status 2 yoki
        3ligida order.user foydalansa, 'qabul qildim' yoki 'qaytarildi' ga o'zgaradi"""
    user = request.user
    order = models.Order.objects.get(id = id)
    if order.status == 1 and order.cart_product.product.author == user: #only product owner can change the status from 'pending' to 'sent'
        order.status = 2
        order.save()
        return Response({'success':'product sent'})
    elif order.status == 2 and order.user == user: #only order user can change the status from 'sent' to 'recieved'
        order.status = 3
        order.save()
        return Response({'congrats':'you recieved the product'})
    elif order.status == 3 and order.user == user:  #only order user can change the status from 'recieved' to 'returned'
        order.status = 2
        order.status = 4
        order.save()
        return Response({'detail':'you return the the good'})
    else:
        return Response({'error':'currently you cannot change the status of the order'})
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cancel_order(request, id):
    try:
        order = models.Order.objects.get(id = id)
        if order.user == request.user:
            if order.status == 1:
                order.delete()
                return Response({'success':'you cancelled the order'})
            elif order.status == 2:
                return Response({'detail':'you cannot cancel the order, because it is already sent'})
            elif order.status == 3:
                return Response({'detail':'you cannot cancel the order, because you have taken it'})
        else:
            return Response({'detail':'you cannot cancel the order, because you are not the user that ordered'})
    except:
        return Response({'detail':'order not found'})