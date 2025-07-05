from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    price = models.FloatField(default=0.0)
    category = models.CharField(max_length=50, default='All')
    subcategory = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to="shop/images", default='')
    pub_date = models.DateField()

    def __str__(self):
        return self.product_name
