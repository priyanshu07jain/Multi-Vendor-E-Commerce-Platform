from apps.catalog.models import Category

class CategorySelector:

    @staticmethod
    def get_categories():

        return (
            Category.objects
            .filter(
                is_active=True
            )
            .select_related(
                "parent"
            )
        )
    


