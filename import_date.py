import datetime



date_month = datetime.datetime.now().strftime('%m')
date_day = datetime.datetime.now().strftime('%d')

month_dict = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
day_dict = {'01': '1st', '02': '2nd', '03': '3rd', '04': '4th', '05': '5th', '06': '6th', '07': '7th', '08': '8th', '09': '9th', '10': '10th', '11': '11th', '12': '12th', '13': '13th', '14': '14th', '15': '15th', '16': '16th', '17': '17th', '18': '18th', '19': '19th', '20': '20th', '21': '21st', '22': '22nd', '23': '23rd', '24': '24th', '25': '25th', '26': '26th', '27': '27th', '28': '28th', '29': '29th', '30': '30th', '31': '31st'}

month = month_dict[date_month]
day = day_dict[date_day]