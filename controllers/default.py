# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
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

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import os
from jinja2 import Environment, FileSystemLoader
from collections import namedtuple
RR_setting = namedtuple("RR_setting","Name Address");
VPN_setting = namedtuple("VPN_setting", "Name AcceptASPath PeerNeighbor");

TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join('/home/www-data/web2py/applications/JunosPortal/static', 'command_template')),
    trim_blocks=False)

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def create_commands(rows_rr,rows_vpn,rows_vpnstatic):
    inet_vpn = 'inet-vpn';
    vpn_policy = 'vpn-policy';
    context = {
        'inet_vpn':inet_vpn,
        'vpn_policy':vpn_policy,
        'rows_vpn':rows_vpn,
        "rows_rr":rows_rr,
        'rows_vpnstatic':rows_vpnstatic
    }
    #
    with open('/home/www-data/web2py/applications/JunosPortal/static/command_template/output.txt', 'w') as f:
        command_set = render_template('command_template.txt', context);
        f.write(command_set);
    return command_set

def preview_config():
    rows_rr=db(db.RouteReflector_conf).select();
    rows_vpn=db(db.VPN.Configuration_To_Be_Deployed == True).select();
    rows_vpnstatic=db(db.VPN_static.Configuration_To_Be_Deployed == True).select();
    commands = create_commands(rows_rr,rows_vpn,rows_vpnstatic).replace("\n", "\\n").replace("\"","\\\""); #processing the data for \n can behave normally in textarea.
    #return dict(commands=commands,rows=rows,lst_RR_settings=lst_RR_settings,lst_VPN_settings=lst_VPN_settings);
    return dict(commands=commands);

def index():
    return dict();

def del_rr(ids):
    if not ids:
        session.flash='Please Select the Check-box to Delete Records'
    else:
        for row in ids:
            db(db.RouteReflector_conf.id == row).delete()
        pass
    pass
    return ''

@auth.requires_login()
def RouteReflector_conf():
    RR = SQLFORM.grid(db.RouteReflector_conf,
                    create=True,
                    searchable=False,
                    editable=True,
                    details=False,
                    deletable=False,
                    exportclasses=dict(tsv_with_hidden_cols=False, csv_with_hidden_cols=False,html=False),
                    selectable = lambda ids: del_rr(ids)
                    );
    if not RR.create_form and not RR.update_form and not RR.view_form:
        o = RR.element(_type='submit', _value='%s' % T('Submit'))
        if o is not None:
            o['_value'] = T("Confirm to Delete")
    return dict(RR=RR);

def del_vpn(ids):
    if not ids:
        session.flash='Please Select the Left_Side Check-box to Delete Records'
    else:
        for row in ids:
            db(db.VPN.id == row).delete()
        pass
    pass
    return ''

@auth.requires_login()
def VPN():
    VPN = SQLFORM.grid(db.VPN,
                   searchable=False,
                    create=True,
                    editable=True,
                    details=False,
                    deletable=False,
                    exportclasses=dict(tsv_with_hidden_cols=False, csv_with_hidden_cols=False,html=False),
                    selectable = lambda ids: del_vpn(ids)
                    );
    if not VPN.create_form and not VPN.update_form and not VPN.view_form:
        o = VPN.element(_type='submit', _value='%s' % T('Submit'))
        if o is not None:
            o['_value'] = T("Confirm to Delete")
    return dict(VPN=VPN);

def del_vpn_static(ids):
    if not ids:
        session.flash='Please Select the Left_Side Check-box to Delete Records'
    else:
        for row in ids:
            db(db.VPN_static.id == row).delete()
        pass
    pass
    return ''

@auth.requires_login()
def VPN_static():
    VPN = SQLFORM.grid(db.VPN_static,
                   searchable=False,
                    create=True,
                    editable=True,
                    details=False,
                    deletable=False,
                    exportclasses=dict(tsv_with_hidden_cols=False, csv_with_hidden_cols=False,html=False),
                    selectable = lambda ids: del_vpn_static(ids)
                    );
    if not VPN.create_form and not VPN.update_form and not VPN.view_form:
        o = VPN.element(_type='submit', _value='%s' % T('Submit'))
        if o is not None:
            o['_value'] = T("Confirm to Delete")
    return dict(VPN=VPN);
