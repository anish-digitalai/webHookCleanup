import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

cloud_url_and_api_end_point = config.get('seetest_urls', 'cloud_url') + config.get('seetest_urls', 'end_point')


def get_device_property(serial_number, property_value):
    end_url = cloud_url_and_api_end_point + "?query=@serialnumber='" + serial_number + "'"

    headers = {
        'Authorization': 'Bearer %s' % config.get('seetest_authorization', 'access_key_admin'),
        'Content-Type': 'application/json'
    }

    response = requests.request('GET', end_url, headers=headers, verify=False)

    value = get_json_value_from_response_content(property_value, response.content)
    return value

def finish_cleanup_state(uid, status):
    end_url = 'https://uscloud.experitest.com/api/v1/cleanup-finish?deviceId=' + str(uid) + '&status=' + str(status)

    headers = {
        'Authorization': 'Bearer %s' % config.get('seetest_authorization', 'access_key_cleanup'),
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', end_url, headers=headers, verify=False)

    if response.status_code == 200:
        print(
            'Python Script (function: finish_cleanup_state) - Successfully finished Cleanup State: %s' % response.text)
    else:
        print(
            'Python Script (function: finish_cleanup_state) - Unable to finish Cleanup State: %s' % response.text)

    return response


def get_json_value_from_response_content(value, response_content):
    data = json.loads(response_content)
    return_value = data['data'][0]['%s' % value]
    return return_value