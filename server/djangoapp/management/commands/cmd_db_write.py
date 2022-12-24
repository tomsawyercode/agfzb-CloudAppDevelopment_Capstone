from django.core.management.base import BaseCommand, CommandError

import datetime

from djangoapp.models import CarMake,CarModel


#python3 manage.py cmd_db_write

#def out(str):
#   self.stdout.write(self.style.SUCCESS(str))

class Command(BaseCommand):
    
    def handle(self, *args, **options):

       clean_data()
       write_Make_Models()  
       print_all()            
       print("Successfully populate")

#----------------------------

def clean_data():
    # Delete all data to start from fresh
    CarMake.objects.all().delete()
    CarModel.objects.all().delete()
    


def write_Make_Models():

    dealerid=11
    make=CarMake(name = "Toyota",description = "Toyota Motor Company of Japan" )
    make.save()
    print("save id",make.id)
    
    mod = CarModel(name="Prius",make=make,  dealerid=dealerid,    type='Sedan', year= datetime.date(1997, 1, 20))
    mod.save()

    mod = CarModel(name="Takoma",make=make,  dealerid=dealerid,    type='Pick Up', year= datetime.date(2000, 1, 20))
    mod.save()

    #---------------------------------------

    make=CarMake(name = "Ford",description = "Ford Motor Company" )
    make.save()
    print("save id",make.id)
    
    mod = CarModel(name="Escape",make=make,  dealerid=dealerid,    type='SUV', year= datetime.date(2010, 1, 20))
    mod.save()

    mod = CarModel(name="F 150",make=make,  dealerid=dealerid,    type='Pick Up', year= datetime.date(2020, 1, 20))
    mod.save()
    
    print("Objects all saved... ")



def print_car():

    # Get related courses
    car = CarModel.objects.get(name__contains='Prius')
    print(car.id)
    print("Car:",car)
    print("Car make:",car.make.name,car.make.description)

    # print reviews ???

def print_all():

    # Get related courses
    for car in CarModel.objects.all():
        print("--------:",car.id)
        print("Car:",car.name,car.year,car.dealerid, car.type)
        print("    make:",car.make.name,car.make.description)






    

