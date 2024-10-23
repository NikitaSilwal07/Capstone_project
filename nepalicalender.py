import calendar
import datetime
import csv

weekdays_nepali = {
    "Sunday": "Aaitabaar",
    "Monday": "Sombaar",
    "Tuesday": "Mangalbaar",
    "Wednesday": "Budhabaar",
    "Thursday": "Bihibaar",
    "Friday": "Shukrabaar",
    "Saturday": "Shanibaar"
}

events_dict = {
    (1, 1): "Naya Barsha",  
    (1, 11): "Loktantra Diwas",  
    (1, 18): "Majdur Diwas",
    (1, 30): "Shree Panchami",  
    (3, 8): "Mahila Diwas",  
    (6, 3): "Sambidhan Diwas",  
    (7, 1): "Paryatan Diwas",  
    (9, 7): "Udhauli Parva",  
    (9, 12): "Mohani Nakha",  
    (9, 15): "Annapurna Yatra",  
    (10, 1): "Maghe Sankranti",  
    (11, 7): "Prajatantra Diwas"
}

def month_days(csv_path):
    with open(csv_path, "r") as file:
        month_data = {}
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            year = int(row[0])
            month_days = list(map(int, row[1:]))
            month_data[year] = month_days
    return month_data

path = "calendar_bs.csv"
bs_month_days = month_days(path)

def bs_conversion(eng_year, eng_month, eng_day, bs_month_days):
    ref_ad = datetime.date(1944, 1, 1)
    ref_bs = (2000, 9, 17)
    ref_day = calendar.SATURDAY
    
    given_date = datetime.date(eng_year, eng_month, eng_day)
    days_diff = (given_date - ref_ad).days

    bs_year, bs_month, bs_day = ref_bs
    day_count = ref_day

    while days_diff != 0:
        days_in_current_month = bs_month_days[bs_year][bs_month - 1]
        bs_day += 1
        if bs_day > days_in_current_month:
            bs_month += 1
            bs_day = 1
        if bs_month > 12:
            bs_year += 1
            bs_month = 1

        day_count = (day_count + 1) % 7
        days_diff -= 1

    return f"{bs_year}-{bs_month}-{bs_day}", calendar.day_name[day_count]

def events(bs_year, bs_month, bs_day):
    return events_dict.get((bs_month, bs_day), "No event")

def create_nepali_calendar(year, month, bs_month_days):
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    months = ["Baishakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin", "Kartik", 
              "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"]

    days_in_month = bs_month_days[year][month - 1]
    ad_month_map = {1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 1, 11: 2, 12: 3}
    ad_month = ad_month_map[month]
    ad_year = year - 57 if ad_month > 3 else year - 56

    first_nep_date, start_day = bs_conversion(ad_year, ad_month, 27, bs_month_days)
    day_idx = weekdays.index(start_day[:3])

    day_list = [" "] * day_idx + [str(i) for i in range(1, days_in_month + 1)]

    calendar_lines = [f"{months[month - 1]} {year}".center(29), " ".join(weekdays)]
    calendar_lines += [" ".join(day_list[i:i + 7]) for i in range(0, len(day_list), 7)]

    return "\n".join(calendar_lines)

def nepali_details(eng_year, eng_month, eng_day):
    bs_date, bs_day_name = bs_conversion(eng_year, eng_month, eng_day, bs_month_days)
    bs_day_name_nepali = weekdays_nepali[bs_day_name]
    bs_year, bs_month, bs_day = map(int, bs_date.split('-'))
    event = events(bs_year, bs_month, bs_day)
    
    return {
        "Nepali Date": bs_date,
        "Day": bs_day_name_nepali,
        "Time": datetime.datetime.now().strftime("%I:%M %p"),
        "Event": event
    }
