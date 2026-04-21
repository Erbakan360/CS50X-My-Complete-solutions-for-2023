-- Keep a log of any SQL queries you execute as you solve the mystery.

-- All you know is that the theft took place on July 28, 2021 and that it took place on Humphrey Street.

SELECT * FROM crime_scene_reports
    WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';
    -- +-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    -- | id  | year | month | day |     street      |                                                                                                       description                                                                                                        |
    -- +-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    -- | 295 | 2021 | 7     | 28  | Humphrey Street | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
    -- | 297 | 2021 | 7     | 28  | Humphrey Street | Littering took place at 16:36. No known witnesses.                                                                                                                                                                       |
    -- +-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

    -- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
        -- Interviews were conducted today with three witnesses who were present at the time
        -- each of their interview transcripts mentions the bakery.

SELECT * FROM interviews
    WHERE transcript LIKE '%bakery%' AND month = 7 AND day = 28;

    -- +-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    -- | id  |  name   | year | month | day |                                                                                                                                                     transcript                                                                                                                                                      |
    -- +-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    -- | 161 | Ruth    | 2021 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
    -- | 162 | Eugene  | 2021 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
    -- | 163 | Raymond | 2021 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
    -- +-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

    -- "Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away."
-- Searches the name and license plate of the people leaving the bakery at 10 o'clock or later.
SELECT name, license_plate FROM people
    WHERE license_plate IN
    -- logs of exit activity at the bakery at 10 o'clock or later.
    (SELECT license_plate FROM bakery_security_logs
        WHERE month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = 'exit')
    ORDER BY name ASC;
    -- +---------+---------------+
    -- |  name   | license_plate | each '+' will indicate how many tables these individuals are in
    -- +---------+---------------+
    -- | Barry   | 6P58WS2       | +
    -- | Bruce   | 94KL13X       | ++++
    -- | Diana   | 322W7JE       | +++
    -- | Iman    | L93JTIZ       | ++
    -- | Kelsey  | 0NTHK55       | +++
    -- | Luca    | 4328GD8       | +++
    -- | Sofia   | G412CB7       | +++
    -- | Vanessa | 5P2BI95       | +
    -- +---------+---------------+

    -- "Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money."

-- Search for names and account numbers of the people withdrawing money on Leggett Street on july 28
SELECT name, bank_accounts.account_number FROM people
    JOIN bank_accounts ON people.id = bank_accounts.person_id
    WHERE account_number IN
    -- Checks for the account numbers withdrawing money on Leggett Street on july 28
    (SELECT account_number FROM atm_transactions
        WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
        ORDER BY amount ASC);
-- +---------+----------------+
-- |  name   | account_number |
-- +---------+----------------+
-- | Bruce   | 49610011       |
-- | Diana   | 26013199       |
-- | Brooke  | 16153065       |
-- | Kenny   | 28296815       |
-- | Iman    | 25506511       |
-- | Luca    | 28500762       |
-- | Taylor  | 76054385       |
-- | Benista | 81061156       |
-- +---------+----------------+

    --  "As the thief was leaving the bakery, they called someone who talked to them for less than a minute."
-- Finding the names, phone numbers and duration of call for all the people who CALLED someone at the time of the crime
SELECT name, people.phone_number, phone_calls.duration FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.caller
    WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60
    ORDER BY phone_calls.duration;
-- +---------+----------------+----------+
-- |  name   |  phone_number  | duration |
-- +---------+----------------+----------+
-- | Kelsey  | (499) 555-9472 | 36       |
-- | Carina  | (031) 555-6622 | 38       |
-- | Taylor  | (286) 555-6063 | 43       |
-- | Bruce   | (367) 555-5533 | 45       |
-- | Diana   | (770) 555-1861 | 49       |
-- | Kelsey  | (499) 555-9472 | 50       |
-- | Sofia   | (130) 555-0289 | 51       |
-- | Benista | (338) 555-6650 | 54       |
-- | Kenny   | (826) 555-1652 | 55       |
-- | Kathryn | (609) 555-5876 | 60       |
-- +---------+----------------+----------+

    -- "In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow."
    -- "The thief then asked the person on the other end of the phone to purchase the flight ticket."
-- Searching for the earliest flights on July 29
-- to find the name of the city the flight leaves to
SELECT flights.id, flights.hour, flights.minute, airports.full_name, airports.city FROM flights
    JOIN airports ON flights.destination_airport_id = airports.id
    WHERE month = 7 AND day = 29 ORDER BY hour ASC;
    -- +----+------+--------+-------------------------------------+---------------+
    -- | id | hour | minute |              full_name              |     city      |
    -- +----+------+--------+-------------------------------------+---------------+
    -- | 36 | 8    | 20     | LaGuardia Airport                   | New York City | the earliest flight out of Fiftyville tomorrow is on destination airport id '4' Where id '36'
    -- | 43 | 9    | 30     | O'Hare International Airport        | Chicago       |
    -- | 23 | 12   | 15     | San Francisco International Airport | San Francisco |
    -- | 53 | 15   | 20     | Tokyo International Airport         | Tokyo         |
    -- | 18 | 16   | 0      | Logan International Airport         | Boston        |
    -- +----+------+--------+-------------------------------------+---------------+

-- All passengers on the flight with flight id 36, their seats and passport numbers.
SELECT passengers.flight_id, name, passengers.passport_number, passengers.seat FROM people
    JOIN passengers ON people.passport_number = passengers.passport_number JOIN flights ON passengers.flight_id = flights.id
    WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND flights.hour = 8 AND flights.minute = 20
    ORDER BY name;
    -- +-----------+--------+-----------------+------+
    -- | flight_id |  name  | passport_number | seat |
    -- +-----------+--------+-----------------+------+
    -- | 36        | Bruce  | 5773159633      | 4A   |
    -- | 36        | Doris  | 7214083635      | 2A   |
    -- | 36        | Edward | 1540955065      | 5C   |
    -- | 36        | Kelsey | 8294398571      | 6C   |
    -- | 36        | Kenny  | 9878712108      | 7A   |
    -- | 36        | Luca   | 8496433585      | 7B   |
    -- | 36        | Sofia  | 1695452385      | 3B   |
    -- | 36        | Taylor | 1988161715      | 6D   |
    -- +-----------+--------+-----------------+------+

    -- Bruce is in all locations throughout the days.
        -- They left the bakery around the time described in Ruths interview.
        -- They were on Leggett Street withdrawing cash around the time described in Eugenes interview.
        -- They called someone while leaving the bakery, which lasted less then a minute as described by Raymond.
        -- And they are on the first flight out of fiftyville.

    -- Now that we know who committed the crime we can determine the accomplice
-- Using Bruces number, the duration and date of the call we can determine that the accomplice is ...
SELECT name FROM people WHERE phone_number IN
    (SELECT receiver FROM phone_calls WHERE caller = '(367) 555-5533' AND month = 7 AND day = 28 AND duration < 60);
-- ...
-- +-------+
-- | name  |
-- +-------+
-- | Robin |
-- +-------+