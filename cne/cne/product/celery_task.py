import os
import uuid
from celery.utils.log import get_task_logger
import zipfile
import glob
from formshare.config.celery_app import celeryApp
from formshare.config.celery_class import CeleryTask
from .sheet8 import generate_sheet_8
from .sheet9 import generate_sheet_9


log = get_task_logger(__name__)


class BuildFileError(Exception):
    """
    Exception raised when there is an error while creating the repository.
    """


class SheetNameError(Exception):
    """
    Exception raised when there is an error while creating the repository.
    """


def internal_build_cne_sheets(
    settings,
    form_schema,
    zip_file,
    task_object=None,
):
    uid = str(uuid.uuid4())
    paths = ["tmp", uid]
    temp_dir = os.path.join(settings["repository.path"], *paths)
    os.makedirs(temp_dir)
    paths = ["tmp", uid, "cuadro_8.xlsx"]
    sheet_8_file = os.path.join(settings["repository.path"], *paths)
    generate_sheet_8(settings, form_schema, sheet_8_file)

    if task_object is not None:
        if task_object.is_aborted():
            return False, zip_file

    paths = ["tmp", uid, "cuadro_9.xlsx"]
    sheet_9_file = os.path.join(settings["repository.path"], *paths)
    generate_sheet_9(settings, form_schema, sheet_9_file)

    with zipfile.ZipFile(
        file=zip_file, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as out_zip:
        for f in glob.glob(temp_dir + "/*.xlsx"):
            out_zip.write(f, arcname=os.path.basename(f))

    return True, zip_file


@celeryApp.task(bind=True, base=CeleryTask)
def build_cne_sheets(
    self,
    settings,
    form_schema,
    zip_file,
):
    internal_build_cne_sheets(settings, form_schema, zip_file, self)
