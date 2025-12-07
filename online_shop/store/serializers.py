from statistics import quantiles

from .models import *
from  rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'username','age',  'password',  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_image', 'category_name']


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id','sub_category_name', ]





class CategoryDetailSerializer(serializers.ModelSerializer):
    category_sub = SubCategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name','category_sub']



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields ='__all__'

class ProductListSerializer(serializers.ModelSerializer):
    create_date = serializers.DateField(format='%d-%m-%y')
    product_images = ProductImageSerializer(read_only=True, many=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'product_images', 'price', 'product_type',
            'avg_rating', 'count_people', 'create_date'
        ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()  # или ваша логика

    def get_count_people(self, obj):
        return obj.get_count_people()  # или ваша логика



class SubCategoryDetailSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True, many=True)

    class Meta:
        model = SubCategory
        fields = ['id','sub_category_name', 'product']


class ReviewSerializer(serializers.ModelSerializer):
    create_date = serializers.DateField(format='%d-%m-%y')
    user = UserProfileSerializer()


    class Meta:
        model = Review
        fields = ['user', 'text', 'stars', 'create_date']


class ProductDetailSerializer(serializers.ModelSerializer):
    create_date = serializers.DateField(format='%d-%m-%y')
    product_images = ProductImageSerializer(read_only=True, many=True)
    subcategory = SubCategoryDetailSerializer()
    product_reviews = ReviewSerializer(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_peaple = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields =['product_name', 'subcategory','price','article_number','video','product_images',
                 'description','product_type', 'create_date','get_avg_rating','get_count_peaple',
                 'product_reviews']

        def get_avg_rating(self, obj):
            return obj.get_avg_rating()

        def get_count_peaple(self, obj):
            return obj.get_count_peaple()






class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True,
                                                    source='product')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity','total_price' ]


    def get_total_price(self, obj):
        return  obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items','total_price']

    def get_total_price(self, obj):
        return  obj.get_total_price()



class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )

    class Meta:
        model = FavoriteItem
        fields = ['id', 'product', 'product_id']


class FavoriteSerializer(serializers.ModelSerializer):
    items = FavoriteItemSerializer(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'items']