from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Create groups."
    def handle(self, *args, **kwargs):

        # Banner
        print("-" * 100)
        print("Create groups.")
        print("-" * 100)

        # User entities
        ENTITIES = (
            'add_',
            'change_',
            'view_',
            'delete_',
        )

        # Database models 
        MODELS = (
            'brand',
            'device'
        )

        try:
            # Create dashboard admin 
            admin, created = Group.objects.get_or_create(name="Admin")

            if created:
                print("Group 'Admin' created.")
            else:
                print("Group 'Admin' already exists.")
                print("Overriding group 'Admin' with default permissions.")

            # Dashboard admin can add, change, view and delete everything
            for entity in ENTITIES:
                for model in MODELS:
                    perm = entity + model
                    perm_obj = Permission.objects.get(codename=perm)
                    admin.permissions.add(perm_obj)

            # Create dashboard user
            user, created = Group.objects.get_or_create(name="User")

            if created:
                print("Group 'User' created.")
            else:
                print("Group 'User' already exists.")
                print("Overriding group 'User' with default permissions.")
            
            # Dashboard user can only add and view data
            for entity in ENTITIES:
                for model in MODELS:
                    if model not in ('brand') and entity not in ('delete_', 'change_'):
                        perm = entity + model
                        perm_obj = Permission.objects.get(codename=perm)
                        user.permissions.add(perm_obj)
            
            print("-" * 100)
            print("Done")
            print("-" * 100)

        except KeyboardInterrupt:
            print("\n\nExiting...\n")
        except Exception as e:
            print("\n\nException caught: {}\n".format(e))
        

