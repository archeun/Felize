from django import template
from projectmanager.services import list_service

register = template.Library()


@register.inclusion_tag('lib/list_component.html')
def render_list(list_items, list_config):
    prepared_list_items = []
    for list_item in list_items:
        prepared_list_item = []
        for col in list_config['cols']:
            if col['value_getter_type'] == list_service.VALUE_GETTER_TYPE_ATTR_CHAIN:
                curr_attr = list_item
                for value_getter in col['value_getter']:
                    curr_attr = getattr(curr_attr, value_getter)
                prepared_list_item.append(curr_attr)
            else:
                prepared_list_item.append(getattr(list_item, col['value_getter']))
        prepared_list_items.append(prepared_list_item)
    return {'list_items': prepared_list_items, 'list_config': list_config, 'page_obj': list_items}
