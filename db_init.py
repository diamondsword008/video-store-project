# create and initalize database csv files with dummy/test data

with open("Videos.csv", "w") as v:
    v.write("videoID,name,year,rating,genre,total_stock,current_stock\n")
    v.write('thelegomovie,"The Lego Movie",2014,PG,Action,3,3\n')
    v.write('goodluckhavefundontdie,"Good Luck, Have Fun, Don\'t Die",2025,R,Sci-Fi,1,1\n')
    v.write('hokum,Hokum,2026,R,Horror,3,3\n')
    v.write('theoutsiders,The Outsiders,1983,PG-13,Drama,2,2\n')
    v.write('theavengers,The Avengers,2012,PG-13,Action,4,4\n')

with open("Customers.csv", "w") as c:
    c.write("customerID,first_name,last_name,email,address\n")
    c.write('1,John,Smith,johnsmith@email.com,"123 Generic St, Anywhere, USA 12345"\n')
    c.write('2,Jane,Doe,janedoe@company.org,"456 Some Lane, Somewhere, USA 98765"\n')
    c.write('3,First,Last,firstlast@example.com,"123 random address"\n')
    c.write('4,Test,Customer,test@customer.org,"456 ambiguous place"\n')

with open("RentalHistory.csv", "w") as r:
    r.write("rentalNo,videoID,customerID,rental_start_date,rental_end_date,returned\n")
    r.write('1,thelegomovie,1,"05/12/2016","05/26/2016",True\n')
    r.write('2,goodluckhavefundontdie,2,"10/04/2026","10/18/2016",False\n')
    r.write('3,goodluckhavefundontdie,1,"10/04/2024","10/18/2014",True\n')
    r.write('4,hokum,1,"10/04/2014","10/18/2014",False\n')
    r.write('5,theoutsiders,1,"10/04/2014","10/18/2014",False\n')
    r.write('6,theavengers,3,"10/04/2014","10/18/2014",True\n')