from setuptools import setup, find_packages

setup(
    name='yuan_dl',
    version='0.1.0',
    packages=['Yuan'],
    install_requires=[
        'pyyaml>=6.0.1'
    ],
    author='NauyHL',
    author_email='liuhy.df.xin@gmail.com',
    description='Provided Simple Tools for Experiment Programming',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NuayHL/Yuan',
    license='LICENSE',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: System :: Logging"
    ],
)