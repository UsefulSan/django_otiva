from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Categories, Ads, Selection
from ads.permissions import SelectionUpdatePermission, AdsUpdatePermission
from ads.serializers import AdDetailViewSerializer, SelectionViewSerializer, SelectionDetailViewSerializer, \
    SelectionCreateViewSerializer, AdDeleteViewSerializer, AdCreateViewSerializer, CategoriesViewSerializer, \
    AdListViewSerializer


@csrf_exempt
def index(request):
    return JsonResponse({'text': 'Otiva REST API on Django REST framework'}, status=200)


class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesViewSerializer


class AdsListView(ListAPIView):
    # model = Ads
    queryset = Ads.objects.all()
    serializer_class = AdListViewSerializer

    def get(self, request, *args, **kwargs):
        ad_cat = request.GET.get('cat')
        if ad_cat:
            self.queryset = self.queryset.filter(category__id__exact=ad_cat)

        ad_name = request.GET.get('text')
        if ad_name:
            self.queryset = self.queryset.filter(name__icontains=ad_name)

        ad_city = request.GET.get('location')
        if ad_city:
            self.queryset = self.queryset.filter(
                author__location__name__icontains=ad_city)

        price_from = request.GET.get('price_from', 0)
        price_to = request.GET.get('price_to', 100000)
        if price_from or price_to:
            self.queryset = self.queryset.filter(
                price__range=[price_from, price_to])

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdDetailViewSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdCreateViewSerializer
    permission_classes = [IsAuthenticated]


class AdDeleteApiView(DestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdDeleteViewSerializer
    permission_classes = [IsAuthenticated, AdsUpdatePermission]


class AdUpdateApiView(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdDeleteViewSerializer
    permission_classes = [IsAuthenticated, AdsUpdatePermission]


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateImageView(UpdateView):
    model = Ads
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES["image"]

        self.object.save()

        return JsonResponse({
            "name": self.object.name,
            "image": self.object.image.url if self.object.image else None
        })


class SelectionView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionViewSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailViewSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateViewSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateViewSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateViewSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]
