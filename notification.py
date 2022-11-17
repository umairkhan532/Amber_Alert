
import requests

from pushnotifier import PushNotifier as pn

pn = pn.PushNotifier('username', 'password', 'package_name', 'api_key')

username = 'umairkhan532'
password = 'Mustanggtr#18'
package_name = 'com.name.app'
api_key = 'E5MA6D4DD6C3VBV46V75B6C3VB5MA6E5MA6EMTTKFB'


requests.post('https://pushnotifier.de', {
                "api_key": 'E5MA6D4DD6C3VBV46V75B6C3VB5MA6E5MA6EMTTKFB',
                "username": "umairkhan532",
                "password":"Mustanggtr#18",
                "package_name" : "com.name.app",
                })


pn.get_all_devices()