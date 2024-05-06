-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with
-- three witnesses who were present at the time – each of their interview transcripts mentions the bakery.


SELECT transcript FROM 	interviews
WHERE year = 2023 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

-- 1st ..Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
--If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

-- 2nd .. I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
--I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

-- 3rd ..  As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
--In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
--The thief then asked the person on the other end of the phone to purchase the flight ticket

SELECT name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25
AND activity = 'exit';

-- Suspect | Vanessa | | Bruce   | | Barry   | | Luca    | | Sofia   | | Iman    | | Diana   | | Kelsey  |

SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE  year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Suspect  | Bruce || Diana || Brooke || Kenny || Iman || Luca || Taylor || Benista |

SELECT name from people
JOIN passengers ON passengers.passport_number = people.passport_number
WHERE passengers.flight_id = (
    SELECT id FROM flights
    WHERE  year = 2023 AND month = 7 AND day = 29 AND origin_airport_id =(
        SELECT id FROM airports WHERE city = 'Fiftyville'
    ) ORDER BY hour,minute
LIMIT 1);

-- Suspect | Doris  || Sofia  || Bruce  || Edward || Kelsey || Taylor | | Kenny  || Luca  |

-- Common Suspect -- Bruce AND Luca

SELECT name FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60;

-- Suspect | Sofia || Kelsey  || Bruce   || Kelsey  || Taylor  || Diana   || Carina  || Kenny   || Benista |

-- Final Suspect -- Bruce

SELECT city FROM airports
WHERE id =(
    SELECT destination_airport_id FROM flights
    WHERE  year = 2023 AND month = 7 AND day = 29 AND origin_airport_id =(
        SELECT id FROM airports WHERE city = 'Fiftyville'
    )ORDER BY hour,minute
LIMIT 1);

--The city the thief ESCAPED TO: New York City

SELECT phone_number FROM people
WHERE name = 'Bruce';

-- Bruce Phone Number =  (367) 555-5533

SELECT name FROM people WHERE phone_number =(
    SELECT receiver FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60 AND caller = '(367) 555-5533');






