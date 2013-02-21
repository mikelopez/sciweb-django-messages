django sciweb pm
===========================================
Private messages between users in django

* Add ``django_pm.context_processors.get_args`` to TEMPLATE_CONTEXT_PROCESSORS in your settings

* Add ``django_pm`` to INSTALLED_APPS in settings


Template Tags Usage
===================

Inbox Page::


    <div class="container">
          <h2>Inbox</h2><hr />
          {{ user|get_inbox_count }} Message(s)

          <hr />
          <table class="table-bordered table">
          {% for i in user|get_inbox_messages %}
          <tr class="{% if i.is_new %}alert alert-success{% else %}{% endif %}">
            <td><a href="{% url get_message %}?message={{i.id}}">
              {% if i.parent_msg %}<b>RE: </b>{% endif %}From {{i.sender}}</a></td>
            <td>Sent at {{i.date_sent}}</td>
          </tr>
              
          {% endfor %}
        </table>

    </div>


Posting a Message
=================
Form generate_recipient will generate any required form elements. send_to_user is the user that will
be receiving the message. This variable name is whatever the user name is::

      {% if not send_to_user %}
        {% for i in userlist %}
          <a href="?user={{i.id}}">{{ i }}</a><br />
        {% endfor %}
      {% endif %}
      {% if send_to_user %}
        <h2>Compose Message</h2>
        <hr />
        <form action="{% url post_message %}" method="POST">{% csrf_token %}
          {{send_to_user|generate_recipient|safe}}
          {{form}}
          <br />
          <input type="submit" value="Send Message" class="btn btn-primary btn-large" />
        </form>
      {% endif %}





Message View Page
===================
Use the following to help build the view message page
::

    <!-- set the message from the template tag return and play with it -->
    <div class="container">
      <h2>Last Messag {{message.id}} From {{sender}}</h2>
      <hr />
      <div class="pull-left" style="width:550px;">
        Original Message:<br />
        <h3>{{message.text}}</h3>
        <hr />
        {% for p in message.get_parents %}
          {% ifnotequal p.id message.id %}
            <b>{{p.sender}}:</b> {{p.text}}<hr />

            {% if p.is_new %}
              {% ifequal p.recipient user %}
                {{p.set_as_read}}
              {% endifequal %}
            {% endif %}

          {% endifnotequal %}
        {% endfor %}
      </div>
      <div class="pull-right" style="width:350px;">
        {% if message %}
          <form action="{% url post_message %}" method="POST">{% csrf_token %}
          {{sender|generate_recipient|safe}}
          {{message|generate_parent|safe}}
          {{form}}
          <br />
          <input type="submit" class="btn btn-primary" value="Reply" />
        </form>
        {% endif %}
      </div>
    </div>

