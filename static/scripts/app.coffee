formatDate = (date)->
  result = "#{date.getFullYear()}-"
  if (date.getMonth() + 1).toString().length < 2
    result += "0"
  result += (date.getMonth() + 1) + "-"
  if date.getDate().toString().length < 2
    result += "0"
  result += date.getDate()
  return result

app = angular.module 'mainApp', []

app.config ($interpolateProvider) ->
  $interpolateProvider.startSymbol '{[{'
  $interpolateProvider.endSymbol '}]}'

app.controller 'MainCtrl', ($http, $timeout) ->
  $this = 
    selected: null
    quotes: []
    getQuotes: () ->
      $http
        method: "GET"
        url: $this.hostname + "/api/v1/quote/"
      .success (result) ->
        $this.meta = result.meta
        $this.quotes = result.objects
        console.log $this.quotes
      .error (error) ->
        console.error error
    init: (url) ->
      $this.hostname = url
      $this.getQuotes()
    select: (quote) ->
      $this.selected = quote
    cancel: () ->
      $this.selected = null
    add: () ->
      $this.selected = 
        date: formatDate new Date()
    save: () ->
      method = ""
      url = $this.hostname
      if $this.selected.resource_uri
        url += $this.selected.resource_uri
        method = "PATCH"
      else
        url += "/api/v1/quote/"
        method = "POST"
      $http
        method: method
        url: url
        data: 
          date: $this.selected.date
          quote: $this.selected.quote
          source: $this.selected.source
      .success (result) ->
        console.log result
        if !$this.selected.resource_uri
          $this.selected = null
        $this.getQuotes()
      .error (error) ->
        console.error error
    delete: () ->
      console.log $this.hostname + $this.selected.resource_uri
      $http
        method: "DELETE"
        url: $this.hostname + $this.selected.resource_uri
      .success (result) ->
        console.log result
        $this.selected = null
        $this.getQuotes()
      .error (error) ->
        console.error error