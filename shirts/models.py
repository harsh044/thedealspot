from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
# Create your models here.

from store.supabase_storage import SupabaseStorage
image_storage = SupabaseStorage(
    bucket_name="product-images"
)

video_storage = SupabaseStorage(
    bucket_name="product-videos"
)

class TheDealSpot(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = AutoSlugField(populate_from='name', unique=True, null=False, default="")
    desc = models.CharField(max_length=1000, null=True)
    discount = models.IntegerField()
    image1 = models.ImageField(storage=image_storage,upload_to="products/", null=False)
    image2 = models.ImageField(storage=image_storage,upload_to="products/", null=False)
    image3 = models.ImageField(storage=image_storage,upload_to="products/", null=True, blank=True)
    image4 = models.ImageField(storage=image_storage,upload_to="products/", null=True, blank=True)
    # Product video
    video = models.FileField(storage=video_storage,upload_to="products/", null=True, blank=True)
    affilate_url = models.URLField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    
class Sizevariant(models.Model):
    SIZES = (
        ('S', "Small"),
        ('M', "Medium"),
        ('L', "Large"),
        ('XL', "Extra Large"),
        ('XXL', "Extra Extra Large"),
    )
    price = models.IntegerField(null=False)
    tshirt = models.ForeignKey(TheDealSpot, on_delete=models.CASCADE)
    size = models.CharField(choices=SIZES, max_length=5)


