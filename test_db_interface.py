import datetime
import unittest
import runpy
from unittest import result

from DBInterface import DBInterface

class TestDBInterfaceGetters(unittest.TestCase):
    def setUp(self):
        # reset tables to db_init.py data
        runpy.run_path("db_init.py")
        # initializing db interface
        self.db = DBInterface()

    def test_get_video_info_valid(self):
        expected = ["thelegomovie","The Lego Movie",2014,"PG","Action",3,3]
        result = self.db.get_video_info("thelegomovie")
        self.assertEqual(result, expected)

    def test_get_video_info_not_in_DB(self):
        result = self.db.get_video_info("failurecase")
        self.assertFalse(result)

    def test_get_video_info_non_ID(self):
        result = self.db.get_video_info(11234)
        self.assertFalse(result)

    def test_get_customer_info_valid(self):
        expected = [1,"John", "Smith", "johnsmith@email.com", "123 Generic St, Anywhere, USA 12345"]
        result = self.db.get_customer_info(1)
        self.assertEqual(result, expected)

    def test_get_customer_info_not_in_DB(self):
        result = self.db.get_customer_info(1002)
        self.assertFalse(result)

    def test_get_current_rentals_valid_customer_ID(self):
        expected = [
            [
            2,
            "goodluckhavefundontdie",
            2,
            datetime.date(2026, 10, 4),
            datetime.date(2016, 10, 18),
            False
        ]
        ]
        result = self.db.get_current_rentals(2)
        self.assertEqual(result, expected)

    def test_get_current_rentals_with_multiple_active_rentals(self):
        expected = [
            [
                4,"hokum",
                1,datetime.date(2014,10,4),
                datetime.date(2014,10,18),False
            ],
            [
                5, "theoutsiders",
                1, datetime.date(2014,10,4),
                datetime.date(2014,10,18),False
            ]
        ]
        result = self.db.get_current_rentals(1)
        self.assertEqual(expected,result)

    def test_get_current_rentals_all_returned(self):
        result = self.db.get_current_rentals(3)
        self.assertFalse(result)

    def test_get_current_rentals_with_no_active_rentals(self):
        result = self.db.get_current_rentals(4)
        self.assertFalse(result)

    def test_get_current_rentals_ID_notIn_DB(self):
        result = self.db.get_current_rentals(1110)
        self.assertFalse(result)

    def test_get_current_rentals_not_ID(self):
        result = self.db.get_current_rentals("this is not an id")
        self.assertFalse(result)

    def test_get_rental_history_valid_customer_ID_single_rental(self):
        result = self.db.get_rental_history(3)
        expected = [[6, 'theavengers', 3, datetime.date(2014, 10, 4), datetime.date(2014, 10, 18), True]]
        self.assertEqual(expected, result)


    def test_get_rental_history_valid_customer_ID_multiple_rentals(self):
        result = self.db.get_rental_history(1)
        expected = [[1, 'thelegomovie', 1, datetime.date(2016, 5, 12), datetime.date(2016, 5, 26), True], [3, 'goodluckhavefundontdie', 1, datetime.date(2024, 10, 4), datetime.date(2014, 10, 18), True]]
        self.assertEqual(result, expected)

    def test_get_rental_history_customerID_notIn_DB(self):
        result = self.db.get_rental_history(2000)
        self.assertFalse(result)

    def test_get_rental_history_nonID(self):
        result = self.db.get_rental_history("this is not an ID")
        self.assertFalse(result)

    def test_get_all_customers(self):
        result = self.db.get_all_customers()
        expected = [[1, 'John', 'Smith', 'johnsmith@email.com', '123 Generic St, Anywhere, USA 12345'], [2, 'Jane', 'Doe', 'janedoe@company.org', '456 Some Lane, Somewhere, USA 98765'], [3, 'First', 'Last', 'firstlast@example.com', '123 random address'], [4, 'Test', 'Customer', 'test@customer.org', '456 ambiguous place']]
        self.assertEqual(expected, result)

    def test_get_all_current_rentals(self):
        result = self.db.get_all_current_rentals()
        expected = [[2, 'goodluckhavefundontdie', 2, datetime.date(2026, 10, 4), datetime.date(2016, 10, 18), False], [4, 'hokum', 1, datetime.date(2014, 10, 4), datetime.date(2014, 10, 18), False], [5, 'theoutsiders', 1, datetime.date(2014, 10, 4), datetime.date(2014, 10, 18), False]]
        self.assertEqual(expected, result)

    def test_get_all_videos(self):
        result = self.db.get_all_videos()
        expected = [['thelegomovie', 'The Lego Movie', 2014, 'PG', 'Action', 3, 3], ['goodluckhavefundontdie', "Good Luck, Have Fun, Don't Die", 2025, 'R', 'Sci-Fi', 1, 1], ['hokum', 'Hokum', 2026, 'R', 'Horror', 3, 3], ['theoutsiders', 'The Outsiders', 1983, 'PG-13', 'Drama', 2, 2], ['theavengers', 'The Avengers', 2012, 'PG-13', 'Action', 4, 4]]
        self.assertEqual(expected, result)

class TestDBInterfaceSetter(unittest.TestCase):
    def setUp(self):
        # reset tables to db_init.py data
        runpy.run_path("db_init.py")
        # initializing db interface
        self.db = DBInterface()

    def test_add_stock_valid_ID_default_value(self):
        video = self.db.get_video_info('hokum')
        initial_current = video[5]
        initial_total = video[6]
        # running method
        self.db.add_stock('hokum')
        video = self.db.get_video_info('hokum')
        current, total = video[5],video[6]
        self.assertEqual(initial_current + 1, current)
        self.assertEqual(initial_total + 1, total)

    def test_add_stock_valid_ID_non_default_value(self):
        amount = 3
        video = self.db.get_video_info('hokum')
        initial_current = video[5]
        initial_total = video[6]
        # running method
        self.db.add_stock('hokum',amount)
        video = self.db.get_video_info('hokum')
        current, total = video[5], video[6]
        self.assertEqual(initial_current + amount, current)
        self.assertEqual(initial_total + amount, total)

    def test_add_stock_negative_amount(self):
        result = self.db.add_stock('thelegomovie',-3)
        self.assertFalse(result)

    def test_add_stock_nonID(self):
        result = self.db.add_stock(12)
        self.assertFalse(result)

    def test_add_new_video_valid_data_types(self):
        self.db.add_new_video('Interstellar',2014,'PG-13','Sci-Fi', 6)
        video = self.db.get_video_info('interstellar')
        expected = ["interstellar","Interstellar",2014,"PG-13","Sci-Fi",6,6]

        self.assertEqual(expected, video)

    def test_add_new_video_invalid_Name(self):
        with self.assertRaises(TypeError):
            self.db.add_new_video(123, 2014, 'PG-13', 'Sci-Fi', 6)

        with self.assertRaises(TypeError):
            self.db.add_new_video(1546, 2014, 'PG-13', 'Sci-Fi', 6)

    def test_add_new_video_invalid_Year(self):
        with self.assertRaises(ValueError):
            self.db.add_new_video(
                "Interstellar", "year", 'PG-13', 'Sci-Fi', 8
            )


    def test_add_new_video_invalid_Rating(self):
        video = self.db.add_new_video("Interstellar",2014,'PG-15','Sci-Fi', 6)
        self.assertFalse(video)

    def test_add_new_video_invalid_Genre_type(self):
        video = self.db.add_new_video("Interstellar",2014,'PG-13',123, 6)
        vid = self.db.get_video_info('interstellar')
        print(vid[4], type(vid[4]))
        self.assertIsInstance(vid[4], str)

    def test_add_new_video_negative_stock(self):
        video = self.db.add_new_video("Interstellar",2014,'PG-13','Sci-Fi', -1)
        self.assertFalse(video)


    def test_add_new_video_invalid_Stock(self):
        with self.assertRaises(TypeError):
            self.db.add_new_video(
                "Interstellar", 2014, 'PG-13', 'Sci-Fi', "stock number"
            )


    def test_add_new_video_video_already_in_DB(self):
        video = self.db.add_new_video('The Lego Movie',2014, 'PG', 'Action',3)
        self.assertFalse(video)

    def test_edit_video_info_valid_attributes(self):
        test_cases = [
            ("name", "New Lego Movie"),
            ("year", 2015),
            ("rating", "R"),
            ("genre", "Comedy"),
            ("total_stock", 10),
            ("current_stock", 8)
        ]

        for attribute, new_data in test_cases:
            with self.subTest(attribute=attribute):
                result = self.db.edit_video_info(
                    "thelegomovie", attribute, new_data
                )

                self.assertTrue(result)

                video = self.db.get_video_info("thelegomovie")
                self.assertEqual(
                    video[list(self.db.video_df.columns).index(attribute)],
                    new_data
                )

    def test_edit_video_info_invalid_data(self):
        value_error_test_cases = [
            ("name", 123),
            ("year", "year/date"),
            ("total_stock", "total stock"),
            ("current_stock", "current stock"),
            ("rating", "rating"),
            ("genre", 123)
        ]

        for attribute, new_data in value_error_test_cases:
            with self.subTest(attribute=attribute):
                with self.assertRaises(TypeError):
                    self.db.edit_video_info(
                        "thelegomovie",
                        attribute,
                        new_data
                    )

    def test_edit_video_info_invalid_videoID(self):
        video = self.db.edit_video_info("invalidmovieID","year",2010)
        self.assertFalse(video)

    def test_edit_video_info_invalid_attribute(self):
        video = self.db.edit_video_info("thelegomovie","audience_score", "90/100")
        self.assertFalse(video)

    def test_delete_movie_valid_ID(self):
        self.db.delete_video("thelegomovie")
        self.assertEqual(self.db.get_video_info("thelegomovie")[6],0)
        self.assertEqual(self.db.get_video_info("thelegomovie")[5],0)

    def test_delete_movie_invalid_ID(self):
        command = self.db.delete_video("thenewnotreallegomovie")
        self.assertFalse(command)

    def test_add_new_customer(self):
        customer = self.db.add_new_customer("First", "last", "example@email.com", "whatever place")
        self.assertIn(
            "First",
            self.db.customer_df["first_name"].values
        )


    @unittest.skip
    def test_new_customer_invalid_data(self):
        test_cases = [
            (123, "Smith", "smith@email.com", "123 Main St"),
            ("John", 321, "smith@email.com", "123 Main St"),
            ("John", "Smith", 12345, "123 Main St"),
            ("John", "Smith", "smith@email.com", 54321)
        ]

        for first_name, last_name, email, address in test_cases:
            with self.subTest(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    address=address
            ):
                with self.assertRaises(TypeError):
                    self.db.add_new_customer(
                        first_name,
                        last_name,
                        email,
                        address
                    )


    def test_edit_customer_info_valid_data(self):
        test_cases = [
            ("first_name", "Johnny"),
            ("last_name", "Smithlee"),
            ("email", "newemail@example.com"),
            ("address", "123 Main St")
        ]

        for attribute, new_data in test_cases:
            with self.subTest(attribute=attribute):
                result = self.db.edit_customer_info(
                1, attribute, new_data
                )

                self.assertTrue(result)

                customer = self.db.get_customer_info(1)
                self.assertEqual(
                    customer[list(self.db.customer_df.columns).index(attribute)],
                    new_data
                )

    def test_edit_customer_info_invalid_attribute(self):
        customer = self.db.edit_customer_info(4, "hair_color", "Ginger")
        self.assertFalse(customer)

    def test_edit_customer_info_invalid_CustomerID(self):
        customer = self.db.edit_customer_info(1002, "first_name", "Stevie")
        self.assertFalse(customer)

    def test_delete_customer_valid_ID(self):
        self.db.delete_customer(4)

        self.assertNotIn(
            4,
            self.db.customer_df["customerID"].values
        )

    def test_delete_customer_invalid_ID(self):
        command = self.db.delete_customer(10000)
        self.assertFalse(command)

class TestDBInterfacerRentalFunctions(unittest.TestCase):
    def setUp(self):
        # reset tables to db_init.py data
        runpy.run_path("db_init.py")
        # initializing db interface
        self.db = DBInterface()

    def test_new_rental_valid_data(self):
        result = self.db.new_rental(
            "hokum",
            4,
            "11/15/2026"
        )
        self.assertTrue(result)
        newest_rental = self.db.rental_df.iloc[-1]
        self.assertEqual(newest_rental["videoID"], "hokum")
        self.assertEqual(newest_rental["customerID"], 4)
        self.assertFalse(newest_rental["returned"])

    def test_new_rental_invalid_data(self):
        test_cases = [
            ("thismovieisnotinDB", 4, "11/15/2026"),  # invalid videoID
            ("hokum", 999, "11/15/2026"),  # invalid customerID
        ]

        for videoID, customerID, rental_end_date in test_cases:
            with self.subTest(
                    videoID=videoID,
                    customerID=customerID
            ):
                result = self.db.new_rental(
                    videoID,
                    customerID,
                    rental_end_date
                )

                self.assertFalse(result)

    def test_new_rental_end_date_before_checkout_date(self):
        result = self.db.new_rental(
            "hokum",
            4,
            "01/01/2020"
        )

        self.assertFalse(result)

    def test_return_rental_valid_data(self):
        self.db.return_rental(4)
        rental = self.db.rental_df[
            self.db.rental_df["rentalNo"] == 4
            ]
        self.assertTrue(rental["returned"].iloc[0])

    def test_return_rental_invalid_data(self):
        result = self.db.return_rental(999)
        self.assertFalse(result)





if __name__ == '__main__':
    unittest.main()