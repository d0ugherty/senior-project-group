from django import template
register = template.Library()

@register.filter
def schedule_week(indexable):
    list = [None, None, None, None, None, None, None,None]
    list[0]=(indexable[0])
    print(len(indexable))

    #for x in (1,len(indexable)+1):
        #day = x.day_of_week
        #print(day)



    print(list)
    return None