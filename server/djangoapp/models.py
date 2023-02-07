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


# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
