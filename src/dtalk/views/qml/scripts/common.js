var titlebarHeight = 26

function findParent(obj) {
	var objParent = obj.parent
	while (objParent != undefined) {
		print( objParent)
		objParent = objParent.parent
	}
	return objParent
}

function destroyAll(obj) {
    for (var i = obj.children.length; i > 0 ; i--) {
        destroyAll(obj.children[i-1])
    }
	obj.destroy()

}
