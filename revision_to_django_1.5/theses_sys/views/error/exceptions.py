import warnings

from django import http
from django.template import (Context, RequestContext,
                             loader, Template, TemplateDoesNotExist)


def page_not_found(request, template_name='404.html'):
    try:
        template = loader.get_template(template_name)
        content_type = None             # Django will use DEFAULT_CONTENT_TYPE
    except TemplateDoesNotExist:
        template = Template(
            '<h1>Not Found</h1>'
            '<p>The requested URL {{ request_path }} was not found on this server.</p>')
        content_type = 'text/html'
    body = template.render(RequestContext(request, {'request_path': request.path}))
    return http.HttpResponseNotFound(body, content_type=content_type)


def server_error(request, template_name='500.html'):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')
    return http.HttpResponseServerError(template.render(Context({})))


def bad_request(request, template_name='400.html'):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseBadRequest('<h1>Bad Request (400)</h1>', content_type='text/html')
    return http.HttpResponseBadRequest(template.render(Context({})))


def permission_denied(request, template_name='403.html'):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return http.HttpResponseForbidden(template.render(RequestContext(request)))