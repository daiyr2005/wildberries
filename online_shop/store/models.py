
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField



class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                                       MaxValueValidator(60)],
                                           null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    STATUS_CHOICES = (
       ('gold', 'gold'),#75%
       ('silver', 'silver'), #50%
       ('bronze', 'bronze'),#25%
       ('simple', 'simple')#0
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='simple')
    date_registered = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.first_name}, {self.last_name}'




class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True)
    category_image = models.ImageField(upload_to='cat_image')

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.sub_category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    article_number = models.PositiveBigIntegerField(unique=True)
    video = models.FileField(upload_to='product_videos')
    description = models.TextField()
    product_type = models.BooleanField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    def get_avg_rating(self):
        review = self.product_reviews.all()
        if review.exists():
            return sum([i.stars for i in review ]) / review.count()
        return 0

    def get_count_people(self):
        return self.product_reviews.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f'{self.product}, {self.image}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    text = models.TextField()
    stars = models.PositiveBigIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    create_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}, {self.product}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return sum([i.get_total_price() for i in self.items.all()])


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f'{self.product},{self.quantity}'

    def get_total_price(self):
        return self.quantity * self.product.price


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'Избранное {self.user.username}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def str(self):
        return f'{self.product.product_name}'


# Create your models here.
