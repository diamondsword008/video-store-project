import pandas as pd # I decided to switch to using pandas dataframes for easier searching and filtering
import re
from typing import Any
from datetime import datetime

class DBInterface():
    """Class for interacting with the Customers, Videos, and RentalHistory databases."""
    def __init__(self):
        self.video_df = pd.read_csv("Videos.csv")
        self.customer_df = pd.read_csv("Customers.csv")
        self.rental_df = pd.read_csv("RentalHistory.csv")

        self.rating_categories = ["NC-17", "R", "PG-13", "PG", "G"]

        self.__enforce_col_datatypes()

    def __enforce_col_datatypes(self):
        self.video_df['rating'] = self.video_df['rating'].astype('category')
        self.video_df['rating'] = self.video_df['rating'].cat.set_categories(self.rating_categories, ordered=True)

        self.rental_df["rental_start_date"] = pd.to_datetime(self.rental_df["rental_start_date"], format="%m/%d/%Y").dt.date
        self.rental_df["rental_end_date"] = pd.to_datetime(self.rental_df["rental_end_date"], format="%m/%d/%Y").dt.date

    # Getters
    def get_video_info(self, videoID: str):
        if videoID in self.video_df["videoID"].values:
            return self.video_df[self.video_df["videoID"] == videoID].values.tolist()[0]
        else:
            return False

    def get_customer_info(self, customerID: int):
        if customerID in self.customer_df["customerID"].values:
            return self.customer_df[self.customer_df["customerID"] == customerID].values.tolist()[0]
        else:
            return False

    def get_current_rentals(self, customerID: int):
        if customerID in self.customer_df["customerID"].values:
            return [y for x in self.rental_df[(self.rental_df["customerID"] == customerID) & (self.rental_df["returned"] == False)].values.tolist() for y in x]
        else:
            return False

    def get_rental_history(self, customerID: int):
        if customerID in self.customer_df["customerID"].values:
            return [y for x in self.rental_df[(self.rental_df["customerID"] == customerID) & (self.rental_df["returned"] == True)].values.tolist() for y in x]
        else:
            return False

    # setters
    def add_stock(self, videoID: str, amount: int=1) -> bool:
        """Increases the current and total stock for an existing video by the specified amount (defaults to one). Returns False if amount < 1 or if the video does not exist, otherwise it executes and returns True."""
        if amount < 1:
            return False
        if videoID in self.video_df["videoID"].values:
            self.video_df.loc[self.video_df["videoID"] == videoID, "current_stock"] += amount
            self.video_df.loc[self.video_df["videoID"] == videoID, "total_stock"] += amount
            self.video_df.to_csv("Videos.csv", index=False)
            return True
        else:
            return False

    def add_new_video(self, name: str, year: int, rating: str, genre: str, total_stock: int):
        """Adds a new video to the Videos csv. The videoID and current_stock columns are automatically added by the function. Returns False if the video already exists or if an invalid rating was input, otherwise it executes and returns True."""
        # TODO: fix categorical column breaking
        videoID = re.sub(r"[^a-zA-Z0-9]", "", name).lower()
        if videoID in self.video_df["videoID"].values or rating not in self.rating_categories:
            return False
        else:
            self.video_df.loc[len(self.video_df)] = [videoID, name, year, rating, genre, total_stock, total_stock]
            self.video_df.to_csv("Videos.csv", index=False)
            return True

    def edit_video_info(self, videoID: str, attribute: str, new_data: Any):
        """Changes the value of the specified attribute of the specified video. Returns False if the video does not exist or if the attribute does not exist, otherwise it executes and returns True."""
        if attribute in self.video_df.columns and videoID in self.video_df["videoID"].values:
            idx = self.video_df.index[self.video_df["videoID"] == videoID]
            self.video_df.loc[idx, attribute] = new_data
            self.video_df.to_csv("Videos.csv", index=False)
            return True
        else:
            return False

    def delete_video(self, videoID: str):
        """Sets the current and total stock of the specified video to zero. Returns False if the video does not exist or if someone is currently renting the video, otherwise it executes and returns True."""
        if videoID in self.video_df["videoID"].values and videoID not in self.rental_df[self.rental_df["returned"] == False]["videoID"].values:
            idx = self.video_df.index[self.video_df["videoID"] == videoID]
            self.video_df.loc[idx, ["current_stock", "total_stock"]] = 0
            self.video_df.to_csv("Videos.csv", index=False)
            return True
        else:
            return False

    def add_new_customer(self, first_name: str, last_name: str, email: str, address: str):
        """Adds a new customer to the Customers csv (!!!Does NOT check if the customer already exists). The customerID column is automatically generated by the function. Returns True when done executing."""
        customerID = max(self.customer_df["customerID"]) + 1
        self.customer_df.loc[len(self.customer_df)] = [customerID, first_name, last_name, email, address]
        self.customer_df.to_csv("Customers.csv", index=False)
        return True

    def edit_customer_info(self, customerID: int, attribute: str, new_data: Any):
        """Changes the value of the specified attribute of the specified customer. Returns False if the customer does not exist or if the attribute does not exist, otherwise it executes and returns True."""
        if attribute in self.customer_df.columns and customerID in self.customer_df["customerID"].values:
            idx = self.customer_df.index[self.customer_df["customerID"] == customerID]
            self.customer_df.loc[idx, attribute] = new_data
            self.customer_df.to_csv("Customers.csv", index=False)
            return True
        else:
            return False

    def delete_customer(self, customerID: int):
        """Deletes the row associated with the customer, and deletes every entry in their rental history. Returns False if the customer does not exist or if they have a current rental, otherwise it executes and returns True."""
        if customerID in self.customer_df["customerID"].values and customerID not in self.rental_df[self.rental_df["returned"] == False]["customerID"].values:
            # drop customer
            idx_cust = self.customer_df[self.customer_df["customerID"] == customerID].index
            self.customer_df.drop(idx_cust, inplace=True)
            self.customer_df.reset_index(drop=True, inplace=True)

            # drop rental history
            rows_rental = self.rental_df[self.rental_df["customerID"] == customerID].index
            self.rental_df.drop(rows_rental, inplace=True)
            self.rental_df.reset_index(drop=True, inplace=True)

            # save to csv
            self.customer_df.to_csv("Customers.csv", index=False)
            self.rental_df.to_csv("RentalHistory.csv", index=False)
            return True
        else:
            return False

    # rental functions
    def new_rental(self, videoID: str, customerID: int, rental_end_date: str):
        """Adds a new active rental to the rental database. !!!rental_end_date MUST be entered in mm/dd/yyyy format. rentalNo is automatically generated by the function, rental_start_date is set to the current day, and returned is set to False. Returns False if the customerID or videoID does not exist, otherwise it executes and returns True."""
        if customerID in self.customer_df["customerID"].values and videoID in self.video_df["videoID"].values:
            rentalNo = max(self.rental_df["rentalNo"]) + 1
            self.rental_df.loc[len(self.rental_df)] = [rentalNo, videoID, customerID, datetime.today().strftime('%m/%d/%Y'), rental_end_date, False]
            self.__enforce_col_datatypes()
            self.rental_df.to_csv("RentalHistory.csv", index=False)
            return True
        else:
            return False

    def return_rental(self, rentalNo: int):
        """Returns an active rental. Returns False if the rental does not exist or has been returned already, otherwise it executes and returns True."""
        if rentalNo in self.rental_df["rentalNo"].values and self.rental_df[self.rental_df["rentalNo"] == rentalNo]["returned"].values == False:
            idx = self.rental_df.index[self.rental_df["rentalNo"] == rentalNo]
            self.rental_df.loc[idx, "returned"] = True
        else:
            return False

"""
# code to make sure functions don't error, can ignore
if __name__ == "__main__":
    import db_init # short script I made to add dummy data for testing. Not pushed to repo
    db = DBInterface()
    print("---------------------------------------------")
    print(db.customer_df)
    print(db.rental_df)
    print("---------------------------------------------")
    db.add_new_customer("John", "Pork", "johnpork@email.com", "123 Discord Lane, Your Mom's House USA")
    db.edit_customer_info(3, "first_name", "Jonathan")
    db.delete_customer(1)
    db.new_rental("goodluckhavefundontdie", 3, "10/26/2026")
    db.return_rental(2)
    print(db.get_current_rentals(3))
    print("---------------------------------------------")
    print(db.customer_df)
    print(db.rental_df)
"""