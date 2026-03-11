from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Testing, Transaction, Budget
from core.serializers import TestingSerializer, TransactionSerializer, BudgetSerializer


# ---------------- BASIC TESTING VIEWS ----------------

def testing_view(request):
    testing_records = Testing.objects.all()
    serializer = TestingSerializer(testing_records, many=True)
    return JsonResponse(serializer.data, safe=False)


def testing_detail_view(request, id):
    testing = get_object_or_404(Testing, id=id)
    serializer = TestingSerializer(testing)
    return JsonResponse(serializer.data)


def health_check(request):
    return JsonResponse({'status': 'ok'})


# ---------------- TRANSACTION CRUD ----------------

class TransactionListView(APIView):
    """
    GET  /api/transactions/  -> List all transactions
    POST /api/transactions/  -> Create new transaction
    """

    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):
    """
    GET    /api/transactions/<id>/
    PUT    /api/transactions/<id>/
    DELETE /api/transactions/<id>/
    """

    def get_object(self, id):
        try:
            return Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, id):
        transaction = self.get_object(id)

        if transaction is None:
            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, id):
        transaction = self.get_object(id)

        if transaction is None:
            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(transaction, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        transaction = self.get_object(id)

        if transaction is None:
            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- BUDGET API (Challenge 3) ----------------

class BudgetListView(APIView):
    """
    GET  /api/budgets/  -> List all budgets
    POST /api/budgets/  -> Create a new budget
    """

    def get(self, request):
        budgets = Budget.objects.all()
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)