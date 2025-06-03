from setuptools import setup, find_packages

setup(
    name="werewolf_vampire_novella",
    version="1.0.0",
    author="Ваше имя",
    description="Визуальная новелла о любви оборотня и вампира",
    packages=find_packages(),
    install_requires=["pygame>=2.5.0"],
    include_package_data=True,
    package_data={
        "": ["images/*.jpg", "images/*.png"],
    },
    entry_points={
        "console_scripts": [
            "novella=main:main",
        ],
    },
)