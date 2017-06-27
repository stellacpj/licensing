# -*- coding: utf-8 -*-
# <*******************
# 
# Copyright 2017 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# 
# *******************>

# ----------------------------------------------------------------------------------------------------------------------
#  This is an app-specific example router
#
#  This simple router is used for setting languages from app/languages directory
#  as a part of the application path:  app/<lang>/controller/function
#  Language from default.py or 'en' (if the file is not found) is used as
#  a default_language
#
# See <web2py-root-dir>/examples/routes.parametric.example.py for parameter's detail
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# To enable this route file you must do the steps:
# 1. rename <web2py-root-dir>/examples/routes.parametric.example.py to routes.py
# 2. rename this APP/routes.example.py to APP/routes.py (where APP - is your application directory)
# 3. restart web2py (or reload routes in web2py admin interface)
#
# YOU CAN COPY THIS FILE TO ANY APPLICATION'S ROOT DIRECTORY WITHOUT CHANGES!
# ----------------------------------------------------------------------------------------------------------------------

from fileutils import abspath
from languages import read_possible_languages

possible_languages = read_possible_languages(abspath('applications', app))
# ----------------------------------------------------------------------------------------------------------------------
# NOTE! app - is an application based router's parameter with name of an application. E.g.'welcome'
# ----------------------------------------------------------------------------------------------------------------------

routers = {
    app: dict(
        default_language=possible_languages['default'][0],
        languages=[lang for lang in possible_languages if lang != 'default']
    )
}

# ----------------------------------------------------------------------------------------------------------------------
# NOTE! To change language in your application using these rules add this line in one of your models files:
# ----------------------------------------------------------------------------------------------------------------------
#   if request.uri_language: T.force(request.uri_language)
