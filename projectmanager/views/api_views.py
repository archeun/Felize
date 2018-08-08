from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from projectmanager.models import Project


class ProjectResourcesChartJsView(APIView):
    """
    Returns the Json response required to build the project-resource chartjs chart.

    * Only admin users are able to access this view.
    """
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format='json'):
        """
        Return a list of all users.
        """
        project_resources = [{'name': project.name, 'count': project.resources.count()} for project in Project.objects.all()]
        return Response(project_resources)
