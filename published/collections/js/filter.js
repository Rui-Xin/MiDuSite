$(document).ready(function(){
$("#bytag").click(function() {
$("#tagbox").fadeToggle(100)
$("#yearbox").hide()
$("#topicbox").hide()
})
$("#byyear").click(function() {
$("#yearbox").fadeToggle(100)
$("#tagbox").hide()
$("#topicbox").hide()
})
$("#bytopic").click(function() {
$("#topicbox").fadeToggle(100)
$("#tagbox").hide()
$("#yearbox").hide()
})
})