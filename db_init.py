# create and initalize database csv files with dummy/test data

with open("Videos.csv", "w") as v:
    v.write("videoID,name,year,rating,genre,total_stock,current_stock\n")
    v.write('thelegomovie,"The Lego Movie",2014,PG,Action,3,3\n')
    v.write('goodluckhavefundontdie,"Good Luck, Have Fun, Don\'t Die",2025,R,Sci-Fi,1,1\n')

with open("Customers.csv", "w") as c:
    c.write("customerID,first_name,last_name,email,address\n")
    c.write('1,John,Smith,johnsmith@email.com,"123 Generic St, Anywhere, USA 12345"\n')
    c.write('2,Jane,Doe,janedoe@company.org,"456 Some Lane, Somewhere, USA 98765"\n')

with open("RentalHistory.csv", "w") as r:
    r.write("rentalNo,videoID,customerID,rental_start_date,rental_end_date,returned\n")
    r.write('1,thelegomovie,1,"05/12/2016","05/26/2016",True\n')
    r.write('2,goodluckhavefundontdie,2,"10/04/2026","10/18/2016",False\n')
    r.write('3,goodluckhavefundontdie,1,"10/04/2024","10/18/2014",True')