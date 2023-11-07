import setuptools
from setuptools import setup
import glob

setup(
	name='techdocs',
<<<<<<< HEAD:techdocs/setup.py
	version='0.2.0',
=======
	version='0.2.1',
>>>>>>> 7b80f1bcac446d89a72c4146689db74f434ec4c6:setup.py
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'techdocs=techdocs.cli:main'
        ],    
    },
    python_requires='>=3.10',


    data_files=glob.glob('techdocs/signatures/**'),
    include_package_data=True,

    packages=setuptools.find_packages(),
)