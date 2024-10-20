from django.http import JsonResponse


def ping(request):  # noqa: ANN001, ARG001
    """Return a Ping Test View.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JSON: Ping Pong.

    """
    data = {"ping": "pong!"}
    return JsonResponse(data)
