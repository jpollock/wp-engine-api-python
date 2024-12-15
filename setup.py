"""Setup configuration for the WP Engine API Python SDK."""

from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wp-engine-api-python",
    version="0.0.2",
    description="WP Engine API SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jeremy Pollock",
    author_email="jeremy.pollock@wpengine.com",
    url="https://github.com/jpollock/wp-engine-api-python",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "wp_engine_api": ["py.typed"],
        "wp_engine_api.generated": ["py.typed"],
    },
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "python-dateutil>=2.8.0",
        "urllib3>=1.26.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="wpengine, wordpress, api, sdk",
    project_urls={
        "Documentation": "https://wpengineapi.com/docs",
        "Source": "https://github.com/jpollock/wp-engine-api-python",
        "Bug Reports": "https://github.com/jpollock/wp-engine-api-python/issues",
    },
)
