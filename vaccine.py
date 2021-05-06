from datetime import timedelta


def vaccine_condition(slot):
    if slot['min_age_limit'] <= MIN_AGE and slot['available_capacity'] > 0:
        return True
    else:
        return False


def check_for_medicine(name, pin_code, date_range):
    from datetime import datetime
    import requests
    import json
    dates = [(datetime.now()+timedelta(days=i)).strftime('%d-%m-%Y') for i in range(0, date_range)]
    slack_url = 'TODO: PASTE SLACK WEBHOOK HERE'

    co_win_url = 'https://api.cowin.gov.in/api/v2/appointment/sessions/public/findByPin'
    
    output = []
    for date in dates:
        url = f'{co_win_url}?pincode={pin_code}&date={date}'
        try:
            r = requests.get(url)
            res = r.json()
            sessions = res['sessions']
            valid_slots = list(filter(vaccine_condition, sessions))
            if len(valid_slots) > 0:
                output.append({'title': f'Vaccine status for {name} on {date} at pinCode: {pin_code}'})
                for slot in valid_slots:
                    name = slot['name']
                    address = slot['address']
                    vaccine = slot['vaccine']
                    slots = slot['slots']
                    fee = slot['fee']
                    dt = slot['date']
                    avl = slot['available_capacity']
                    output.append({ 'title': f'name: {name}, address: {address}, vaccine: {vaccine}, slots: {slots}, fee: {fee}, date: {dt}, aval_capacity: {avl}', 'short': False})

        except Exception as e:
            print(e)

    if len(output) > 0:
        payload = {
            "attachments": [
                {
                    "color": "#D00000",
                    "fields": output
                }
            ]
        }
        payload = json.dumps(payload)
        requests.post(slack_url, data=payload)

MIN_AGE = 44

if __name__ == '__main__':
    import time
    while True:
        name = 'Sourabh Mishra'
        pin_code = '110053'
        date_range_check = 3
        check_for_medicine(name, pin_code, date_range_check)
        # run in every 30 s
        time.sleep(30)
   
