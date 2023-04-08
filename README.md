# Tagforest (WIP)

Repository of [tagforest.fr](https://tagforest.fr) and [api.tagforest.fr](https://api.tagforest.fr).

Organize ressources (notes, lessons, music, movies, books, etc...) with a graph of tags.

Example:

```
     Science             University
     /     \               |  
Biology   Chemistry        |  
     \     /               |  
   Biochemistry            |  
            |              |  
  (biochemistry university notes)
```

Here, the "Biochemistry" tag is a descendant of the "Biology" and "Chemistry" tags. Every
entry tagged with "Biochemistry" will also belong to "Science", "Biology" and "Chemistry"
tags.
You could also say the "Biochemistry" tag has been tagged with "Biology" and "Chemistry"
tags. 

The goal of tagforest is to provide an easy to use interface to setup graph of tags and
tag ressources, and browse, filter and sort tags to easily find and represent all of 
your ressources.

Tags will be sorted based on a combination of parameters, which could include:
- topological sorting
- how many direct descendants (tag or ressources) does the tag have
- modification / creation date of descendants of the tag
- etc...

## tagforestrest

REST API, made with Django REST Framework

Python modules used: django, djangorestframework, dj-rest-auth, django-cors-headers

## tagforest-frontend-vue

Single-page javascript frontend, made with VueJS and Axios

NPM modules used: vue, vue-router, vuex, axios

## TODO

### Important

- Generate better example tree
- Improve editor

### Less important

- Add backend and frontend tests
- Add search option to find tags in graph view
- Handle and display errors (such as backend HTTP error codes) in frontend
- Use graph algorithms instead of query unions and intersections (networkx library ?)
- Add visibility options on tags and their descendents (public, invite-only, private)
- Turn backend and frontend into reusable apps
