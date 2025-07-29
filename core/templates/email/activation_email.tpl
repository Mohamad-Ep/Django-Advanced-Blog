{% extends "mail_templated/base.tpl" %}
{% block subject %}
Activation Email Account 
{% endblock %}

{% block html %}
Active Link : <br>

<a href="http://127.0.0.1:8002/accounts/api/v1/activation/confirm/{{token}}/" target="_blank">Click Acitve Email</a>
{% endblock %}