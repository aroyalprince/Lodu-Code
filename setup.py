from setuptools import setup, find_packages

setup(
    name='lodu-code',
    version='1.0.1',
    description='The Official Desi Programming Language built by Prince Kumar Pandit.',
    long_description='Lodu Code is a fully functional, desi programming language that uses Hindi slangs for syntax. Build variables, loops, conditions, arrays, and functions with absolute swag.',
    author='Prince Kumar Pandit',
    author_email='artistkprincekumar@gmail.com',  # <-- BHAI YAHAN APNA ASLI EMAIL DAAL DENA
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lodu=lodu.lodu_runner:main',  # <-- YE SABSE ZAROORI HAI! Ye tera 'lodu' terminal command banayega
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)