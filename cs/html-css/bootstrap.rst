overview
========

- A component library (not a framework)

- features

  * responsive
   
  * mobile-first

- JS dependencies (in loading order)

  * jquery

  * popper.js

- browser compatibility:
  
  * latest, stable releases of all major browsers.

package content
===============

- ``*.map`` is map file used for debugging.

css
---

- ``bootstrap[.min].css`` include all modules: layout, content, components, utilities.
  Without ``.min``, is just source files compiled together. With ``.min``, also minified.

- ``bootstrap-grid[.min].css`` includes: grid layout system and flex utilities.

- ``bootstrap-reboot[.min].css`` includes: reboot content module.

js
--

- ``bootstrap[.min].js`` include bootstrap js library.

- ``bootstrap.bundle[.min].js`` include also popper.js library.

- In source distro, there is individual js files for each components under ``js/dist/``.

setup
=====

- viewport tag::

    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

- bootstrap css tag.

- jquery, popper.js, bootstrap script tags.

global styles
=============

- change all elements' box-sizing to ``border-box``.

data api
========

- Nearly all Bootstrap plugins can be enabled and configured through HTML alone
  with data attributes.

- To disable the data attribute API, unbind all events on the document
  namespaced with ``data-api``. to target a specific plugin, just include the
  plugin’s name as a namespace along with the ``data-api`` namespace.

evnets
======

- Custom events for most plugins’ unique actions.

- Custom events come in an infinitive and past participle form - where the
  infinitive (ex. show) is triggered at the start of an event, and its past
  participle form (ex. shown) is triggered on the completion of an action.

- All infinitive events provide preventDefault() functionality. This provides
  the ability to stop the execution of an action before it starts.

APIs
====

- All public APIs are single, chainable methods, and return the collection
  acted upon.

- All methods should accept an optional options object, a string which targets
  a particular method, or nothing (which initiates a plugin with default
  behavior).

- Each plugin also exposes its raw constructor on a ``Constructor`` property:
  ``$.fn.popover.Constructor``. If you’d like to get a particular plugin
  instance, retrieve it directly from an element:
  ``$('[rel="popover"]').data('popover')``.

- You can change the default settings for a plugin by modifying the plugin’s
  ``Constructor.Default`` object.

- call ``.noConflict`` on the plugin you wish to revert the value of to its
  previously assigned value.

- The version of each of Bootstrap’s jQuery plugins can be accessed via the
  ``VERSION`` property of the plugin’s constructor.
