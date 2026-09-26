from glob import glob
import os

from setuptools import find_packages, setup


package_name = 'san_de9_autonom'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='narancslee',
    maintainer_email='204051657+narancslee@users.noreply.github.com',
    description='ROS 2 Python package for the autonomous robot assignment.',
    license='GNU General Public License v3.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_simulator = san_de9_autonom.robot_simulator:main',
            'waypoint_controller = san_de9_autonom.waypoint_controller:main',
        ],
    },
)
