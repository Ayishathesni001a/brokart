from django import template

register = template.Library()

@register.filter(name='chunks')
def chunks(list_data, chunk_size):
    if not list_data:  # Handle None or empty list
        return []
    
    chunk = []
    for i, data in enumerate(list_data):
        chunk.append(data)
        if (i + 1) % chunk_size == 0:  # Use modulo for cleaner logic
            yield chunk
            chunk = []
    
    if chunk:  # Yield any remaining items in the last chunk
        yield chunk
