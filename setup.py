from setuptools import setup, find_packages

setup(name='clean_folder',
      version='0.0.1',
      description='Sort and clean disordered folders',
      url="https://github.com/YaroslavaSegal/SORT_DIR/clean_folder",
      author='Yaroslava_Segal',
      author_email='yaroslavasiehal@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']},
      zip_safe=False)
