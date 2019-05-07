# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 11:59:32 2019

@author: Krutika Lodaya
"""
import speech_recognition as sr
import os
from flask import Flask, render_template, request, Response,session, make_response, redirect
import urllib3
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from flask_cors import CORS, cross_origin
from FAQ_BOT_test import test_model



APP = Flask(__name__)
CORS(APP)
APP.config['SECRET_KEY'] = 'onelogindemopytoolkit'
APP.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saml')

@APP.route('/', methods=['GET'])
def my_form():
    """
    Opens the page for chatbot
    """
    return render_template('AIchatbot_ver_5.9.html')

@APP.route('/faqbot', methods=['POST'])
@cross_origin()
def objectname():
    """
    Get data from the user.
    preprocessing on the data recieved.
    Collect the pickle made from the trained model and pass to testing module.
    Get response from the testing module and return reponse to user.
    """
    try:
        text = request.form['input']
        print(text)
        text_input = text.lower()
        obj = test_model("Latin.pickle")
        out_text = obj.predict_class(text_input)
        if (out_text[0][0] == "soil"):
            return Response('water', status=200,mimetype="text/html")
        else:
            return Response(out_text[0][0], status=200, mimetype="text/html")
    except:
         text =None
         return Response("Error",status = 200, mimetype = "text/html")

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=APP.config['\saml'])
    return auth


def prepare_flask_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    url_data = urlparse(request.url)
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': url_data.port,
        'script_name': request.path,
        'get_data': request.args.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.form.copy()
    }


@APP.route('/', methods=['GET', 'POST'])
def index():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    if 'sso' in request.args:
        return redirect(auth.login())
    elif 'sso2' in request.args:
        return_to = '%sattrs/' % request.host_url
        return redirect(auth.login(return_to))
    elif 'slo' in request.args:
        name_id = None
        session_index = None
        if 'samlNameId' in session:
            name_id = session['samlNameId']
        if 'samlSessionIndex' in session:
            session_index = session['samlSessionIndex']

        return redirect(auth.logout(name_id=name_id, session_index=session_index))
    elif 'acs' in request.args:
        auth.process_response()
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()
        if len(errors) == 0:
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            session['samlSessionIndex'] = auth.get_session_index()
            self_url = OneLogin_Saml2_Utils.get_self_url(req)
            if 'RelayState' in request.form and self_url != request.form['RelayState']:
                return redirect(auth.redirect_to(request.form['RelayState']))
    elif 'sls' in request.args:
        dscb = lambda: session.clear()
        url = auth.process_slo(delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return redirect(url)
            else:
                success_slo = True

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()

    return render_template(
        'AIchatbot_ver_5.9.html',
        errors=errors,
        not_auth_warn=not_auth_warn,
        success_slo=success_slo,
        attributes=attributes,
        paint_logout=paint_logout
    )


@APP.route('/attrs/')
def attrs():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()

    return render_template('attrs.html', paint_logout=paint_logout,
                           attributes=attributes)


@APP.route('/metadata/')
def metadata():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp

if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True, threaded=True)
