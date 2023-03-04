import requests
from typing import Dict, Union
import qrcode
from io import BytesIO


# TODO: rewrite to use aiohttp
# TODO: use pydantic for models


class AuthError(Exception):
    pass


class NotFoundError(Exception):
    pass


class UnknownError(Exception):
    pass


class WireguardApiClient:
    def __init__(self, base_url, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.auth(password)

    def auth(self, password) -> bool:
        self.session.get(self.base_url + "/session")
        r = self.session.post(self.base_url + "/session", json={"password": password})
        if r.status_code != 204:
            if "invalid" in r.text.lower():
                raise AuthError("Invalid password")
            else:
                raise AuthError("Unknown error")
        return True

    def get_clients(self) -> Dict:
        r = self.session.get(self.base_url + "/wireguard/client")
        if r.status_code == 401:
            raise AuthError("Not Logged In")
        return r.json()

    def get_client_by_pub_key(self, pub_key) -> Union[Dict, None]:
        clients = self.get_clients()
        for client in clients:
            if client.get("publicKey") == pub_key:
                return client
        raise NotFoundError("Client not found")

    def get_client_by_uuid(self, uuid) -> Union[Dict, None]:
        clients = self.get_clients()
        for client in clients:
            if client.get("id") == uuid:
                return client
        raise NotFoundError("Client not found")

    def get_client_configuration(self, uuid) -> bytes:
        r = self.session.get(self.base_url + f"/wireguard/client/{uuid}/configuration")
        if r.status_code == 401:
            raise AuthError("Not Logged In")
        if r.status_code == 404:
            raise NotFoundError("Client not found")
        return r.text.encode()

    def get_client_qr_code(self, uuid) -> bytes:
        config = self.get_client_configuration(uuid)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(config)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = BytesIO()
        img.save(img_io, "PNG")
        return img_io.getvalue()

    def create_profile(self, name) -> Dict:
        r = self.session.post(self.base_url + "/wireguard/client", json={"name": name})
        if r.status_code == 401:
            raise AuthError("Not Logged In")
        pub_key = r.json().get("publicKey")
        if not pub_key:
            raise UnknownError("No public key in response")
        added_client = self.get_client_by_pub_key(pub_key)
        if not added_client:
            raise UnknownError("New client not found")
        return added_client

    def disable_client(self, uuid) -> Dict:
        r = self.session.post(self.base_url + f"/wireguard/client/{uuid}/disable")
        if r.status_code == 401:
            raise AuthError("Not Logged In")
        if r.status_code == 404:
            raise NotFoundError("Client not found")
        edited_client = self.get_client_by_uuid(uuid)
        if edited_client.get("enabled") is not False:
            raise UnknownError("Client not disabled")
        return edited_client

    def enable_client(self, uuid) -> Dict:
        r = self.session.post(self.base_url + f"/wireguard/client/{uuid}/enable")
        if r.status_code == 401:
            raise AuthError("Not Logged In")
        if r.status_code == 404:
            raise NotFoundError("Client not found")
        edited_client = self.get_client_by_pub_key(uuid)
        if edited_client.get("enabled") is not True:
            raise UnknownError("Client not enabled")
        return edited_client

    def change_client_name(self, uuid, name) -> Dict:
        r = self.session.put(
            self.base_url + f"/wireguard/client/{uuid}/name", json={"name": name}
        )
        if r.status_code == 401:
            raise AuthError("Not Logged In")
        if r.status_code == 404:
            raise NotFoundError("Client not found")
        if r.status_code == 500:
            raise UnknownError("Invalid name")
        edited_client = self.get_client_by_uuid(uuid)
        if edited_client.get("name") != name:
            raise UnknownError("Name not changed")
        return edited_client

    def change_client_address(self, uuid, address) -> Dict:
        r = self.session.put(
            self.base_url + f"/wireguard/client/{uuid}/address",
            json={"address": address},
        )
        if r.status_code == 401:
            raise AuthError("Not Logged In")
        if r.status_code == 404:
            raise NotFoundError("Client not found")
        if r.status_code == 500:
            raise UnknownError("Invalid address")
        edited_client = self.get_client_by_uuid(uuid)
        if edited_client.get("address") != address:
            raise UnknownError("Address not changed")
        return edited_client

    def delete_client(self, uuid) -> bool:
        r = self.session.delete(self.base_url + f"/wireguard/client/{uuid}")
        if r.status_code == 401:
            raise AuthError("Not Logged In")
        if r.status_code == 404:
            raise NotFoundError("Client not found")

        try:
            self.get_client_by_uuid(uuid)
        except NotFoundError:
            return True
        raise UnknownError("Client not deleted")
