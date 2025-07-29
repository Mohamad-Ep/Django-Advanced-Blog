{% extends "mail_templated/base.tpl" %}
{% block subject %}
Activation Account 
{% endblock %}

{% block html %}
token user : {{token}}
<img src="https://www.nicepng.com/png/detail/136-1366211_group-of-10-guys-login-user-icon-png.png"><br>
{% endblock %}