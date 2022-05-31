import os
import uuid
from formshare.products import register_product_instance
from cne.product.celery_task import build_cne_sheets


def generate_cne_sheets(request, user, project, form, form_schema):
    settings = {}
    for key, value in request.registry.settings.items():
        if isinstance(value, str):
            settings[key] = value

    uid = str(uuid.uuid4())
    paths = ["products", uid + ".zip"]
    repo_dir = request.registry.settings["repository.path"]
    zip_file = os.path.join(repo_dir, *paths)

    task = build_cne_sheets.apply_async(
        (
            settings,
            form_schema,
            zip_file,
        ),
        queue="FormShare",
    )
    register_product_instance(
        request,
        user,
        project,
        form,
        "cne_sheets",
        task.id,
        zip_file,
        "application/zip",
        False,
        True,
    )
