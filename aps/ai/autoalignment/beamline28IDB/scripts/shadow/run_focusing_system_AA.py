#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------- #
# Copyright (c) 2021, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2021. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# ----------------------------------------------------------------------- #
import os

from aps.ai.autoalignment.common.simulation.facade.parameters import Implementors
from aps.ai.autoalignment.beamline28IDB.facade.focusing_optics_factory import focusing_optics_factory_method, ExecutionMode
from aps.ai.autoalignment.beamline28IDB.simulation.facade.focusing_optics_interface import get_default_input_features, Layout
from aps.ai.autoalignment.common.facade.parameters import Movement, AngularUnits, DistanceUnits

from aps.ai.autoalignment.common.util.common import PlotMode, AspectRatio, ColorMap
from aps.ai.autoalignment.common.util.wrappers import plot_distribution, load_beam
from aps.ai.autoalignment.common.util.shadow.common import PreProcessorFiles
from aps.ai.autoalignment.common.util import clean_up

if __name__ == "__main__":
    verbose = False

    plot_mode = PlotMode.INTERNAL
    aspect_ratio = AspectRatio.AUTO
    color_map = ColorMap.VIRIDIS

    nbins_h = 2160
    nbins_v = 2560

    detector_x = nbins_h * 0.65 * 1e-3
    detector_y = nbins_v * 0.65 * 1e-3

    x_range = [-detector_x/2, detector_x/2]
    y_range = [-detector_y/2, detector_y/2]

    os.chdir("../../../../../../work_directory/28-ID")

    clean_up()

    input_beam = load_beam(Implementors.SHADOW, "primary_optics_system_beam.dat")

    # Focusing Optics System -------------------------

    focusing_system = focusing_optics_factory_method(execution_mode=ExecutionMode.SIMULATION, implementor=Implementors.SHADOW)
    focusing_system.initialize(input_photon_beam=input_beam,
                               input_features=get_default_input_features(layout=Layout.AUTO_ALIGNMENT),
                               rewrite_preprocessor_files=PreProcessorFiles.NO,
                               layout=Layout.AUTO_ALIGNMENT)

    # ----------------------------------------------------------------
    # perturbation of the incident beam to make adjustements necessary

    random_seed = 2120 # for repeatability

    focusing_system.perturbate_input_photon_beam(shift_h=0.0, shift_v=0.0)

    output_beam = focusing_system.get_photon_beam(verbose=verbose, debug_mode=False, random_seed=random_seed)

    plot_distribution(Implementors.SHADOW, output_beam,
                      xrange=x_range, yrange=y_range, nbins_h=nbins_h, nbins_v=nbins_v,
                      title="Initial Beam",
                      plot_mode=plot_mode, aspect_ratio=aspect_ratio, color_map=color_map)

    #--------------------------------------------------
    # interaction with the beamline

    focusing_system.change_h_bendable_mirror_shape(200, movement=Movement.RELATIVE)

    plot_distribution(Implementors.SHADOW, focusing_system.get_photon_beam(verbose=verbose, debug_mode=False, random_seed=random_seed),
                      xrange=x_range, yrange=y_range, nbins_h=nbins_h, nbins_v=nbins_v,
                      title="Change H-KB Shape",
                      plot_mode=plot_mode, aspect_ratio=aspect_ratio, color_map=color_map)

    focusing_system.move_h_bendable_mirror_motor_pitch(0.1, movement=Movement.RELATIVE, units=AngularUnits.MILLIRADIANS)

    plot_distribution(Implementors.SHADOW, focusing_system.get_photon_beam(verbose=verbose, debug_mode=False, random_seed=random_seed),
                      xrange=x_range, yrange=y_range, nbins_h=nbins_h, nbins_v=nbins_v,
                      title="Change H-KB Pitch",
                      plot_mode=plot_mode, aspect_ratio=aspect_ratio, color_map=color_map)

    print(focusing_system.get_h_bendable_mirror_motor_pitch(units=AngularUnits.MILLIRADIANS))

    focusing_system.move_h_bendable_mirror_motor_translation(10.0, movement=Movement.RELATIVE, units=DistanceUnits.MICRON)

    plot_distribution(Implementors.SHADOW, focusing_system.get_photon_beam(verbose=verbose, debug_mode=False, random_seed=random_seed),
                      xrange=x_range, yrange=y_range, nbins_h=nbins_h, nbins_v=nbins_v,
                      title="Change H-KB Translation",
                      plot_mode=plot_mode, aspect_ratio=aspect_ratio, color_map=color_map)

    print(focusing_system.get_h_bendable_mirror_motor_translation(units=DistanceUnits.MICRON))

    #--------------------------------------------------

    focusing_system.change_v_bimorph_mirror_shape(100, movement=Movement.RELATIVE)

    plot_distribution(Implementors.SHADOW, focusing_system.get_photon_beam(verbose=verbose, debug_mode=False, random_seed=random_seed),
                      xrange=x_range, yrange=y_range, nbins_h=nbins_h, nbins_v=nbins_v,
                      title="Change V-KB Shape",
                      plot_mode=plot_mode, aspect_ratio=aspect_ratio, color_map=color_map)


    focusing_system.move_v_bimorph_mirror_motor_pitch(3.2, movement=Movement.ABSOLUTE, units=AngularUnits.MILLIRADIANS)

    plot_distribution(Implementors.SHADOW, focusing_system.get_photon_beam(verbose=verbose, debug_mode=False, random_seed=random_seed),
                      xrange=x_range, yrange=y_range, nbins_h=nbins_h, nbins_v=nbins_v,
                      title="Change V-KB Pitch",
                      plot_mode=plot_mode, aspect_ratio=aspect_ratio, color_map=color_map)

    print(focusing_system.get_v_bimorph_mirror_motor_pitch(units=AngularUnits.MILLIRADIANS))

    focusing_system.move_v_bimorph_mirror_motor_translation(-10.0, movement=Movement.RELATIVE, units=DistanceUnits.MICRON)

    plot_distribution(Implementors.SHADOW, focusing_system.get_photon_beam(verbose=verbose, debug_mode=False, random_seed=random_seed),
                      xrange=x_range, yrange=y_range, nbins_h=nbins_h, nbins_v=nbins_v,
                      title="Change V-KB Translation",
                      plot_mode=plot_mode, aspect_ratio=aspect_ratio, color_map=color_map)

    print(focusing_system.get_v_bimorph_mirror_motor_translation(units=DistanceUnits.MICRON))

    # ----------------------------------------------------------------

    clean_up()
