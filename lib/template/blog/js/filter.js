$(document).ready(function(){
	$("#bytag").click(function() {
		$("#yearbox").hide()
		$("#tagbox").fadeToggle(100)
	})
	$("#byyear").click(function() {
		$("#tagbox").hide()
		$("#yearbox").fadeToggle(100)
	})
})
