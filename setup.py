from setuptools import setup, Command

version = "0.4.0"

class VersionCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


if __name__ == "__main__":
    setup(
        version=version,
        packages=["classyconf"],
        download_url="https://github.com/hernantz/classyconf/tarball/{}".format(version),
        cmdclass={"version": VersionCommand},
    )
