from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv
import os

class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_CHIMERA"] = self.options["hyperscan"].build_chimera
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

        venv = VirtualBuildEnv(self)
        venv.generate(scope="build")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            bin_path = os.path.join(self.cpp.build.bindirs[0], "hs_example")
            self.run(bin_path, run_environment=True)

            if self.options["hyperscan"].build_chimera:
                bin_path = os.path.join(self.cpp.build.bindirs[0], "ch_example")
                self.run(bin_path, run_environment=True)
