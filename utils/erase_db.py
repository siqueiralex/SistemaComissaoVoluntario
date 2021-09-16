from django.apps import apps

models = apps.get_models()

print("Erasing all DB data...")
for model in models:
    model.objects.all().delete()
    
print("Done!")