from django.shortcuts import render
from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ContactSerializer
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response


class ContactAPIView(views.APIView):
    """
    A simple APIView for creating contact entires.
    """

    serializer_class = ContactSerializer

    def get_serializer_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        try:
            # Parse the JSON we receive from the client
            data = JSONParser().parse(request)
            # We serialize that data to point the JSON fields to the right model fields
            serializer = ContactSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                # If the data is valid according to the types and constraints we
                # added in the serializer, we save it to the db
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse(
                {"result": "error", "message": "Json decoding error"}, status=400
            )
