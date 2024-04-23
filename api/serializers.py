from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Expense
from .utils import get_expense_from_audio
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        # No one can read the password
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "url",
            # "response",
            "product",
            "total",
            "category",
            "created_at",
            "author",
        ]
        extra_kwargs = {
            # "response": {"read_only": True},
            "product": {"read_only": True},
            "total": {"read_only": True},
            "category": {"read_only": True},
            "author": {"read_only": True},
        }

    def create(self, validated_data):

        expense_instance = Expense(**validated_data)
        response = get_expense_from_audio(validated_data["url"])
        # expense_instance.response = response
        expense_instance.product = response["product"]
        expense_instance.total = response["total"]
        expense_instance.category = response["category"]
        expense_instance.save()
        return expense_instance
