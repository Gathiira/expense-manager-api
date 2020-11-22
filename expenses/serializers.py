from rest_framework import serializers

from .models import ExpenseModel, IncomeModel


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model=ExpenseModel
        fields =['id','owner', 'category', 'amount', 'description', 'created_at']

        extra_kwargs = {
            'owner':{
                'write_only':True
            }
        }

        lookup_field = 'id'

        def validate(self, attrs):
            pass

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeModel
        fields = ['id', 'owner','source','amount','description','created_at']

        extra_kwargs = {
            'owner': {
                'write_only':True
            }
        }

    def validate(self, attrs):
        return attrs

    # def create(self, validated_data):
    #     pass