from django import template

register = template.Library()

@register.simple_tag
def get_page_range(page, max_pages):
    num_pages = page.paginator.num_pages
    page_number = page.number

    start = max(page_number - max_pages // 2, 1)
    end = min(start + max_pages, num_pages + 1)

    start = max(end - max_pages, 1)

    return range(start, end)