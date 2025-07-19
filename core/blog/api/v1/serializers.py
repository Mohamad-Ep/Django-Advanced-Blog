from rest_framework import serializers
from ...models import Post,Category
from accounts.models import Profile
# __________________________________________________________

# class PostSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=50)
#     status = serializers.BooleanField(default=False)
    
# __________________________________________________________

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
# __________________________________________________________

class PostSerializer(serializers.ModelSerializer):
    # published_date = serializers.ReadOnlyField()
    # category = serializers.SlugRelatedField(slug_field='name',queryset=Category.objects.all(),many=False)
    author = serializers.StringRelatedField(read_only=True)
    relative_url = serializers.URLField(source='get_absolute_api_url',read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')
    
    class Meta:
        model = Post
        fields = ['id','title','status','relative_url','published_date','author','category','absolute_url']
        read_only_fields = ['published_date']
        
    def get_abs_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
         
    def to_representation(self, instance):                  # تابعی برای تغییر فیلدها در زمان نمایش
        rep = super().to_representation(instance)
        request = self.context.get('request')
        # print(request.__dict__)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('relative_url')
            rep.pop('absolute_url')
        else:
            rep.pop('author')
            
        rep['category'] = CategorySerializer(instance.category).data
        rep['name'] = 'test'
        return rep
    
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)
# __________________________________________________________
