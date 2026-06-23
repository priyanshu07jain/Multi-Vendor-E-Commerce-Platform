from django.utils.text import slugify

from apps.catalog.models import Category


class CategoryService:

    @staticmethod
    def create_category(
        name,
        description="",
        parent=None,
    ):

        return Category.objects.create(
            name=name,
            slug=slugify(name),
            description=description,
            parent=parent,
        )