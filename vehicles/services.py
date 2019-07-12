from serious_django_services import Service

### Define your services here.

# EXAMPLE:
# class SomeServiceSpecificException(Exception):
#    pass
# 
# 
# class SomeService(Service):
#    service_exceptions = (SomeServiceSpecificException,)
# 
#    @classmethod
#    def get_something(cls, user):
#        cls.require_permission(user, SomePermission)
#        queryset = Something.objects.all()
#        return queryset
# 
#    @classmethod
#    def do_something(cls, user, data):
#        cls.require_permission(user, SomeOtherPermission)
# 
#        something = foo()
#        if not ...:
#            raise SomeServiceSpecificException("oh no!")
#        else:
#            return something
