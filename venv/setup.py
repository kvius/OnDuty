from setuptools import setup, find_packages

setup(
    name='OnDuty',
    version='0.1',
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'PyQt5==5.15.4',
        # Додайте інші залежності, якщо вони є
    ],
    test_suite='tests',
)
