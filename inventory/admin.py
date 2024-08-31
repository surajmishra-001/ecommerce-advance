from django.contrib import admin
from .models import (
    Category, Subcategory, Product, ProductVariant, ProductReview,
    ProductShipping, ProductImage, ReviewImage, Discount, DiscountHistory,
    PriceHistory, InventoryTransaction, Coupon, CouponUsage
)

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1

class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 1

class InventoryTransactionInline(admin.TabularInline):
    model = InventoryTransaction
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'seo_meta_title', 'created_at')
    search_fields = ('name', 'slug', 'description')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'thumbnail')}),
        ('SEO', {'fields': ('seo_meta_title', 'seo_meta_description', 'seo_meta_keywords', 'additional_seo')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'description', 'seo_meta_title', 'created_at')
    search_fields = ('name', 'slug', 'description')
    list_filter = ('category', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('category', 'name', 'slug', 'description')}),
        ('SEO', {'fields': ('seo_meta_title', 'seo_meta_description', 'seo_meta_keywords', 'additional_seo')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sku', 'category', 'subcategory', 'stock_quantity', 'tax', 'created_at')
    search_fields = ('name', 'slug', 'sku', 'description')
    list_filter = ('category', 'subcategory', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline, ProductReviewInline, ProductImageInline]
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'sku', 'description', 'category', 'subcategory', 'stock_quantity', 'tax')}),
        ('SEO', {'fields': ('seo_meta_title', 'seo_meta_description', 'seo_meta_keywords', 'additional_seo')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'sku', 'price', 'stock_quantity', 'created_at')
    search_fields = ('product__name', 'name', 'sku')
    list_filter = ('product', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('product', 'name', 'sku', 'price', 'stock_quantity')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_verified', 'created_at')
    search_fields = ('product__name', 'user__username', 'rating')
    list_filter = ('product', 'rating', 'is_verified', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('product', 'user', 'rating', 'is_verified', 'comment')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

class ProductShippingAdmin(admin.ModelAdmin):
    list_display = ('product', 'shipping_method', 'local_shipping_cost', 'regional_shipping_cost', 'national_shipping_cost', 'created_at')
    search_fields = ('product__name', 'shipping_method')
    list_filter = ('product', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('product', 'shipping_method', 'local_shipping_cost', 'regional_shipping_cost', 'national_shipping_cost', 'shipping_cost_multiply_quantity', 'estimated_delivery_time', 'additional_shipping_info')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main', 'created_at')
    search_fields = ('product__name', 'is_main')
    list_filter = ('product', 'is_main', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('product', 'image', 'is_main')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review', 'uploaded_at')
    search_fields = ('review__product__name', 'review__user__username')
    list_filter = ('review', 'uploaded_at')
    fieldsets = (
        (None, {'fields': ('review', 'image')}),
        ('Dates', {'fields': ('uploaded_at',)}),
    )
    readonly_fields = ('uploaded_at',)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'discount_type', 'discount_value', 'start_date', 'end_date', 'created_at')
    search_fields = ('product_variant__name', 'discount_type', 'discount_value')
    list_filter = ('product_variant', 'discount_type', 'start_date', 'end_date', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('product_variant', 'discount_type', 'discount_value', 'start_date', 'end_date')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

class DiscountHistoryAdmin(admin.ModelAdmin):
    list_display = ('discount', 'old_discount_type', 'old_discount_value', 'new_discount_type', 'new_discount_value', 'created_at', 'updated_at')
    search_fields = ('discount__code', 'old_discount_type', 'new_discount_type')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('applied_at', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('discount', 'old_discount_type', 'old_discount_value', 'new_discount_type', 'new_discount_value')
        }),
        ('Dates', {
            'fields': ('applied_at', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'old_price', 'new_price', 'changed_at', 'created_at', 'updated_at')
    search_fields = ('product_variant__product__name', 'old_price', 'new_price')
    list_filter = ('changed_at', 'created_at', 'updated_at')
    readonly_fields = ('changed_at', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('product_variant', 'old_price', 'new_price')
        }),
        ('Dates', {
            'fields': ('changed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'transaction_type', 'quantity', 'description', 'created_at', 'updated_at')
    search_fields = ('product_variant__product__name', 'transaction_type', 'description')
    list_filter = ('transaction_type', 'created_at', 'updated_at')
    readonly_fields = ('transaction_date', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('product_variant', 'transaction_type', 'quantity', 'description')
        }),
        ('Dates', {
            'fields': ('transaction_date', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'active', 'created_at')
    search_fields = ('code', 'discount_type', 'discount_value')
    list_filter = ('discount_type', 'valid_from', 'valid_to', 'active', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'active')}),
        ('Products', {'fields': ('products',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user', 'product', 'used_at')
    search_fields = ('coupon__code', 'user__username', 'product__name')
    list_filter = ('coupon', 'user', 'product', 'used_at')
    fieldsets = (
        (None, {'fields': ('coupon', 'user', 'product')}),
        ('Dates', {'fields': ('used_at',)}),
    )
    readonly_fields = ('used_at',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ProductShipping, ProductShippingAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ReviewImage, ReviewImageAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(DiscountHistory, DiscountHistoryAdmin)
admin.site.register(PriceHistory, PriceHistoryAdmin)
admin.site.register(InventoryTransaction, InventoryTransactionAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponUsage, CouponUsageAdmin)
