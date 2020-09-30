import os

import yaml
import boxsdk


JWT_KEYS_FILE_PATH = os.path.join(
    "box_jwt.yml"
)
APPROVED_INVOICES_FOLDER_ID = "123336415364"
box_jwt_keys = None
box_auth = None
box_client = None


def get_box_jwt_keys():
    """
    Loads Box Platform JWT keys into a global variable.
    """
    global box_jwt_keys
    if not box_jwt_keys:
        with open(JWT_KEYS_FILE_PATH, "r") as fh:
            box_jwt_keys = yaml.load(fh, Loader=yaml.FullLoader)

    return box_jwt_keys


def get_box_auth():
    """
    Authenticates a Box SDK JWTAuth instance into Box Platform APIs.
    """
    global box_auth
    if not box_auth:
        box_jwt_keys = get_box_jwt_keys()
        box_auth = boxsdk.JWTAuth.from_settings_dictionary(box_jwt_keys)

    return box_auth


def get_box_client(as_user_email=None):
    """
    Sets up a Box Platform API client as a global variable.
    """
    global box_client
    if not box_client:
        box_auth = get_box_auth()
        box_client = boxsdk.Client(box_auth)

    if as_user_email:
        user = box_client.users(filter_term=as_user_email, limit=1).next()
        box_client = box_client.as_user(user)

    return box_client
