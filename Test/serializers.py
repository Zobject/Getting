from rest_framework import serializers
from Test.models import Test

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)

    class Meta:
        model = Test
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Test.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.save()
        return instance