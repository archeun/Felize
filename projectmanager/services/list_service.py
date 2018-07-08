VALUE_GETTER_TYPE_ATTR_SINGLE = 'single_attr'
VALUE_GETTER_TYPE_ATTR_CHAIN = 'chain_attr'


def get_project_list_config(params):
    return {
        'params': params,
        'cols': [
            {
                'name': 'Project Code',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_SINGLE,
                'value_getter': 'code',
            },
            {
                'name': 'Name',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_SINGLE,
                'value_getter': 'name',
            },
            {
                'name': 'Client Name',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_CHAIN,
                'value_getter': ['client', 'name'],
            }
        ]
    }
