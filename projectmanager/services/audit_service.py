from reversion.models import Version


def get_previous_for_version(versioned_obj, date):
    """Returns the latest version of an object prior to the given date."""
    versions = Version.objects.get_for_object(versioned_obj)
    versions = versions.filter(revision__date_created__lt=date)
    try:
        version = versions[0]
    except IndexError:
        return None
    else:
        return version


def get_audit_feed_data(versions):
    feed = []
    for version in versions:
        current = version.object
        previous = get_previous_for_version(current, version.revision.date_created)
        model_field_dict = None
        if previous:
            model_field_dict = previous.field_dict
        feed_entry = current.get_diff_feed_entry(model_field_dict)
        if feed_entry != {}:
            feed_entry['changed_date'] = version.revision.date_created
            feed_entry['user'] = version.revision.user
        feed.append(feed_entry)
    return feed
