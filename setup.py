from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='textgenerator',
    version='1.0',
    license='BSD',
    description='Genetrate text by templates.',
    author='Shalamov Maxim',
    author_email='mvshalamov@gmail.com',
    company='Rambler&Co',
    install_requires=['pymorphy2==0.8', 'PyYAML==3.11'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ]
)