#! coding=utf-8

HTML_MAIL = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
    <style>
    {{ bt_css }}
    </style>
  </head>
  <body>

    <div class="container">
      <h2>{{ title }}</h2>
      {% for item in tpl_obj %}
      <div class="panel panel-info">
        <div class="panel-heading">
          <h4 class="panel-title">{{ item.repo }}</h4>
        </div>
        <div class="panel-body">
          <p>Number of commits: {{ item.n_commits }}</p>
          <p>Number of inserts: {{ item.n_inserts }}</p>
          <p>Number of deletes: {{ item.n_deletes }}</p>
        </div>
      </div>
      {% endfor %}
    </div>


    <script src="//code.jquery.com/jquery-1.11.0.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>

  </body>
</html>
'''
