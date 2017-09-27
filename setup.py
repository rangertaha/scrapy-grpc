
from os.path import dirname, join
from setuptools import setup, find_packages


setup(
    name='scrapy-grpc',
    version='1.0',
    url='https://github.com/rangertaha/scrapy-grpc',
    description='Scrapy extension to control spiders using gRPC',
    author='rangertaha',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'Twisted>=10.0.0',
        'Scrapy>=0.24.0',
        'grpcio>=1.6.0',
        'six>=1.5.2',
    ],
)
