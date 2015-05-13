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
      $this.selected = nulle
    save: () ->
      console.log $this.hostname + $this.selected.resource_uri
      $http.patch
        url: $this.hostname + $this.selected.resource_uri
        data: 
          data: $this.selected.date
          quote: $this.selected.quote
          source: $this.selected.source
      .success (result) ->
        console.log result
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
        $this.getQuotes()
      .error (error) ->
        console.error error