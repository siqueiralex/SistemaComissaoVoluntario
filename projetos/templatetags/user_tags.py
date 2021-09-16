from django import template

register = template.Library()


@register.filter('has_group')
def has_group(user, group_name):
    """
    Verifica se este usuário pertence a um grupo
    """
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False

@register.filter('index')
def index(list, i):
    
    return list[i]

@register.filter('day')
def atribute(item):
    
    return item.day

@register.filter('month')
def atribute(item):
    
    return item.month

@register.filter('fds')
def atribute(item):
    
    return item.weekday() >=5