import os

from setuptools import setup, Command

version = "0.1.0"

def readme():
    with open("README.md") as r:
        return r.read()


class VersionCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    name='classyconf',
    version=version,
    description='Extensible library for separation of settings from code.',
    long_description=readme(),
    author="Hernan Lozano", author_email="hernantz@gmail.com",
    license="MIT",
    packages=['classyconf'],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ],
    url='http://github.com/hernantz/classyconf',
    download_url='https://github.com/hernantz/classyconf/tarball/{}'.format(version),
    cmdclass={'version': VersionCommand},
    test_suite="tests",
)
