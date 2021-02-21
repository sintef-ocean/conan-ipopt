from conans import AutoToolsBuildEnvironment, ConanFile, tools
from conans.tools import PkgConfig
from conans.errors import ConanInvalidConfiguration
import os


class IpoptConan(ConanFile):
    name = "ipopt"
    version = "3.13.3"
    license = ("EPL-2.0",)
    author = "SINTEF Ocean"
    url = "https://github.com/sintef-ocean/conan-ipopt"
    homepage = "https://github.com/coin-or/Ipopt"
    description =\
        "Ipopt (Interior Point OPTimizer) is a" \
        " software package for large-scale nonlinear optimization."
    topics = ("Nonlinear optimization", "COIN-OR")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_hsl": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_hsl": False
    }
    generators = "pkg_config"

    build_requires = ("coinbrew/2021.01@sintef/stable")
    requires = (
        "coinmumps/4.10.0@sintef/stable",
        "openblas/[>=0.3.12]"
    )
    _name = "Ipopt"

    def requirements(self):

        if self.options.with_hsl:
            self.requires("coinhsl/[>=2014.01.17]@sintef/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC  # is this an option with mingw?

    def configure(self):

        if self.settings.compiler == "Visual Studio":
            raise ConanInvalidConfiguration(
                "This recipe is does not support Visual Studio")

        self.options["openblas"].shared = self.options.shared
        self.options["openblas"].use_thread = True
        self.options["openblas"].build_lapack = True
        # self.options["openblas"].dynamic_arch = True

    def source(self):

        self.run(
            "coinbrew fetch {}@{} --option ".format(self._name, self.version) +
            "--skip-dependencies")

    def build(self):

        env_build = AutoToolsBuildEnvironment(self)
        environ = env_build.vars.copy()
        environ["PKG_CONFIG_PATH"] = self.build_folder

        with tools.environment_append(environ):

            cmd_str = str()
            cmd_str += "coinbrew build {}@{} ".format(self._name, self.version)
            cmd_str += "--no-prompt "
            cmd_str += "--skip-dependencies "
            cmd_str += "--verbosity=4 "
            cmd_str += "--parallel-jobs {} ".format(tools.cpu_count())

            if not self.settings.os == "Windows" and not self.options.shared:
                cmd_str += "--static "
                # --enable-static
                # --enable-shared

            if self.settings.build_type == "Debug":
                cmd_str += "--enable-debug "

            if self.settings.compiler == "Visual Studio":
                cmd_str += "--enable-msvc={} ".format(self.settings.compiler.runtime)

            if self.options.fPIC:
                cmd_str += "--with-pic "

            pkg_openblas = PkgConfig("openblas")
            pkg_mumps = PkgConfig("coinmumps")
            cmd_str += "--with-lapack=\"{}\" ".format(" ".join(pkg_openblas.libs))
            cmd_str += "--with-mumps=\"{}\" ".format(" ".join(pkg_mumps.libs))
            cmd_str += "--with-mumps-cflags=\"{}\" ".format(" ".join(pkg_mumps.cflags))
            if self.options.with_hsl:
                pkg_coinhsl = PkgConfig("coinhsl")
                cmd_str += "--with-hsl=\"{}\" ".format(" ".join(pkg_coinhsl.libs))
                cmd_str += "--with-hsl-cflags=\"{}\" ".format(" ".join(pkg_coinhsl.cflags))

            self.run(cmd_str)

    def package(self):
        self.copy("*", src="dist")
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        os.unlink(os.path.join(self.package_folder, "lib", "libipopt.la"))
        os.unlink(os.path.join(self.package_folder, "lib", "libsipopt.la"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "IPOPT"
        self.cpp_info.libs = ["ipopt", "sipopt"]
        self.cpp_info.includedirs = [os.path.join("include", "coin-or")]

        # TODO: add system_libs dependencies, pthread,
        # gomp1, omp5, gfortran{3,4,5} or other openmp/fortran runtimes

    def imports(self):
        self.copy("license*", dst="licenses", folder=True, ignore_case=True)
