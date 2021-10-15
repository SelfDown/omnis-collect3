# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="omnis-collect",
    version="3.0.2",
    author="zzhang",
    author_email="zzhang@cenboomh.com",
    description="一个web 接口配置工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SelfDown/omnis-collect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
