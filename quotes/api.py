from django.http.response import HttpResponse
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import csrf_exempt, Resource, ModelResource
from quotes.models import Quote
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie import http
import logging
 
class BaseCorsResource(Resource):
    def error_response(self, *args, **kwargs):
        response = super(BaseCorsResource, self).error_response(*args, **kwargs)
        return self.add_cors_headers(response, expose_headers=True)
        
    def add_cors_headers(self, response, expose_headers=False):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'content-type, authorization'
        if expose_headers:
            response['Access-Control-Expose-Headers'] = 'Location'
        return response    
    
    def create_response(self, *args, **kwargs):
        """
        Create the response for a resource. Note this will only
        be called on a GET, POST, PUT request if 
        always_return_data is True
        """
        response = super(BaseCorsResource, self).create_response(*args, **kwargs)
        return self.add_cors_headers(response)
 
    def post_list(self, request, **kwargs):
        """
        In case of POST make sure we return the Access-Control-Allow Origin
        regardless of returning data
        """
        #logger.debug("post list %s\n%s" % (request, kwargs));
        response = super(BaseCorsResource, self).post_list(request, **kwargs)
        return self.add_cors_headers(response, True)
    
    def post_detail(self, request, **kwargs):
        """
        In case of POST make sure we return the Access-Control-Allow Origin
        regardless of returning data
        """
        #logger.debug("post detail %s\n%s" (request, **kwargs));
        response = super(BaseCorsResource, self).post_list(request, **kwargs)
        return self.add_cors_headers(response, True)
    
    def put_list(self, request, **kwargs):
        """
        In case of PUT make sure we return the Access-Control-Allow Origin
        regardless of returning data
        """
        response = super(BaseCorsResource, self).put_list(request, **kwargs)
        return self.add_cors_headers(response, True)    
    
    def put_detail(self, request, **kwargs):
        response = super(BaseCorsResource, self).put_detail(request, **kwargs)
        return self.add_cors_headers(response, True)
        
    def method_check(self, request, allowed=None):
        """
        Check for an OPTIONS request. If so return the Allow- headers
        """
        if allowed is None:
            allowed = []
            
        request_method = request.method.lower()
        allows = ','.join(map(lambda s: s.upper(), allowed))
 
        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response['Access-Control-Allow-Methods'] = "GET, PUT, POST, PATCH"
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)
 
        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)
 
        return request_method
    
    def wrap_view(self, view):
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            request.format = kwargs.pop('format', None)
            wrapped_view = super(BaseCorsResource, self).wrap_view(view)
            return wrapped_view(request, *args, **kwargs)
        return wrapper

class QuoteResource(BaseCorsResource, ModelResource):
    class Meta:
        object_class = Quote                                                # Object class of resource
        fields = ['quote', 'source', 'date']
        queryset = Quote.objects.all()                                      # Method that will get objects collection
        resource_name = 'quote'                                                 # Resource name that will be used while usage
        authorization = Authorization()                                         # Authorization method (Currently always authorized)
        always_return_data = True
        filtering = {
            'date': ['exact', 'gt', 'lt', 'gte', 'lte']
        }
