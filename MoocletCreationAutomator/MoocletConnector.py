from MoocletCreationAutomator.secure import MOOCLET_API_TOKEN
import requests
import json


class MoocletConnector:

    def __init__(self, token=MOOCLET_API_TOKEN):
        self.token = MOOCLET_API_TOKEN
        self.url = "https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/"

    def create_mooclet_object(self, params):
        endpoint = "mooclet"
        objects = requests.post(
            url=self.url + endpoint,
            data=params,
            headers={'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 201:
            print("unable to create mooclet")
            print(objects.json())
        else:
            print(objects.json())
            print(objects.json()["id"])
            return objects.json()["id"]

    def create_version_object(self, params):
        endpoint = "version"
        objects = requests.post(
            url=self.url + endpoint,
            data=params,
            headers={'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 201:
            print(objects.json())
            print(f"unable to create version for {params['name']}")
        else:
            print(objects.json())
            return objects.json()["name"]

    def create_policy_parameter(self, params):
        endpoint = "policyparameters"
        objects = requests.post(
            url=self.url + endpoint,
            data=params,
            headers={'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 201:
            print(objects.json())
            print(f"unable to create policy parameters")
        else:
            print(objects.json())

    def create_variable(self, params):
        endpoint = "variable"
        objects = requests.post(
            url=self.url + endpoint,
            data=params,
            headers={'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 201:
            print(objects.json())
            print(f"unable to create variables")
        else:
            print(objects.json())

