from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from tools.models import Tool


class ToolsList(APIView):
    """
    List all tools, or create a new tool.
    """

    serializer_class = serializers.ToolSerializer

    def get(self, request, format=None):
        tools = Tool.objects.all()
        serializer = self.serializer_class(tools, many=True)

        return Response(data=serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(available=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ToolDetail(APIView):
    """
    Retrieve, update or delete a tool instance.
    """

    def get_object(self, id):
        try:
            return Tool.objects.get(pk=id)
        except Tool.DoesNotExist:
            raise NotFound()

    def get(self, request, id, format=None):
        tool = self.get_object(id)
        serializer = serializers.ToolSerializer(tool)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        tool = self.get_object(id)
        serializer = serializers.ToolSerializer(tool, data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        tool = self.get_object(id)
        deleted_rows = tool.delete()

        if len(deleted_rows) <= 0:
            return Response(
                data={
                    "errors": {"global": "Nepodarilo sa vymazať nástroj"},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class BulkToolsList(APIView):
    """
    Bulk list tools
    """

    serializer_class = serializers.ToolSerializer

    def post(self, request, format=None):
        if not isinstance(request.data, list):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

        tools = Tool.objects.filter(id__in=request.data)
        serializer = self.serializer_class(tools, many=True)

        return Response(data=serializer.data)
