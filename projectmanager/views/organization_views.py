from django.shortcuts import render, get_object_or_404
from projectmanager.models import Organization


def organization_list(request):
    organizations = Organization.objects.order_by('name')[:5]
    context = {'organizations': organizations, }
    return render(request, 'projectmanager/organization/index.html', context)


def organization_details(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    return render(request, 'projectmanager/organization/detail.html', {'organization': organization})
