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
                    "message": "Nepodarilo sa uložiť náradie",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(available=True)
        return Response(
            data={
                "message": "Náradie uložené",
            },
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
        return Response(serializer.data)

    def put(self, request, id, format=None):
        tool = self.get_object(id)
        serializer = serializers.ToolSerializer(tool, data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "message": "Nepodarilo sa uložiť náradie",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(data={"message": "Náradie uložené"})

    def delete(self, request, id, format=None):
        tool = self.get_object(id)
        tool.delete()

        return Response(
            data={
                "message": "Náradie vymazané",
            },
        )
