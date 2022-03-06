$( document ).ready(function() {
  Shiny.addCustomMessageHandler('alertarg', function(arg) {
    alert(arg);
  })
});
