from rest_framework import serializers

from ads.models import Ads, Selection, Categories
from users.models import Users


class CheckFalse:
    def __call__(self, value):
        if value:
            raise serializers.ValidationError('The ad cannot be published at the time of creation')


class CategoriesViewSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(min_length=5)

    class Meta:
        model = Categories
        fields = '__all__'


class AdListViewSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Ads
        fields = ['name', 'category']


class AdDetailViewSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(slug_field='first_name', read_only=True)

    class Meta:
        model = Ads
        fields = '__all__'


class AdCreateViewSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='id', queryset=Categories.objects.all())
    author = serializers.SlugRelatedField(slug_field='id', queryset=Users.objects.all())
    is_published = serializers.BooleanField(validators=[CheckFalse()])
    name = serializers.CharField(min_length=10)

    class Meta:
        model = Ads
        fields = '__all__'


class AdDeleteViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        exclude = ['author']


class SelectionDetailViewSerializer(serializers.ModelSerializer):
    items = AdDetailViewSerializer(many=True, read_only=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateViewSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field='id',
        queryset=Ads.objects.all())
    owner = serializers.SlugRelatedField(required=False, slug_field='id', queryset=Users.objects.all())

    class Meta:
        model = Selection
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._items = self.initial_data.pop("items")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        request = self.context.get('request', None)
        selection = Selection.objects.create(**validated_data, owner_id=request.user.id)

        for item in self._items:
            item_obj, _ = Ads.objects.get_or_create(pk=item)
            selection.items.add(item_obj)
        selection.save()
        return selection

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.items.clear()
        for item in self._items:
            item_obj, _ = Ads.objects.get_or_create(pk=item)
            instance.items.add(item_obj)
        instance.save()
        return instance


class SelectionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']
