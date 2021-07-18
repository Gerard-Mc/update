from django.shortcuts import render
from checkout.models import OrderLineItem, Category


def portfolio(request):
    """ View displays all products and sorts by categories """
    # All products loaded when page loads.
    products = OrderLineItem.objects.all()
    # categories_string is a conversion from list to string.
    # to be used in a query string for user sorting options in portfolio.html.
    categories_string = ""
    # Default sort and direction to be displayed in the HTML dropdown menu.
    sort_display = ""
    direction_display = ""
    # category_sort_display for HTML dropdown. Sent through the view context.
    # Default is "Rating DESC"
    category_sort_display = "Rating DESC"
    active_category = ""

    if request.GET:
        if 'category' in request.GET:
            # split() splits the string into a list
            categories = request.GET['category'].split(",")
            #  Filter products to the above category/categories.
            products = products.filter(category__name__in=categories)
            # Converting the list back to string.
            if len(categories) > 1:
                for i in range(len(categories)):
                    # Adds comma to maintain the established format.
                    categories_string += "" + categories[i] + ","
                # Removes comma after final word.
                categories_string = categories_string[:-1]
                active_category = "all"
            else:
                # Converts lists with a single item to string.
                for i in categories:
                    categories_string += i
                    active_category = i
            # Takes sort parameter value from URL.
            if 'sort' in request.GET:
                sort = request.GET['sort']
                sort_display = sort.capitalize()
                # Checks the direction param value.
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    direction_display = direction.upper()
                    # Inverts the sort direction.
                    if direction == 'desc':
                        direction_display = direction.upper()
                        sort = f'-{sort}'
                        products = products.order_by(sort)
                # Sort products by chosen entity field.
                products = products.order_by(sort)
                category_sort_display = sort_display + " " + direction_display

    context = {
        'active_category': active_category,
        'category_sort_display': category_sort_display,
        'products': products,
        'category': categories_string,
    }

    return render(request, 'products/portfolio.html', context)
