[![GCC Conan](https://github.com/sintef-ocean/conan-ipopt/workflows/GCC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-ipopt/actions?query=workflow%3A"GCC+Conan")
[![Clang Conan](https://github.com/sintef-ocean/conan-ipopt/workflows/Clang%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-ipopt/actions?query=workflow%3A"Clang+Conan")


[Conan.io](https://conan.io) recipe for [ipopt](http://github.com/coin-or/ipopt).

The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/en/latest/reference/commands/misc/remote.html?highlight=remotes):

   ```bash
   $ conan remote add sintef https://conan.sintef.io/public
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project. This file describes dependencies and your configuration of choice, e.g.:

   ```
   [requires]
   ipopt/[>=3.13.3]@sintef/stable

   [options]
   None

   [imports]
   licenses, * -> ./licenses @ folder=True

   [generators]
   cmake_paths
   cmake_find_package
   ```

   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.13)
   project(TheProject CXX)

   include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
   find_package(IPOPT MODULE REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor IPOPT::IPOPT)
   ```
   Then, do
   ```bash
   $ mkdir build && cd build
   $ conan install .. -s build_type=<build_type>
   ```
   where `<build_type>` is e.g. `Debug` or `Release`.
   You can now continue with the usual dance with cmake commands for configuration and compilation. For details on how to use conan, please consult [Conan.io docs](http://docs.conan.io/en/latest/)

## Package options

Option | Default | Domain
---|---|---
shared  | True | [True, False]
fPIC | True | [True, False]
with_hsl | False | [True, False]

`with_hsl` uses the `coinhsl/[>=2014.01.17]@sintef/stable` requirement. Take a look at its
readme regarding HSL source, [coinhsl](https://github.com/sintef-ocean/conan-coinhsl).


## Known recipe issues

  - This recipe has not been tested on Windows and is likely to fail.
