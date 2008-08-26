from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='slc.dbtableedit',
      version=version,
      description="Edit and View simple RDB Tables",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='edit relational database table',
      author='Syslab.comGmbH',
      author_email='info@syslab.com',
      url='http://svn.plone.org/svn/collective/slc.dbtableedit',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['slc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.lead>=1.0b3,<2.0dev'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
