$(document).ready( function() {

    function toggle(node) {
	node.find(".title").toggle();
	node.find(".edit-link").toggle();
	node.find(".inputs").toggleClass("hide"); // note: .toggle() on a form was failing for some reason?!
    }

    $(".section-title .edit-link a").click(function(e) {

	e.preventDefault();

	parent = $(e.target).parents("li.section-title");

	var title = parent.find(".title").text();

	parent.find("input:text").val(title);
	toggle(parent);

	parent.find(".text-input").focus();
    });

});