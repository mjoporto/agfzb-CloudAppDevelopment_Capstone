from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CarModel(models.Model):

    car_choices = (('Sedan', 'Sedan'), ('SUV', "SUV"), ('WAGON', 'WAGON'),
                   ("Coupe", "Coupe"), ("Van", "Van"), ("Pickup", "Pickup"))

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=50)
    car_types = models.CharField(
        max_length=50, choices=car_choices, default=car_choices[1])
    year = models.DateField(default=now)

    def __str__(self):
        return "Name: " + self.name + \
            " Make Name: " + self.make.name + \
            " Type: " + self.car_types + \
            " Dealer ID: " + str(self.dealer_id) + \
            " Year: " + str(self.year)


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, id, dealership, name, purchase, review):
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review

    def set_purchase_details(self, purchase_date, car_make, car_model, car_year):
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review


    