from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import UserPortfolio


def _serialize_portfolio(obj: UserPortfolio) -> dict:
    return {
        "id": obj.id,
        "name": obj.name,
        "sectors": obj.sectors,
        "commodities": obj.commodities,
        "result": obj.result,
        "created_at": obj.created_at.isoformat(),
        "updated_at": obj.updated_at.isoformat(),
    }


portfolio_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["result"],
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Optional portfolio name/label"),
        "sectors": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
        "commodities": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
        "result": openapi.Schema(type=openapi.TYPE_OBJECT, description="Raw portfolio result payload returned by the training API"),
    },
)


portfolio_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "sectors": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
        "commodities": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
        "result": openapi.Schema(type=openapi.TYPE_OBJECT),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
        "updated_at": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
    },
)


@swagger_auto_schema(
    method="post",
    request_body=portfolio_request_schema,
    responses={
        201: openapi.Response("Created portfolio", portfolio_response_schema),
        400: "Bad Request",
        401: "Unauthorized",
    },
)
@swagger_auto_schema(
    method="get",
    responses={
        200: openapi.Response(
            "List of portfolios for the authenticated user",
            openapi.Schema(type=openapi.TYPE_ARRAY, items=portfolio_response_schema),
        ),
        401: "Unauthorized",
    },
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user_portfolios(request):
    """List or create portfolios for the authenticated user.

    GET  -> return all portfolios (most recent first) for the user.
    POST -> create a new portfolio record from the provided result payload.
    """

    user = request.user

    if request.method == "POST":
        data = request.data
        result = data.get("result")
        if result is None:
            return Response({"error": "'result' field is required"}, status=status.HTTP_400_BAD_REQUEST)

        name = data.get("name", "")
        sectors = data.get("sectors")
        commodities = data.get("commodities")

        obj = UserPortfolio.objects.create(
            user=user,
            name=name,
            sectors=sectors,
            commodities=commodities,
            result=result,
        )
        return Response(_serialize_portfolio(obj), status=status.HTTP_201_CREATED)

    # GET -> list
    qs = UserPortfolio.objects.filter(user=user).order_by("-created_at")
    return Response([_serialize_portfolio(p) for p in qs], status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="get",
    responses={
        200: openapi.Response("Latest portfolio for the authenticated user", portfolio_response_schema),
        401: "Unauthorized",
        404: "Not Found - user has no saved portfolio",
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def latest_user_portfolio(request):
    """Return the most recently saved portfolio for the authenticated user."""

    user = request.user
    obj = UserPortfolio.objects.filter(user=user).order_by("-created_at").first()
    if obj is None:
        return Response({"detail": "No saved portfolio for this user."}, status=status.HTTP_404_NOT_FOUND)
    return Response(_serialize_portfolio(obj), status=status.HTTP_200_OK)
