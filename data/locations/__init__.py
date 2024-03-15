# my_package/__init__.py
import os

# Dynamically import all subpackages
package_dir = os.path.dirname(__file__)
for name in os.listdir(package_dir):
    if os.path.isdir(os.path.join(package_dir, name)) and not name.startswith('__'):
        globals()[name] = __import__(f'{__name__}.{name}', fromlist=['*'])

# Specify which subpackages to expose
__all__ = [name for name in os.listdir(package_dir) if os.path.isdir(os.path.join(package_dir, name)) and not name.startswith('__')]

