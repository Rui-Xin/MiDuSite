$(document).ready(function(){
$("#bytag").click(function() {
$("#tagbox").fadeToggle(100)
$("#yearbox").hide()
})
$("#byyear").click(function() {
$("#yearbox").fadeToggle(100)
$("#tagbox").hide()
})
})