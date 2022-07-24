from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializers
from dev_projects.models import Project,Review,Tag

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'/api/dev_projects'},
        {'GET':'/api/dev_projects/id'},
        {'GET':'/api/dev_projects/id/vote'},

        {'POST':'/api/dev_users/token'},
        {'POST':'/api/dev_users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializers(projects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request,pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializers(project,many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def remove_Tag(request):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)
    project.tags.remove(tag)

    return Response('Tag was deleted')