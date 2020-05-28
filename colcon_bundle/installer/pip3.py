# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os

from colcon_bundle.installer.base_pip_installer import \
    BasePipInstallerExtensionPoint


class Pip3BundleInstallerExtensionPoint(BasePipInstallerExtensionPoint):
    """Python 3 pip installer."""

    def __valid_python3_version(version_string):
        try:
            version_float = float(version_string)
        except ValueError:
            raise parser.ArgumentTypeError(version_string + " cannot be "
            "converted to a float... Make sure it is of form 3.X")
        if version_float < 3.4:
            raise parser.ArgumentTypeError("Only 3.4 and higher are "
            "supported")
        if version_float >= 4:
            raise parser.ArgumentTypeError("Only 3.X are supported")
        return version_string
 
    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            '--pip3-args',
            nargs='*', metavar='*', type=str.lstrip,
            help='Pass arguments to CMake projects. '
                 'Arguments matching other options in colcon must be prefixed '
                 'by a space,\ne.g. --pip3-args " --help"')
        parser.add_argument(
            '--pip3-requirements', type=str, default=None,
            help='Path to a requirements.txt. All packages in the file'
                 'will be installed into Python3 in the bundle')
        parser.add_argument(
            '--python3-version', type=str, default='3.5',
            help='Python3 version number. Default is 3.5, but can be one of'
            '3.4, 3.5, and so on')

    def version(self):
        print("===========version==========")
        print(self.context.args.python3_version)
        return self.context.args.python3_version

    def initialize(self, context):  # noqa: D102
        super().initialize(context)
        self._python_path = os.path.join(
            self.context.prefix_path, 'usr', 'bin', ('python' +
                self.context.args.python3_version))
        self._pip_args = self.context.args.pip3_args
        if self.context.args.python3_version != '3.5':
            self._upgrade_pip = True
        self.additional_requirements = self.context.args.pip3_requirements
