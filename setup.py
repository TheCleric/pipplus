import ppsetuptools

ppsetuptools.setup(
    packages=ppsetuptools.find_packages(  # type: ignore
        exclude=["tests", "tests.*"]
    ),
)
