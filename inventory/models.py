from django.db import models
from django.utils.text import slugify
import uuid
from .validators import validate_thumbnail_size

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='category_thumbnails/', validators=[validate_thumbnail_size])
    seo_meta_title = models.CharField(max_length=70, blank=True, null=True)
    seo_meta_description = models.CharField(max_length=160, blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    additional_seo = models.TextField(blank=True, help_text="Additional SEO code or metadata")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    seo_meta_title = models.CharField(max_length=70, blank=True, null=True)
    seo_meta_description = models.CharField(max_length=160, blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    additional_seo = models.TextField(blank=True, help_text="Additional SEO code or metadata")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (in {self.category.name})"

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    tax = models.FloatField(default=0)
    seo_meta_title = models.CharField(max_length=70, blank=True, null=True)
    seo_meta_description = models.CharField(max_length=160, blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    additional_seo = models.TextField(blank=True, help_text="Additional SEO code or metadata")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
            models.Index(fields=['subcategory']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = self.generate_sku()
        super().save(*args, **kwargs)

    def generate_sku(self):
        return f"SKU-{uuid.uuid4().hex[:8].upper()}"

    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['product']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    is_verified = models.BooleanField(default=False)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

class ProductShipping(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shipping_details')
    shipping_method = models.CharField(max_length=100)
    local_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    regional_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    national_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost_multiply_quantity = models.BooleanField(default=False)
    estimated_delivery_time = models.CharField(max_length=100, blank=True, null=True)
    additional_shipping_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['shipping_method']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return f"Shipping details for {self.product.name} - {self.shipping_method}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False, help_text="Indicates if this is the main image for the product.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['is_main']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return f"Image for {self.product.name} - {'Main' if self.is_main else 'Secondary'}"

class ReviewImage(models.Model):
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='review_photos/', validators=[validate_thumbnail_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['review']),
            models.Index(fields=['uploaded_at']),
        ]

    def __str__(self):
        return f"Image for review of {self.review.product.name} by {self.review.user.username}"

class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('percent', 'Percentage'),
    ]

    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='discounts')
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product_variant']),
            models.Index(fields=['discount_type']),
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        if self.discount_type == 'fixed':
            return f"{self.discount_value} off on {self.product_variant.name}"
        else:
            return f"{self.discount_value}% off on {self.product_variant.name}"

class DiscountHistory(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='history')
    applied_at = models.DateTimeField(auto_now_add=True)
    old_discount_type = models.CharField(max_length=10, choices=Discount.DISCOUNT_TYPE_CHOICES)
    old_discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    new_discount_type = models.CharField(max_length=10, choices=Discount.DISCOUNT_TYPE_CHOICES)
    new_discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['discount']),
            models.Index(fields=['applied_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return f"Discount changed for {self.discount.product_variant.name} on {self.applied_at}"

class PriceHistory(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='price_history')
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    changed_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product_variant']),
            models.Index(fields=['changed_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return f"Price changed for {self.product_variant.name} on {self.changed_at}"

class InventoryTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='inventory_transactions')
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product_variant']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['transaction_date']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def save(self, *args, **kwargs):
        if self.transaction_type == 'IN':
            self.product_variant.stock_quantity += self.quantity
        elif self.transaction_type == 'OUT':
            self.product_variant.stock_quantity -= self.quantity
        self.product_variant.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.product_variant.name} ({self.quantity})"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=[('fixed', 'Fixed'), ('percent', 'Percentage')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, related_name='coupons', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['discount_type']),
            models.Index(fields=['valid_from']),
            models.Index(fields=['valid_to']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return f"Coupon {self.code} - {self.discount_type} {self.discount_value}"

class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='coupon_usages', null=True, blank=True)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['coupon']),
            models.Index(fields=['user']),
            models.Index(fields=['product']),
            models.Index(fields=['used_at']),
        ]

    def __str__(self):
        return f"Coupon {self.coupon.code} used by {self.user.username} on {self.used_at}"
