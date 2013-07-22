from django.http import HttpResponseServerError
from datamining.libs.utils import json_response as json_resp
         
# borrowed from Django


def json_response(func):
    """
    This is what this function does

    :param func:
    """
    def _ret(*args, **kwargs):

        """

        :param args:
        :param kwargs:
        :return: :rtype:
        """

        return_value = func(*args, **kwargs)

        ret = {}

        if return_value is False:
            ret['success'] = False
        else:
            ret['success'] = True

        try:
            # Sometimes the serialization fails, i.e. when there are too deeply nested objects or even classes inside
            json_ret = json_resp(ret)
        except TypeError, e:
            print u'\n\n===============Exception=============\n\n' + unicode(e) + u'\n\n'
            print ret
            print '\n\n'

            return HttpResponseServerError(content=str(e))

        return json_ret
    return _ret
