from rest_framework import serializers
from dev_projects.models import Project,Tag,Review
from dev_users.models import Profile

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =  '__all__'

class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectSerializers(serializers.ModelSerializer):
    owner = ProfileSerializers(many=False)
    tags = TagSerializers(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializers(reviews,many=True)
        return serializer.data