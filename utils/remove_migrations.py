import os, shutil

folders_to_look = ['dashboard', 'projetos']

print("Removing all migrations...")
for folder in folders_to_look:
    if os.path.isdir(os.path.join('.', folder,'migrations')):
        folder = os.path.join('.', folder,'migrations')
        for file in os.listdir(folder):
            if file != "__init__.py":
                file = os.path.join(folder,file)
                if os.path.isdir(file):
                    shutil.rmtree(file)
                if os.path.isfile(file):
                    os.remove(file)

print("Done!")