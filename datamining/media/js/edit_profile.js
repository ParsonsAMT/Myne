$(document).ready( function() {

	for ( var i in selected_areas ) {
	    $("#expertise-"+selected_areas[i]).addClass("selected");
	}

	$(".expertise").hover(function() {
		$(this).addClass("hover");
	    },
	    function() {
		$(this).removeClass("hover");
	    });

	$(".expertise").click(function() {
		clickExpertise(this);
	    });

	$("form").submit(function() {
		$(".expertise.selected").each(function() {
			var id = $(this).attr("id").replace("expertise-","");
			$("form").append('<input type="hidden" name="expertise" value="'+id+'" />');
		    });
		return true;
	    });

    });

function clickExpertise(obj) {    
    if ( ! $(obj).hasClass("selected") &&
	 $(".expertise.selected").length >= 5 ) {
	alert("You have already selected 5 areas. Please de-select one before selecting another.");
    } else {
	$(obj).toggleClass("selected");
    }
}