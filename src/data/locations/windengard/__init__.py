# my_package/subpackages/__init__.py
import os

# Dynamically import all modules in the subpackage
package_dir = os.path.dirname(__file__)
for name in os.listdir(package_dir):
    if os.path.isfile(os.path.join(package_dir, name)) and name.endswith('.py') and not name.startswith('__'):
        module_name = os.path.splitext(name)[0]
        globals()[module_name] = __import__(f'{__name__}.{module_name}', fromlist=['*'])

# Specify which modules to expose
__all__ = [os.path.splitext(name)[0] for name in os.listdir(package_dir) if os.path.isfile(os.path.join(package_dir, name)) and name.endswith('.py') and not name.startswith('__')]