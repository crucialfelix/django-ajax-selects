# Change Log

## [1.5.1](https://github.com/crucialfelix/django-ajax-selects/tree/1.5.1) (2016-10-13)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.5.0...1.5.1)

**Implemented enhancements:**

- Prefer document.createElement to document.write [\#182](https://github.com/crucialfelix/django-ajax-selects/issues/182)

**Fixed bugs:**

- fix: add related for multiple select [\#184](https://github.com/crucialfelix/django-ajax-selects/pull/184) ([crucialfelix](https://github.com/crucialfelix))

## [1.5.0](https://github.com/crucialfelix/django-ajax-selects/tree/1.5.0) (2016-09-05)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.4.3...1.5.0)

- Added Support for Django 1.10
- Dropped Django 1.5

**Fixed bugs:**

- Initial fields are duplicated when new row added. [\#94](https://github.com/crucialfelix/django-ajax-selects/issues/94)

**Closed issues:**

- ValueError in Django 1.10 [\#177](https://github.com/crucialfelix/django-ajax-selects/issues/177)
- Django 1.10 did add popup [\#174](https://github.com/crucialfelix/django-ajax-selects/issues/174)
- Example not Working [\#161](https://github.com/crucialfelix/django-ajax-selects/issues/161)

**Merged pull requests:**

- Fix documentation to format code properly [\#165](https://github.com/crucialfelix/django-ajax-selects/pull/165) ([joshblum](https://github.com/joshblum))
- install.sh not working [\#162](https://github.com/crucialfelix/django-ajax-selects/pull/162) ([hdzierz](https://github.com/hdzierz))

## [1.4.3](https://github.com/crucialfelix/django-ajax-selects/tree/1.4.3) (2016-03-13)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.4.2...1.4.3)

**Closed issues:**

- Additional stacked inlines clear un-saved autocomplete fields [\#156](https://github.com/crucialfelix/django-ajax-selects/issues/156)
- support request: ManyToOneRel doesn't have expected attributes [\#154](https://github.com/crucialfelix/django-ajax-selects/issues/154)

**Merged pull requests:**

- Stop using deprecated \_meta api. [\#160](https://github.com/crucialfelix/django-ajax-selects/pull/160) ([kramarz](https://github.com/kramarz))
- Fixed file name in documentation for custom templates. [\#158](https://github.com/crucialfelix/django-ajax-selects/pull/158) ([sebslomski](https://github.com/sebslomski))
- Fixes re-initialization upon adding inlines [\#157](https://github.com/crucialfelix/django-ajax-selects/pull/157) ([funkyfuture](https://github.com/funkyfuture))

## [1.4.2](https://github.com/crucialfelix/django-ajax-selects/tree/1.4.2) (2016-01-18)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.4.1...1.4.2)

**Fixed bugs:**

- Selected data lost when adding new rows via ajax [\#145](https://github.com/crucialfelix/django-ajax-selects/issues/145)
- Inline forms raise TypeError when not filled in [\#142](https://github.com/crucialfelix/django-ajax-selects/issues/142)

**Merged pull requests:**

- Fix incorrect has\_changed result for AutoCompleteSelectField that has not been filled in. [\#152](https://github.com/crucialfelix/django-ajax-selects/pull/152) ([unklphil](https://github.com/unklphil))
- Only trigger reset\(\) initially if data hasn't changed. [\#146](https://github.com/crucialfelix/django-ajax-selects/pull/146) ([jmfederico](https://github.com/jmfederico))

## [1.4.1](https://github.com/crucialfelix/django-ajax-selects/tree/1.4.1) (2015-11-18)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.4.0...1.4.1)

**Closed issues:**

- Templates not included in pypi1.4.0 package [\#141](https://github.com/crucialfelix/django-ajax-selects/issues/141)
- Documentation seems to be broken on RTD [\#140](https://github.com/crucialfelix/django-ajax-selects/issues/140)

## [1.4.0](https://github.com/crucialfelix/django-ajax-selects/tree/1.4.0) (2015-11-07)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.3.6...1.4.0)

**Implemented enhancements:**

- Pass `request` to `LookupChannel` methods, make overriding easier [\#40](https://github.com/crucialfelix/django-ajax-selects/issues/40)

**Fixed bugs:**

- AttributeError on invalid form data [\#135](https://github.com/crucialfelix/django-ajax-selects/issues/135)
- Doesn't work with readonly\_fields [\#120](https://github.com/crucialfelix/django-ajax-selects/issues/120)
- Add another popup doesn't add `?\_popup=1` to url in Django 1.8 [\#118](https://github.com/crucialfelix/django-ajax-selects/issues/118)
- Field appers duplicated when marked as readonly in admin [\#84](https://github.com/crucialfelix/django-ajax-selects/issues/84)

**Closed issues:**

- can't import register module [\#139](https://github.com/crucialfelix/django-ajax-selects/issues/139)
- How to fire lookup for value in text field using javascript [\#137](https://github.com/crucialfelix/django-ajax-selects/issues/137)
- tests not included in MANIFEST.in [\#136](https://github.com/crucialfelix/django-ajax-selects/issues/136)
- Content of input not included in field, only dropdown choices for make\_ajax\_field  [\#134](https://github.com/crucialfelix/django-ajax-selects/issues/134)
- documentation for add link on ajax fields for django admin inlines [\#127](https://github.com/crucialfelix/django-ajax-selects/issues/127)
- Can't specify widget for AutoCompleteSelectMultipleField [\#126](https://github.com/crucialfelix/django-ajax-selects/issues/126)
- RemovedInDjango19Warning in ajax\_select [\#125](https://github.com/crucialfelix/django-ajax-selects/issues/125)
- Django's form change\_data always include autocomplete fields [\#123](https://github.com/crucialfelix/django-ajax-selects/issues/123)
- AttributeError: 'int' object has no attribute 'isnumeric' [\#117](https://github.com/crucialfelix/django-ajax-selects/issues/117)
- Error with TheForm in Django 1.8 [\#115](https://github.com/crucialfelix/django-ajax-selects/issues/115)
- Not Secure.  invalid literal for long\(\) with base 10 [\#114](https://github.com/crucialfelix/django-ajax-selects/issues/114)
- ImportError: No module named ajax\_select [\#112](https://github.com/crucialfelix/django-ajax-selects/issues/112)
- 'AutoCompleteSelectWidget' object has no attribute 'choices' [\#111](https://github.com/crucialfelix/django-ajax-selects/issues/111)
- "Uncaught TypeError: Cannot read property 'autocomplete' of undefined" [\#107](https://github.com/crucialfelix/django-ajax-selects/issues/107)
- Regression?  Or UUID PK not supported [\#103](https://github.com/crucialfelix/django-ajax-selects/issues/103)
- Support lookup channels from third-party apps [\#98](https://github.com/crucialfelix/django-ajax-selects/issues/98)
- callbacks for select doesn't work [\#97](https://github.com/crucialfelix/django-ajax-selects/issues/97)
- DeprecationWarning: Creating a ModelForm without either the 'fields' attribute or the 'exclude' attribute is deprecated [\#96](https://github.com/crucialfelix/django-ajax-selects/issues/96)
- AutoCompleteSelectField has no attribute 'limit\_choices\_to' in Django 1.7 [\#83](https://github.com/crucialfelix/django-ajax-selects/issues/83)
- Custom form [\#81](https://github.com/crucialfelix/django-ajax-selects/issues/81)
- avoid warning when installing via pip [\#53](https://github.com/crucialfelix/django-ajax-selects/issues/53)
- search\_fields like in ModelAdmin [\#21](https://github.com/crucialfelix/django-ajax-selects/issues/21)
- Issues when using django-admin-sortable [\#12](https://github.com/crucialfelix/django-ajax-selects/issues/12)

**Merged pull requests:**

- Get rid of terrible `\_as\_pk` function \(fixes \#117, \#120, and \#135\) [\#138](https://github.com/crucialfelix/django-ajax-selects/pull/138) ([hwkns](https://github.com/hwkns))
- Reset button handling [\#132](https://github.com/crucialfelix/django-ajax-selects/pull/132) ([jmerdich](https://github.com/jmerdich))
- Remove unnecessary backquotes in README.md [\#131](https://github.com/crucialfelix/django-ajax-selects/pull/131) ([zablotski](https://github.com/zablotski))
- Feature autodiscover [\#129](https://github.com/crucialfelix/django-ajax-selects/pull/129) ([morr0350](https://github.com/morr0350))
- Example for get\_formset on inline admin [\#128](https://github.com/crucialfelix/django-ajax-selects/pull/128) ([rlskoeser](https://github.com/rlskoeser))
- ajax\_lookup should respond with content type `application/json` [\#119](https://github.com/crucialfelix/django-ajax-selects/pull/119) ([unklphil](https://github.com/unklphil))
- Add AjaxSelectAdminStackedInline to work similarly to AjaxSelectAdminTabularInline [\#89](https://github.com/crucialfelix/django-ajax-selects/pull/89) ([unklphil](https://github.com/unklphil))

## [1.3.6](https://github.com/crucialfelix/django-ajax-selects/tree/1.3.6) (2015-04-06)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.3.5...1.3.6)

**Closed issues:**

- 'AutoCompleteSelectWidget' object has no attribute 'choices' [\#110](https://github.com/crucialfelix/django-ajax-selects/issues/110)
- \_\_init\_\_\(\) got an unexpected keyword argument 'mimetype' [\#108](https://github.com/crucialfelix/django-ajax-selects/issues/108)
- Limit number of results returned by lookup and auto load additional results when user scrolls to bottom of list [\#105](https://github.com/crucialfelix/django-ajax-selects/issues/105)
- Support reverse relationships [\#99](https://github.com/crucialfelix/django-ajax-selects/issues/99)
- 'set' object does not support indexing [\#93](https://github.com/crucialfelix/django-ajax-selects/issues/93)
- deck area [\#92](https://github.com/crucialfelix/django-ajax-selects/issues/92)
- Inline won't work with new lines \(SOLVED\) [\#87](https://github.com/crucialfelix/django-ajax-selects/issues/87)
- Bug in ajax\_selects.js \(addKiller function call\) [\#79](https://github.com/crucialfelix/django-ajax-selects/issues/79)
- AutoCompleteSelectField breaks when using localization and long ids [\#68](https://github.com/crucialfelix/django-ajax-selects/issues/68)
- format\_match did not work with django-ajax-select 1.3.3 [\#58](https://github.com/crucialfelix/django-ajax-selects/issues/58)
- Support Non-integer Primary Keys \(mongodb etc\) [\#34](https://github.com/crucialfelix/django-ajax-selects/issues/34)
- non operation with mongodb [\#3](https://github.com/crucialfelix/django-ajax-selects/issues/3)

**Merged pull requests:**

- Change order for running script by .sh \#112 \(NOTICE\) [\#113](https://github.com/crucialfelix/django-ajax-selects/pull/113) ([skrzypek](https://github.com/skrzypek))
- Update README.md [\#101](https://github.com/crucialfelix/django-ajax-selects/pull/101) ([cormier](https://github.com/cormier))
- Added option for fields in TheForm superclass [\#91](https://github.com/crucialfelix/django-ajax-selects/pull/91) ([onyekaa](https://github.com/onyekaa))

## [1.3.5](https://github.com/crucialfelix/django-ajax-selects/tree/1.3.5) (2014-08-02)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.3.4...1.3.5)

**Closed issues:**

- ajax-selects/fields.py simplejson is deprecated [\#74](https://github.com/crucialfelix/django-ajax-selects/issues/74)
- Document the use in template for 'quick installation' [\#71](https://github.com/crucialfelix/django-ajax-selects/issues/71)
- Document how to use an ajax field in a ListFilter in admin [\#70](https://github.com/crucialfelix/django-ajax-selects/issues/70)
- Issue with Ajax-Search on Media-Fields [\#60](https://github.com/crucialfelix/django-ajax-selects/issues/60)
- Set width of jquery autocomplete widget [\#30](https://github.com/crucialfelix/django-ajax-selects/issues/30)

**Merged pull requests:**

- Fix issue 58 and pull request 76 [\#85](https://github.com/crucialfelix/django-ajax-selects/pull/85) ([camillobruni](https://github.com/camillobruni))
- Django's HttpResponse object has deprecated the mimetype kwarg in 1.7 [\#82](https://github.com/crucialfelix/django-ajax-selects/pull/82) ([squidsoup](https://github.com/squidsoup))
- Support non-int primary keys [\#78](https://github.com/crucialfelix/django-ajax-selects/pull/78) ([AlexHill](https://github.com/AlexHill))
- correct import deprecated since Django 1.4 [\#77](https://github.com/crucialfelix/django-ajax-selects/pull/77) ([gertingold](https://github.com/gertingold))
- maintain compatibility with Python 2.6 [\#75](https://github.com/crucialfelix/django-ajax-selects/pull/75) ([gertingold](https://github.com/gertingold))

## [1.3.4](https://github.com/crucialfelix/django-ajax-selects/tree/1.3.4) (2014-03-30)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.3.3...1.3.4)

**Closed issues:**

- Custom validation with django-ajax-selects [\#73](https://github.com/crucialfelix/django-ajax-selects/issues/73)
- DeprecationWarning django.utils.simplejson [\#63](https://github.com/crucialfelix/django-ajax-selects/issues/63)
- When create select list always show \(in bottom list\) add new object. [\#62](https://github.com/crucialfelix/django-ajax-selects/issues/62)

**Merged pull requests:**

- Trivial typo fix \(chanel\_name\) [\#69](https://github.com/crucialfelix/django-ajax-selects/pull/69) ([gthb](https://github.com/gthb))
- Fixes \#18 - AJAX Selector and dynamic inlines [\#67](https://github.com/crucialfelix/django-ajax-selects/pull/67) ([peterfarrell](https://github.com/peterfarrell))
- Using json as opposed to simplejson \(depreciated\) [\#65](https://github.com/crucialfelix/django-ajax-selects/pull/65) ([krzysztof](https://github.com/krzysztof))

## [1.3.3](https://github.com/crucialfelix/django-ajax-selects/tree/1.3.3) (2013-11-13)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.3.2...1.3.3)

**Merged pull requests:**

- Remove protocol from dynamically loaded urls. [\#54](https://github.com/crucialfelix/django-ajax-selects/pull/54) ([jellonek](https://github.com/jellonek))

## [1.3.2](https://github.com/crucialfelix/django-ajax-selects/tree/1.3.2) (2013-11-09)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.3.1...1.3.2)

## [1.3.1](https://github.com/crucialfelix/django-ajax-selects/tree/1.3.1) (2013-10-09)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.3.0...1.3.1)

**Closed issues:**

- parameters to triggers [\#43](https://github.com/crucialfelix/django-ajax-selects/issues/43)
- django.conf.urls.defaults depreciated [\#38](https://github.com/crucialfelix/django-ajax-selects/issues/38)
- How do you pass a class name for the addKiller [\#37](https://github.com/crucialfelix/django-ajax-selects/issues/37)
- AutoComplete and AutoCompleteSelect renders fine but AutoCompleteMultipleSelect isnt working [\#31](https://github.com/crucialfelix/django-ajax-selects/issues/31)
- django inline formset [\#18](https://github.com/crucialfelix/django-ajax-selects/issues/18)

## [1.3.0](https://github.com/crucialfelix/django-ajax-selects/tree/1.3.0) (2013-10-08)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.2.5...1.3.0)

**Closed issues:**

- ContentNotRenderedError [\#39](https://github.com/crucialfelix/django-ajax-selects/issues/39)
- Please add a change trigger to the target. [\#35](https://github.com/crucialfelix/django-ajax-selects/issues/35)
- can\_add isn't working in lookups [\#23](https://github.com/crucialfelix/django-ajax-selects/issues/23)

**Merged pull requests:**

- Follow the Meta definition of the original modelform [\#49](https://github.com/crucialfelix/django-ajax-selects/pull/49) ([artscoop](https://github.com/artscoop))

## [1.2.5](https://github.com/crucialfelix/django-ajax-selects/tree/1.2.5) (2012-08-22)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.2.4...1.2.5)

**Closed issues:**

- dj1.4 Error importing template source loader django.template.loaders.filesystem.load\_template\_source: [\#15](https://github.com/crucialfelix/django-ajax-selects/issues/15)
- fixed bug: AutoCompleteSelectMultipleField does not honor 'widget' parameter [\#14](https://github.com/crucialfelix/django-ajax-selects/issues/14)
- error 'this.data\("autocomplete"\) is undefined' [\#10](https://github.com/crucialfelix/django-ajax-selects/issues/10)
- Fire the change event on selection [\#8](https://github.com/crucialfelix/django-ajax-selects/issues/8)
- ValueError: translation table must be 256 characters long [\#5](https://github.com/crucialfelix/django-ajax-selects/issues/5)
- Error on Pop-Up [\#19](https://github.com/crucialfelix/django-ajax-selects/issues/19)

**Merged pull requests:**

- Small fix in CSS [\#2](https://github.com/crucialfelix/django-ajax-selects/pull/2) ([karlmoritz](https://github.com/karlmoritz))

## [1.2.4](https://github.com/crucialfelix/django-ajax-selects/tree/1.2.4) (2012-01-15)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.2.3...1.2.4)

## [1.2.3](https://github.com/crucialfelix/django-ajax-selects/tree/1.2.3) (2011-11-29)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.2.1...1.2.3)

## [1.2.1](https://github.com/crucialfelix/django-ajax-selects/tree/1.2.1) (2011-10-19)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.1.5...1.2.1)

## [1.1.5](https://github.com/crucialfelix/django-ajax-selects/tree/1.1.5) (2011-08-24)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.1.3...1.1.5)

## [1.1.3](https://github.com/crucialfelix/django-ajax-selects/tree/1.1.3) (2010-06-06)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.1.1...1.1.3)

## [1.1.1](https://github.com/crucialfelix/django-ajax-selects/tree/1.1.1) (2010-06-03)
[Full Changelog](https://github.com/crucialfelix/django-ajax-selects/compare/1.1.0...1.1.1)

## [1.1.0](https://github.com/crucialfelix/django-ajax-selects/tree/1.1.0) (2010-03-06)


\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*
