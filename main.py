#!/usr/bin/env python
import os
import jinja2
import webapp2
import operator

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("calculator.html")

    def post(self):
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        password = self.request.get("password")

        data = first_name + " " + last_name + " " + password
        return self.write(data)

class RegisterHandler(BaseHandler):
    def post(self):
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        password = self.request.get("password")

        data = first_name + " " + last_name + " " + password
        return self.write(data)

class CalculateHandler(BaseHandler):
    def post(self):
        first_number = float(self.request.get("first-number"))
        second_number = float(self.request.get("second-number"))
        operation = self.request.get("operation_list")

        ops = {"plus": operator.add, "minus": operator.sub,'multiply' : operator.mul, 'divide' : operator.div}

        if second_number != 0:
            return self.write(ops[operation](first_number,second_number))
        else:
            return self.write("Cannot divide by 0!")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/register",RegisterHandler),
    webapp2.Route("/calculate",CalculateHandler)
], debug=True)
