from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=40)
    description = models.CharField(max_length=400)

    def __str__(self):
        return "Make: {}\nDescription: {}"\
            .format(self.name, self.description)

class CarModel(models.Model):
    CAR_TYPES = (
            ("SEDAN", "Sedan"), ("SUV", "SUV"), ("WAGON", "Wagon")
        )

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=40)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=40, choices=CAR_TYPES)
    year = models.DateField()

    def __str__(self):
        return "Make: {}\nName: {}\nDealer ID: {}\nType: {}\nYear: {}"\
            .format(self.make, self.name, self.dealer_id, self.car_type, self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, id, purchase_date=None, car_make=None, car_model=None, car_year=None):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        if purchase_date:
            self.purchase_date = purchase_date
            self.car_make = car_make
            self.car_model = car_model
            self.car_year = car_year
        self.id = id

    def __str__(self):
        return "Reviewer: " + self.name