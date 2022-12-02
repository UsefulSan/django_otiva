from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView

from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Categories, Ads, Selection
from ads.permissions import SelectionUpdatePermission, AdsUpdatePermission
from ads.serializers import AdDetailViewSerializer, SelectionViewSerializer, SelectionDetailViewSerializer, \
    SelectionCreateViewSerializer, AdDeleteViewSerializer, AdCreateViewSerializer, CategoriesViewSerializer


@csrf_exempt
def index(request):
    return JsonResponse({'text': 'Otiva REST API on Django REST framework'}, status=200)


class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesViewSerializer


class AdsListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        queryset = Ads.objects.select_related("author", "category").all().order_by("-price")
        category_search = request.GET.get('cat', None)
        if category_search:
            queryset = queryset.filter(category__id__icontains=category_search)
        ads_search = request.GET.get('text', None)
        if ads_search:
            queryset = queryset.filter(name__icontains=ads_search)
        place_search = request.GET.get('location', None)
        if place_search:
            queryset = queryset.filter(author__location__name__icontains=place_search)
        price_from, price_to = request.GET.get('price_from', None), request.GET.get('price_to', None)
        if price_from and price_to:
            queryset = queryset.filter(price__range=(price_from, price_to))

        paginator = Paginator(queryset, settings.TOTAL_ON_PAGE)
        page_num = int(request.GET.get("page", 1))
        page_obj = paginator.get_page(page_num)

        ads = []
        for ad in page_obj:
            ads.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author.first_name,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'image': ad.image.url if ad.image else None,
                'category': ad.category.name
            })
        response = {
            "items": ads,
            "page": page_num,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


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
