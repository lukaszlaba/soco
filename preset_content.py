'''
This file is part of soco.
'''
#                                                           norm        norm
#                                        abs max min   abs max  min abs max min  V  max   abs  max min abs max min  M   max  max  max
#                                        Fx   Fx  Fx   Fy  Fy   Fy  Fz  Fz  Fz  tot  Mx    My  My   My  Mz  Mz Mz  tot  com  ten  shear
preset_dict =   {   'None':             [ 0,  0,  0,    0,  0,  0,  0,  0,  0,  0,    0,    0,  0,  0,  0,  0,  0,  0,    0,  0,  0],
                    'All':              [ 1,  1,  1,    1,  1,  1,  1,  1,  1,  1,    1,    1,  1,  1,  1,  1,  1,  1,    1,  1,  1],
                    'Beam':             [ 1,  0,  0,    0,  1,  1,  1,  0,  0,  1,    1,    1,  0,  0,  1,  0,  0,  0,    0,  0,  1],
                    'Frame':            [ 1,  0,  0,    1,  0,  0,  1,  0,  0,  1,    1,    1,  1,  1,  1,  0,  0,  1,    1,  1,  1],
                    'Baseplate':        [ 0,  1,  1,    1,  0,  0,  1,  0,  0,  1,    1,    1,  0,  0,  1,  0,  0,  1,    1,  1,  1],
                    'Brace':            [ 0,  1,  1,    1,  0,  0,  1,  0,  0,  1,    1,    1,  0,  0,  1,  0,  0,  1,    1,  1,  1],
                }