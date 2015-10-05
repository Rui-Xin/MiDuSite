$(document).ready(function(){
	$("#tagbox").hide()
	$("#yearbox").hide()
	$("#bytag").click(function() {
		$("#yearbox").hide()
		$("#tagbox").fadeToggle(100)
	})
	$("#byyear").click(function() {
		$("#tagbox").hide()
		$("#yearbox").fadeToggle(100)
	})
})
