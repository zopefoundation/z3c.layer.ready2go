===========================
Ready-2-Go Layer for Zope 3
===========================

This package contains the `ready2go` layer. This layer supports a correct set of
component registration and can be used for inheritation in custom skins.

Important
---------

This layer supports the ``z3c.pagelet`` and the ``z3c.form`` pattern. This
means every page e.g. the error page is based on the ``z3c.pagelet``
concept. By default we use the ``<div>``-based layout for z3c forms.


``IReady2GoBrowserLayer`` Layer
-------------------------------

The `ready2go` layer is useful for build custom presentation skins without
access to ZMI menus like ``zmi_views`` etc. This means there is no menu item
registred if you use this layer.

For more information about what this layer offers, see ``z3c.layer.pagelet``.


Testing
-------

For testing the ``IReady2GoBrowserLayer`` layer we use the testing skin
defined in the tests package which uses the ``IReady2GoBrowserLayer`` layer as
the only base layer.  This means, that our testing skin provides only the
views defined in the minimal package and it's testing views defined in tests.

Login as manager first:

  >>> from webtest.app import TestApp
  >>> manager = TestApp(
  ...     make_wsgi_app(), extra_environ={
  ...         'wsgi.handleErrors': False,
  ...         'HTTP_AUTHORIZATION': 'Basic mgr:mgrpw'})
  >>> err_manager = TestApp(
  ...     make_wsgi_app(), extra_environ={
  ...         'HTTP_AUTHORIZATION': 'Basic mgr:mgrpw'})

Check if we can access the ``page.html`` view which is registred in the
``ftesting.zcml`` file with our skin:

  >>> skinURL = 'http://localhost/++skin++Ready2GoTestSkin'
  >>> res = manager.get(skinURL + '/page.html')
  >>> res.request.url
  'http://localhost/++skin++Ready2GoTestSkin/page.html'


Pagelet support
---------------

Check if we can access the test page given from the ``z3c.layer.pagelet``
``ftesting.zcml`` configuration.

  >>> print(res.html) #doctest: +PARSE_HTML
  <html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
  <title>PageletTestLayout</title>
  </head>
  <body>
    test page
  </body>
  </html>


Not Found
~~~~~~~~~

Now check the not found page which is a exception view on the exception
``zope.publisher.interfaces.INotFound``:

  >>> manager.get(skinURL + '/foobar.html')
  Traceback (most recent call last):
  ...
  NotFound: Object: <zope.site.folder.Folder ...>, name: 'foobar.html'

  >>> res = err_manager.get(skinURL + '/foobar.html', status=404)
  >>> print(res.html)
  <html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
  <title>PageletTestLayout</title>
  </head>
  <body>
    <div>
    <br />
    <br />
    <h3>
      The page you are trying to access is not available
    </h3>
    <br />
    <b>
      Please try the following:
    </b>
    <br />
    <ol>
      <li>
        Make sure that the Web site address is spelled correctly.
      </li>
      <li>
        <a href="javascript:history.back(1);">
          Go back and try another URL.
        </a>
      </li>
    </ol>
  </div>
  </body>
  </html>


User error
~~~~~~~~~~

And check the user error page which is a view registred for
``zope.exceptions.interfaces.IUserError`` exceptions:

  >>> res = err_manager.get(skinURL + '/@@usererror.html')
  >>> print(res.html)
  <html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
  <title>PageletTestLayout</title>
  </head>
  <body>
    <div>
    <div>simply user error</div>
  </div>
  </body>
  </html>


Common exception (system error)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

And check error view registred for
``zope.interface.common.interfaces.IException``:

  >>> res = err_manager.get(skinURL + '/@@systemerror.html', status=500)
  >>> print(res.html)
  <html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
  <title>PageletTestLayout</title>
  </head>
  <body>
    <div>
    <br />
    <br />
    <h3>A system error occurred</h3>
    <br />
    <b>Please contact the administrator.</b>
    <a href="javascript:history.back(1);">
      Go back and try another URL.
    </a>
  </div>
  </body>
  </html>


Forbidden 403
~~~~~~~~~~~~~

And check the ``zope.security.interfaces.IUnauthorized`` view, use a new
unregistred user (test browser) for this.

  >>> unauthorized = TestApp(make_wsgi_app())
  >>> unauthorized.get(skinURL + '/@@forbidden.html')
  Traceback (most recent call last):
  ...
  AppError: Bad response: 403 Forbidden

  >>> res = unauthorized.get(skinURL + '/@@forbidden.html', status=403)
  >>> print(res.html)
  <html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
  <title>PageletTestLayout</title>
  </head>
  <body>
    <div>
    <br />
    <br />
    <h3>Unauthorized</h3>
    <br />
    <b>You are not authorized.</b>
  </div>
  </body>
  </html>

As you can see, this test will return a 403 Forbidden error. But this is only
because we do not have an unauthenticated principal available. See the test
below what happens if we register an unauthenticated princiapl.


Unauthorized 401
~~~~~~~~~~~~~~~~

If we use an authenticated principal and access the forbitten page, we will get
a 401 Unauthorized instead of a 403 Forbidden error page.

  >>> from zope.configuration import xmlconfig
  >>> import zope.principalregistry
  >>> def zcml(s):
  ...     context = xmlconfig.file('meta.zcml', zope.principalregistry)
  ...     xmlconfig.string(s, context)

  >>> zcml("""
  ...    <configure
  ...        xmlns="http://namespaces.zope.org/zope"
  ...        >
  ...
  ...      <unauthenticatedPrincipal
  ...         id="zope.unknown"
  ...         title="Anonymous user"
  ...         description="A person we don't know"
  ...         />
  ...
  ...    </configure>
  ... """)

  >>> manager2 = TestApp(make_wsgi_app(), extra_environ={
  ...         'wsgi.handleErrors': True})
  >>> res = manager2.get(skinURL + '/@@forbidden.html')
  Traceback (most recent call last):
  ...
  AppError: Bad response: 401 Unauthorized

  >>> res = manager2.get(skinURL + '/@@forbidden.html', status=401)
  >>> print(res.html)
  <html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
  <title>PageletTestLayout</title>
  </head>
  <body>
    <div>
    <br />
    <br />
    <h3>Unauthorized</h3>
    <br />
    <b>You are not authorized.</b>
  </div>
  </body>
  </html>


Form and form layout support
----------------------------

This layer offers also form macros given from ``z3c.formui``. Let's create a
simple form:

  >>> from z3c.form import testing
  >>> testing.setupFormDefaults()

Before we can start writing forms, we must have the content to work with:

  >>> import zope.interface
  >>> import zope.schema
  >>> class IPerson(zope.interface.Interface):
  ...
  ...     name = zope.schema.TextLine(
  ...         title='Name',
  ...         required=True)
  ...
  ...     age = zope.schema.Int(
  ...         title='Age',
  ...         description=u"The person's age.",
  ...         min=0,
  ...         default=20,
  ...         required=False)

  >>> from zope.schema.fieldproperty import FieldProperty
  >>> @zope.interface.implementer(IPerson)
  ... class Person(object):
  ...     name = FieldProperty(IPerson['name'])
  ...     age = FieldProperty(IPerson['age'])
  ...
  ...     def __init__(self, name, age):
  ...         self.name = name
  ...         self.age = age
  ...
  ...     def __repr__(self):
  ...         return '<%s %r>' % (self.__class__.__name__, self.name)

Okay, that should suffice for now. Let's now create a working add form:

  >>> from z3c.form import field
  >>> from z3c.formui import form, layout
  >>> class PersonAddForm(form.AddForm):
  ...
  ...     fields = field.Fields(IPerson)
  ...
  ...     def create(self, data):
  ...         return Person(**data)
  ...
  ...     def add(self, object):
  ...         self.context[object.id] = object
  ...
  ...     def nextURL(self):
  ...         return 'index.html'

Let's create a request:

  >>> from z3c.form.testing import TestRequest
  >>> from zope.interface import alsoProvides
  >>> divRequest = TestRequest()

And support the div form layer for our request:

  >>> from z3c.formui.interfaces import IDivFormLayer
  >>> alsoProvides(divRequest, IDivFormLayer)

Now create the form:

  >>> root = getRootFolder()
  >>> addForm = PersonAddForm(root, divRequest)

Since we have not specified a template yet, we have to do this now. We use our
div based form template:

  >>> import os
  >>> import z3c.formui
  >>> divFormTemplate = os.path.join(os.path.dirname(z3c.formui.__file__),
  ...     'div-form.pt')

  >>> from z3c.template.template import TemplateFactory
  >>> divFormFactory = TemplateFactory(divFormTemplate, 'text/html')

Now register the form (content) template:

  >>> import zope.interface
  >>> import zope.component
  >>> from z3c.template.interfaces import IContentTemplate
  >>> zope.component.provideAdapter(divFormFactory,
  ...     (zope.interface.Interface, IDivFormLayer),
  ...     IContentTemplate)

And let's define a layout template which simply calls the render method. For a
more adavanced content/layout render concept see ``z3c.pagelet``.

  >>> import tempfile
  >>> temp_dir = tempfile.mkdtemp()

  >>> myLayout = os.path.join(temp_dir, 'myLayout.pt')
  >>> with open(myLayout, 'w') as file:
  ...     _ = file.write('''<html>
  ...   <body>
  ...     <tal:block content="structure view/render">
  ...       content
  ...     </tal:block>
  ...   </body>
  ... </html>''')
  >>> myLayoutFactory = TemplateFactory(myLayout, 'text/html')

  >>> from z3c.template.interfaces import ILayoutTemplate
  >>> zope.component.provideAdapter(myLayoutFactory,
  ...     (zope.interface.Interface, zope.interface.Interface), ILayoutTemplate)

Now we can get our layout template:

  >>> layout = zope.component.getMultiAdapter((addForm, divRequest),
  ...     ILayoutTemplate)

  >>> layout
  <zope.browserpage.viewpagetemplatefile.ViewPageTemplateFile object at ...>


DIV-based Layout
----------------

Let's now render the page. Note the output doesn't contain the layout template:

  >>> addForm.update()
  >>> print(addForm.render())
  <form action="http://127.0.0.1" method="post"
        enctype="multipart/form-data" class="edit-form"
        id="form" name="form">
    <div class="viewspace">
      <div class="required-info">
        <span class="required">*</span>&ndash; required
      </div>
      <div>
        <div id="form-widgets-name-row" class="row required">
          <div class="label">
            <label for="form-widgets-name">
              <span>Name</span>
              <span class="required">*</span>
            </label>
          </div>
          <div class="widget">
            <input id="form-widgets-name" name="form.widgets.name"
                   class="text-widget required textline-field"
                   value="" type="text" />
          </div>
        </div>
        <div id="form-widgets-age-row" class="row">
          <div class="label">
            <label for="form-widgets-age">
              <span>Age</span>
            </label>
          </div>
          <div class="widget">
            <input id="form-widgets-age" name="form.widgets.age"
                   class="text-widget int-field"
                   value="20" type="text" />
          </div>
        </div>
      </div>
    </div>
    <div>
      <div class="buttons">
        <input id="form-buttons-add" name="form.buttons.add"
               class="submit-widget button-field" value="Add" type="submit" />
      </div>
    </div>
  </form>


Form Macros
-----------

Try at least to load the confguration, which will make sure that all macros
get registered correctly.

  >>> from zope.configuration import xmlconfig
  >>> import zope.component
  >>> import zope.security
  >>> import zope.viewlet
  >>> import zope.browserpage
  >>> import zope.browserresource
  >>> import z3c.macro
  >>> import z3c.template
  >>> import z3c.formui
  >>> xmlconfig.XMLConfig('meta.zcml', zope.browserpage)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.browserresource)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.component)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.security)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.viewlet)()
  >>> xmlconfig.XMLConfig('meta.zcml', z3c.macro)()
  >>> xmlconfig.XMLConfig('meta.zcml', z3c.template)()
  >>> xmlconfig.XMLConfig('configure.zcml', z3c.formui)()


Div layout macros
-----------------

Now we can see that we have different form macros available:

  >>> from z3c.macro.interfaces import IMacroTemplate
  >>> objects = (None, addForm, divRequest)
  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form')
  [...div-form.pt'), ...metal:define-macro': 'form'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'subform')
  [...div-form.pt'), ...define-macro': 'subform'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-label')
  [...div-form.pt'), ...define-macro': 'label'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-required-info')
  [...div-form.pt'), ...define-macro', 'required-info'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-header')
  [...div-form.pt'), ...define-macro': 'header'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-errors')
  [...div-form.pt'), ...define-macro': 'errors'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'widget-rows')
  [...div-form.pt'), ...define-macro': 'widget-rows'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'widget-row')
  [...div-form.pt'), ...define-macro': 'widget-row'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-groups')
  [...div-form.pt'), ...define-macro': 'groups'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-buttons')
  [...div-form.pt'), ...define-macro', 'buttons'...


Cleanup
-------

  >>> import shutil
  >>> shutil.rmtree(temp_dir)
