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

from aps.ai.autoalignment.common.simulation.facade.parameters import Implementors
from aps.ai.autoalignment.common.util.common import PlotMode, AspectRatio, ColorMap

from aps.ai.autoalignment.common.util.srw.common import get_srw_wavefront_distribution_info, plot_srw_wavefront_spatial_distribution, \
    load_srw_wavefront, save_srw_wavefront
from aps.ai.autoalignment.common.util.shadow.common import get_shadow_beam_spatial_distribution, get_shadow_beam_divergence_distribution, \
    plot_shadow_beam_divergence_distribution, plot_shadow_beam_spatial_distribution, \
    load_shadow_beam, load_source_beam, save_shadow_beam, save_source_beam

EXPERIMENTAL_NOISE_TO_SIGNAL_RATIO = (100 / 5e4)
NOISE_DEFAULT_VALUE = 70 * EXPERIMENTAL_NOISE_TO_SIGNAL_RATIO

def load_beam(implementor, file_name, **kwargs):
    if implementor == Implementors.SRW: return load_srw_wavefront(file_name)
    elif implementor == Implementors.SHADOW:
        try:
            if kwargs.get("which_beam") == "source": return load_source_beam(file_name)
            else:                                    return load_shadow_beam(file_name)
        except: return load_shadow_beam(file_name)

def save_beam(beam, file_name, implementor=Implementors.SHADOW, **kwargs):
    if implementor == Implementors.SRW: save_srw_wavefront(srw_wavefront=beam, file_name=file_name)
    elif implementor == Implementors.SHADOW:
        try:
            if kwargs["which_beam"] == "source": save_source_beam(source_beam=beam, file_name=file_name)
            else:                                save_shadow_beam(shadow_beam=beam, file_name=file_name)
        except: save_shadow_beam(shadow_beam=beam, file_name=file_name)

def get_distribution_info(implementor, beam, xrange=None, yrange=None, do_gaussian_fit=False, **kwargs):
    if implementor == Implementors.SRW: return get_srw_wavefront_distribution_info(beam, xrange, yrange, do_gaussian_fit)
    elif implementor == Implementors.SHADOW:
        nbins_h                = kwargs.get("nbins_h",   201)
        nbins_v                = kwargs.get("nbins_v",   201)
        nolost                 = kwargs.get("nolost",    1)
        add_noise              = kwargs.get("add_noise", False)
        noise                  = kwargs.get("noise",     NOISE_DEFAULT_VALUE if add_noise else None)
        percentage_fluctuation = kwargs.get("percentage_fluctuation", 10.0) * 1e-2
        calculate_over_noise   = kwargs.get("calculate_over_noise", False)
        noise_threshold        = kwargs.get("noise_threshold", 1.5)

        if kwargs.get("distribution") == "divergence": return get_shadow_beam_divergence_distribution(shadow_beam=beam,
                                                                                                      nbins_h=nbins_h, nbins_v=nbins_v,
                                                                                                      nolost=nolost,
                                                                                                      xrange=xrange, yrange=yrange,
                                                                                                      do_gaussian_fit=do_gaussian_fit)
        else:                                          return get_shadow_beam_spatial_distribution(shadow_beam=beam,
                                                                                                   nbins_h=nbins_h, nbins_v=nbins_v,
                                                                                                   nolost=nolost,
                                                                                                   xrange=xrange, yrange=yrange,
                                                                                                   do_gaussian_fit=do_gaussian_fit,
                                                                                                   add_noise=add_noise,
                                                                                                   noise=noise,
                                                                                                   percentage_fluctuation=percentage_fluctuation,
                                                                                                   calculate_over_noise=calculate_over_noise,
                                                                                                   noise_threshold=noise_threshold)

def plot_distribution(implementor, beam, title="X,Z", xrange=None, yrange=None, plot_mode=PlotMode.INTERNAL, aspect_ratio=AspectRatio.AUTO, color_map=ColorMap.RAINBOW, **kwargs):
    if implementor == Implementors.SRW: plot_srw_wavefront_spatial_distribution(beam, title, xrange, yrange, plot_mode, aspect_ratio, color_map)
    elif implementor == Implementors.SHADOW:
        nbins_h                = kwargs.get("nbins_h",   201)
        nbins_v                = kwargs.get("nbins_v",   201)
        nolost                 = kwargs.get("nolost",    1)
        add_noise              = kwargs.get("add_noise", False)
        noise                  = kwargs.get("noise",     NOISE_DEFAULT_VALUE if add_noise else None)
        percentage_fluctuation = kwargs.get("percentage_fluctuation", 10.0) * 1e-2
        calculate_over_noise   = kwargs.get("calculate_over_noise", False)
        noise_threshold        = kwargs.get("noise_threshold", 1.5)

        if kwargs.get("distribution") == "divergence": plot_shadow_beam_divergence_distribution(shadow_beam=beam,
                                                                                                nbins_h=nbins_h, nbins_v=nbins_v,
                                                                                                nolost=nolost,
                                                                                                title=title,
                                                                                                xrange=xrange, yrange=yrange,
                                                                                                plot_mode=plot_mode,
                                                                                                aspect_ratio=aspect_ratio,
                                                                                                color_map=color_map)
        else:                                          plot_shadow_beam_spatial_distribution(shadow_beam=beam,
                                                                                             nbins_h=nbins_h, nbins_v=nbins_v,
                                                                                             nolost=nolost,
                                                                                             title=title,
                                                                                             xrange=xrange, yrange=yrange,
                                                                                             plot_mode=plot_mode,
                                                                                             aspect_ratio=aspect_ratio,
                                                                                             color_map=color_map,
                                                                                             add_noise=add_noise,
                                                                                             noise=noise,
                                                                                             percentage_fluctuation=percentage_fluctuation,
                                                                                             calculate_over_noise=calculate_over_noise,
                                                                                             noise_threshold=noise_threshold)
