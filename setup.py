from setuptools import setup, find_packages


setup(
    name='gocept.exttest',
    version='1.1.dev0',
    author='gocept gmbh & co. kg',
    author_email='mail@gocept.com',
    url='https://bitbucket.org/gocept/gocept.exttest',
    description="Helper to integrate external tests with python unittests.",
    long_description=(
        open('README.txt').read() +
        '\n\n' +
        open('CHANGES.txt').read()),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='ZPL',
    namespace_packages=['gocept'],
    install_requires=[
        'setuptools',
        'zc.recipe.testrunner',
    ],
    extras_require=dict(test=[
        'mock',
    ]),
)
