from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(null=True, max_length=30)
    description = models.CharField(null=True, max_length=200)
    # - Any other fields you would like to include in car make model
    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.description

class CarModel(models.Model):
    # - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=30)
    dealer_id = models.IntegerField(default=0)
    SALOON = 'Saloon'
    SUV = 'SUV'
    CAMPER_VAN = 'Camper Van'
    CONVERTIBLE = 'Convertible'
    TYPE_CHOICES = [
        (SALOON, 'Saloon'),
        (SUV, 'SUV'),
        (CAMPER_VAN, 'Camper Van'),
        (CONVERTIBLE, 'Convertible')
    ]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SUV
    )
    year = models.DateField(null=True)
    # - Any other fields you would like to include in car model
    def __str__(self):
        return "Type: " + self.type + "," \
        "Name: " + self.name

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip, state):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
        self.state = state
    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
    def __str__(self):
        return "Dealer name: " + self.review