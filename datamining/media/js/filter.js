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
			var op = $("input[name=selectoption]:checked").val();
			$("form").append('<input type="hidden" name="expertise" value="'+id+'" />');
			$("form").append('<input type="hidden" name="option" value="'+op+'" />');
			});
		return true;
	    });
	
	$("#emailgroup").click(function() {
	    var el = "";
	    $("input[name=checkemail]:checked").each(function() {
	        el += this.value+"@school.edu,";
        });
        location.href = 'mailto:'+el;
	});
	
});
    
function clickExpertise(obj) {    
    $(obj).toggleClass("selected");
}