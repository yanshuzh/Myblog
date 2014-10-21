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
	document.getElementById('classify01').removeAttribute("readonly")
	document.getElementById('classify02').removeAttribute("readonly")
	document.getElementById('classify03').removeAttribute("readonly")
	document.getElementById('classify04').removeAttribute("readonly")
}

