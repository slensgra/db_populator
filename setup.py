from setuptools import setup, find_packages

setup(
    name='db_populator',
    version='1.0.1',
    description="Port of DDF for algorithmically creating an initial dataset",
    long_description=open("README.md").read(),
    author='Samuel Lensgraf',
    author_email='sam.lensgraf@gmail.com',
    url='http://github.com/slensgra/db_populator',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        "django >= 1.4",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
    keywords='django,database,graph',
)
