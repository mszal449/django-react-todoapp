from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from .models import Task
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.forms.models import model_to_dict
from django.http import HttpResponse


@csrf_exempt
def tasks(request):
    # Get the query parameters
    title = request.GET.get('title')
    description = request.GET.get('description')
    done = request.GET.get('done')
    fav = request.GET.get('fav')

    # Filter tasks based on query parameters (case-insensitive)
    tasks = Task.objects.all()

    if title is not None:
        tasks = tasks.filter(title__icontains=title)

    if description is not None:
        tasks = tasks.filter(description__icontains=description)

    if done is not None:
        tasks = tasks.filter(done=done.lower() == 'true')

    if fav is not None:
        tasks = tasks.filter(fav=fav.lower() == 'true')

    # Serialize tasks data
    data = {'tasks': list(tasks.values())}

    # Return JSON response
    return JsonResponse(data, status=200)


@csrf_exempt
def task(request, pk):
    try:
        found_task = Task.objects.get(id=pk)
        return JsonResponse({'task': model_to_dict(found_task)}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def task_create(request):
    # Extract data from the request
    data = json.loads(request.body)
    title = data.get("title")
    description = data.get("description")
    fav = data.get("fav", False)
    done = data.get("done", False)

    # Check if fields are complete
    if not title or not description:
        return JsonResponse({'message': 'Missing fields'}, status=400)

    new_task = Task(title=title, description=description, fav=fav, done=done)

    # Check if data is valid
    try:
        new_task.full_clean()
    except ValidationError as e:
        return JsonResponse({'message': 'Invalid fields', 'errors': dict(e)}, status=400)

    # Save
    new_task.save()
    return JsonResponse({'message': 'Task created', 'task': model_to_dict(new_task)}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def task_update(request, pk):
    found_task = Task.objects.get(id=pk)

    # Check if task exists
    if not found_task:
        return JsonResponse({'message': 'Task not found'}, status=404)

    data = json.loads(request.body)
    title = data.get('title')
    description = data.get('description')
    fav = data.get('fav')
    done = data.get('done')

    # update values
    if title:
        found_task.title = title
    if description:
        found_task.description = description
    if fav is not None:
        found_task.fav = fav
    if done is not None:
        found_task.done = done

    # Check if data is valid
    try:
        found_task.full_clean()
    except ValidationError as e:
        return JsonResponse({'message': 'Invalid fields', 'errors': dict(e)}, status=400)

    found_task.save()
    return JsonResponse({'message': 'Task updated', 'task': model_to_dict(found_task)}, status=204)


@csrf_exempt
@require_http_methods(["DELETE"])
def task_delete(request, pk):
    try:
        searched_task = Task.objects.get(id=pk)
        searched_task.delete()
        return HttpResponse(status=204)
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Task not found'}, status=404)
