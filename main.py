#
# header comment! Overview, name, etc.
#

import sqlite3
import matplotlib.pyplot as plt


###############################
# Command One Function:
# Asks for partial station name and retrieves the stations that are
# like the users input.
# Outputs Station_ID: Station_Name in ASC Order
def command_1(dbCursor):
    # command_1
    print()
    name = input("Enter partial station name (wildcards _ and %): ")

    sql = """Select Station_ID, Station_Name
           from Stations
           where Station_Name like ?
           order by Station_Name"""
    dbCursor.execute(sql, (f"{name}",))

    rows = dbCursor.fetchall();

    # display results
    if not rows:
        print("**No stations found...")
    # row[0](Station_ID), row[1](Station_Name)
    for row in rows:
        print(row[0], ":", row[1])


###############################
# Command Two Function:
# Prints the ridership of all stations in order of station_name
# and outputs the percentage
# Outputs Station_Name:Num_Riders (%) in ASC Order
def command_2(dbCursor):
    # command_2
    print("** ridership all stations **");

    # Grabs total ridership number
    dbCursor.execute("Select sum(Num_Riders) From Ridership;")
    total = dbCursor.fetchone();

    sql = """Select Station_Name, sum(Num_Riders) from Stations
           join Ridership on Stations.Station_ID = Ridership.Station_ID
           group by Stations.Station_ID
           order by Station_Name"""
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()

    # row[0](station_name), row[1](ridership), %
    for row in rows:
        print(row[0], ":", f"{row[1]:,}", f"({(row[1] / total[0] * 100):.2f}%)")


###############################
# Command Three Function:
# Outputs the 10 busiest stations in terms of ridership
# in descending order by ridership
# Outputs Station_Name:Num_Riders (%) in DESC Order
def command_3(dbCursor):
    # command_3
    print("** top-10 stations **");

    # Grabs total ridership number
    dbCursor.execute("Select sum(Num_Riders) From Ridership;")
    total = dbCursor.fetchone();

    sql = """Select Station_Name, sum(Num_Riders) from Stations
           join Ridership on Stations.Station_ID = Ridership.Station_ID
           group by Stations.Station_ID
           order by sum(Num_Riders) DESC
           limit 10"""
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()

    # row[0](station_name), row[1](ridership), %
    for row in rows:
        print(row[0], ":", f"{row[1]:,}", f"({(row[1] / total[0] * 100):.2f}%)")


################################
# Command Four Function:
# Outputs the 10 lest busiest stations in terms of ridership
# in ascending order by riderhsip
# Outputs Station_Name:Num_Riders (%) in ASC Order
def command_4(dbCursor):
    # command_4
    print("** least-10 stations **");

    # Grabs total ridership number
    dbCursor.execute("Select sum(Num_Riders) From Ridership;")
    total = dbCursor.fetchone();

    sql = """Select Station_Name, sum(Num_Riders) from Stations
           join Ridership on Stations.Station_ID = Ridership.Station_ID
           group by Stations.Station_ID
           order by sum(Num_Riders)
           limit 10"""
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()

    # row[0](station_name), row[1](ridership), %
    for row in rows:
        print(row[0], ":", f"{row[1]:,}", f"({(row[1] / total[0] * 100):.2f}%)")


################################
# Command Five Function:
# Asks for color and outputs all stop names that are
# part of the line in ascending order, states if line does not exist
# Outputs Stop_Name:Direction Accesible in ASC Order
def command_5(dbCursor):
    # command_5
    print()
    # Grabs color input and puts into right format
    color = input("Enter a line color (e.g. Red or Yellow): ").capitalize()
    if color == "Purple-express":
        color = "Purple-Express"

    sql = """Select Stop_Name, Direction, ADA from Stops
           join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
           join Lines on StopDetails.Line_ID = Lines.Line_ID
           where color = ?
           order by Stop_Name"""
    dbCursor.execute(sql, (f"{color}",))
    rows = dbCursor.fetchall()

    if not rows:
        print("**No such line...")
    # row[0](stop )
    for row in rows:
        if (row[2] == 1):
            print(row[0], ":", f"direction = {row[1]:s}", "(accessible? yes)")
        else:
            print(row[0], ":", f"direction = {row[1]:s}", "(accessible? no)")


################################
# Command Six Function:
# Outputs total ridership by month in ascending order by month
# Gives user option to plot the data
# Outputs Month:Ridership in ASC Order
def command_6(dbCursor):
    # command_6
    print("** ridership by month **");

    sql = """Select strftime('%m',Ride_Date), sum(Num_Riders) from Ridership
         group by strftime('%m',Ride_Date)
         order by strftime('%m',Ride_Date)"""
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()

    # row[0](month), row[1](Num_Riders)
    for row in rows:
        print(row[0], ":", f"{row[1]:,}")

    print()
    ans = input("Plot? (y/n) ")

    # plots if user responds yes
    if ans == "y":
        x = []
        y = []

        for row in rows:
            x.append(row[0])
            y.append(row[1])

        plt.xlabel("month")
        plt.ylabel("number of riders(x*10^8)")
        plt.title("monthly ridership")

        plt.ioff()
        plt.plot(x, y)
        plt.show()


################################
# Command Seven Function:
# Outputs total ridership by yearh in ascending order by year
# Gives user option to plot the data
# Outputs Year:Ridership in ASC Order
def command_7(dbCursor):
    # command_7
    print("** ridership by year **");

    sql = """Select strftime('%Y',Ride_Date), sum(Num_Riders) from Ridership
         group by strftime('%Y',Ride_Date)
         order by strftime('%Y',Ride_Date)"""
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()

    # row[0](year), row[1](Num_Riders)
    for row in rows:
        print(row[0], ":", f"{row[1]:,}")

    print()
    ans = input("Plot? (y/n) ")

    # plots if user responds yes
    if ans == "y":
        x = []
        y = []

        for row in rows:
            x.append(row[0])
            y.append(row[1])

        plt.xlabel("year")
        plt.ylabel("number of riders(x*10^8)")
        plt.title("yearly ridership")

        plt.ioff()
        plt.plot(x, y)
        plt.show()


################################
# Command Eight Function:
# Asks user for year and two stations, then outputs the daily ridership
# at each station, and gives user the option to plot it
# Outputs Date:Ridership in ASC Order
def command_8(dbCursor):
    # command_8
    print()
    year = input("Year to compare against? ")
    print()
    wildcardOne = input("Enter station 1 (wildcards _ and %): ")

    sql = """Select date(Ride_Date), sum(Num_Riders), 
          Stations.Station_ID, Stations.Station_Name, 
          count(Stations.Station_ID) 
          from Ridership
          join Stations on Ridership.Station_ID = Stations.Station_ID
          where strftime('%Y',Ride_Date) = ?
          and Station_Name like ?
          group by date(Ride_Date)"""
    dbCursor.execute(sql, (f"{year}", f"{wildcardOne}"))
    rows1 = dbCursor.fetchall();
    # rows1 = first stations
    if not rows1:
        print("**No station found...")
        return 0
    if rows1[0][4] > 1:
        print("**Multiple stations found...")
        return 0

    print()
    wildcardTwo = input("Enter station 2 (wildcards _ and %): ")
    dbCursor.execute(sql, (f"{year}", f"{wildcardTwo}"))
    rows2 = dbCursor.fetchall();
    # rows2 = second station

    if not rows2:
        print("**No station found...")
        return 0
    if rows2[0][4] > 1:
        print("**Multiple stations found...")
        return 0

    print("Station 1:", rows1[0][2], rows1[0][3])
    for row in range(5):
        print(rows1[row][0], rows1[row][1])
    for row in range(len(rows1) - 5, len(rows1)):
        print(rows1[row][0], rows1[row][1])

    print("Station 2:", rows2[0][2], rows2[0][3])
    for row in range(5):
        print(rows2[row][0], rows2[row][1])
    for row in range(len(rows1) - 5, len(rows2)):
        print(rows2[row][0], rows2[row][1])

    print()
    ans = input("Plot? (y/n) ")

    # plots if user responds yes
    if ans == "y":
        x = []
        y1 = []
        y2 = []
        day = 1

        for row in rows1:
            x.append(day)
            y1.append(row[1])
            day = day + 1
        for row in rows2:
            y2.append(row[1])

        plt.xlabel("day")
        plt.ylabel("number of riders")
        plt.title("riders each day of " + year)

        plt.ioff()
        plt.plot(x, y1, label=rows1[0][3])
        plt.plot(x, y2, label=rows2[0][3])
        plt.legend()
        plt.show()


################################
# Command Nine Function:
# Asks user for line color, then outputs all station names and lattitude
# and longitude with that color, and gives user the option to plot it
# Outputs Date:Ridership in ASC Order
def command_9(dbCursor):
    # command_9

    # Grabs color input and puts into right format
    print()
    color = input("Enter a line color (e.g. Red or Yellow): ").capitalize()
    if color == "Purple-express":
        color = "Purple-Express"

    sql = """Select distinct Station_Name, 
           Stops.Latitude, Stops.Longitude from Stations
           join Stops on Stations.Station_ID = Stops.Station_ID
           join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
           join Lines on StopDetails.Line_ID = Lines.Line_ID
           where color = ?
           order by Station_Name"""
    dbCursor.execute(sql, (f"{color}",))
    rows = dbCursor.fetchall()

    if not rows:
        print("**No such line...")
        return 0

    for row in rows:
        print(row[0], ":", f"({row[1]:,},", f"{row[2]:,})")

    print()
    ans = input("Plot? (y/n) ")

    # plots if user responds yes
    if ans == "y":
        #
        # populate x and y lists with (x, y) coordinates --- note that
        # longitude
        # are the X values and latitude are the Y values
        #
        x = []
        y = []

        for row in rows:
            x.append(row[2])
            y.append(row[1])

        image = plt.imread("chicago.png")
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868]  # area covered by the map:
        plt.imshow(image, extent=xydims)

        plt.title(color + " line")

        #
        # color is the value input by user, we can use that to plot the
        # figure *except* we need to map Purple-Express to Purple:
        #
        if (color.lower() == "purple-express"):
            color = "Purple"  # color="#800080"

        plt.plot(x, y, "o", c=color)
        #
        # annotate each (x, y) coordinate with its station name:
        #
        for row in rows:
            plt.annotate(row[0], (row[2], row[1]))

        plt.xlim([-87.9277, -87.5569])
        plt.ylim([41.7012, 42.0868])

        plt.show()


##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()

    print("General stats:")
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print(" # of stations:", f"{row[0]:,}")
    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone();
    print(" # of stops:", f"{row[0]:,}")
    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone();
    print(" # of ride entries:", f"{row[0]:,}")
    dbCursor.execute("Select min(date(ride_date)),max(date(ride_date)) From Ridership;")
    rows = dbCursor.fetchall();
    print(" date range:", rows[0][0], "-", rows[0][1])

    dbCursor.execute("Select sum(Num_Riders) From Ridership;")
    total = dbCursor.fetchone();
    print(" Total ridership:", f"{total[0]:,}")
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'W';")
    wday = dbCursor.fetchone();
    print(" Weekday ridership:", f"{wday[0]:,}", f"({round(wday[0] / total[0] * 100, 2)}%)")
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'A';")
    sday = dbCursor.fetchone();
    print(" Saturday ridership:", f"{sday[0]:,}", f"({round(sday[0] / total[0] * 100, 2)}%)")
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'U';")
    shday = dbCursor.fetchone();
    print(" Sunday/holiday ridership:", f"{shday[0]:,}", f"({round(shday[0] / total[0] * 100, 2)}%)")
    dbCursor.close()


##################################################################
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)
dbCursor = dbConn.cursor()
print()
command = input("\nPlease enter a command (1-9, x to exit): ")

while command != "x":
    if command == "1":
        command_1(dbCursor)
        command = input("\nPlease enter a command (1-9, x to exit): ")
    elif command == "2":
        command_2(dbCursor)
        command = input("\nPlease enter a command (1-9, x to exit): ")
    elif command == "3":
        command_3(dbCursor)
        command = input("\nPlease enter a command (1-9, x to exit): ")
    elif command == "4":
        command_4(dbCursor)
        command = input("\nPlease enter a command (1-9, x to exit): ")
    elif command == "5":
        command_5(dbCursor)
        command = input("\nPlease enter a command (1-9, x to exit): ")
    elif command == "6":
        command_6(dbCursor)
        command = input("\nPlease enter a command (1-9, x to exit): ")
    elif command == "7":
        command_7(dbCursor)
        command = input("\nPlease enter a command (1-9, x to exit): ")
    elif command == "8":
        command_8(dbCursor)
        command = input("\nPlease enter a command (1-9, x to exit): ")
    elif command == "9":
        command_9(dbCursor)
        command = input("\nPlease enter a command (1-9, x to exit): ")
    else:
        print("**Error, unknown command, try again...\n")
        command = input("\nPlease enter a command (1-9, x to exit): ")

dbCursor.close()

#
# done
#
