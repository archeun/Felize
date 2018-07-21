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
                'config': {
                    'url': {
                        'view_name': 'projectmanager:update_project',
                        'params': [
                            {'name': 'pk', 'getter': 'id'}
                        ]
                    }
                }
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
# wickann92
# Wicky_1


# anudiesoftv2v12ANU
