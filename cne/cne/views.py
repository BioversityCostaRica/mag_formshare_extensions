from formshare.plugins.utilities import FormSharePrivateView
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from formshare.processes.db import get_project_id_from_name, get_form_data
from formshare.processes.odk.api import get_odk_path
from cne.product.cne_sheets import generate_cne_sheets


class ExportCNESheets(FormSharePrivateView):
    def process_view(self):
        user_id = self.request.matchdict["userid"]
        project_code = self.request.matchdict["projcode"]
        form_id = self.request.matchdict["formid"]
        project_id = get_project_id_from_name(self.request, user_id, project_code)
        project_details = {}
        if project_id is not None:
            project_found = False
            for project in self.user_projects:
                if project["project_id"] == project_id:
                    project_found = True
                    project_details = project
            if not project_found:
                raise HTTPNotFound
        else:
            raise HTTPNotFound

        if project_details["access_type"] >= 4:
            raise HTTPNotFound

        form_data = get_form_data(self.request, project_id, form_id)
        if form_data is None:
            raise HTTPNotFound

        if self.request.method == "POST":
            self.returnRawViewResult = True

            location = self.request.route_url(
                "form_download_cne_sheets",
                userid=user_id,
                projcode=project_code,
                formid=form_id,
            )
            return HTTPFound(location=location)

        return {
            "projectDetails": project_details,
            "formid": form_id,
            "formDetails": form_data,
            "userid": user_id,
        }


class GenerateCNESheets(FormSharePrivateView):
    def __init__(self, request):
        FormSharePrivateView.__init__(self, request)
        self.checkCrossPost = False
        self.returnRawViewResult = True

    def process_view(self):
        user_id = self.request.matchdict["userid"]
        project_code = self.request.matchdict["projcode"]
        form_id = self.request.matchdict["formid"]
        options = int(self.request.params.get("options", "1"))
        project_id = get_project_id_from_name(self.request, user_id, project_code)
        project_details = {}
        if project_id is not None:
            project_found = False
            for project in self.user_projects:
                if project["project_id"] == project_id:
                    project_found = True
                    project_details = project
            if not project_found:
                raise HTTPNotFound
        else:
            raise HTTPNotFound

        form_data = get_form_data(self.request, project_id, form_id)
        if form_data is None:
            raise HTTPNotFound

        if project_details["access_type"] >= 4:
            raise HTTPNotFound

        odk_dir = get_odk_path(self.request)
        generate_cne_sheets(
            self.request,
            self.user.id,
            project_id,
            form_id,
            odk_dir,
            form_data["form_schema"],
            options,
        )

        next_page = self.request.route_url(
            "form_details",
            userid=user_id,
            projcode=project_code,
            formid=form_id,
            _query={"tab": "task", "product": "cne_sheets"},
            _anchor="products_and_tasks",
        )
        self.returnRawViewResult = True
        return HTTPFound(location=next_page)
