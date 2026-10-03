from . import ml


def model_status(request):
    """Makes `model_info` available in every template."""
    return {"model_info": ml.model_info()}
