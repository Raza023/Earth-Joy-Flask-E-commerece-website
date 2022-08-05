$(document).ready(function()
{
	/*alert("Chumma Lako") */
	$(".dropdown").click(function()
	{
		$(".dropdown-list ul").toggleClass("active");
	})
	
	/* select dropdown list */
	
	$(".dropdown-list ul li").click(function()
	{
		var icon_text = $(this).html();
		$(".default-option").html(icon_text);
	})
	
	/*Hide drop down list when click outside the bar*/
	$(document).on("click",function(event)
	{
		if(!$(event.target).closest(".dropdown").length)
		{
			$(".dropdown-list ul").removeClass("active")
		}
	})
});