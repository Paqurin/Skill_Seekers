#!/usr/bin/env python3
"""
Skill Seeker Setup
Install script for unified CLI interface
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

# Read requirements
requirements = [
    'requests>=2.25.0',
    'beautifulsoup4>=4.9.0',
    'click>=8.0.0',
    'rich>=10.0.0',
    'pyyaml>=5.4.0',
]

# Optional requirements
extras_require = {
    'dev': [
        'pytest>=6.0.0',
        'pytest-cov>=2.12.0',
    ],
    'api': [
        'anthropic>=0.3.0',
    ],
    'mcp': [
        'mcp>=0.1.0',
    ],
}

setup(
    name='skillseeker',
    version='2.0.0',
    description='Convert documentation websites to Claude AI skills',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Skill Seeker Contributors',
    url='https://github.com/yourusername/Skill_Seekers',
    license='MIT',

    packages=find_packages(exclude=['tests', 'docs']),
    package_dir={'': '.'},

    install_requires=requirements,
    extras_require=extras_require,

    entry_points={
        'console_scripts': [
            'skillseeker=cli.skillseeker:main',
            'ss=cli.skillseeker:main',  # Short alias
        ],
    },

    python_requires='>=3.7',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

    keywords='claude ai documentation scraper skill automation',
)
