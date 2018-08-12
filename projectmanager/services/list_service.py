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


def get_project_resource_list_config(params):
    return {
        'params': params,
        'cols': [
            {
                'name': 'Name',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_CHAIN,
                'value_getter': ['employee', 'get_full_name'],
                'config': {
                    'url': {
                        'view_name': 'projectmanager:update_project_resource',
                        'params': [
                            {'name': 'pk', 'getter': 'id'}
                        ]
                    }
                }
            },
            {
                'name': 'Resource Type',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_SINGLE,
                'value_getter': 'resource_type',
            },
            {
                'name': 'Allocation Starts',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_SINGLE,
                'value_getter': 'allocation_start_date',
            },
            {
                'name': 'Allocation Ends',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_SINGLE,
                'value_getter': 'allocation_end_date',
            },
            {
                'name': 'Work Hours per Day',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_SINGLE,
                'value_getter': 'work_hours_per_day',
            }
        ]
    }


def get_audit_list_config(params):
    return {
        'params': params,
        'cols': [
            {
                'name': 'Object',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_SINGLE,
                'value_getter': 'revision',
                'config': {
                    'url': {
                        'view_name': 'projectmanager:audit_detail',
                        'params': [
                            {'name': 'pk', 'getter': 'id'}
                        ]
                    }
                }
            },
            {
                'name': 'Type',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_SINGLE,
                'value_getter': 'content_type',
            },
            {
                'name': 'Data',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_SINGLE,
                'value_getter': 'serialized_data',
            },
            {
                'name': 'User',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_CHAIN,
                'value_getter': ['revision', 'user'],
            },
            {
                'name': 'Date/Time',
                'value_getter_type': VALUE_GETTER_TYPE_ATTR_CHAIN,
                'value_getter': ['revision', 'date_created'],
            }
        ]
    }
