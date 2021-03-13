from setuptools import setup


setup(
    name="gwtoolkit",
    version="0.0.1",
    license="MIT",
    author="David M. Brown",
    author_email="davebshow@gmail.com",
    description="Tools for working with groundwater data",
    url='',
    packages=['gwtoolkit'],
    extras_require={
        'test': ['pytest']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
    ]
)
