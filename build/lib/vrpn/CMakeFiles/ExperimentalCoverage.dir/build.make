# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/sarahaguasvivas/gpc_controller

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sarahaguasvivas/gpc_controller/build

# Utility rule file for ExperimentalCoverage.

# Include the progress variables for this target.
include lib/vrpn/CMakeFiles/ExperimentalCoverage.dir/progress.make

lib/vrpn/CMakeFiles/ExperimentalCoverage:
	cd /home/sarahaguasvivas/gpc_controller/build/lib/vrpn && /usr/bin/ctest -D ExperimentalCoverage

ExperimentalCoverage: lib/vrpn/CMakeFiles/ExperimentalCoverage
ExperimentalCoverage: lib/vrpn/CMakeFiles/ExperimentalCoverage.dir/build.make

.PHONY : ExperimentalCoverage

# Rule to build all files generated by this target.
lib/vrpn/CMakeFiles/ExperimentalCoverage.dir/build: ExperimentalCoverage

.PHONY : lib/vrpn/CMakeFiles/ExperimentalCoverage.dir/build

lib/vrpn/CMakeFiles/ExperimentalCoverage.dir/clean:
	cd /home/sarahaguasvivas/gpc_controller/build/lib/vrpn && $(CMAKE_COMMAND) -P CMakeFiles/ExperimentalCoverage.dir/cmake_clean.cmake
.PHONY : lib/vrpn/CMakeFiles/ExperimentalCoverage.dir/clean

lib/vrpn/CMakeFiles/ExperimentalCoverage.dir/depend:
	cd /home/sarahaguasvivas/gpc_controller/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sarahaguasvivas/gpc_controller /home/sarahaguasvivas/gpc_controller/lib/vrpn /home/sarahaguasvivas/gpc_controller/build /home/sarahaguasvivas/gpc_controller/build/lib/vrpn /home/sarahaguasvivas/gpc_controller/build/lib/vrpn/CMakeFiles/ExperimentalCoverage.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : lib/vrpn/CMakeFiles/ExperimentalCoverage.dir/depend

