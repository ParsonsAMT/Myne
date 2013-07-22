import urllib, pycurl, cStringIO, BeautifulSoup

from BeautifulSoup import BeautifulSoup,BeautifulStoneSoup

from django.conf import settings
from settings import HAYSTACK_SOLR_URL
import string 

from django.core.paginator import InvalidPage, EmptyPage
from django import template
register = template.Library()

from django.core.mail import EmailMessage

# this just adds an email prefix from settings to all Datamyne
# emails. but might do more stuff later
class DataminingEmail(EmailMessage):
    def __init__(self,*args,**kwargs):
        super(DataminingEmail,self).__init__(*args,**kwargs)
        self.subject = "%s%s" % (settings.EMAIL_SUBJECT_PREFIX, self.subject)

class NamePaginator(object):
    """Pagination for string-based objects"""
    
    def __init__(self, object_list, on=None, per_page=25):
        self.object_list = object_list
        self.count = len(object_list)
        self.pages = []
        
        # chunk up the objects so we don't need to iterate over the whole list for each letter
        chunks = {}
        
        for obj in self.object_list:
            if on: obj_str = str(getattr(obj, on))
            else: obj_str = str(obj)
            
            letter = str.upper(obj_str[0])
            
            if letter not in chunks: chunks[letter] = []
            
            chunks[letter].append(obj)
        
        # the process for assigning objects to each page
        current_page = NamePage(self)
        
        for letter in string.ascii_uppercase:
            if letter not in chunks: 
                current_page.add([], letter)
                continue
            
            sub_list = chunks[letter] # the items in object_list starting with this letter
            
            new_page_count = len(sub_list) + current_page.count
            # first, check to see if sub_list will fit or it needs to go onto a new page.
            # if assigning this list will cause the page to overflow...
            # and an underflow is closer to per_page than an overflow...
            # and the page isn't empty (which means len(sub_list) > per_page)...
            if new_page_count > per_page and \
                    abs(per_page - current_page.count) < abs(per_page - new_page_count) and \
                    current_page.count > 0:
                # make a new page
                self.pages.append(current_page)
                current_page = NamePage(self)
            
            current_page.add(sub_list, letter)
        
        # if we finished the for loop with a page that isn't empty, add it
        if current_page.count > 0: self.pages.append(current_page)
        
    def page(self, num):
        """Returns a Page object for the given 1-based page number."""
        if len(self.pages) == 0:
            return None
        elif num > 0 and num <= len(self.pages):
            return self.pages[num-1]
        else:
            raise InvalidPage
    
    @property
    def num_pages(self):
        """Returns the total number of pages"""
        return len(self.pages)

class NamePage(object):
    def __init__(self, paginator):
        self.paginator = paginator
        self.object_list = []
        self.letters = []
    
    @property
    def count(self):
        return len(self.object_list)
    
    @property
    def start_letter(self):
        if len(self.letters) > 0: 
            self.letters.sort(key=str.upper)
            return self.letters[0]
        else: return None
    
    @property
    def end_letter(self):
        if len(self.letters) > 0: 
            self.letters.sort(key=str.upper)
            return self.letters[-1]
        else: return None
    
    @property
    def number(self):
        return self.paginator.pages.index(self) + 1
    
    def add(self, new_list, letter=None):
        if len(new_list) > 0: self.object_list = self.object_list + new_list
        if letter: self.letters.append(letter)
    
    def __repr__(self):
        if self.start_letter == self.end_letter:
            return self.start_letter
        else:
            return '%c-%c' % (self.start_letter, self.end_letter)



def get_doc_contents(file_name,path): 
    params = {
        'literal.id': 'doc1',
        'uprefix': 'attr_',
        'commit': 'false',
        'defaultField': 'text',
        'extractOnly': 'true', 
        'captureAttr': 'true',
        'extractFormat': 'text',
        'resource.name': file_name
    }
    
    url = HAYSTACK_SOLR_URL + "/update/extract"
    
    if params is not None:
     fullURL = "%s?%s" % (url, urllib.urlencode(params))
    else:
     fullURL = url
    

    # upload binary file with pycurl by http post
    # http://stackoverflow.com/questions/256564/putting-a-pycurl-xml-server-response-into-a-variable-python
    response = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, fullURL)
    c.setopt(c.HTTPPOST, [("file1", (pycurl.FORM_FILE, str(path)))])
    c.setopt(c.WRITEFUNCTION, response.write)
    #c.setopt(c.VERBOSE, 1)
    c.perform()
    c.close()
    
    soup = BeautifulStoneSoup(response.getvalue())
    #print soup.prettify()
    doc = soup.find('str', attrs={'name':file_name})
    if doc: 
        #print doc.string.encode('ascii', 'replace')
        return doc.string                    

from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.utils import simplejson as json
from django.http import HttpResponse
from decimal import Decimal       
from datetime import datetime           

#############################################################################
# JSON Operations
##############################################################################
# borrowed from Dojango
def json_encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to an object dynamically are being ignored (and it also has 
    problems with some models).
    """

    def _any(data):
        ret = None
        # Opps, we used to check if it is of type list, but that fails 
        # i.e. in the case of django.newforms.utils.ErrorList, which extends
        # the type "list". Oh man, that was a dumb mistake!
        if isinstance(data, list):
            ret = _list(data)
        # Same as for lists above.
        elif isinstance(data, dict):
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, Model):
            ret = _model(data)
        # here we need to encode the string as unicode (otherwise we get utf-16 in the json-response)
        elif isinstance(data, basestring):
            ret = unicode(data)
        # see http://code.djangoproject.com/ticket/5868
        elif isinstance(data, Promise):
            ret = force_unicode(data)
        elif isinstance(data, datetime):
            # For dojo.date.stamp we convert the dates to use 'T' as separator instead of space
            # i.e. 2008-01-01T10:10:10 instead of 2008-01-01 10:10:10
            ret = str(data).replace(' ', 'T')
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return json.dumps(ret, cls=DateTimeAwareJSONEncoder)

def json_response(data):
    data = json_encode(data)
    mimetype = "text/json"
    ret = HttpResponse(data, mimetype=mimetype+"; charset=%s" % 'utf-8')
    # The following are for IE especially
    ret['Pragma'] = "no-cache"
    ret['Cache-Control'] = "must-revalidate"
    ret['If-Modified-Since'] = str(datetime.now())
    return ret        

if __name__ == "__main__":
    import doctest
    doctest.testmod()      
