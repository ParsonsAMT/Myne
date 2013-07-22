from datamining.apps.api.decorators import json_response    
from haystack.query import SearchQuerySet
from datamining.apps.profiles.models import FacultyMember,Course,Section

def _get_node_data(obj):
    node = []
            
    if type(obj) == FacultyMember: 
        for i in Section.objects.filter(instructors__pk = obj.pk):
            print i.course
            entry = {'score':0,'results':[]}
            entry['name'] = str(i.course)
            entry['id'] = "%s-%s" %('course', i.course.pk)
            entry['category'] = 'course'
            node.append(entry)
    elif type(obj) == Course:
        for i in Section.objects.filter(course__pk = obj.pk):
            for j in i.instructors.all():
                entry = {'score':0,'results':[]}
                entry['name'] = str(j)
                entry['id'] = "%s-%s" %('facultymember', j.pk)
                entry['category'] = 'facultymember'
                node.append(entry)   
    return node 

@json_response 
def req_related(request):
    if request.GET.get('query'):                   
        query = request.GET.get('query')
    else:
        query = 'motion graphics'
        
    #downplay courses and tags
    #upplay people and projects
    sqs = SearchQuerySet()
    sqs.query.add_model(FacultyMember)
    sqs.query.add_model(Course) 
    
    results = sqs.filter(content=query)    
    
    rsp = {'root': query, 'results': [] }   
    

    
    for i in results:  
        # n.b. can cause model collisions if two applications have a model by the same name
        # at the time of writing, this is neither the case nor expected in the near future
        # we are not using i.app_label in order to reduce JSON response output
        row = {
                'id': "%s-%s" %(i.model_name, i.pk), 
                'category': i.model_name,
                'score': i.score, 
                'name': str(i.object),
                'results': _get_node_data(i.object)                             
               }
        rsp['results'].append(row)

    return rsp