function Todeletemood (obj) {
	// body...
	var r = confirm("Delete this mood !")
	if(r==true)
	{
		obj.parentNode.removeChild(obj)
		alert("Delete ok")

	}
	else
	{
		alert("cancel")
	}
}

function InputControl()
{
	document.getElementById("classifydiv02").style.display="";

}
function CancelControl()
{
	document.getElementById("classifydiv02").style.display="none";

}

