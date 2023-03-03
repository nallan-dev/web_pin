from logging import ERROR, INFO, Logger

import requests

from conf import settings

CHANGE_STATE_URL = f"http://localhost:{settings.WEB_APP_PORT}/"


def switch_data(
    pk_api_name: str,
    entity_id: int,
    to_state: int,
    logger: Logger,
) -> int:
    payload = {pk_api_name: entity_id, "state": to_state}
    response = requests.post(url=CHANGE_STATE_URL, data=payload)
    if response.status_code == 200:
        logger_str = "%s %s to %s data: %s"
        logger_level = INFO
        ret_code = 0
    else:
        logger_str = "ERROR %s send %s to %s data: %s"
        logger_level = ERROR
        ret_code = 1
    logger.log(
        logger_level,
        logger_str,
        response.status_code,
        response.request.method,
        CHANGE_STATE_URL,
        payload,
    )
    return ret_code
