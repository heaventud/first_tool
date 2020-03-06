<!DOCTYPE html>
{# Update the template_structure.html document too #}
{%- block before_style -%}
<meta charset="utf-8">
{%- endblock before_style -%}
{% block style %}
<style  type="text/css" >
{% block table_styles %}
{% for s in table_styles %}
    #T_{{uuid}} {{s.selector}} {
    {% for p,val in s.props %}
      {{p}}: {{val}};
    {% endfor -%}
    }
{%- endfor -%}
{% endblock table_styles %}
{% block before_cellstyle %}{% endblock before_cellstyle %}
{% block cellstyle %}
{%- for s in cellstyle %}
    {%- for selector in s.selectors -%}{%- if not loop.first -%},{%- endif -%}#T_{{uuid}}{{selector}}{%- endfor -%} {
    {% for p,val in s.props %}
        {{p}}: {{val}};
    {% endfor %}
    }
{%- endfor -%}
{%- endblock cellstyle %}
td a {
    display: block;
   }
</style>
{%- endblock style %}
{%- block before_table %}{% endblock before_table %}
{%- block table %}
<table id="T_{{uuid}}" {% if table_attributes %}{{ table_attributes }}{% endif %}>
{%- block caption %}
{%- if caption -%}
    <caption>{{caption}}</caption>
{%- endif -%}
{%- endblock caption %}
{%- block thead %}
<thead>
    {%- block before_head_rows %}{% endblock %}
    {%- for r in head %}
    {%- block head_tr scoped %}
    <tr>
        {%- for c in r %}
        {%- if c.is_visible != False %}
        <{{ c.type }} class="{{c.class}}" {{ c.attributes|join(" ") }}>{{c.value}}</{{ c.type }}>
        {%- endif %}
        {%- endfor %}
    </tr>
    {%- endblock head_tr %}
    {%- endfor %}
    {%- block after_head_rows %}{% endblock %}
</thead>
{%- endblock thead %}
{%- block tbody %}
<tbody>
    {% block before_rows %}{% endblock before_rows %}
    {% for r in body %}
    {% block tr scoped %}
    <tr>
        {% for c in r %}
            {% if loop.index >= 2 %}
                {% if c.is_visible != False %}
                    <{{ c.type }} class="{{ c.class }}"> <a href='Temp/dir_{{loop.index}}/details.html'>{{ c.value }}</a>  {{ c.attributes|join(" ") }}</{{ c.type }}>
                {% else %}
                    <{{ c.type }}{{ c.attributes|join(" ") }}>{{ c.value }}</{{ c.type }}>
                {% endif %}
            {% endif %}
        {%- endfor %}
    </tr>
    {% endblock tr %}
    {%- endfor %}
    {%- block after_rows %}{%- endblock after_rows %}
</tbody>
{%- endblock tbody %}
</table>
{%- endblock table %}
{%- block after_table %}{% endblock after_table %}