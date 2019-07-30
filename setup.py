# coding=utf-8

from setuptools import setup
from setuptools import find_packages
from distutils.cmd import Command
from distutils.extension import Extension
import os
import sys
import io
import subprocess
import platform
import numpy as np
from Cython.Build import cythonize
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

if "--line_trace" in sys.argv:
    line_trace = True
    print("Build with line trace enabled ...")
    sys.argv.remove("--line_trace")
else:
    line_trace = False

PACKAGE = "Sentry"
NAME = "Sentry"
VERSION = "0.0.1"
DESCRIPTION = "Sentry " + VERSION
AUTHOR = "kerry"

ext_modules = [
    "sentry/Analysis/SeriesValues.pyx",
    "sentry/Analysis/transformer.pyx",
    "sentry/Analysis/SecurityValueHolders.pyx",
    "sentry/Analysis/CrossSectionValueHolders.pyx",
    "sentry/Analysis/TechnicalAnalysis/StatefulTechnicalAnalysers.pyx",
    "sentry/Analysis/TechnicalAnalysis/StatelessTechnicalAnalysers.pyx",
    "sentry/Math/Accumulators/impl.pyx",
    "sentry/Math/Accumulators/IAccumulators.pyx",
    "sentry/Math/Accumulators/StatefulAccumulators.pyx",
    "sentry/Math/Accumulators/StatelessAccumulators.pyx",
    "sentry/Math/Distributions/NormalDistribution.pyx",
    "sentry/Math/Distributions/norm.pyx",
    "sentry/Math/ErrorFunction.pyx",
    "sentry/Math/MathConstants.pyx",
    "sentry/Math/udfs.pyx",
    "sentry/Utilities/Asserts.pyx",
    "sentry/Utilities/Tools.pyx"
]

def generate_extensions(ext_modules, line_trace=False):

    extensions = []

    if line_trace:
        print("define cython trace to True ...")
        define_macros = [('CYTHON_TRACE', 1), ('CYTHON_TRACE_NOGIL', 1)]
    else:
        define_macros = []

    for pyxfile in ext_modules:
        ext = Extension(name='.'.join(pyxfile.split('/'))[:-4],
                        sources=[pyxfile],
                        define_macros=define_macros)
        extensions.append(ext)
    return extensions


if platform.system() != "Windows":
    import multiprocessing
    n_cpu = multiprocessing.cpu_count()
else:
    n_cpu = 0


ext_modules_settings = cythonize(generate_extensions(ext_modules, line_trace),
                                 compiler_directives={'embedsignature': True, 'linetrace': line_trace},
                                 nthreads=n_cpu)

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules_settings,
    include_dirs=[np.get_include()]
)
