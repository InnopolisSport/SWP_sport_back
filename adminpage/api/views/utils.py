import json
import re
from time import sleep
from datetime import time, datetime

import requests
from bs4 import BeautifulSoup
from django.conf import settings

from sport.models import SelfSportType
from sport.models.self_sport import SelfSportReport


class ImageErrors:
    IMAGE_FILE_SIZE_TOO_BIG = (
        10,
        f"Image file size too big, expected <= {settings.MAX_IMAGE_SIZE} bytes"
    )
    INVALID_IMAGE_SIZE = (
        11,
        f"Invalid image width/height, expected them to be in range "
        f"{settings.MIN_IMAGE_DIMENSION}px..{settings.MAX_IMAGE_DIMENSION}px"
    )


def parse_activity_app_name(url):
    if (re.match(r'https?://(www\.)?strava\.com/activities/\d+', url, re.IGNORECASE) is not None
            or re.match(r'https?://(www\.)?strava\.app\.link/\w*', url, re.IGNORECASE) is not None):
        return 'strava'

    if (re.match(r'https?://(www\.)?home\.trainingpeaks\.com/athlete/workout/\w+', url, re.IGNORECASE) is not None
            or re.match(r'https?://(www\.)?tpks\.ws/\w+', url, re.IGNORECASE) is not None):
        return 'training_peaks'

    return None


def evaluate_activity(activity_data):
    """Calculate sport hours and approve an activity.

    Arguments:
    activity_data -- parsed activity info
    """
    max_hours_cnt = 3

    # Fraction of the distance student is allowed to miss and still get an hour.
    # To avoid cumulating of the error, it is only applied for the last hour in the activity.
    dist_error = 0.05

    def evaluate(dist_for_hour, min_avg_speed):
        received_hours_cnt = int((activity_data['distance'] + dist_for_hour * dist_error) / dist_for_hour)
        activity_data['hours'] = min(max_hours_cnt, received_hours_cnt)
        activity_data['approved'] = activity_data['hours'] != 0 and activity_data['avg_speed'] >= min_avg_speed

    if activity_data['training_type'] == 'Running':
        evaluate(5, 8.6)
    elif activity_data['training_type'] == 'Walking':
        evaluate(6.5, 6.5)
    elif activity_data['training_type'] == 'Biking':
        evaluate(15, 20.0)
    elif activity_data['training_type'] == 'Swimming':
        if activity_data['distance'] < 4 - 1.5 * dist_error:
            activity_data['hours'] = (activity_data['distance'] + 1.5 * dist_error) / 1.5
        else:
            activity_data['hours'] = 3
        activity_data['approved'] = activity_data['hours'] != 0 and activity_data['avg_speed'] >= 2.4


def parse_strava_activity_info(html):
    soup = BeautifulSoup(html)
    try:
        json_string = soup.html.body.find_all(
            'div', attrs={"data-react-class": "ActivityPublic"}
        )[0].get("data-react-props")
    except IndexError:
        return None
    data = json.loads(json_string)
    beautified_data = json.dumps(data, sort_keys=True, indent=2)

    time_string = data['activity']["time"]
    training_type = data['activity']["type"]
    distance_float = float(data['activity']["distance"][:-3])  # km

    if len(time_string) == 5:
        time_string = "00:" + time_string
    elif len(time_string) == 2:
        time_string = "00:00:" + time_string
    elif len(time_string) == 4:
        time_string = "00:0" + time_string
    elif len(time_string) == 7:
        time_string = "0" + time_string
    format_string = "%H:%M:%S"

    parsed_time = datetime.strptime(time_string, format_string)
    if parsed_time.second != 0:
        if parsed_time.minute == 59:
            final_time = time(parsed_time.hour + 1, 0, 0)
        else:
            final_time = time(parsed_time.hour, parsed_time.minute + 1, 0)
    total_minutes = final_time.hour * 45 + final_time.minute

    speed = round(distance_float / (total_minutes / 60), 1)  # for Run, Ride, Walk
    pace = round(total_minutes / (distance_float * 10), 1)  # for Swim

    approved = None
    out_dict = dict()
    out_dict['distance'] = distance_float
    k = 0.95  # 5% bonus for distanse
    if training_type == "Run":
        academic_hours = round(distance_float / (5 * k))
        out_dict['type'] = 'Running'
        out_dict['avg_speed'] = speed
        if speed >= 8.6:
            approved = True
    elif training_type == "Swim":
        distance_float += 0.05  # bonus 50m because Strava unauth rounds by 1 digit
        if distance_float < 3.95:
            academic_hours = round(distance_float / (1.5 * k))
        else:
            academic_hours = 3
        out_dict['type'] = 'Swimming'
        out_dict['avg_pace'] = pace
        if pace <= 2.5:
            approved = True
    elif training_type == "Ride":
        academic_hours = round(distance_float / (15 * k))
        out_dict['type'] = 'Biking'
        out_dict['avg_speed'] = speed
        if speed >= 20:
            approved = True
    elif training_type == "Walk":
        academic_hours = round(distance_float / (6.5 * k))
        out_dict['type'] = 'Walking'
        out_dict['avg_speed'] = speed
        if speed >= 6.5:
            approved = True
    if academic_hours > 3:
        academic_hours = 3
    out_dict['hours'] = academic_hours
    if academic_hours <= 0:
        approved = False
    else:
        approved = True

    out_dict['approved'] = approved

    return out_dict


def parse_training_peaks_activity_info(html):
    response_text = html
    soup = BeautifulSoup(response_text, features="html.parser")

    public_activity_wrapper = None
    for elem in soup.find_all('script', type='text/javascript'):
        public_activity_wrapper = re.search(r'var publicActivityWrapper = (.*);', str(elem.string))
        if public_activity_wrapper is not None:
            break

    json_activity_info = json.loads(public_activity_wrapper.group(1))

    # json_activity_info['workout']['distance'] seems to be always measured in meters
    activity_data = {'training_type': json_activity_info['workout']['userTags'],
                     'distance': round(json_activity_info['workout']['distance'] / 1000, 2),
                     'avg_heart_rate': json_activity_info['workout']['heartRateAverage']}
    activity_data['avg_speed'] = round(activity_data['distance'] / json_activity_info['workout']['totalTime'], 2)
    # TODO parse has_gps, avg_pace

    if json_activity_info['workout']['userTags'] == 'Cycling':
        activity_data['training_type'] = 'Biking'
    else:
        activity_data['training_type'] = json_activity_info['workout']['userTags']
    evaluate_activity(activity_data)

    return activity_data


def parse_self_sport_reports():
    reports = SelfSportReport.objects.filter(parsed_data__isnull=True)
    while len(reports):
        for report in reports:
            response = requests.get(report.link)
            if response.status_code == 429:
                sleep(3600)
                response = requests.get(report.link)
            elif response.status_code != 200:
                print('parser: parsing error1')
                return {'message': 'parsing error'}

            html = response.text
            parsed_data = None
            app_name = parse_activity_app_name(report.link)
            if app_name == 'strava':
                parsed_data = parse_strava_activity_info(html)
            elif app_name == 'training_peaks':
                parsed_data = parse_training_peaks_activity_info(html)

            if parsed_data is None:
                print('parser: parsing error2')
                return {'message': 'parsing error'}

            print(f'report_id: {report.id}, parsed_data: {parsed_data}')

            report.training_type = SelfSportType.objects.get(name=parsed_data['training_type'])
            report.hours = parsed_data['hours']
            report.save()

            sleep(60)

        reports = SelfSportReport.objects.filter(parsed_data__isnull=True)
