# model_gatherer.py

from django.apps import apps

def get_all_models():
    all_models = []
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            all_models.append(model)
    return all_models
