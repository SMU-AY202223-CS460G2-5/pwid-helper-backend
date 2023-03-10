from typing import Any, Dict

Json = Dict[str, Any]


def generate_response_json(
    success: bool = True,
    data: Any = None,
) -> Json:
    """returns a json payload for response

    Args:
        success (bool, optional): Indication of the response status. Defaults to True.
        data (Any, optional): Any data accommpanying the response. Defaults to None.

    Returns:
        Json: A json payload for response
    """
    payload = {"success": success}
    if data:
        payload["data"] = data
    return payload
